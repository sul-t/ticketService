from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from beanie.operators import In
from bson.objectid import ObjectId

from auth.src.core.model import User
from auth.src.core.database import client



class UsersDAO:
    model = User

    @classmethod
    async def create_user(cls, name, password):
        await init_beanie(database=client['users'], document_models=[cls.model])

        user = cls.model(name=name, role='user', password=password)
        await user.insert()

    @classmethod
    async def find_user(cls, name):
        await init_beanie(database=client['users'], document_models=[cls.model])

        first_or_none_user = await cls.model.find_one(
            cls.model.name == name
        )

        return first_or_none_user
    
    @classmethod
    async def find_user_by_id(cls, user_id):
        await init_beanie(database=client['users'], document_models=[cls.model])

        data = await cls.model.find({}).to_list()
        for result in data:
            print(result)

        first_or_none_user = await cls.model.find_one({"_id": ObjectId(user_id)})

        return first_or_none_user
    



