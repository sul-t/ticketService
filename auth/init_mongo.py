import asyncio
from auth.src.core.database import init_mongo


asyncio.run(init_mongo())

