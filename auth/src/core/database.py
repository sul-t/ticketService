import argparse
from datetime import datetime

from pymongo import AsyncMongoClient
from bson import ObjectId
from bson.errors import InvalidId

from motor.motor_asyncio import AsyncIOMotorClient

from auth.src.core.config import get_db_url


DB_URL = get_db_url()


client = AsyncIOMotorClient(DB_URL)