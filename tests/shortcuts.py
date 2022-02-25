from fastapi import status
from fastapi.testclient import TestClient
from functools import wraps


class Client:
    def __init__(self, client: TestClient):
        self.client = client
        self.headers = None

    def register(self, register_url: str, user_data: dict):
        response = self.client.post(
            url=register_url,
            json=user_data
        )
        assert response.status_code == status.HTTP_201_CREATED, response.json()

    def login(self, login_url: str, user_data: dict):
        response = self.client.post(
            url=login_url,
            data=user_data
        )
        assert response.status_code == status.HTTP_200_OK, response.json()
        access_token = response.json()['access_token']
        token_type: str = response.json()['token_type']
        self.headers = {
            "Authorization": f"{token_type.title()} {access_token}"
        }

    def logout(self):
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
