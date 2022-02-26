from typing import List
from fastapi import WebSocket
from dataclasses import dataclass, field


@dataclass
class ConnectionManager:
    _connection_pool: List[WebSocket] = field(default_factory=list)

    async def connect(self, web_socket: WebSocket) -> None:
        await web_socket.accept()
        self._connection_pool.append(web_socket)

    def dissconect(self, web_socket: WebSocket) -> None:
        self._connection_pool.remove(web_socket)

    async def broad_cast(self, data: dict):
        for web_socket in self._connection_pool:
            await web_socket.send_json(data)
