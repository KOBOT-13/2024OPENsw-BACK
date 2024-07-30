from django.core.management.base import BaseCommand

from books.models import Book
from quizzes.models import Quiz

class Command(BaseCommand):
    help = 'Load initial quiz data'

    def handle(self, *args, **kwargs):
        quizzes = {
            1: [
                {
                    "question": "아기 돼지 삼형제에서 벽돌로 집을 지은 돼지는 누구일까요?",
                    "options": ["첫째 돼지", "둘째 돼지", "셋째 돼지", "엄마 돼지"],
                    "answer": "셋째 돼지"
                },
                {
                    "question": "아기 돼지 삼형제에서 늑대가 지푸라기 집을 부순 방법은 무엇일까요?",
                    "options": ["망치로 내려치기", "물 붓기", "기도하기", "입김 불기"],
                    "answer": "입김 불기"
                },
                {
                    "question": "아기 돼지 삼형제에서 나무로 집을 지은 돼지는 누구일까요?",
                    "options": ["첫째 돼지", "둘째 돼지", "셋째 돼지", "아빠 돼지"],
                    "answer": "둘째 돼지"
                },
                {
                    "question": "아기 돼지 삼형제에서 지푸라기로 집을 지은 돼지는 누구일까요?",
                    "options": ["첫째 돼지", "둘째 돼지", "셋째 돼지", "아빠 돼지"],
                    "answer": "첫째 돼지"
                },
                {
                    "question": "늑대가 마지막으로 셋째 돼지 집에 들어가려고 했을 때 들어간 곳은 어디일까요?",
                    "options": ["하수구", "굴뚝", "대문", "창문"],
                    "answer": "굴뚝"
                }
            ],
            2: [
                {
                    "question": "백설공주에 나오는 난쟁이의 수는 몇명일까요?",
                    "options": ["5", "6", "7", "8"],
                    "answer": "7"
                },
                {
                    "question": "백설공주를 독살하려고 한 방법은 무엇일까요?",
                    "options": ["독사과", "독물", "독포도", "독포도주"],
                    "answer": "독사과"
                },
                {
                    "question": "왕비가 백설공주를 해칠 것을 시킨 사람은 누구일가요?",
                    "options": ["사냥꾼", "목사", "의사", "경찰관"],
                    "answer": "사냥꾼"
                },
                {
                    "question": "왕비가 누가 세상에서 가장 아름답냐고 묻는 대상은 누구일까요?",
                    "options": ["마법사", "마법 의자", "마법 거울", "백설공주"],
                    "answer": "마법 거울"
                },
                {
                    "question": "백설공주를 사랑한 사람은 누구일까요?",
                    "options": ["왕자", "기사", "늑대", "사냥꾼"],
                    "answer": "왕자"
                }
            ],
            3: [
                {
                    "question": "피터팬에서 피터팬이 사는 곳은 어디일까요?",
                    "options": ["네버랜드", "원더랜드", "드림랜드", "페어리랜드"],
                    "answer": "네버랜드"
                },
                {
                    "question": "피터팬의 친구는 누구일까요?",
                    "options": ["티나벨", "팅커벨", "티피벨", "탱커벨"],
                    "answer": "팅커벨"
                },
                {
                    "question": "피터팬의 적은 누구일까요?",
                    "options": ["후크 선장", "블랙비어드", "스컬리", "레드비어드"],
                    "answer": "후크 선장"
                },
                {
                    "question": "웬디가 사는 곳은 어디일까요?",
                    "options": ["서울", "부산", "뉴욕", "런던"],
                    "answer": "런던"
                },
                {
                    "question": "피터팬이 항상 입는 옷의 색깔은 무엇일까요?",
                    "options": ["빨강", "파랑", "초록", "노랑"],
                    "answer": "초록"
                }
            ],
            4: [
                {
                    "question": "놀부의 아내가 흥부의 싸다귀를 때린 물건은 무엇일까요?",
                    "options": ["책", "주걱", "몽둥이", "김치"],
                    "answer": "주걱"
                },
                {
                    "question": "흥부가 다리를 고쳐준 동물은 어떤 동물일까요?",
                    "options": ["강아지", "고양이", "제비", "까마귀"],
                    "answer": "제비"
                },
                {
                    "question": "제비가 흥부의 집에 떨어뜨린 씨앗은 무엇일까요?",
                    "options": ["포도씨", "수박씨", "사과씨", "박씨"],
                    "answer": "박씨"
                },
                {
                    "question": "놀부의 집 박 속에서 나온 것은 무엇일까요?",
                    "options": ["금은보화", "기와집", "스마트폰", "도깨비"],
                    "answer": "도깨비"
                },
                {
                    "question": "흥부의 박에서 나온 것은 무엇일까요?",
                    "options": ["자동차", "금은보화", "도끼", "블루투스 이어폰"],
                    "answer": "금은보화"
                }
            ],
            5: [
                {
                    "question": "헨젤과 그레텔의 부모님의 직업은 무엇일까요?",
                    "options": ["나무꾼", "농부", "어부", "의사"],
                    "answer": "나무꾼"
                },
                {
                    "question": "헨젤과 그레텔이 들어간 숲 속 집은 어떤 집일까요?",
                    "options": ["과자 집", "나무 집", "돌 집", "얼음 집"],
                    "answer": "과자 집"
                },
                {
                    "question": "헨젤과 그레텔을 잡아먹으려한 사람은 누구일까요?",
                    "options": ["거인", "마녀", "늑대", "사냥꾼"],
                    "answer": "마녀"
                },
                {
                    "question": "헨젤과 그레텔이 돌아가기 위해 길에 떨어뜨린 것은 무엇일까요?",
                    "options": ["한조각", "연필가루", "빵조각", "꽃조각"],
                    "answer": "빵조각"
                },
                {
                    "question": "헨젤과 그레텔이 마녀를 물리친 방법은 무엇일까요?",
                    "options": ["기도하기", "불에 태움", "덫에 가둠", "독을 먹임"],
                    "answer": "불에 태움"
                }
            ]
        }

        for book_id, quiz_list in quizzes.items():
            book = Book.objects.get(id=book_id)
            for quiz_data in quiz_list:
                Quiz.objects.get_or_create(
                    book=book,
                    question=quiz_data["question"],
                    defaults={
                        "options": quiz_data["options"],
                        "answer": quiz_data["answer"]
                    }
                )
                self.stdout.write(self.style.SUCCESS(f"Quiz '{quiz_data['question']}' for book '{book.title}' added or already exists."))
