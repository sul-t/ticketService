import pytest
from httpx import AsyncClient
from beanie import init_beanie
from src.core.model import User
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
import asyncio


# @pytest.fixture(scope="session")
# def event_loop():
#     try:
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope="module")
async def async_client():

    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        yield client


@pytest.fixture(autouse=True)
async def clearing_mongo():
    client = AsyncIOMotorClient(
        f"mongodb://{settings.DB_USER}:{settings.DB_PASSWORD}@localhost:{settings.DB_PORT}"
    )

    try:
        await init_beanie(database=client["ticket"], document_models=[User])
        await User.find({}).delete_many()

        yield
    except Exception as e:
        print(f"Error: {e}")

        raise

