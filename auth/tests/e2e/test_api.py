from datetime import datetime, timezone

import pytest

from fastapi import status
from httpx import AsyncClient
from jose import jwt

from src.core.config import get_auth_data
from src.core.model import User


pytestmark = pytest.mark.e2e


def create_jwt_token(user_id: str = None, exp: datetime = None) -> str:
    auth_data = get_auth_data()
    payload = {}
    if user_id:
        payload["sub"] = user_id
    if exp:
        payload["exp"] = exp

    return jwt.encode(payload, auth_data["secret_key"], algorithm=auth_data["algorithm"])


@pytest.mark.asyncio
async def test_auth_happy_path(async_client: AsyncClient) -> None:
    user_data = {"name": "user@ya.ru", "password": "admin"}

    response = await async_client.post(url="/signup", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "Authorization" in response.json()

    login_response = await async_client.post(url="/signin", json=user_data)
    assert login_response.status_code == status.HTTP_200_OK
    assert "Authorization" in login_response.json()


@pytest.mark.asyncio
async def test_auth_unhappy_path_expired_token(async_client: AsyncClient) -> None:
    user_data = await User(name="user@ya.ru", role="user", password="admin").insert()

    expired_token = create_jwt_token(user_id=str(user_data.id), exp=datetime(2000, 1, 1))

    response = await async_client.get(url="/", cookies={"user_jwt_token": expired_token})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Токен истек"


@pytest.mark.asyncio
async def test_auth_unhappy_path_invalid_token(async_client: AsyncClient) -> None:
    response = await async_client.get(url="/", cookies={"user_jwt_token": "invalid_token"})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Не валидный токен!"


@pytest.mark.asyncio
async def test_auth_unhappy_path_found_user(async_client: AsyncClient) -> None:
    user_data = await User(name="user@ya.ru", role="user", password="admin").insert()
    await User.find({}).delete_many()

    jwt_token = create_jwt_token(user_id=str(user_data.id), exp=datetime.now(timezone.utc))

    response = await async_client.get(url="/", cookies={"user_jwt_token": jwt_token})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Пользователь не найден"


@pytest.mark.asyncio
async def test_auth_unhappy_path_found_user_id(async_client: AsyncClient) -> None:
    jwt_token = create_jwt_token(exp=datetime.now(timezone.utc))

    response = await async_client.get(url="/", cookies={"user_jwt_token": jwt_token})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Не найден ID пользователя"


@pytest.mark.asyncio
async def test_auth_unhappy_path_invalid_params(async_client: AsyncClient) -> None:
    user_data = {"name": "user", "password": "admin"}

    response = await async_client.post(url="/signup", json=user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    user_data = {"name": "user@ya.ru", "password": ""}

    response = await async_client.post(url="/signup", json=user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
