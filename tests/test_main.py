import pytest
from fastapi import status

from tests.example_data import user_data_register, user_data_login, item_data
from settings import tokenUrl


@pytest.mark.asyncio
async def test_register(client):
    await client.register("/users/register", user_data=user_data_register)


@pytest.mark.asyncio
async def test_get_me(client):
    await client.login(tokenUrl, user_data={**user_data_login, "scope": "me"})
    response = await client.get("/users/me")
    assert response.status_code == status.HTTP_200_OK, response.json()
    retrieved_user_data = response.json()
    assert user_data_register["username"] == retrieved_user_data["username"], "username is not the same"
    assert user_data_register["email"] == retrieved_user_data["email"], "email is not the same"
    assert user_data_register["full_name"] == retrieved_user_data["full_name"], "full_name is not the same"
    assert retrieved_user_data.get("id"), "id is not recived"


@pytest.mark.asyncio
async def test_check_my_empty_items(client):
    await client.login(tokenUrl, {**user_data_login, "scope": "items.read"})
    response = await client.get("/items/")
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_item(client):
    await client.login(tokenUrl, {**user_data_login, "scope": "items.write"})
    response = await client.post(
        "/items/create",
        json=item_data
    )
    assert response.status_code == status.HTTP_201_CREATED, response.json()


@pytest.mark.asyncio
async def test_check_my_items(client):
    await client.login(tokenUrl, {**user_data_login, "scope": "items.read"})
    response = await client.get("/items/")
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json(), "no items"


@pytest.mark.asyncio
async def test_graph_ql(client):
    await client.login(tokenUrl, user_data_login)
    response = await client.post("/graphql", json={"query": "query{world(x:2)}", "variables": None})
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json(), "empty response"


def test_web_socket(client):
    data = "{\"hello\":\"world\"}"
    with client.websocket_connect("/web_socket") as web_socket_1, \
            client.websocket_connect("/web_socket") as web_socket_2:
        web_socket_1.send_json(data)
        recived_data_1 = web_socket_1.receive_json()
        recived_data_2 = web_socket_2.receive_json()
        assert data == recived_data_1, "request and response are not the same"
        assert recived_data_1 == recived_data_2, "client rcived not the same data"
