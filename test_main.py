from fastapi.testclient import TestClient
from fastapi import status
from tortoise.contrib.test import finalizer, initializer

from os import remove, path
from pytest import fixture
from typing import Generator
from settings import TORTOISE_ORM_TEST

from main import app
from settings import tokenUrl


@fixture
def client() -> Generator:
    _, db_name = TORTOISE_ORM_TEST['connections']['default'].split("//")
    if path.exists(db_name):
        remove(db_name)
    with TestClient(app) as client:
        yield client


def test_one(client: TestClient):
    user_data = {
        "username": "testname",
        "email": "test@email.ru",
        "full_name": "full_name",
        "password": "password"
    }
    # register
    response = client.post(
        "/users/register",
        json=user_data
    )
    assert response.status_code == status.HTTP_201_CREATED, response.json()
    # login
    response = client.post(
        tokenUrl,
        data=user_data
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
    access_token = response.json()['access_token']
    token_type: str = response.json()['token_type']
    headers = {
        "Authorization": f"{token_type.title()} {access_token}"
    }
    # get me info
    response = client.get(
        "/users/me",
        headers=headers
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
    retrieved_user_data = response.json()
    assert user_data["username"] == retrieved_user_data["username"], "username is not the same"
    assert user_data["email"] == retrieved_user_data["email"], "email is not the same"
    assert user_data["full_name"] == retrieved_user_data["full_name"], "full_name is not the same"
    assert retrieved_user_data.get("id"), "id is not recived"
    # get my items
    response = client.get(
        "/items",
        headers=headers
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == []
    # create item
    item_data = {
        "title": "test item title",
        "date_created": "2022-02-24T14:12:49.047Z"
    }
    response = client.post(
        "/items/create",
        headers=headers,
        json=item_data
    )
    assert response.status_code == status.HTTP_201_CREATED, response.json()
    # get my items
    response = client.get(
        "/items",
        headers=headers
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()
