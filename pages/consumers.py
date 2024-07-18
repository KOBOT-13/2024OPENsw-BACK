import json
import websockets
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
import os
from django.conf import settings

class SpeechToTextConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.client = speech.SpeechClient(credentials=self.get_credentials())
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
        )
        self.streaming_config = speech.StreamingRecognitionConfig(config=self.config, interim_results=True)
        self.requests = []
        self.responses = []

    async def disconnect(self, close_code):
        await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            self.requests.append(speech.StreamingRecognizeRequest(audio_content=bytes_data))
            if not self.responses:
                self.responses = self.client.streaming_recognize(config=self.streaming_config, requests=iter(self.requests))
            async for response in self.responses:
                for result in response.results:
                    if result.is_final:
                        await self.save_transcript(result.alternatives[0].transcript)
                        await self.send(text_data=json.dumps({
                            'message': result.alternatives[0].transcript
                        }))

    async def save_transcript(self, transcript):
        transcript_path = os.path.join(settings.MEDIA_ROOT, "transcript.txt")
        with open(transcript_path, "a") as f:
            f.write(transcript + "\n")

    def get_credentials(self):
        credentials_path = os.path.join(os.path.dirname(__file__), 'path_to_your_credentials_file.json')
        return service_account.Credentials.from_service_account_file(credentials_path)
