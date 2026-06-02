import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")

        from openbook.assistant.services.client import lm_client
        response = await sync_to_async(lm_client.get_user_message)(message)
        await self.send(response)

    async def disconnect(self, close_code):
        pass


class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.current_question = None
        await self.accept()
        await self._send_question()

    async def receive(self, text_data):
        data = json.loads(text_data)
        answer = data.get("answer", "").upper()

        if self.current_question and answer:
            correct = self.current_question.check_answer(answer)
            await self.send(json.dumps({
                "type": "result",
                "correct": correct,
                "correct_answer": self.current_question.correct_choice,
                "correct_text": self.current_question.get_choice_text(self.current_question.correct_choice),
            }))

        await self._send_question()

    async def _send_question(self):
        from openbook.quiz.quiz_logic import QuizManager
        json_path = str(settings.BASE_DIR / "openbook/quiz/data/questions.json")
        manager = await sync_to_async(QuizManager)(json_path)
        question = await sync_to_async(manager.get_random_question)()
        self.current_question = question

        if question:
            await self.send(json.dumps({
                "type": "question",
                "question": question.question_text,
                "choices": {
                    "A": question.choice_a,
                    "B": question.choice_b,
                    "C": question.choice_c,
                    "D": question.choice_d,
                },
            }))

    async def disconnect(self, close_code):
        pass
