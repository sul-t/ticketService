import argparse
from datetime import datetime

from pymongo import AsyncMongoClient
from bson import ObjectId
from bson.errors import InvalidId

from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import get_db_url, settings


DB_URI = get_db_url()
client = AsyncIOMotorClient(DB_URI)
