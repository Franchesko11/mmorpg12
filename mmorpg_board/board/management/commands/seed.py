from django.core.management.base import BaseCommand
from board.models import Category
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Seeds the database with initial categories'

    def handle(self, *args, **options):
        categories = [
            'Танки', 'Хилы', 'ДД', 'Торговцы', 'Гилдмастеры',
            'Квестгиверы', 'Кузнецы', 'Кожевники', 'Зельевары', 'Мастера заклинаний'
        ]

        for category_name in categories:
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'name': category_name}
            )
            if not created and not category.slug:
                category.save()