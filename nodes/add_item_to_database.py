from aiohttp import ClientSession
from exospherehost import BaseNode
from pydantic import BaseModel
from dotenv import load_dotenv
from .utils import get_mongo_client

load_dotenv()

DATABASE_NAME = "WhatPeopleWant"
COLLECTION_NAME = "items"

async def get_item_from_hacker_news(item_id: int) -> dict:
    async with ClientSession() as session:
        async with session.get(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json") as response:
            return await response.json()

async def add_item_to_database(item_id: int, item: dict) -> str:
    client = get_mongo_client()
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    inserted_id = (await collection.insert_one({
        "item_id": item_id,
        **item
    })).inserted_id
    return str(inserted_id)

class AddItemToDatabaseNode(BaseNode):
    class Inputs(BaseModel):
        item_id: str

    class Outputs(BaseModel):
        object_id: str

    async def execute(self) -> Outputs:
        item_id = int(self.inputs.item_id)
        object_id = await add_item_to_database(item_id, await get_item_from_hacker_news(item_id))
        return self.Outputs(object_id=object_id)
