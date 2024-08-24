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
            {
                "name": "첫째 돼지",
                "book_id": 1,
                "character_image": "character/첫째돼지.png",
                "greeting": "안녕! 나는 첫째 돼지야. 너무 서둘러서 지푸라기로 집을 지었지만, 더 좋은 방법을 배우고 있어. 너도 나처럼 실수에서 배운 적 있니?",
                "speaker": "nseonghoon",
                "volume": 5,
                "speed": -1,
                "pitch": -3,
                "alpha": -4,
                "end_pitch": -3,
                "emotion": 0,
                'emotion_strength': 0
            },
            {
                "name": "둘째 돼지",
                "book_id": 1,
                "character_image": "character/둘째돼지.png",
                "greeting": "안녕! 나는 둘째 돼지야. 나무로 집을 지었는데, 튼튼하다고 생각했지만 결국 늑대에게 당했어. 다음번엔 더 잘할 거야! 넌 어떤 모험을 하고 있니?",
                "speaker": "dara_ang",
                "volume": 5,
                "speed": -1,
                "pitch": 3,
                "alpha": -2,
                "end_pitch": -2,
                "emotion": 0,
                'emotion_strength': 0
            },
            {
                "name": "셋째 돼지",
                "book_id": 1,
                "character_image": "character/셋째돼지.png",
                "greeting": "안녕하세요! 나는 셋째 돼지예요. 벽돌로 튼튼한 집을 지어서 늑대를 막아냈죠. 계획하고 신중하게 행동하는 게 중요하다고 생각해요. 당신은 어떤 계획을 세우고 있나요?",
                "speaker": "nihyun",
                "volume": 5,
                "speed": -1,
                "pitch": -2,
                "alpha": -1,
                "end_pitch": 0,
                "emotion": 0,
                'emotion_strength': 0
            },
            {
                "name": "늑대",
                "book_id": 1,
                "character_image": "character/늑대.png",
                "greeting": "흐흐, 나는 늑대다. 돼지들의 집을 부수려고 했지만 실패했지. 하지만 난 쉽게 포기하지 않아. 너도 목표를 위해 끝까지 도전한 적이 있겠지?",
                "speaker": "nyoungil",
                "volume": 5,
                "speed": -2,
                "pitch": 3,
                "alpha": 0,
                "end_pitch": -2,
                "emotion": 0,
                'emotion_strength': 0
            },
            {
                "name": "백설공주",
                "book_id": 2,
                "character_image": "character/백설공주.png",
                "greeting": "안녕하세요! 저는 백설공주예요. 일곱 난쟁이들과 행복하게 살고 있답니다. 제 이야기가 더 궁금하신가요?",
                "speaker": "dara-danna",
                "volume": 5,
                "speed": -1,
                "pitch": -2,
                "alpha": 2,
                "end_pitch": 0,
                "emotion": 0,
                'emotion_strength': 0
            },
            {
                "name": "새 왕비",
                "book_id": 2,
                "character_image": "character/왕비.png",
                "greeting": "안녕하세요. 저는 새 왕비예요. 거울에게 세상에서 가장 아름다운 사람이 되고 싶었지만, 결국 그 욕망이 저를 파멸로 이끌었죠. 저랑 대화해보시겠어요?",
                "speaker": "nsabina",
                "volume": 5,
                "speed": -3,
                "pitch": -1,
                "alpha": -2,
                "end_pitch": 0,
                "emotion": 0,
                'emotion_strength': 0
            },
            {
                "name": "일곱난쟁이",
                "book_id": 2,
                "character_image": "character/일곱난쟁이.png",
                "greeting": "안녕하세요! 우리는 일곱 난쟁이들이에요. 백설공주를 보호하며 함께 살고 있죠. 언제든 우리에게도 궁금한 점이 있다면 물어봐요!",
                "speaker": "ngaram",
                "volume": 5,
                "speed": -1,
                "pitch": -1,
                "alpha": -2,
                "end_pitch": 0,
                "emotion": 0,
                'emotion_strength': 0
            },
            {
                "name": "피터팬",
                "book_id": 3,
                "character_image": "character/피터팬.png",
                "greeting": "안녕! 나는 피터팬이야. 네버랜드에서 모험을 즐기며 영원히 어린아이로 살고 있어. 너도 날아오르고 싶지 않아?",
                "speaker": "ndonghyun",
                "volume": 5,
                "speed": 0,
                "pitch": 1,
                "alpha": 1,
                "end_pitch": 2,
                "emotion": 0,
                'emotion_strength': 0
            },
            {
                "name": "팅커벨",
                "book_id": 3,
                "character_image": "character/팅커벨.png",
                "greeting": "안녕하세요! 나는 팅커벨이에요. 피터팬과 함께 네버랜드를 모험하고 있답니다. 작은 요정이지만 강한 의지를 가지고 있어요. 당신도 자신만의 마법을 찾고 있나요?",
                "speaker": "ngaram",
                "volume": 5,
                "speed": -1,
                "pitch": 2,
                "alpha": 0,
                "end_pitch": 2,
                "emotion": 0,
                'emotion_strength': 0
            },
            {
                "name": "후크선장",
                "book_id": 3,
                "character_image": "character/후크선장.png",
                "greeting": "나는 후크선장이야. 피터팬을 쫓는 해적이지. 하지만 그 녀석을 잡기란 쉽지 않아. 너도 나처럼 끈질기게 도전해본 적 있니?",
                "speaker": "nraewon",
                "volume": 5,
                "speed": 0,
                "pitch": 2,
                "alpha": 0,
                "end_pitch": -2,
                "emotion": 0,
                'emotion_strength': 0
            },
            {
                "name": "흥부",
                "book_id": 4,
                "character_image": "character/흥부.png",
                "greeting": "안녕하세요! 저는 흥부입니다. 어려운 상황 속에서도 희망을 잃지 않았죠. 제비 덕분에 새 삶을 시작할 수 있었어요. 당신은 어떤 희망을 품고 있나요?",
                "speaker": "nkyungtae",
                "volume": 5,
                "speed": -2,
                "pitch": 1,
                "alpha": 1,
                "end_pitch": 2,
                "emotion": 0,
                'emotion_strength': 0
            },
            {
                "name": "놀부",
                "book_id": 4,
                "character_image": "character/놀부.png",
                "greeting": "안녕! 나는 놀부야. 욕심 때문에 큰 화를 입었지. 너도 나처럼 욕심을 부린 적 있니?",
                "speaker": "nwoosik",
                "volume": 5,
                "speed": -1,
                "pitch": -2,
                "alpha": 1,
                "end_pitch": 2,
                "emotion": 0,
                'emotion_strength': 0
            },
            {
                "name": "제비",
                "book_id": 4,
                "character_image": "character/제비.png",
                "greeting": "안녕하세요! 저는 흥부에게 행복을 가져다 준 제비랍니다. 작은 친절이 큰 변화를 가져올 수 있다는 걸 알게 되었어요. 당신은 최근에 어떤 친절을 베풀었나요?",
                "speaker": "nwoof",
                "volume": 5,
                "speed": -2,
                "pitch": 1,
                "alpha": 0,
                "end_pitch": -1,
                "emotion": 0,
                'emotion_strength': 0
            },
            {
                "name": "헨젤",
                "book_id": 5,
                "character_image": "character/헨젤.png",
                "greeting": "안녕하세요! 나는 헨젤이에요. 그레텔과 함께 숲 속 마녀의 집에서 살아남았죠. 모험 속에서 항상 용기를 내야 해요. 당신은 어떤 모험을 하고 있나요?",
                "speaker": "nsiyoon",
                "volume": 5,
                "speed": -2,
                "pitch": -1,
                "alpha": 2,
                "end_pitch": 0,
                "emotion": 0,
                'emotion_strength': 0
            },
            {
                "name": "그레텔",
                "book_id": 5,
                "character_image": "character/그레텔.png",
                "greeting": "안녕하세요! 나는 그레텔이에요. 오빠와 함께 마녀를 이기고 탈출했어요. 항상 침착함이 중요한 법이죠. 당신은 위기 속에서 어떻게 대처하나요?",
                "speaker": "vara",
                "volume": 5,
                "speed": -1,
                "pitch": 2,
                "alpha": -1,
                "end_pitch": -2,
                "emotion": 2,
                'emotion_strength': 2
            },
            {
                "name": "마녀",
                "book_id": 5,
                "character_image": "character/마녀.png",
                "greeting": "안녕, 나는 숲 속의 마녀야. 헨젤과 그레텔을 잡으려 했지만 결국 실패했지. 나랑 이야기해볼래?",
                "speaker": "nsunhee",
                "volume": 5,
                "speed": -2,
                "pitch": 1,
                "alpha": 1,
                "end_pitch": -1,
                "emotion": 0,
                'emotion_strength': 0
            }
        ]


        for character_data in characters_data:
            book = Book.objects.get(id=character_data["book_id"])
            description = f"{character_data['name']}에 대한 설명입니다."
            greeting = character_data["greeting"]
            Character.objects.get_or_create(
                name=character_data["name"],
                book=book,
                defaults={
                    "character_image": character_data["character_image"],
                    "description": description,
                    "greeting": greeting,
                    "speaker": character_data["speaker"],
                    "volume": character_data["volume"],
                    "speed": character_data["speed"],
                    "pitch": character_data["pitch"],
                    "emotion": character_data["emotion"],
                    "emotion_strength": character_data["emotion_strength"],
                    "format": "mp3",
                    "alpha": character_data["alpha"],
                    "end_pitch": character_data["end_pitch"],
                }

            )
            self.stdout.write(self.style.SUCCESS(f"Character '{character_data['name']}' added or already exists."))
