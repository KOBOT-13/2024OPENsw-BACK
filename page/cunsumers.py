import json
from channels.generic.websocket import AsyncWebsocketConsumer
from google.cloud import page_v1p1beta1 as page
import asyncio

class SpeechToTextConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.client = page.SpeechClient()
        self.config = page.RecognitionConfig(
            encoding=page.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US',
        )
        self.streaming_config = page.StreamingRecognitionConfig(config=self.config)
        self.responses = self.client.streaming_recognize(self.streaming_config)
        self.requests = asyncio.Queue()

        asyncio.create_task(self.process_responses())

    async def disconnect(self, close_code):
        await self.client.close()

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            await self.requests.put(page.StreamingRecognizeRequest(audio_content=bytes_data))
            await self.process_requests()

    async def process_requests(self):
        async for request in self.requests:
            self.responses.write(request)

    async def process_responses(self):
        async for response in self.responses:
            for result in response.results:
                transcript = result.alternatives[0].transcript
                await self.send(text_data=json.dumps({'transcript': transcript}))
