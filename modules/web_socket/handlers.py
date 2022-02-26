from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List


router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.connection_pool: List[WebSocket] = []

    async def connect(self, web_socket: WebSocket) -> None:
        await web_socket.accept()
        self.connection_pool.append(web_socket)

    def dissconect(self, web_socket: WebSocket):
        self.connection_pool.remove(web_socket)


@router.websocket("/ws")
async def web_socket_end_point(web_socket: WebSocket):
    await web_socket.accept()
    try:
        while True:
            data = await web_socket.receive_json()
            await web_socket.send_json(data)
    except WebSocketDisconnect:
        pass
