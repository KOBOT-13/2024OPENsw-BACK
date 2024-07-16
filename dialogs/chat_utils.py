import os
from openai import OpenAI

# 발급받은 API 키 설정
api_key = "user_API_KEY" #API 키는 원준이에게 여쭤보세요..!
os.environ["OPENAI_API_KEY"] = api_key

# OpenAI 클라이언트 설정

client = OpenAI()

# 키 값을 받고 if 문으로 로직 짜주세요
characters = "답변은 한국어로 하고 백설공주의 마녀의 입장에서 대답해줘"

# 챗봇 함수 정의

def chatbot(input_message):
    try:
        # GPT-4 모델 선택
        model = "gpt-3.5-turbo"
       
        messages = [
                {   "role":"system",
                     "content": characters
                     },
                {
                    "role": "user",
                    "content": input_message,
                }
            ]
        

        # OpenAI API 호출
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )

        # ChatCompletion 객체에서 응답 메시지 추출
        if response.choices:
            bot_response = response.choices[0].message.content
        else:
            bot_response = "No response from the model"

        return bot_response

    except Exception as e:
        return f"Error: {str(e)}"

# 메인 함수 (챗봇 실행)
if __name__ == "__main__":
    print("챗봇을 시작합니다. 종료하려면 '그만'이라고 입력하세요.")
    
    while True:
        user_input = input("사용자: ")

        # 종료 조건 설정
        if user_input.lower() == '그만':
            print("챗봇을 종료합니다.")
            break

        # 챗봇 함수 호출 및 응답 출력
        bot_response = chatbot(user_input)
        print(f"챗봇: {bot_response}")
