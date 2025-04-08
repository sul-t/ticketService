from datetime import datetime

import pytest

from httpx import AsyncClient


pytestmark = pytest.mark.e2e

@pytest.mark.asyncio
async def test_create_event_happy_path(async_http_client: AsyncClient):
    event_data = {
        "name": 'Поднятие уровня в одиночку',
        "description": 'Сюжет будет построен на оригинальной манхве',
        "event_date": datetime.now(),
        "available_tickets": 150,
        "ticket_price": 1000
    }

    headers = {"X-User-Role": 'admin'}

    response = await async_http_client.post(url='', json=event_data, headers=headers)
    assert response.json()['ok'] == True