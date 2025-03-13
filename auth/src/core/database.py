from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import get_db_uri

client = AsyncIOMotorClient(get_db_uri())
