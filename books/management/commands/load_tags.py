from django.core.management.base import BaseCommand
from books.models import Tag

class Command(BaseCommand):
    help = 'Load initial tag data'

    def handle(self, *args, **kwargs):
        tags = [
            "사랑",
            "모험",
            "지혜",
            "공주",
            "용기",
            "효",
            "선",
            "가족",
            "행복",
            "은혜",
            "우정",
            "청결",
            "위로",
            "성실",
            "신비",
            "창의",
            "희생",
        ]

        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added tag '{tag.name}'"))
            else:
                self.stdout.write(self.style.WARNING(f"Tag '{tag.name}' already exists"))
