import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_auth_success(async_client: AsyncClient) -> None:
    user_data = {"name": "user@ya.ru", "password": "admin"}
    responce = await async_client.post(url="/signup", json=user_data)

    assert responce.status_code == status.HTTP_201_CREATED
    assert "jwt_token" in responce.json()

    login_response = await async_client.post(url="/signin", json=user_data)

    assert login_response.status_code == status.HTTP_200_OK
    assert "jwt_token" in login_response.json()
    print('DDDDDDDDDDDddd')