from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Response

@receiver(post_save, sender=Response)
def notify_about_response(sender, instance, created, **kwargs):
    if created:
        subject = f'Новый отклик на ваше объявление "{instance.post.title}"'
        message = render_to_string('board/email/new_response.txt', {
            'post': instance.post,
            'response': instance
        })
        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[instance.post.author.email],
            fail_silently=False
        )

@receiver(post_save, sender=Response)
def notify_accepted_response(sender, instance, **kwargs):
    if instance.accepted:
        subject = f'Ваш отклик принят: "{instance.post.title}"'
        message = render_to_string('board/response_accepted.txt', {
            'post': instance.post,
            'response': instance
        })
        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[instance.author.email],
            fail_silently=False
        )