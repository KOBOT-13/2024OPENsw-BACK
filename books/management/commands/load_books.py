from django.core.management.base import BaseCommand
from books.models import Book

class Command(BaseCommand):
    help = 'Load initial book data'

    def handle(self, *args, **kwargs):
        books = [
            {
                "title": "아기 돼지 삼형제",
                "author": "조지프 제이콥스",
                "publisher": " ",
                "synopsis": "아기 돼지 삼형제는 세 마리의 아기돼지가 늑대를 피해 집을 짓는 이야기입니다. 첫째 돼지는 빨리 집을 짓기 위해 짚으로 집을 짓고, 둘째 돼지는 나무로 집을 짓습니다. 그러나 늑대가 나타나 이 두 집을 쉽게 무너뜨리자, 셋째 돼지는 벽돌로 튼튼한 집을 짓습니다. 결국, 늑대는 셋째 돼지의 집을 무너뜨리지 못하고 돼지 삼형제는 안전하게 지내게 됩니다.",
                "category": "fable",
                "tag_ids": [3],
                "cover_image": "book_cover/아기돼지삼형제.png"
           },
            {
                "title": "백설공주",
                "author": "그림형제",
                "publisher": " ",
                "synopsis": "백설공주는 아름다운 공주로, 질투심 많은 계모 여왕의 미움을 받습니다. 여왕은 마법의 거울을 통해 자신이 가장 아름답다는 것을 확인하려 하지만, 거울은 항상 백설공주가 더 아름답다고 말합니다. 분노한 여왕은 사냥꾼을 시켜 백설공주를 죽이려 하지만, 백설공주는 숲 속으로 도망쳐 일곱 난쟁이의 집에 숨습니다. 여왕은 독이 든 사과로 백설공주를 속여 잠들게 하지만, 왕자의 키스로 백설공주는 깨어나고, 두 사람은 행복하게 결혼하게 됩니다.",
                "category": "fantasy", 
                "tag_ids": [1,4],
                "cover_image": "book_cover/백설공주.png"
            },
            {
                "title": "피터팬",
                "author": "제임스 매튜 배리",
                "publisher": " ",
                "synopsis": "피터팬은 네버랜드라는 신비한 섬에서 영원히 어린아이로 사는 소년입니다. 피터팬은 날아다니는 능력을 가지고 있으며, 요정 팅커벨과 함께 모험을 즐깁니다. 어느 날 피터팬은 런던에서 웬디 다알링과 그녀의 두 동생 존, 마이클을 만나 네버랜드로 데려갑니다. 네버랜드에서 아이들은 인디언, 인어, 해적 등과 만나고, 악당인 후크 선장과 그의 해적들과 싸웁니다. 결국 피터팬과 그의 친구들은 후크 선장을 물리치고, 웬디와 그녀의 동생들은 집으로 돌아가지만, 피터팬은 다시 네버랜드로 돌아갑니다. 피터팬은 영원히 어른이 되지 않고 모험을 계속 이어갑니다.",
                "category": "fantasy",
                "tag_ids": [2,5,11],
                "cover_image": "book_cover/피터팬.png"
            },
            {
                "title": "흥부와 놀부",
                "author": "작자 미상",
                "publisher": " ",
                "synopsis": "흥부와 놀부는 한국의 전통 설화로, 형제의 이야기를 다룹니다. 욕심 많고 못된 형 놀부는 부유하게 살고, 착하고 가난한 동생 흥부는 가난하게 삽니다. 어느 날 흥부는 다친 제비를 치료해주고, 제비는 은혜를 갚기 위해 박씨를 가져옵니다. 흥부가 그 박씨를 심자, 커다란 박이 열리고, 그 안에서 많은 재물이 나옵니다. 이를 본 놀부는 일부러 제비 다리를 부러뜨려 박씨를 받지만, 그의 박에서 나온 것은 벌레와 해충뿐이었습니다. 결국 흥부의 선행이 보답을 받는다는 교훈을 전합니다.",
                "category": "traditional fairy tale",
                "tag_ids": [7,10],
                "cover_image": "book_cover/흥부와놀부.png"
            },
            {
                "title": "헨젤과 그레텔",
                "author": "그림형제",
                "publisher": " ",
                "synopsis": "헨젤과 그레텔은 가난한 나무꾼의 남매입니다. 그들의 계모는 아이들을 숲에 버리기로 결심하고, 아버지를 설득합니다. 헨젤과 그레텔은 빵 부스러기를 떨어뜨려 길을 표시하지만, 새들이 그 빵을 먹어버립니다. 숲에서 길을 잃은 남매는 과자로 만들어진 집을 발견하고, 그 집에 살고 있는 마녀에게 잡혀갑니다. 마녀는 헨젤을 살찌워 먹으려 하지만, 그레텔의 지혜로 마녀를 오븐에 밀어 넣고 탈출합니다. 남매는 마녀의 보물을 가지고 집으로 돌아와 아버지와 함께 행복하게 살게 됩니다.",
                "category": "fantasy",
                "tag_ids": [3,5],
                "cover_image": "book_cover/헨젤과그레텔.png"
            }

        ]

        for book_data in books:
            tag_ids = book_data.pop('tag_ids')
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                author=book_data['author'],
                publisher=book_data['publisher'],
                synopsis=book_data['synopsis'],
                category=book_data['category'],
                cover_image = book_data['cover_image']
            )
            if created:
                book.tags.set(tag_ids)
                self.stdout.write(self.style.SUCCESS(f"Successfully added book '{book.title}'"))
            else:
                self.stdout.write(self.style.WARNING(f"Book '{book.title}' already exists"))
