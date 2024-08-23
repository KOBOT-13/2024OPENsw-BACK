import os
from openai import OpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from django.conf import settings
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
        else:
            bot_response = "No response from the model"
        return bot_response

    except Exception as e:
        return f"An error occurred: {e}"