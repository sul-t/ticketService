from collections.abc import AsyncGenerator
from datetime import datetime, timedelta

from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy import MetaData, inspect, text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer
from main import app
from src.core.database import async_session


def create_database(connection, cfg):
        cfg.attributes["connection"] = connection

        inspector = inspect(connection)
        if "alembic_version" not in inspector.get_table_names():
            alembic_upgrade(cfg, "head")




async def drop_database(engine: AsyncEngine):
    async with engine.begin() as conn:
        metadata = MetaData()
        await conn.run_sync(lambda sync_conn: metadata.reflect(sync_conn, schema="public"))

        table_names = [table.name for table in metadata.tables.values()]

        if table_names:
            await conn.execute(text(f"TRUNCATE {', '.join(table_names)} RESTART IDENTITY CASCADE"))


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:alpine", driver="asyncpg") as container:
        yield container


@pytest.fixture(scope="function")
async def postgres_engine(postgres_container: PostgresContainer):
    try:
        postgres_url = postgres_container.get_connection_url()
        engine = create_async_engine(postgres_url)

        async with engine.begin() as conn:
            await conn.run_sync(create_database, Config("alembic.ini"))

        yield engine
    finally:
        await engine.dispose()


@pytest.fixture(autouse=True)
async def postgres_session_factory(postgres_engine: AsyncEngine):
    async_session_maker = async_sessionmaker(postgres_engine, expire_on_commit=False)

    async def override_get_session() -> AsyncGenerator:
        async with async_session_maker() as session:
            yield session

    app.dependency_overrides[async_session] = override_get_session

    yield async_session_maker

    await drop_database(postgres_engine)



@pytest.fixture
def example_event_data() -> dict:
    return {
        "name": "Поднятие уровня в одиночку",
        "description": "Сюжет будет построен на оригинальной манхве",
        "event_date": (datetime.now() + timedelta(days=15)).isoformat(),
        "available_tickets": 150,
        "ticket_price": 1000
    }

@pytest.fixture
async def setup_test_data(async_http_client: AsyncClient, example_event_data: dict):
    response = await async_http_client.post(url="/events", json=example_event_data)

    return response.json()["ok"]


@pytest.fixture
async def async_http_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1:8001", headers={"X-User-Role": "admin"}) as client:
        yield client

