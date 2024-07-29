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
# 대화 요약 메모리 초기화
memory = ConversationSummaryBufferMemory(
    llm=ChatOpenAI(temperature=0), return_messages=True)
# OpenAI 클라이언트 초기화
client = OpenAI()
# 캐릭터 키 설정
character_key = 1
# 대화 기록
convo_history = []
# 캐릭터 맵
character_map = {
    0: "답변은 한국어로 하고 백설공주의 마녀의 입장에서 대답해줘",
    1: "답변은 한국어로 하고 토끼와 거북이의 토끼의 입장에서 대답해줘",
    2: "답변은 한국어로 하고 토끼와 거북이의 거북이의 입장에서 대답해줘",
    3: "답변은 한국어로 하고 아기돼지 삼형제의 첫째돼지의 입장에서 대답해줘",
    4: "답변은 한국어로 하고 아기돼지 삼형제의 둘째돼지의 입장에서 대답해줘",
    5: "답변은 한국어로 하고 아기돼지 삼형제의 셋째돼지의 입장에서 대답해줘"
}
# 캐릭터 설정
characters = character_map[character_key]
# 챗봇 함수 정의
def chatbot(input_message):
    try:
        model = "gpt-3.5-turbo"
        convo_history.append({"role": "user", "content": input_message})
        # 이전 대화 요약 가져오기
        summary = memory.load_memory_variables({}).get("history", "")
        # 메시지 구성
        messages = [
            {"role": "system", "content": characters},
            {"role": "system", "content": f"이전 대화 요약: {summary}"},
            {"role": "user", "content": input_message},
        ]
        # OpenAI API 호출
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )
        # 응답 메시지 추출
        if response.choices:
            bot_response = response.choices[0].message.content
        else:
            bot_response = "No response from the model"
        convo_history.append({"role": "assistant", "content": bot_response})
        # 메모리에 대화 내용 저장
        memory.save_context(
            inputs={"user": input_message},
            outputs={"assistant": bot_response}
        )
        return bot_response
    except Exception as e:
        return f"Error: {str(e)}"
    