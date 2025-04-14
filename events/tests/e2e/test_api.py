from datetime import datetime, timedelta

from fastapi import status
from httpx import AsyncClient
import pytest


pytestmark = pytest.mark.e2e


async def find_event_data(async_http_client: AsyncClient):
    event_data_for_finding = {
        "date_from": datetime.now().date(),
        "date_to": ((datetime.now() + timedelta(days=30)).date()).isoformat()
    }

    return await async_http_client.get("/events", params=event_data_for_finding)


@pytest.mark.asyncio
async def test_create_event_happy_path(async_http_client: AsyncClient, setup_test_data: dict):
    assert setup_test_data


@pytest.mark.asyncio
async def test_update_event_happy_path(async_http_client: AsyncClient, setup_test_data: dict):
    assert setup_test_data

    event_data = await find_event_data(async_http_client)

    new_event_data = {
        "name": "Щелкунчик",
        "description": "Балет Петра Чайковского",
        "event_date": (datetime.now() + timedelta(days=10)).isoformat(),
        "available_tickets": 50,
        "ticket_price": 1000
    }

    response = await async_http_client.put(url=f"/events/{event_data.json()[0]['id']}", json=new_event_data)
    assert response.json()["ok"]
    assert response.json()["data"]["details"]["errors"][0] is None


@pytest.mark.asyncio
async def test_delete_not_started_event_happy_path(async_http_client: AsyncClient, setup_test_data: dict):
    assert setup_test_data

    event_data = await find_event_data(async_http_client)

    response = await async_http_client.delete(f"/events/{event_data.json()[0]['id']}")
    assert response.json()["ok"]
    assert response.json()["data"]["message"] == "Мероприятие успешно удалено и деньги возвращены"


@pytest.mark.asyncio
async def test_delete_event_happy_path(async_http_client: AsyncClient, example_event_data: dict):
    example_event_data["event_date"] = (datetime.now()).isoformat()
    response = await async_http_client.post(url="/events", json=example_event_data)
    assert response.json()["ok"]

    event_data = await find_event_data(async_http_client)

    response = await async_http_client.delete(f"/events/{event_data.json()[0]['id']}")
    assert response.json()["ok"]
    assert response.json()["data"]["message"] == "Мероприятие успешно удалено"


@pytest.mark.asyncio
async def test_get_event_by_id_happy_path(async_http_client: AsyncClient, setup_test_data: dict, example_event_data: dict):
    assert setup_test_data

    event_data = await find_event_data(async_http_client)

    response = await async_http_client.get(url=f"/events/{event_data.json()[0]['id']}")
    assert response.json() == example_event_data

@pytest.mark.asyncio
async def test_get_event_by_date_happy_path(async_http_client: AsyncClient, setup_test_data: dict, example_event_data: dict):
    assert setup_test_data

    response = await find_event_data(async_http_client)
    response_data = response.json()[0]

    response_data.pop("id")

    assert response_data == example_event_data


#unhappy path
@pytest.mark.asyncio
async def test_create_event_unhappy_path(async_http_client: AsyncClient):
    response = await async_http_client.post(url='/events', json={'name': 'Поднятие уровня в одиночку'})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.asyncio
async def test_update_event_unhappy_path(async_http_client: AsyncClient, example_event_data: dict):
    response = await async_http_client.put(url='/events/1234', json=example_event_data)
    assert response.json()['ok'] == False

@pytest.mark.asyncio
async def test_delete_event_unhappy_path(async_http_client: AsyncClient):
    response = await async_http_client.delete(url='/events/1234')
    assert response.json()['ok'] == False

@pytest.mark.asyncio
async def test_get_event_by_id_unhappy_path(async_http_client: AsyncClient):
    response = await async_http_client.get(url='/events/1234')
    assert response.json()['ok'] == False

@pytest.mark.asyncio
async def test_get_event_by_date_unhappy_path(async_http_client: AsyncClient):
    response = await async_http_client.get(url='/events')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY




