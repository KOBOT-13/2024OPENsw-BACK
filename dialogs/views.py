import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class UserMessageView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_403_FORBIDDEN)

        try:
            # 요청 데이터 로드
            data = json.loads(request.body)
            input_message = data.get('message')

            if not input_message:
                return Response({'error': 'No message provided'}, status=status.HTTP_400_BAD_REQUEST)
            print(input_message)
            bot_response = chatbot(input_message)

            if isinstance(bot_response, JsonResponse):
                bot_response_data = json.loads(bot_response.content)
                bot_response_message = bot_response_data.get('message')
            else:
                return Response({'error': 'Invalid response from chatbot function'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # TTS 파라미터 설정
            tts_params = {
                'speaker': data.get('speaker', 'nara'),
                'volume': int(data.get('volume', 0)),
                'speed': int(data.get('speed', 0)),
                'pitch': int(data.get('pitch', 0)),
                'emotion': int(data.get('emotion', 0)),
                'emotion_strength': float(data.get('emotion_strength', 0.0)),
                'format': data.get('format', 'mp3'),
                'alpha': int(data.get('alpha', 0)),
                'end_pitch': int(data.get('end_pitch', 0)),
                'text': bot_response_message
            }

            # TTSRequest 생성
            tts_request = TTSRequest.objects.create(
                text=tts_params['text'],
                speaker=tts_params['speaker'],
                volume=tts_params['volume'],
                speed=tts_params['speed'],
                pitch=tts_params['pitch'],
                emotion=tts_params['emotion'],
                emotion_strength=tts_params['emotion_strength'],
                format=tts_params['format'],
                alpha=tts_params['alpha'],
                end_pitch=tts_params['end_pitch']
            )

            # TTS API 호출
            client_id = os.getenv('CLOVA_CLIENT_ID')
            client_secret = os.getenv('CLOVA_CLIENT_SECRET')
            if not client_id or not client_secret:
                raise ImproperlyConfigured("CLOVA client credentials are not set.")
            
            url = 'https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-NCP-APIGW-API-KEY-ID': client_id,
                'X-NCP-APIGW-API-KEY': client_secret
            }

            try:
                # POST 요청 보내기
                response = requests.post(url, data=tts_params, headers=headers)
                response.raise_for_status()  # 상태 코드가 4xx 또는 5xx이면 예외 발생

                # 응답 확인
                if response.status_code == 200:
                    tts_dir = os.path.join(settings.MEDIA_ROOT, 'tts')
                    os.makedirs(tts_dir, exist_ok=True)
                    file_path = os.path.join(tts_dir, f'{tts_request.id}.mp3')

                    with open(file_path, 'wb') as f:
                        f.write(response.content)

                    tts_request.tts_file = f'tts/{tts_request.id}.mp3'
                    tts_request.save()

                    return Response({
                        'message': 'TTS mp3 생성 성공',
                        'file_url': f"{settings.MEDIA_URL}tts/{tts_request.id}.mp3",
                        'tts_request_id': tts_request.id
                    }, status=status.HTTP_201_CREATED)

                else:
                    return Response({'error': f'Error: {response.status_code}, {response.text}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except requests.RequestException as e:
                return Response({'error': f'Request failed: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)