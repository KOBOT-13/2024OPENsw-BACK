import os
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Run load files in sequence'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to load data...'))

        # call_command를 사용하여 각 관리 명령어를 호출합니다.
        call_command('load_books')
        self.stdout.write(self.style.SUCCESS('Loaded books data'))

        call_command('load_characters')
        self.stdout.write(self.style.SUCCESS('Loaded characters data'))

        call_command('load_users')
        self.stdout.write(self.style.SUCCESS('Loaded users data'))

        call_command('load_quizzes')
        self.stdout.write(self.style.SUCCESS('Loaded quizzes data'))

        self.stdout.write(self.style.SUCCESS('All data loaded successfully'))
