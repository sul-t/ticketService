from collections.abc import AsyncGenerator
from functools import partial
import traceback

import pytest

from alembic.config import Config
from alembic.command import upgrade as alembic_upgrade
from alembic.runtime import migration

from httpx import ASGITransport, AsyncClient

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import delete
from testcontainers.postgres import PostgresContainer

from main import app
from src.core.database import async_session
from src.core.models import Event
from config import get_db_uri


async def get_test_async_session(test_postgres_container: PostgresContainer) -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(test_postgres_container.get_connection_url())
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
def test_postgres_container():
    with PostgresContainer("postgres:alpine", driver='asyncpg') as container:
        alembic_cfg = Config('alembic.ini')
        alembic_cfg.set_main_option('sqlalchemy.url', container.get_connection_url())

        alembic_upgrade(alembic_cfg, 'head')

        yield container


@pytest.fixture(autouse=True)
async def setup_test_database(test_postgres_container: PostgresContainer):
    app.dependency_overrides[async_session] = partial(get_test_async_session, test_postgres_container)
    
    async for session in get_test_async_session(test_postgres_container):
        try:
            await session.execute(delete(Event))
            await session.commit()
            yield session
        finally:
            await session.close()


@pytest.fixture
async def async_http_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000/events") as client:
        yield client