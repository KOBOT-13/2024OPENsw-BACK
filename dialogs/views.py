import os
import tempfile
import wave
import urllib.request
from pydub import AudioSegment
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse, FileResponse, Http404
from django.conf import settings
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
from .serializers import ConversationSerializer, MessageSerializer, AudioTextSerializer
from .models import Conversation, Message, AudioText, TTSRequest
# from .forms import AudioUploadForm
from google.cloud import speech_v1p1beta1 as speech
import io


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class AudioTextView(APIView):
    def get(self, request):
        audiotexts = AudioText.objects.all()
        serializer = AudioTextSerializer(audiotexts, many=True)
        return Response(serializer.data)


def tts(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        speaker = request.POST.get('speaker', 'nara')
        volume = int(request.POST.get('volume', 0))
        speed = int(request.POST.get('speed', 0))
        pitch = int(request.POST.get('pitch', 0))
        emotion = int(request.POST.get('emotion', 0))
        emotion_strength = int(request.POST.get('emotion_strength', 0))
        format = request.POST.get('format', 'mp3')
        alpha = int(request.POST.get('alpha', 0))
        end_pitch = int(request.POST.get('end_pitch', 0))
        
        client_id = settings.NCP_CLIENT_ID
        client_secret = settings.NCP_CLIENT_SECRET
        encText = urllib.parse.quote(text)
        data = (
            f"speaker={speaker}&volume={volume}&speed={speed}&pitch={pitch}&emotion={emotion}"
            f"&emotion_strength={emotion_strength}&format={format}&alpha={alpha}&end_pitch={end_pitch}&text={encText}"
        )
        url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
        request_api = urllib.request.Request(url)
        request_api.add_header("Content-Type", "application/x-www-form-urlencoded")
        request_api.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        request_api.add_header("X-NCP-APIGW-API-KEY", client_secret)
        
        tts_request = TTSRequest.objects.create(
            text=text,
            speaker=speaker,
            volume=volume,
            speed=speed,
            pitch=pitch,
            emotion=emotion,
            emotion_strength=emotion_strength,
            format=format,
            alpha=alpha,
            end_pitch=end_pitch
        )

        try:
            response = urllib.request.urlopen(request_api, data=data.encode('utf-8'))
            rescode = response.getcode()
            if rescode == 200:
                response_body = response.read()
                tts_dir = os.path.join(settings.MEDIA_ROOT, 'tts')
                os.makedirs(tts_dir, exist_ok=True)  # 디렉토리가 없으면 생성합니다
                file_path = os.path.join(tts_dir, f'{tts_request.id}.mp3')
                with open(file_path, 'wb') as f:
                    f.write(response_body)
                tts_request.tts_file = f'tts/{tts_request.id}.mp3'
                tts_request.save()
                file_url = f"{settings.MEDIA_URL}tts/{tts_request.id}.mp3"
                return JsonResponse({'message': 'TTS mp3 생성 성공', 'file_url': file_url, 'tts_request_id': tts_request.id})
            else:
                return JsonResponse({'error': 'API 요청 실패', 'code': rescode})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return render(request, 'tts_form.html')

def get_tts_file(request, tts_request_id):
    try:
        tts_request = TTSRequest.objects.get(id=tts_request_id)
        file_path = os.path.join(settings.MEDIA_ROOT, tts_request.tts_file.path)
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), content_type='audio/mpeg')
        else:
            raise Http404("파일을 찾을 수 없습니다.")
    except TTSRequest.DoesNotExist:
        raise Http404("TTS 요청을 찾을 수 없습니다.")
    
def list_tts_files(request):
    tts_requests = TTSRequest.objects.all()
    files = [
        {
            'id': tts_request.id,
            'text': tts_request.text,
            'speaker': tts_request.speaker,
            'volume': tts_request.volume,
            'speed': tts_request.speed,
            'pitch': tts_request.pitch,
            'emotion': tts_request.emotion,
            'emotion_strength': tts_request.emotion_strength,
            'format': tts_request.format,
            'alpha': tts_request.alpha,
            'end_pitch': tts_request.end_pitch,
            'created_at': tts_request.created_at,
            'file_url': request.build_absolute_uri(tts_request.tts_file.url) if tts_request.tts_file else None
        }
        for tts_request in tts_requests
    ]
    return JsonResponse(files, safe=False)
