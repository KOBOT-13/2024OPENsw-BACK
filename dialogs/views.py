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

# def get_sample_rate(filepath):
#     """파일의 샘플링 주파수를 반환합니다."""
#     with wave.open(filepath, 'rb') as audio_file:
#         sample_rate = audio_file.getframerate()
#     return sample_rate

# def convert_audio(filepath):
#     """WAV 파일을 16kHz 모노 채널로 변환합니다."""
#     try:
#         audio = AudioSegment.from_wav(filepath)
#         audio = audio.set_channels(1)  # 모노 채널로 설정
#         audio = audio.set_frame_rate(16000)  # 16kHz로 설정
#         converted_filepath = filepath.replace(".wav", "_converted.wav")
#         audio.export(converted_filepath, format="wav")
#         print(f"변환된 파일의 경로: {converted_filepath}")
#         return converted_filepath
#     except Exception as e:
#         print(f"오디오 변환 중 오류 발생: {str(e)}")
#         raise RuntimeError(f"오디오 변환 중 오류 발생: {str(e)}")

# def inspect_audio(filepath):
#     """오디오 파일의 채널 수, 샘플링 주파수, 길이를 출력합니다."""
#     try:
#         audio = AudioSegment.from_wav(filepath)
#         print(f"Channels: {audio.channels}")
#         print(f"Sample Rate: {audio.frame_rate}")
#         print(f"Duration: {len(audio) / 1000} seconds")
#     except Exception as e:
#         print(f"오디오 파일 검사 중 오류 발생: {str(e)}")

# def transcribe_audio(request):
#     if request.method == 'POST' and request.FILES.get('audioFile'):
#         file = request.FILES['audioFile']
#         try:
#             # 업로드된 파일을 임시 파일로 저장
#             with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#                 for chunk in file.chunks():
#                     temp_file.write(chunk)
#                 filepath = temp_file.name

#             print(f"업로드된 파일의 경로: {filepath}")

#             sample_rate = get_sample_rate(filepath)
#             print(f"파일의 샘플링 주파수: {sample_rate}")

#             converted_filepath = convert_audio(filepath)
#             inspect_audio(converted_filepath)  # 변환된 파일 검사
            
#             # 서비스 계정 JSON 파일 경로
#             credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
#             if not credentials_path:
#                 return JsonResponse({'error': 'Google credentials path is not set in environment variables.'})

#             credentials = service_account.Credentials.from_service_account_file(credentials_path)
#             client = speech.SpeechClient(credentials=credentials)

#             with open(converted_filepath, "rb") as audio_file:
#                 content = audio_file.read()

#             audio = speech.RecognitionAudio(content=content)
#             config = speech.RecognitionConfig(
#                 encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#                 sample_rate_hertz=16000,
#                 language_code="en-US",
#             )

#             response = client.recognize(config=config, audio=audio)
#             print(f"API 응답: {response}")

#             if not response.results:
#                 return JsonResponse({'error': "No audio detected or audio quality is poor."})

#             transcript = " ".join([result.alternatives[0].transcript for result in response.results])
#             return JsonResponse({'transcript': transcript})

#         except Exception as e:
#             return JsonResponse({'error': f"예기치 않은 오류가 발생했습니다: {str(e)}"})
#         finally:
#             if os.path.exists(filepath):
#                 os.remove(filepath)
#             if os.path.exists(converted_filepath):
#                 os.remove(converted_filepath)

#     return render(request, "transcribe_audio.html")

# def get_sample_rate(audio_file):
#     with wave.open(io.BytesIO(audio_file), 'rb') as wf:
#         return wf.getframerate()

# def transcribe_audio(request):
#     if request.method == 'POST':
#         form = AudioUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             audio_file = request.FILES['audio_file'].read()

#             # 오디오 파일을 pydub로 읽어오기
#             audio = AudioSegment.from_file(io.BytesIO(audio_file))

#             # 모노로 변환
#             if audio.channels > 1:
#                 audio = audio.set_channels(1)

#             # 바이트 스트림으로 변환
#             audio_content = io.BytesIO()
#             audio.export(audio_content, format="wav")
#             audio_content.seek(0)

#             # 샘플레이트 추출
#             sample_rate = get_sample_rate(audio_content.read())

#             client = speech.SpeechClient()

#             # RecognitionAudio에 바이트 스트림으로 읽어온 오디오 내용 설정
#             audio = speech.RecognitionAudio(content=audio_content.read())

#             config = speech.RecognitionConfig(
#                 encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#                 sample_rate_hertz=sample_rate,  # 감지된 샘플레이트 사용
#                 language_code="en-US",
#             )

#             try:
#                 response = client.recognize(config=config, audio=audio)
#                 result_text = ""
#                 for result in response.results:
#                     result_text += result.alternatives[0].transcript

#                 return HttpResponse(result_text)
#             except Exception as e:
#                 return HttpResponse(f"Error: {e}")

#     else:
#         form = AudioUploadForm()

#     return render(request, 'transcribe_audio.html', {'form': form})
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