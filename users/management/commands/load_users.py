from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Load initial user data'

    def handle(self, *args, **kwargs):
        users = [
            {'email': 'admin@admin.com', 'username': 'admin', 'password': 'password', 'is_staff': True, 'is_superuser': True},

             # 더 많은 유저 데이터를 여기에 추가합니다.
        ]

        for user_data in users:
            if not User.objects.filter(email=user_data['email']).exists():
                user = User.objects.create_user(
                    email=user_data['email'],
                    username=user_data['username'],
                    password=user_data['password'],
                )
                user.is_staff = user_data['is_staff']
                user.is_superuser = user_data['is_superuser']
                user.save()
                print(f"Successfully added user '{user.username}'")
            else:
                print(f"User with email '{user_data['email']}' already exists")
