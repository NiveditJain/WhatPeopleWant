import os
from pymongo import AsyncMongoClient
from dotenv import load_dotenv

load_dotenv()

_mongo_client = None

def get_mongo_client():
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = AsyncMongoClient(os.getenv("MONGO_URI"))
    return _mongo_client