import os
from openai import OpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from django.conf import settings
import re 
# 환경 변수 로드
api_key = settings.OPENAI_API_KEY

# OpenAI API 키 환경 변수에 설정
os.environ["OPENAI_API_KEY"] = api_key

# 언어 모델 초기화
chat_model = ChatOpenAI(openai_api_key=api_key)

client = OpenAI()

def story_analyze(title, character_list, synopsis):
    try:

        model = 'gpt-4o'  
        
        # 메시지 구성
        messages = [
            {"role": "system", "content": "You are a helpful book analyst."},
            {"role": "user", "content": f"책의 제목은 '{title}'이고 내용은 다음과 같습니다:\n\n{synopsis}\n\n이 내용을 분석하고, 중요한 부분이 빠지지 않도록 요약해줘. 답변의 첫 문장은 책 제목을 넣어줘"}
        ]
        
        # ChatOpenAI 모델을 이용한 대화 생성
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )
        
        if response.choices:
            bot_response = response.choices[0].message.content

            return bot_response
        else:
            bot_response = "No response from the model"
        return bot_response

    except Exception as e:
        return f"An error occurred: {e}"
    
def make_tag (title, synopsis):
    try: 
        model = 'gpt-4o'
        
        messages = [
            {"role": "system", "content": "You are a helpful book analyst."},
            {"role": "system", "content": '''tags = [
            "사랑","모험","지혜","공주","용기","효","선","가족","행복","은혜","우정","청결","위로","성실","신비","창의","희생",
        ], category : (판타지, 소설, 그림책, 위인전, 전래동화, 우화)'''},
            {"role": "user", "content": f"동화의 제목은 {title} 이고, 내용은 {synopsis}야 이를 통해 동화의 tags 중 어울리는 것들을 리스트로 뽑아줘 예시 : [용기, 지혜] , 그리고 카테고리(category)는 하나만 뽑아줘 "}
        ]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )
        
        if response.choices:
            bot_response = response.choices[0].message.content
            
            tags_match = re.search(r"tags:\s*\[(.*?)\]", bot_response)
            category_match = re.search(r"category:\s*(\S+)", bot_response)
            tags = []
            category = None
            if tags_match:
                tags_str = tags_match.group(1)  
                tags = [tag.strip() for tag in tags_str.split(',')] 

            if category_match:
                category = category_match.group(1)  
            return tags, category
        else:
            bot_response = "No response from the model"
        return tags, category

    except Exception as e:
        return f"An error occurred: {e}"
    