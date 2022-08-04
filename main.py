from typing import List
from Speech_Recognition import recognizer
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
app = FastAPI()

temp = Jinja2Templates(directory='templates')


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, websockets: List[WebSocket]):
        for connection in self.active_connections:
            if connection not in websockets:
                await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get(request: Request):
    return temp.TemplateResponse('index.html', {"request": request})


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive()
            data_bytes = data['bytes']
            recognizer.AcceptWaveform(data_bytes)
            text = recognizer.Result()
            text = text[14:-3]
            print(text)
            await manager.send_personal_message(f"You wrote: {text}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {text}", [websocket])
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
