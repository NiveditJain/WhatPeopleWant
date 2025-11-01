from exospherehost import BaseNode
from pydantic import BaseModel
from .utils import get_mongo_client

DATABASE_NAME = "WhatPeopleWant"
COLLECTION_NAME = "items"

class GetUpdatedAncestorsNode(BaseNode):
    class Inputs(BaseModel):
        start_id: str
        end_id: str

    class Outputs(BaseModel):
        ancestor_id: str

    async def execute(self) -> list[Outputs]:
        client = get_mongo_client()
        data = await (await client[DATABASE_NAME][COLLECTION_NAME].aggregate(
            [
                {
                    "$match": {
                        "item_id": {
                            "$gte": int(self.inputs.start_id),
                            "$lte": int(self.inputs.end_id)
                        },
                        "ancestor_id": {
                            "$ne": None
                        },
                        "ancestor_id": {
                            "$exists": True
                        }
                    }
                },
                {
                    "$group": {
                        "_id": "$ancestor_id",
                        "count": {
                            "$sum": 1
                        }
                    }
                },
                {
                    "$match": {
                        "count": {
                            "$gte": 1
                        }
                    }
                }
            ]
        )).to_list()
        return [self.Outputs(ancestor_id=str(item["_id"])) for item in data]