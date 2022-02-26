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
    await client.login(tokenUrl, {**user_data_login, **{"scope": "items.read"}})
    response = await client.get("/items/")
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_item(client):
    await client.login(tokenUrl, {**user_data_login, **{"scope": "items.write"}})
    response = await client.post(
        "/items/create",
        json=item_data
    )
    assert response.status_code == status.HTTP_201_CREATED, response.json()


@pytest.mark.asyncio
async def test_check_my_items(client):
    await client.login(tokenUrl, {**user_data_login, **{"scope": "items.read"}})
    response = await client.get("/items/")
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json(), "no items"
