from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from modules.web_socket.utils import ConnectionManager


router = APIRouter()
manager = ConnectionManager()


@router.websocket("/web_socket")
async def web_socket_end_point(web_socket: WebSocket):
    await manager.connect(web_socket)
    try:
        while True:
            data = await web_socket.receive_json()
            await manager.broad_cast(data)
    except WebSocketDisconnect:
        manager.dissconect(web_socket)
