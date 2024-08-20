from django.core.management.base import BaseCommand
from books.models import Book, Character

class Command(BaseCommand):
    help = 'Load initial character data'

    CHARACTER_MAP = {
        0: "아기 돼지 삼형제의 첫째 돼지",
        1: "아기 돼지 삼형제의 둘째 돼지",
        2: "아기 돼지 삼형제의 셋째 돼지",
        3: "아기 돼지 삼형제의 늑대",
        4: "백설공주의 백설공주",
        5: "백설공주의 새 왕비",
        6: "백설공주의 일곱난쟁이",
        7: "피터팬의 피터팬",
        8: "피터팬의 팅커벨",
        9: "피터팬의 후크선장",
        10: "흥부와 놀부의 흥부",
        11: "흥부와 놀부의 놀부",
        12: "흥부와 놀부의 제비",
        13: "헨젤과 그레텔의 헨젤",
        14: "헨젤과 그레텔의 그레텔",
        15: "헨젤과 그레텔의 마녀",
    }

    def handle(self, *args, **kwargs):
        characters_data = [
            {"name": "첫째 돼지", "book_id": 1, "character_image":"character/첫째돼지.png"},
            {"name": "둘째 돼지", "book_id": 1, "character_image":"character/둘째돼지.png"},
            {"name": "셋째 돼지", "book_id": 1, "character_image":"character/셋째돼지.png"},
            {"name": "늑대", "book_id": 1, "character_image":"character/늑대.png"},
            {"name": "백설공주", "book_id": 2, "character_image":"character/백설공주.png"},
            {"name": "새 왕비", "book_id": 2, "character_image":"character/왕비.png"},
            {"name": "일곱난쟁이", "book_id": 2, "character_image":"character/일곱난쟁이.png"},
            {"name": "피터팬", "book_id": 3, "character_image":"character/피터팬.png"},
            {"name": "팅커벨", "book_id": 3, "character_image":"character/팅커벨.png"},
            {"name": "후크선장", "book_id": 3, "character_image":"character/후크선장.png"},
            {"name": "흥부", "book_id": 4, "character_image":"character/흥부.png"},
            {"name": "놀부", "book_id": 4, "character_image":"character/놀부.png"},
            {"name": "제비", "book_id": 4, "character_image":"character/제비.png"},
            {"name": "헨젤", "book_id": 5, "character_image":"character/헨젤.png"},
            {"name": "그레텔", "book_id": 5, "character_image":"character/그레텔.png"},
            {"name": "마녀", "book_id": 5, "character_image":"character/마녀.png"},
        ]

        for character_data in characters_data:
            book = Book.objects.get(id=character_data["book_id"])
            description = f"{character_data['name']}에 대한 설명입니다."
            greeting = f"안녕하세요, 저는 {character_data['name']}입니다."
            Character.objects.get_or_create(
                name=character_data["name"],
                book=book,
                defaults={
                    "character_image": character_data["character_image"],
                    "description": description,
                    "greeting": greeting,
                    "speaker": "vara",
                    "volume": 0,
                    "speed": 0,
                    "pitch": 0,
                    "emotion": 0,
                    "emotion_strength": 0,
                    "format": "mp3",
                    "alpha": 0,
                    "end_pitch": 0,
                }
            
            )
            self.stdout.write(self.style.SUCCESS(f"Character '{character_data['name']}' added or already exists."))
