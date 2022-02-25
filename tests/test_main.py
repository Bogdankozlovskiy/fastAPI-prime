from fastapi.testclient import TestClient
from fastapi import status
from tortoise.contrib.test import finalizer, initializer

from os import remove
from pytest import fixture
from typing import Generator
from settings import TORTOISE_ORM_TEST

from main import test_app as app
from settings import tokenUrl
from tests.shortcuts import Client


user_data = {
    "username": "testname",
    "email": "test@email.ru",
    "full_name": "full_name",
    "password": "password"
}


@fixture
def client() -> Generator:
    _, db_name = TORTOISE_ORM_TEST['connections']['default'].split("//")
    with TestClient(app) as client:
        yield Client(client)
    remove(db_name)


def test_get_me(client: Client):
    client.register("/users/register", user_data)
    client.login(tokenUrl, user_data)

    response = client.get("/users/me")
    assert response.status_code == status.HTTP_200_OK, response.json()
    retrieved_user_data = response.json()
    assert user_data["username"] == retrieved_user_data["username"], "username is not the same"
    assert user_data["email"] == retrieved_user_data["email"], "email is not the same"
    assert user_data["full_name"] == retrieved_user_data["full_name"], "full_name is not the same"
    assert retrieved_user_data.get("id"), "id is not recived"


def test_check_my_empty_items(client: Client):
    client.register("/users/register", user_data)
    client.login(tokenUrl, user_data)

    response = client.get("/items")
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == []


def test_create_item(client: Client):
    client.register("/users/register", user_data)
    client.login(tokenUrl, user_data)
    # create item
    item_data = {
        "title": "test item title",
        "date_created": "2022-02-24T14:12:49.047Z"
    }
    response = client.post(
        "/items/create",
        json=item_data
    )
    assert response.status_code == status.HTTP_201_CREATED, response.json()
    # get my items
    response = client.get("/items")
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json(), "no items"
