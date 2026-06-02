# WebSocket URL für den Chat
# Frontend verbindet sich so:
#
#   const socket = new WebSocket("ws://localhost:8000/ws/chat/")
#
#   // Nachricht schicken — muss JSON sein mit "message" als key
#   socket.send(JSON.stringify({ message: "Erkläre mir X" }))
#
#   // Die Antwort kommt Token für Token zurück (einzelne Strings, kein JSON)
#   // Einfach aneinanderhängen um den kompletten Text aufzubauen
#   let antwort = ""
#   socket.onmessage = (event) => {
#       antwort += event.data
#       console.log(antwort)  // wächst mit jedem Token
#   }
#
#   // Verbindung sauber schließen wenn nicht mehr gebraucht
#   socket.close()

from django.urls import re_path
from openbook.ai.consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/$", ChatConsumer.as_asgi()),
]
