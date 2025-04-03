from typing import Annotated

from bson.objectid import ObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.database import init_mongo_db
from src.core.model import User


class UsersDAO:
    model = User

    def __init__(self, client: Annotated[AsyncIOMotorClient, Depends(init_mongo_db)]):
        self.client = client

    async def add_user(self, name: str, password: str) -> User:
        return await self.model(name=name, role="user", password=password).insert()

    async def get_user_by_name(self, name: str) -> User | None:
        return await self.model.find_one(self.model.name == name)

    async def get_user_by_id(self, user_id: str) -> User | None:
        return await self.model.find_one({"_id": ObjectId(user_id)})
