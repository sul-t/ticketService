from collections.abc import AsyncGenerator

from beanie import init_beanie
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
import pytest
from testcontainers.mongodb import MongoDbContainer

from main import app
from src.core.database import init_mongo_db
from src.core.model import User


async def overaide_init_mongo_db(mongo_db_container: MongoDbContainer) -> AsyncGenerator[AsyncIOMotorClient, None]:
    client: AsyncIOMotorClient = AsyncIOMotorClient(mongo_db_container.get_connection_url())
    await init_beanie(database=client["ticket"], document_models=[User])

    try:
        yield client
    finally:
        client.close()


@pytest.fixture(scope="session")
async def mongo_db_container():
    with MongoDbContainer("mongo") as container:
        yield container


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000") as client:
        yield client


@pytest.fixture(autouse=True)
async def mongo_db_connection(mongo_db_container: MongoDbContainer) -> AsyncGenerator[AsyncIOMotorClient, None]:
    app.dependency_overrides[init_mongo_db] = lambda: overaide_init_mongo_db(mongo_db_connection)

    client: AsyncIOMotorClient = AsyncIOMotorClient(mongo_db_container.get_connection_url())

    try:
        await init_beanie(database=client["ticket"], document_models=[User])
        await User.find({}).delete_many()

        yield client

    finally:
        client.close()
