import os
import json
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import openai
# from openai import OpenAI
# from langchain.memory import ConversationSummaryMemory
# from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("API key for OpenAI is not set")

# OpenAI 클라이언트 설정
openai.api_key = api_key

# memory = ConversationSummaryMemory(
#     llm= ChatOpenAI(temperature = 0), return_messages=True)

# client = OpenAI()

# Character 설정
character_key = 1

# 대화 기록
convo_history = []

character_map = {
    0: "답변은 한국어로 하고 백설공주의 마녀의 입장에서 대답해줘",
    1: "답변은 한국어로 하고 토끼와 거북이의 토끼의 입장에서 대답해줘",
    2: "답변은 한국어로 하고 토끼와 거북이의 거북이의 입장에서 대답해줘",
    3: "답변은 한국어로 하고 아기돼지 삼형제의 첫째돼지의 입장에서 대답해줘",
    4: "답변은 한국어로 하고 아기돼지 삼형제의 둘째돼지의 입장에서 대답해줘",
    5: "답변은 한국어로 하고 아기돼지 삼형제의 셋째돼지의 입장에서 대답해줘"
}  # 겹치는 부분은 모델 자체에 넣기 

# character_key에 해당하는 characters를 설정
characters = character_map[character_key]



# 챗봇 함수 정의
# input message 어떻게 변경할지 + DB 에 대화 내용 넣기 + 출력 메세지는 어디로 보낼지 ... 
def chatbot(input_message):
    messages = [
        {"role": "system", "content": characters},
        {"role": "user", "content": input_message}
    ]

    # OpenAI API 호출
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    )

    # 응답 메시지 추출
    if response.choices:
        bot_response = response.choices[0].message['content']
    else:
        bot_response = "No response from the model"

    return bot_response