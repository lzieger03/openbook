from channels.generic.websocket import AsyncWebsocketConsumer
from openbook.ai.services.llm import stream_response
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        async for token in stream_response(message):
            await self.send(token)

    async def disconnect(self, close_code):
        pass