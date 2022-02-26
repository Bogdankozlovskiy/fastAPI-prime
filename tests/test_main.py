from fastapi import status
from settings import tokenUrl
from tests.shortcuts import Client
from tests.example_data import user_data_login, user_data_register


def test_get_me(client: Client):
    client.register("/users/register", user_data_register)
    client.login(tokenUrl, {**user_data_login, **{"scope": "me"}})

    response = client.get("/users/me")
    assert response.status_code == status.HTTP_200_OK, response.json()
    retrieved_user_data = response.json()
    assert user_data_register["username"] == retrieved_user_data["username"], "username is not the same"
    assert user_data_register["email"] == retrieved_user_data["email"], "email is not the same"
    assert user_data_register["full_name"] == retrieved_user_data["full_name"], "full_name is not the same"
    assert retrieved_user_data.get("id"), "id is not recived"


def test_check_my_empty_items(client: Client):
    client.register("/users/register", user_data_register)
    client.login(tokenUrl, {**user_data_login, **{"scope": "items.read"}})

    response = client.get("/items")
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == []


def test_create_item(client: Client):
    client.register("/users/register", user_data_register)
    client.login(tokenUrl, {**user_data_login, **{"scope": "items.read items.write"}})
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
