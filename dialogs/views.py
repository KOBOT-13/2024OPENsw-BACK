from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, viewsets, generics
from .serializers import *
from rest_framework.permissions import IsAuthenticated
import os
import json
import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status   
from .serializers import *
from .chat_utils  import *
from books.models import Character
from .models import *
from rest_framework.decorators import action
from django.utils import timezone

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def start_conversation(self, request):
        user = request.user
        book_id = request.data.get('book')
        character_id = request.data.get('character')
        character_instance = get_object_or_404(Character, id=character_id)
        
        print(f"Received request to start conversation: user={user}, book_id={book_id}, character_id={character_id}")
        
        # Check if the conversation already exists
        existing_conversation = Conversation.objects.filter(user=user, book_id=book_id, character_id=character_id).first()
        
        if existing_conversation:
            print(f"Found existing conversation: {existing_conversation.id}")
            serializer = self.get_serializer(existing_conversation)
            summary_message = get_object_or_404(SummaryMessage, character_sender = character_instance)
            summary_message.end_key = 1
            summary_message.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Create a new conversation if it does not exist
        print("No existing conversation found, creating a new one.")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            print(f"Created new conversation: {serializer.instance.id}")
        
            default_summary_message = SummaryMessage.objects.create(
                user_sender = user,
                character_sender = character_instance,
                end_key = 1
            )
            
            default_summary_message.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

class MessageAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation_id = conversation_id)
    
    
class MessagetoTTS(APIView): # 메시지를 받으면 사용자의 질문, gpt의 대답(TTS파일 포함)을 저장합니다.
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_403_FORBIDDEN)

        try:
            # 요청 데이터 로드
            data = json.loads(request.body)
            input_message = data.get('message')
            conversation_id = data.get('conversation_id')
            character_id = data.get('character_id')
            summary_message_id = data.get('summary_message_id')
            
            conversation = get_object_or_404(Conversation, id=conversation_id)
            user_instance = request.user
            character_instance = get_object_or_404(Character, id=character_id)
            
            conversation.updated_at = timezone.now()
            conversation.save()
            
            user_request = Message.objects.create(
                conversation = conversation,
                sender_type = 'user',
                user_sender = user_instance,
                message = input_message,
                character_sender = character_instance
            )
            
            user_request.save()
            
            if not input_message:
                return Response({'error': 'No message provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            summary_message = get_object_or_404(SummaryMessage, id=summary_message_id)
            end_key = summary_message.end_key
            bot_response, chat_summary_message = chatbot(input_message, character_id, summary_message.message, end_key)
            summary_message.message = chat_summary_message
            summary_message.end_key = 0
            summary_message.save()
            
            print(summary_message)

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
                'text': bot_response
            }
            
            # TTSRequest 생성
            tts_request = Message.objects.create(              
                conversation = conversation,
                sender_type = 'character',
                user_sender = user_instance,
                message = bot_response,
                character_sender = character_instance
            )

            # TTS API 호출
            client_id = settings.CLOVA_CLIENT_ID
            client_secret = settings.CLOVA_CLIENT_SECRET
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
                        'message': bot_response,
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

class EndChat(APIView):
    def post(self, request):
        data = json.loads(request.body)
        conversation_id = data.get("conversation_id")
        
        summary_message = get_object_or_404(SummaryMessage, id=conversation_id)
        summary_message.end_key = 0
        summary_message.save()
        
        return Response({'status': 'success', 'message': 'Chat ended successfully.'}, status=status.HTTP_200_OK)