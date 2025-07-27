from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Post, Response, Category
from .forms import PostForm, ResponseForm
from django.contrib.auth import get_user_model

User = get_user_model()


class PostListView(ListView):
    model = Post
    template_name = 'board/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['response_form'] = ResponseForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'board/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Объявление успешно создано!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'board/post_form.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            messages.error(request, 'Вы не можете редактировать это объявление!')
            return redirect(obj)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Объявление успешно обновлено!')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'board/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            messages.error(request, 'Вы не можете удалить это объявление!')
            return redirect(obj)
        return super().dispatch(request, *args, **kwargs)


class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if Response.objects.filter(post=post, author=self.request.user).exists():
            form.add_error(None, 'Вы уже оставляли отклик на это объявление!')
            return self.form_invalid(form)

        form.instance.post = post
        form.instance.author = self.request.user
        response = form.save()

        # Отправка email уведомления автору объявления
        subject = f'Новый отклик на ваше объявление "{post.title}"'
        message = f'Пользователь {self.request.user.email} оставил отклик на ваше объявление "{post.title}":\n\n{response.text}\n\nВы можете просмотреть все отклики в личном кабинете.'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [post.author.email],
            fail_silently=False,
        )

        messages.success(self.request, 'Ваш отклик успешно отправлен!')
        return redirect(post)


class ResponseListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'board/response_list.html'
    context_object_name = 'responses'

    def get_queryset(self):
        return Response.objects.filter(post__author=self.request.user).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        response_id = request.POST.get('response_id')
        action = request.POST.get('action')

        if response_id and action:
            response = get_object_or_404(Response, pk=response_id, post__author=request.user)

            if action == 'accept':
                response.accepted = True
                response.save()

                # Отправка email уведомления автору отклика
                subject = f'Ваш отклик на объявление "{response.post.title}" принят!'
                message = f'Автор объявления "{response.post.title}" принял ваш отклик.\n\nТекст отклика: {response.text}'
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [response.author.email],
                    fail_silently=False,
                )

                messages.success(request, 'Отклик принят! Автор уведомлен.')
            elif action == 'delete':
                response.delete()
                messages.success(request, 'Отклик удалён!')

        return redirect('response_list')