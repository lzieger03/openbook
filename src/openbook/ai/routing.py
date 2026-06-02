# WebSocket-Routen für das KI-Modul
#
# Chat (LLM-Kommunikation):
#   const socket = new WebSocket("ws://localhost:8000/ws/chat/")
#   socket.send(JSON.stringify({ message: "Erkläre mir X" }))
#   socket.onmessage = (e) => console.log(e.data)  // komplette Antwort als String
#
# Quiz:
#   const socket = new WebSocket("ws://localhost:8000/ws/quiz/")
#   // Beim Verbinden kommt sofort die erste Frage:
#   //   { type: "question", question: "...", choices: { A: "...", B: "...", C: "...", D: "..." } }
#   // Antwort schicken:
#   socket.send(JSON.stringify({ answer: "A" }))
#   // Antwort: erst Auswertung, dann nächste Frage
#   //   { type: "result", correct: true, correct_answer: "A", correct_text: "Paris" }
#   //   { type: "question", ... }

from django.urls import re_path
from openbook.ai.consumer import ChatConsumer, QuizConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/$", ChatConsumer.as_asgi()),
    re_path(r"ws/quiz/$",  QuizConsumer.as_asgi()),
]
