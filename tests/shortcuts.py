from fastapi import status
from dataclasses import dataclass, field
from httpx import AsyncClient
from functools import wraps
from typing import Optional, Dict


@dataclass
class Client:
    client: AsyncClient
    headers: Optional[Dict] = field(default=None)

    async def register(self, register_url: str, user_data: dict):
        response = await self.client.post(
            url=register_url,
            json=user_data
        )
        assert response.status_code == status.HTTP_201_CREATED, response.json()

    async def login(self, login_url: str, user_data: dict):
        response = await self.client.post(
            url=login_url,
            data=user_data
        )
        assert response.status_code == status.HTTP_200_OK, response.json()
        access_token = response.json()['access_token']
        token_type: str = response.json()['token_type']
        self.headers = {
            "Authorization": f"{token_type.title()} {access_token}"
        }

    async def logout(self):
        self.headers = None

    def __getattr__(self, attr: str):
        func = getattr(self.client, attr)
        assert callable(func), "it is not calleble option"

        @wraps(func)
        def wrapped_client(*args, **kwargs):
            if self.headers is not None:
                if kwargs.get("headers"):
                    kwargs['headers'].update(self.headers)
                else:
                    kwargs['headers'] = self.headers
            return func(*args, **kwargs)
        return wrapped_client
