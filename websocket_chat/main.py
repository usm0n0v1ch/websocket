from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Dict

app = FastAPI()

# Подключаем статику
app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, chat_name: str, websocket: WebSocket):
        await websocket.accept()
        if chat_name not in self.active_connections:
            self.active_connections[chat_name] = []
        self.active_connections[chat_name].append(websocket)

    def disconnect(self, chat_name: str, websocket: WebSocket):
        if chat_name in self.active_connections:
            self.active_connections[chat_name].remove(websocket)
            if not self.active_connections[chat_name]:
                del self.active_connections[chat_name]

    async def broadcast(self, chat_name: str, message: str):
        if chat_name in self.active_connections:
            for connection in self.active_connections[chat_name]:
                await connection.send_text(message)


chat_manager = ChatManager()


@app.get("/")
async def get():
    # Указываем кодировку UTF-8 для открытия файла
    with open("templates/index.html", encoding="utf-8") as file:
        return HTMLResponse(file.read())


@app.websocket("/ws/{chat_name}")
async def websocket_endpoint(websocket: WebSocket, chat_name: str):
    await chat_manager.connect(chat_name, websocket)
    try:
        while True:
            message = await websocket.receive_text()
            await chat_manager.broadcast(chat_name, message)
    except WebSocketDisconnect:
        chat_manager.disconnect(chat_name, websocket)
