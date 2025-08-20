from dotenv import load_dotenv
from exospherehost import BaseNode
from pydantic import BaseModel
from datetime import datetime
from .utils import get_mongo_client

DATABASE_NAME = "WhatPeopleWant"
COLLECTION_NAME = "runs"

load_dotenv()

class AddDatabasePointerNode(BaseNode):
    class Inputs(BaseModel):
        item_id: str

    class Outputs(BaseModel):
        start_id: str
        end_id: str

    async def execute(self) -> Outputs:
        client = get_mongo_client()
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        base_item = await collection.find_one({}, sort=[("end_id", -1)])

        start_id = 0
        if base_item:
            start_id = int(base_item["end_id"]) + 1

        await collection.insert_one({
            "end_id": int(self.inputs.item_id),
            "start_id": start_id,
            "created_at": datetime.now()
        })

        return self.Outputs(start_id=str(start_id), end_id=str(self.inputs.item_id))
