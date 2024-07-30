import os
from openai import OpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 로드
api_key = os.getenv('api_key')

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

# 캐릭터 설정
characters = CHARACTER_MAP[character_key]

# 챗봇 함수 정의
def chatbot(input_message):
    try:
        model = "gpt-3.5-turbo"
        convo_history.append({"role": "user", "content": input_message})

        # 이전 대화 요약 가져오기
        summary = memory.load_memory_variables({}).get("history", "")

        # 메시지 구성
        messages = [
            {"role": "system", "content": "답변은 한국어로하고 너는 " + characters + "이야, 정확한 이야기의 내용을 근거해서 대답해줘"},
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

# 메인 함수 (챗봇 실행)
if __name__ == "__main__":
    print("챗봇을 시작합니다. 종료하려면 '그만'이라고 입력하세요.")
    
    while True:
        user_input = input("사용자: ")

        # 종료 조건
        if user_input.lower() == '그만':
            print("챗봇을 종료합니다.")
            
            # 대화 내용 요약 출력
            print(memory.load_memory_variables({})["history"])
            break

        # 챗봇 함수 호출 및 응답 출력
        bot_response = chatbot(user_input)
        print(f"챗봇: {bot_response}")
