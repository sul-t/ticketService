from beanie import init_beanie
from bson.objectid import ObjectId

from src.core.model import User
from src.core.database import client


class UsersDAO:
    model = User

    @classmethod
    async def _init(cls):
        await init_beanie(database=client['ticket'], document_models=[cls.model])

    @classmethod
    async def add_user(cls, name: str, password: str):
        await cls._init()
        return await cls.model(name=name, role='user', password=password).insert()

    @classmethod
    async def get_user_by_name(cls, name: str):
        await cls._init()
        return await cls.model.find_one(cls.model.name == name)

    @classmethod
    async def get_user_by_id(cls, user_id: str):
        await cls._init()
        return await cls.model.find_one({'_id': ObjectId(user_id)})
