from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import get_db_uri
from beanie import init_beanie

from src.core.model import User


async def init_mongo_db() -> AsyncGenerator[AsyncIOMotorClient, None]:
    client: AsyncIOMotorClient = AsyncIOMotorClient(get_db_uri())
    await init_beanie(database=client["ticket"], document_models=[User])

    try:
        yield client
    finally:
        client.close()
