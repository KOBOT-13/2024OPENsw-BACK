from django.core.management.base import BaseCommand
from books.models import Book

class Command(BaseCommand):
    help = 'Load initial book data'

    def handle(self, *args, **kwargs):
        more_books = [
            {
                "title": "신데렐라",
                "author": "샤를 페로",
                "category": "fantasy",
                "tag_ids": [1, 4],
                "cover_image": "morebook_cover/1.png"
            },
            {
                "title": "잠자는 숲속의 공주",
                "author": "샤를 페로",
                "category": "fantasy",
                "tag_ids": [1, 4],
                "cover_image": "morebook_cover/2.png"
            },
            {
                "title": "토끼와 거북이",
                "author": "이솝 우화",
                "category": "fable",
                "tag_ids": [3, 14],
                "cover_image": "morebook_cover/3.png"
            },
            {
                "title": "빨간 모자",
                "author": "샤를 페로",
                "category": "fantasy",
                "tag_ids": [3],
                "cover_image": "morebook_cover/4.png"
            },
            {
                "title": "장화 신은 고양이",
                "author": "샤를 페로",
                "category": "fantasy",
                "tag_ids": [5, 2, 3],
                "cover_image": "morebook_cover/5.png"
            },
            {
                "title": "라푼젤",
                "author": "그림형제",
                "category": "fantasy",
                "tag_ids": [1, 4, 3],
                "cover_image": "morebook_cover/6.png"
            },
            {
                "title": "미녀와 야수",
                "author": "쟌 마리 르 프랭스 드 보몽",
                "category": "fantasy",
                "tag_ids": [1, 4, 3, 5],
                "cover_image": "morebook_cover/7.png"
            },
            {
                "title": "인어공주",
                "author": "한스 크리스티안 안데르센",
                "category": "fantasy",
                "tag_ids": [1, 4],
                "cover_image": "morebook_cover/8.png"
            },
            {
                "title": "미운 오리 새끼",
                "author": "한스 크리스티안 안데르센",
                "category": "fable",
                "tag_ids": [5, 1, 9],
                "cover_image": "morebook_cover/9.png"
            },
            {
                "title": "피노키오",
                "author": "카를로 콜로디",
                "category": "fantasy",
                "tag_ids": [3, 1],
                "cover_image": "morebook_cover/10.png"
            },
            {
                "title": "알라딘과 요술 램프",
                "author": "작자 미상",
                "category": "fantasy",
                "tag_ids": [2, 5, 3],
                "cover_image": "morebook_cover/11.png"
            },
            {
                "title": "알리바바와 40인의 도둑",
                "author": "작자 미상",
                "category": "fantasy",
                "tag_ids": [2, 5, 15],
                "cover_image": "morebook_cover/12.png"
            },
            {
                "title": "톰 소여의 모험",
                "author": "작자 미상",
                "category": "novel",
                "tag_ids": [2, 5, 3],
                "cover_image": "morebook_cover/13.png"
            },
            {
                "title": "해와 달이 된 오누이",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [5, 8, 1, 3],
                "cover_image": "morebook_cover/14.png"
            },
            {
                "title": "콩쥐팥쥐",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [5, 10],
                "cover_image": "morebook_cover/15.png"
            },
            {
                "title": "견우와 직녀",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [1, 9],
                "cover_image": "morebook_cover/1.png"
            },
            {
                "title": "심정천",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [1, 8, 6, 17],
                "cover_image": "morebook_cover/2.png"
            },
            {
                "title": "별주부전",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [3, 5],
                "cover_image": "morebook_cover/3.png"
            },
            {
                "title": "금도끼와 은도끼",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [10, 14],
                "cover_image": "morebook_cover/4.png"
            },
            {
                "title": "선녀와 나무꾼",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [1, 8],
                "cover_image": "morebook_cover/5.png"
            },
            {
                "title": "장화홍련전",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [8, 1, 5, 10],
                "cover_image": "morebook_cover/6.png"
            },
            {
                "title": "호랑이와 곶감",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [3, 5],
                "cover_image": "morebook_cover/7.png"
            },
            {
                "title": "청개구리",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [6, 8],
                "cover_image": "morebook_cover/8.png"
            },
            {
                "title": "바리데기",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [6],
                "cover_image": "morebook_cover/9.png"
            },
            {
                "title": "선비와 구렁이",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [7, 10],
                "cover_image": "morebook_cover/10.png"
            },
            {
                "title": "호랑이와 팥죽 할머니",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [7, 10],
                "cover_image": "morebook_cover/11.png"
            },
            {
                "title": "황금알을 낳는 거위",
                "author": "이솝 우화",
                "category": "fable",
                "tag_ids": [3, 10],
                "cover_image": "morebook_cover/12.png"
            },
            {
                "title": "엄지공주",
                "author": "한스 크리스티안 안데르센",
                "category": "fantasy",
                "tag_ids": [4, 5, 10],
                "cover_image": "morebook_cover/13.png"
            },
            {
                "title": "브레멘 음악대",
                "author": "그림형제",
                "category": "fantasy",
                "tag_ids": [5, 2, 11],
                "cover_image": "morebook_cover/14.png"
            },
            {
                "title": "피리 부는 사나이",
                "author": "그림형제",
                "category": "fantasy",
                "tag_ids": [10, 15],
                "cover_image": "morebook_cover/15.png"
            },
            {
                "title": "콧구멍을 후비면",
                "author": "사이토 타카코",
                "category": "picture book",
                "tag_ids": [12, 3],
                "cover_image": "morebook_cover/1.png"
            },
            {
                "title": "소공자",
                "author": "프랜시스 호지슨 버넷",
                "category": "novel",
                "tag_ids": [8, 10],
                "cover_image": "morebook_cover/2.png"
            },
            {
                "title": "이상한 나라의 앨리스",
                "author": "루이스 캐럴",
                "category": "fantasy",
                "tag_ids": [5, 2, 3],
                "cover_image": "morebook_cover/3.png"
            },
            {
                "title": "잭과 콩나무",
                "author": "에드 브라이언",
                "category": "fantasy",
                "tag_ids": [5, 2, 3],
                "cover_image": "morebook_cover/4.png"
            },
            {
                "title": "파랑새",
                "author": "모리스 메테르링크",
                "category": "fantasy",
                "tag_ids": [9, 8],
                "cover_image": "morebook_cover/5.png"
            },
            {
                "title": "강아지 똥",
                "author": "권정생",
                "category": "picture book",
                "tag_ids": [5, 1],
                "cover_image": "morebook_cover/6.png"
            },
            {
                "title": "구름빵",
                "author": "백희나",
                "category": "picture book",
                "tag_ids": [8, 9],
                "cover_image": "morebook_cover/7.png"
            },
            {
                "title": "누가 내머리에 똥 쌌어",
                "author": "베르너 홀츠바르트",
                "category": "picture book",
                "tag_ids": [3, 2],
                "cover_image": "morebook_cover/8.png"
            },
            {
                "title": "마당을 나온 암탉",
                "author": "황선미",
                "category": "novel",
                "tag_ids": [1, 2, 5],
                "cover_image": "morebook_cover/9.png"
            },
            {
                "title": "모모",
                "author": "미하엘 엔데",
                "category": "novel",
                "tag_ids": [3, 9],
                "cover_image": "morebook_cover/10.png"
            },
            {
                "title": "찰리와 초콜릿 공장",
                "author": "로알드 달",
                "category": "fantasy",
                "tag_ids": [5, 2, 8],
                "cover_image": "morebook_cover/11.png"
            },
            {
                "title": "생각을 모으는 사람",
                "author": "모니카 페트",
                "category": "novel",
                "tag_ids": [3, 9],
                "cover_image": "morebook_cover/12.png"
            },
            {
                "title": "수박 수영장",
                "author": "안녕달",
                "category": "picture book",
                "tag_ids": [8, 9],
                "cover_image": "morebook_cover/13.png"
            },
            {
                "title": "감정 호텔",
                "author": "리디아 브란코비치",
                "category": "picture book",
                "tag_ids": [9, 5, 13],
                "cover_image": "morebook_cover/14.png"
            },
            {
                "title": "알사탕",
                "author": "백희나",
                "category": "picture book",
                "tag_ids": [1, 8],
                "cover_image": "morebook_cover/15.png"
            },
            {
                "title": "장수탕 선녀님",
                "author": "백희나",
                "category": "picture book",
                "tag_ids": [10, 7],
                "cover_image": "morebook_cover/1.png"
            },
            {
                "title": "오싹오싹 팬티",
                "author": "애런 레이놀즈",
                "category": "picture book",
                "tag_ids": [5, 3],
                "cover_image": "morebook_cover/2.png"
            },
            {
                "title": "엄마의 여름 방학",
                "author": "김유진",
                "category": "picture book",
                "tag_ids": [8, 9],
                "cover_image": "morebook_cover/3.png"
            },
            {
                "title": "무지개 물고기",
                "author": "마르쿠스 피스터",
                "category": "picture book",
                "tag_ids": [11, 10],
                "cover_image": "morebook_cover/4.png"
            },
            {
                "title": "수상한 신호등",
                "author": "더 캐빈 컴퍼니",
                "category": "picture book",
                "tag_ids": [3],
                "cover_image": "morebook_cover/5.png"
            },
            {
                "title": "세종대왕",
                "author": "-",
                "category": "biography",
                "tag_ids": [14, 3],
                "cover_image": "morebook_cover/6.png"
            },
            {
                "title": "이순신",
                "author": "-",
                "category": "biography",
                "tag_ids": [5, 3, 17],
                "cover_image": "morebook_cover/7.png"
            },
            {
                "title": "김구",
                "author": "-",
                "category": "biography",
                "tag_ids": [5, 10, 17],
                "cover_image": "morebook_cover/8.png"
            },
            {
                "title": "유관순",
                "author": "-",
                "category": "biography",
                "tag_ids": [5, 3, 17],
                "cover_image": "morebook_cover/9.png"
            },
            {
                "title": "장영실",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 14],
                "cover_image": "morebook_cover/10.png"
            },
            {
                "title": "정약용",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 14],
                "cover_image": "morebook_cover/11.png"
            },
            {
                "title": "안중근",
                "author": "-",
                "category": "biography",
                "tag_ids": [5, 10, 17],
                "cover_image": "morebook_cover/12.png"
            },
            {
                "title": "홍길동",
                "author": "허균",
                "category": "novel",
                "tag_ids": [3, 10],
                "cover_image": "morebook_cover/13.png"
            },
            {
                "title": "신사임당",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 14],
                "cover_image": "morebook_cover/14.png"
            },
            {
                "title": "아인슈타인",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 14, 16],
                "cover_image": "morebook_cover/15.png"
            },
            {
                "title": "마리 퀴리",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 5, 16],
                "cover_image": "morebook_cover/1.png"
            },
            {
                "title": "넬슨 만델라",
                "author": "-",
                "category": "biography",
                "tag_ids": [5, 3],
                "cover_image": "morebook_cover/2.png"
            },
            {
                "title": "간디",
                "author": "-",
                "category": "biography",
                "tag_ids": [5],
                "cover_image": "morebook_cover/3.png"
            },
            {
                "title": "마틴 루터 킹",
                "author": "-",
                "category": "biography",
                "tag_ids": [5, 3],
                "cover_image": "morebook_cover/4.png"
            },
            {
                "title": "레오나르도 다빈치",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 16],
                "cover_image": "morebook_cover/5.png"
            },
            {
                "title": "헬렌 켈러",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 1],
                "cover_image": "morebook_cover/6.png"
            },
            {
                "title": "에디슨",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 5, 16],
                "cover_image": "morebook_cover/7.png"
            },
            {
                "title": "슈바이처",
                "author": "-",
                "category": "biography",
                "tag_ids": [10, 14],
                "cover_image": "morebook_cover/8.png"
            },
            {
                "title": "윤동주",
                "author": "-",
                "category": "biography",
                "tag_ids": [10, 5, 17],
                "cover_image": "morebook_cover/9.png"
            },
            {
                "title": "벌거벗은 임금님",
                "author": "한스 크리스티안 안데르센",
                "category": "picture book",
                "tag_ids": [3, 5],
                "cover_image": "morebook_cover/10.png"
            },
            {
                "title": "토끼와 자라",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [3, 10],
                "cover_image": "morebook_cover/11.png"
            },
            {
                "title": "혹부리영감",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [10],
                "cover_image": "morebook_cover/12.png"
            },
            {
                "title": "은혜 갚은 두꺼비",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [7, 10],
                "cover_image": "morebook_cover/13.png"
            },
            {
                "title": "호두까기 인형",
                "author": "에른스트 테오도어 빌헬름 호프만",
                "category": "fantasy",
                "tag_ids": [1, 7, 5, 2],
                "cover_image": "morebook_cover/14.png"
            },
            {
                "title": "행복한 왕자",
                "author": "오스카 와일드",
                "category": "novel",
                "tag_ids": [1, 13, 7],
                "cover_image": "morebook_cover/15.png"
            },
            {
                "title": "개구리 왕자",
                "author": "그림형제",
                "category": "fantasy",
                "tag_ids": [1, 4, 15],
                "cover_image": "morebook_cover/1.png"
            },
            {
                "title": "개미와 베짱이",
                "author": "이솝 우화",
                "category": "fable",
                "tag_ids": [14, 3],
                "cover_image": "morebook_cover/2.png"
            },
            {
                "title": "늑대와 일곱마리 아기 염소",
                "author": "그림형제",
                "category": "fable",
                "tag_ids": [3, 5, 8],
                "cover_image": "morebook_cover/3.png"
            },
            {
                "title": "시골쥐와 도시쥐",
                "author": "이솝 우화",
                "category": "fable",
                "tag_ids": [3, 9],
                "cover_image": "morebook_cover/4.png"
            },
            {
                "title": "거인의 정원",
                "author": "오스카 와일드",
                "category": "fantasy",
                "tag_ids": [9, 11],
                "cover_image": "morebook_cover/5.png"
            },
            {
                "title": "여우와 두루미",
                "author": "이솝 우화",
                "category": "fable",
                "tag_ids": [3, 11],
                "cover_image": "morebook_cover/6.png"
            },
            {
                "title": "구두쇠 스크루지",
                "author": "찰스 디킨스",
                "category": "novel",
                "tag_ids": [10, 9],
                "cover_image": "morebook_cover/7.png"
            },
            {
                "title": "훈장님과 꿀단지",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [3, 5],
                "cover_image": "morebook_cover/8.png"
            },
            {
                "title": "빨간 부채 파란 부채",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [3, 10],
                "cover_image": "morebook_cover/9.png"
            },
            {
                "title": "젊어지는 샘물",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [10],
                "cover_image": "morebook_cover/10.png"
            },
            {
                "title": "돌멩이 수프",
                "author": "작자 미상",
                "category": "picture book",
                "tag_ids": [10, 9],
                "cover_image": "morebook_cover/11.png"
            },
            {
                "title": "구둣방 할아버지와 꼬마 요정",
                "author": "그림형제",
                "category": "picture book",
                "tag_ids": [14, 7],
                "cover_image": "morebook_cover/12.png"
            },
            {
                "title": "바보 이반",
                "author": "레프 톨스토이",
                "category": "novel",
                "tag_ids": [14, 10],
                "cover_image": "morebook_cover/13.png"
            },
            {
                "title": "양치기 소년",
                "author": "이솝 우화",
                "category": "fable",
                "tag_ids": [10],
                "cover_image": "morebook_cover/14.png"
            },
            {
                "title": "사이 좋은 형제",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [8, 9],
                "cover_image": "morebook_cover/15.png"
            },
            {
                "title": "해와 바람",
                "author": "이솝 우화",
                "category": "fable",
                "tag_ids": [3],
                "cover_image": "morebook_cover/1.png"
            },
            {
                "title": "커다란 순무",
                "author": "이솝 우화",
                "category": "traditional fairy tale",
                "tag_ids": [14, 8],
                "cover_image": "morebook_cover/2.png"
            },
            {
                "title": "삼년고개",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [3],
                "cover_image": "morebook_cover/3.png"
            },
            {
                "title": "사자와 생쥐",
                "author": "이솝 우화",
                "category": "fable",
                "tag_ids": [7, 11],
                "cover_image": "morebook_cover/4.png"
            },
            {
                "title": "도깨비 방망이",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [10, 3],
                "cover_image": "morebook_cover/5.png"
            },
            {
                "title": "요술항아리",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [14, 10],
                "cover_image": "morebook_cover/6.png"
            },
            {
                "title": "우렁각시",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [7, 10],
                "cover_image": "morebook_cover/7.png"
            },
            {
                "title": "소가 된 게으름뱅이",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [14],
                "cover_image": "morebook_cover/8.png"
            },
            {
                "title": "요술 맷돌",
                "author": "작자 미상",
                "category": "picture book",
                "tag_ids": [10],
                "cover_image": "morebook_cover/9.png"
            },
            {
                "title": "곰과 두 친구",
                "author": "이솝 우화",
                "category": "fable",
                "tag_ids": [3, 11],
                "cover_image": "morebook_cover/10.png"
            },
            {
                "title": "소금장수와 당나귀",
                "author": "이솝 우화",
                "category": "fable",
                "tag_ids": [10, 14],
                "cover_image": "morebook_cover/11.png"
            },
            {
                "title": "도깨비 감투",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [10],
                "cover_image": "morebook_cover/12.png"
            },
            {
                "title": "개와 고양이",
                "author": "이솝 우화",
                "category": "traditional fairy tale",
                "tag_ids": [10, 3],
                "cover_image": "morebook_cover/13.png"
            },
            {
                "title": "라이트 형제",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 5, 14, 16],
                "cover_image": "morebook_cover/14.png"
            },
            {
                "title": "스티브잡스",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 14, 16],
                "cover_image": "morebook_cover/15.png"
            },
            {
                "title": "오성과 한음",
                "author": "-",
                "category": "biography",
                "tag_ids": [11, 3],
                "cover_image": "morebook_cover/1.png"
            },
            {
                "title": "나이팅게일",
                "author": "-",
                "category": "biography",
                "tag_ids": [1, 7],
                "cover_image": "morebook_cover/2.png"
            },
            {
                "title": "스티븐호킹",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 14, 5, 16],
                "cover_image": "morebook_cover/3.png"
            },
            {
                "title": "방정환",
                "author": "-",
                "category": "biography",
                "tag_ids": [1, 8],
                "cover_image": "morebook_cover/4.png"
            },
            {
                "title": "페스탈로치",
                "author": "-",
                "category": "biography",
                "tag_ids": [1, 8],
                "cover_image": "morebook_cover/1.png"
            },
            {
                "title": "칭키즈 칸",
                "author": "-",
                "category": "biography",
                "tag_ids": [5],
                "cover_image": "morebook_cover/2.png"
            },
            {
                "title": "이태석",
                "author": "-",
                "category": "biography",
                "tag_ids": [1, 10],
                "cover_image": "morebook_cover/3.png"
            },
            {
                "title": "주시경",
                "author": "-",
                "category": "biography",
                "tag_ids": [3],
                "cover_image": "morebook_cover/4.png"
            },
            {
                "title": "조앤 롤링",
                "author": "-",
                "category": "biography",
                "tag_ids": [14, 5, 3],
                "cover_image": "morebook_cover/5.png"
            },
            {
                "title": "황금을 버린 형제",
                "author": "작자 미상",
                "category": "picture book",
                "tag_ids": [8, 1, 10],
                "cover_image": "morebook_cover/6.png"
            },
            {
                "title": "링컨",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 14, 1],
                "cover_image": "morebook_cover/7.png"
            },
            {
                "title": "윈스턴 처칠",
                "author": "-",
                "category": "biography",
                "tag_ids": [5, 3],
                "cover_image": "morebook_cover/8.png"
            },
            {
                "title": "효성스런 호랑이",
                "author": "작자 미상",
                "category": "traditional fairy tale",
                "tag_ids": [1, 8, 10],
                "cover_image": "morebook_cover/9.png"
            },
            {
                "title": "마더 테레사",
                "author": "-",
                "category": "biography",
                "tag_ids": [1, 10, 17],
                "cover_image": "morebook_cover/10.png"
            },
            {
                "title": "아이작 뉴턴",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 14, 16],
                "cover_image": "morebook_cover/11.png"
            },
            {
                "title": "찰스 다윈",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 14, 16],
                "cover_image": "morebook_cover/12.png"
            },
            {
                "title": "송아지와 바꾼 무",
                "author": "작자 미상",
                "category": "picture book",
                "tag_ids": [10, 14],
                "cover_image": "morebook_cover/13.png"
            },
            {
                "title": "안네의 일기",
                "author": "안네 프랑크",
                "category": "novel",
                "tag_ids": [5, 8, 13, 1],
                "cover_image": "morebook_cover/14.png"
            },
            {
                "title": "마지막 잎새",
                "author": "오 헨리",
                "category": "novel",
                "tag_ids": [5, 1, 13, 8, 9],
                "cover_image": "morebook_cover/15.png"
            },
            {
                "title": "작은 아씨들",
                "author": "루이자 메이 올컷",
                "category": "novel",
                "tag_ids": [8, 1, 9],
                "cover_image": "morebook_cover/1.png"
            },
            {
                "title": "플랜더스의 개",
                "author": "위다",
                "category": "novel",
                "tag_ids": [1, 8, 9, 11, 13],
                "cover_image": "morebook_cover/2.png"
            },
            {
                "title": "비밀의 화원",
                "author": "프랜시스 호지슨 버넷",
                "category": "novel",
                "tag_ids": [1, 8, 9],
                "cover_image": "morebook_cover/3.png"
            },
            {
                "title": "사랑의 학교",
                "author": "에드몬드 데 아미치스",
                "category": "novel",
                "tag_ids": [1, 9, 11],
                "cover_image": "morebook_cover/4.png"
            },
            {
                "title": "키다리 아저씨",
                "author": "진 웹스터",
                "category": "novel",
                "tag_ids": [1, 9, 11],
                "cover_image": "morebook_cover/5.png"
            },
            {
                "title": "제인 에어",
                "author": "샬럿 브론테",
                "category": "novel",
                "tag_ids": [1, 5],
                "cover_image": "morebook_cover/6.png"
            },
            {
                "title": "조지 워싱턴",
                "author": "-",
                "category": "biography",
                "tag_ids": [5, 14],
                "cover_image": "morebook_cover/7.png"
            },
            {
                "title": "벤자민 프랭클린",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 14],
                "cover_image": "morebook_cover/8.png"
            },
            {
                "title": "리처드 파인만",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 16],
                "cover_image": "morebook_cover/9.png"
            },
            {
                "title": "제인 구달",
                "author": "-",
                "category": "biography",
                "tag_ids": [1, 14, 3],
                "cover_image": "morebook_cover/10.png"
            },
            {
                "title": "마가렛 대처",
                "author": "-",
                "category": "biography",
                "tag_ids": [5, 14, 3],
                "cover_image": "morebook_cover/11.png"
            },
            {
                "title": "앨프리드 노벨",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 1, 14, 16],
                "cover_image": "morebook_cover/12.png"
            },
            {
                "title": "리오넬 메시",
                "author": "-",
                "category": "biography",
                "tag_ids": [5, 14, 17],
                "cover_image": "morebook_cover/13.png"
            },
            {
                "title": "페르난디 마젤란",
                "author": "-",
                "category": "biography",
                "tag_ids": [2, 5],
                "cover_image": "morebook_cover/14.png"
            },
            {
                "title": "안토니오 비발디",
                "author": "-",
                "category": "biography",
                "tag_ids": [14, 16],
                "cover_image": "morebook_cover/15.png"
            },
            {
                "title": "베토벤",
                "author": "-",
                "category": "biography",
                "tag_ids": [5, 14, 16],
                "cover_image": "morebook_cover/1.png"
            },
            {
                "title": "모차르트",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 16],
                "cover_image": "morebook_cover/2.png"
            },
            {
                "title": "오즈의 마법사",
                "author": "라이먼 프랭크 봄",
                "category": "novel",
                "tag_ids": [2, 5, 3, 1, 15],
                "cover_image": "morebook_cover/3.png"
            },
            {
                "title": "슈베르트",
                "author": "-",
                "category": "biography",
                "tag_ids": [3, 14, 16],
                "cover_image": "morebook_cover/4.png"
            },
            {
                "title": "정글북",
                "author": "루디야드 키플링",
                "category": "novel",
                "tag_ids": [1, 8, 5],
                "cover_image": "morebook_cover/5.png"
            },
            {
                "title": "지킬박사와 하이드씨",
                "author": "로버트 루이스 스티븐슨",
                "category": "novel",
                "tag_ids": [5, 10],
                "cover_image": "morebook_cover/6.png"
            },
            {
                "title": "보물섬",
                "author": "로버트 루이스 스티븐슨",
                "category": "novel",
                "tag_ids": [2, 5, 3, 15],
                "cover_image": "morebook_cover/7.png"
            },
            {
                "title": "걸리버여행기",
                "author": "조나단 스위프트",
                "category": "novel",
                "tag_ids": [2, 10, 15],
                "cover_image": "morebook_cover/8.png"
            },
            {
                "title": "빨간 머리 앤",
                "author": "루시 모드 몽고메리",
                "category": "novel",
                "tag_ids": [5, 1],
                "cover_image": "morebook_cover/9.png"
            },
            {
                "title": "홍당무",
                "author": "쥘 르나르",
                "category": "novel",
                "tag_ids": [8, 5],
                "cover_image": "morebook_cover/10.png"
            },
            {
                "title": "파브르곤충기",
                "author": "장앙리 카시미르 파브르",
                "category": "novel",
                "tag_ids": [14, 16, 3],
                "cover_image": "morebook_cover/11.png"
            },
            {
                "title": "어린왕자",
                "author": "앙투안 드 생텍쥐페리",
                "category": "novel",
                "tag_ids": [1, 3, 15],
                "cover_image": "morebook_cover/12.png"
            },
            {
                "title": "백조 왕자",
                "author": "한스 크리스티안 안데르센",
                "category": "novel",
                "tag_ids": [1, 8],
                "cover_image": "morebook_cover/13.png"
            },
            {
                "title": "어제 저녁",
                "author": "백희나",
                "category": "picture book",
                "tag_ids": [9, 15],
                "cover_image": "morebook_cover/14.png"
            },
            {
                "title": "삐약이 엄마",
                "author": "백희나",
                "category": "picture book",
                "tag_ids": [8, 1],
                "cover_image": "morebook_cover/15.png"
            },
            {
                "title": "왕자와 거지",
                "author": "마크 트웨인",
                "category": "novel",
                "tag_ids": [1, 5, 3],
                "cover_image": "morebook_cover/1.png"
            },
            {
                "title": "큰바위 얼굴",
                "author": "너새니얼 호손",
                "category": "novel",
                "tag_ids": [1, 14, 3],
                "cover_image": "morebook_cover/2.png"
            },
            {
                "title": "나폴레옹",
                "author": "-",
                "category": "biography",
                "tag_ids": [14, 5, 3],
                "cover_image": "morebook_cover/3.png"
            },
            {
                "title": "해저이만리",
                "author": "쥘 베른",
                "category": "fantasy",
                "tag_ids": [2, 15, 5],
                "cover_image": "morebook_cover/4.png"
            },
            {
                "title": "고양이 목에 방울 달기",
                "author": "이솝 우화",
                "category": "fable",
                "tag_ids": [5, 3],
                "cover_image": "morebook_cover/5.png"
            },
            {
                "title": "알프스 소녀 하이디",
                "author": "요하나 슈피리",
                "category": "novel",
                "tag_ids": [8, 1, 9],
                "cover_image": "morebook_cover/6.png"
            },
            {
                "title": "사람은 무엇으로 사는가",
                "author": "레프 톨스토이",
                "category": "novel",
                "tag_ids": [1, 9],
                "cover_image": "morebook_cover/7.png"
            },
            {
                "title": "허클베리 핀의 모험",
                "author": "마크 트웨인",
                "category": "novel",
                "tag_ids": [2, 10, 5],
                "cover_image": "morebook_cover/8.png"
            },
            {
                "title": "꿀벌 마야의 모험",
                "author": "발데마르 본젤스",
                "category": "novel",
                "tag_ids": [2, 11],
                "cover_image": "morebook_cover/9.png"
            },
            {
                "title": "신밧드의 모험",
                "author": "작자 미상",
                "category": "novel",
                "tag_ids": [2, 5, 3],
                "cover_image": "morebook_cover/10.png"
            },
            {
                "title": "손오공",
                "author": "오승은",
                "category": "novel",
                "tag_ids": [2, 10, 5],
                "cover_image": "morebook_cover/11.png"
            },
            {
                "title": "당근 할머니",
                "author": "안녕달",
                "category": "picture book",
                "tag_ids": [8, 1, 9],
                "cover_image": "morebook_cover/12.png"
            },
            {
                "title": "팥빙수의 전설",
                "author": "이지은",
                "category": "picture book",
                "tag_ids": [15, 9],
                "cover_image": "morebook_cover/13.png"
            },
            {
                "title": "공주와 완두콩",
                "author": "한스 크리스티안 안데르센",
                "category": "picture book",
                "tag_ids": [10, 3],
                "cover_image": "morebook_cover/14.png"
            },
            {
                "title": "진짜 진짜 행복해",
                "author": "애나벨 세구라 란츠",
                "category": "picture book",
                "tag_ids": [8, 1, 11, 9],
                "cover_image": "morebook_cover/15.png"
            },
            {
                "title": "무례한 친구가 생겼어요",
                "author": "크리스티나 퍼니발",
                "category": "picture book",
                "tag_ids": [10, 11],
                "cover_image": "morebook_cover/1.png"
            },
            {
                "title": "달샤베트",
                "author": "백희나",
                "category": "picture book",
                "tag_ids": [10, 15],
                "cover_image": "morebook_cover/2.png"
            },
            {
                "title": "이상한 엄마",
                "author": "백희나",
                "category": "picture book",
                "tag_ids": [8, 1, 15],
                "cover_image": "morebook_cover/3.png"
            },
            {
                "title": "이상한 손님",
                "author": "백희나",
                "category": "picture book",
                "tag_ids": [8, 15],
                "cover_image": "morebook_cover/4.png"
            },
            {
                "title": "나는 개다",
                "author": "백희나",
                "category": "picture book",
                "tag_ids": [8, 1, 9],
                "cover_image": "morebook_cover/5.png"
            },
            {
                "title": "알사탕 제조법",
                "author": "백희나",
                "category": "picture book",
                "tag_ids": [2, 15],
                "cover_image": "morebook_cover/6.png"
            },
            {
                "title": "돼지책",
                "author": "앤서니 브라운",
                "category": "picture book",
                "tag_ids": [8, 1],
                "cover_image": "morebook_cover/7.png"
            },
            {
                "title": "고릴라",
                "author": "앤서니 브라운",
                "category": "picture book",
                "tag_ids": [8, 1, 13, 9],
                "cover_image": "morebook_cover/8.png"
            },
            {
                "title": "우리 엄마",
                "author": "앤서니 브라운",
                "category": "picture book",
                "tag_ids": [8, 1, 7, 9],
                "cover_image": "morebook_cover/9.png"
            },
            {
                "title": "기분을 말해봐",
                "author": "앤서니 브라운",
                "category": "picture book",
                "tag_ids": [5, 9],
                "cover_image": "morebook_cover/10.png"
            },
            {
                "title": "마술 연필",
                "author": "앤서니 브라운",
                "category": "picture book",
                "tag_ids": [2, 15],
                "cover_image": "morebook_cover/11.png"
            },
            {
                "title": "겁쟁이 윌리",
                "author": "앤서니 브라운",
                "category": "picture book",
                "tag_ids": [5, 3],
                "cover_image": "morebook_cover/12.png"
            },
            {
                "title": "나의 프리다",
                "author": "앤서니 브라운",
                "category": "picture book",
                "tag_ids": [15, 5, 11],
                "cover_image": "morebook_cover/13.png"
            },
            {
                "title": "행복한 미술관",
                "author": "앤서니 브라운",
                "category": "picture book",
                "tag_ids": [8, 3, 16],
                "cover_image": "morebook_cover/14.png"
            },
            {
                "title": "도깨비를 빨아버린 우리엄마",
                "author": "사토 와키코",
                "category": "picture book",
                "tag_ids": [8, 5, 16, 12],
                "cover_image": "morebook_cover/15.png"
            },
            {
                "title": "터널",
                "author": "앤서니 브라운",
                "category": "picture book",
                "tag_ids": [8, 1, 5, 9],
                "cover_image": "morebook_cover/1.png"
            },
            {
                "title": "아낌없이 주는 나무",
                "author": "셸 실버스타인",
                "category": "picture book",
                "tag_ids": [1, 5, 11, 9, 17],
                "cover_image": "morebook_cover/2.png"
            },
            {
                "title": "샌지와 빵집주인",
                "author": "로빈 자엔스",
                "category": "picture book",
                "tag_ids": [5, 3],
                "cover_image": "morebook_cover/3.png"
            },
            {
                "title": "도서관에 간 사자",
                "author": "미셸 누드슨",
                "category": "picture book",
                "tag_ids": [5, 3],
                "cover_image": "morebook_cover/4.png"
            },
            {
                "title": "파란수염",
                "author": "샤를 페로",
                "category": "picture book",
                "tag_ids": [2, 10, 5],
                "cover_image": "morebook_cover/5.png"
            },
            {
                "title": "너는 특별하단다",
                "author": "맥스 루카도",
                "category": "picture book",
                "tag_ids": [1, 5, 13, 9],
                "cover_image": "morebook_cover/6.png"
            },
            {
                "title": "이야기 이야기",
                "author": "게일 헤일리",
                "category": "picture book",
                "tag_ids": [2, 15, 5],
                "cover_image": "morebook_cover/7.png"
            },
            {
                "title": "도서관 생쥐",
                "author": "다니엘 커크",
                "category": "picture book",
                "tag_ids": [3, 16],
                "cover_image": "morebook_cover/8.png"
            },
            {
                "title": "나야? 고양이야?",
                "author": "기타무라 사토시",
                "category": "picture book",
                "tag_ids": [8, 2],
                "cover_image": "morebook_cover/9.png"
            },
            {
                "title": "마법의 막대기",
                "author": "클레이 라이스",
                "category": "picture book",
                "tag_ids": [15, 5, 16],
                "cover_image": "morebook_cover/10.png"
            },
            {
                "title": "색깔을 만드는 아기고양이",
                "author": "마거릿 와이즈 브라운",
                "category": "picture book",
                "tag_ids": [16, 9],
                "cover_image": "morebook_cover/11.png"
            },
            {
                "title": "나는 책이 싫어!",
                "author": "맨주샤 퍼워기",
                "category": "picture book",
                "tag_ids": [2, 15, 16],
                "cover_image": "morebook_cover/12.png"
            }
        ]

        for book_data in more_books:
            tag_ids = book_data.pop('tag_ids')
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                author=book_data['author'],
                category=book_data['category'],
                cover_image = book_data['cover_image']
            )
            if created:
                book.tags.set(tag_ids)
                self.stdout.write(self.style.SUCCESS(f"Successfully added book '{book.title}'"))
            else:
                self.stdout.write(self.style.WARNING(f"Book '{book.title}' already exists"))
