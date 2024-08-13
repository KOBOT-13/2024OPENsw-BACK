from django.core.management.base import BaseCommand
from books.models import Tag

class Command(BaseCommand):
    help = 'Load initial tag data'

    def handle(self, *args, **kwargs):
        tags = [
            "로맨스",
            "우정",
            "모험",
            "판타지",
            "동화",
            "전설",
            "고전",
            "역사",
            "과학",
            "공포"
        ]

        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added tag '{tag.name}'"))
            else:
                self.stdout.write(self.style.WARNING(f"Tag '{tag.name}' already exists"))
