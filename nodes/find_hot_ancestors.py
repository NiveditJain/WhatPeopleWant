from exospherehost import BaseNode
from pydantic import BaseModel
from utils import get_mongo_client

DATABASE_NAME = "WhatPeopleWant"
COLLECTION_NAME = "items"
HOT_THRESHOLD = 3

class FindHotAncestors(BaseNode):
    class Inputs(BaseModel):
        start_id: str
        end_id: str

    class Outputs(BaseModel):
        ancestor_id: str

    async def execute(self) -> Outputs:
        client = get_mongo_client()
        hot_ancestor_ids = await (await client[DATABASE_NAME][COLLECTION_NAME].aggregate(
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
                            "$gte": HOT_THRESHOLD
                        }
                    }
                },
                {
                    "$project": {
                        "count": 0
                    }
                }
            ]
        )).to_list()
        return [
            self.Outputs(ancestor_id=str(ancestor_id["_id"]))
            for ancestor_id in hot_ancestor_ids
        ]
    
import asyncio

async def main():
    data = await FindHotAncestors()._execute(FindHotAncestors.Inputs(start_id="1", end_id="1000000000"), FindHotAncestors.Secrets())
    print(data)

asyncio.run(main())