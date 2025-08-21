from exospherehost import BaseNode
from pydantic import BaseModel
from .utils import get_mongo_client

DATABASE_NAME = "WhatPeopleWant"
COLLECTION_NAME = "items"

class AddAncestorIdNode(BaseNode):
    class Inputs(BaseModel):
        start_id: str
        end_id: str

    class Outputs(BaseModel):
        pass

    async def execute(self) -> Outputs:
        client = get_mongo_client()
        await client[DATABASE_NAME][COLLECTION_NAME].aggregate(
            [
                {
                    "$match": {
                        "item_id": {
                            "$gte": int(self.inputs.start_id),
                            "$lte": int(self.inputs.end_id)
                        }
                    }
                },
                {
                    "$graphLookup": {
                        "from": COLLECTION_NAME,
                        "startWith": "$parent",
                        "connectFromField": "parent",
                        "connectToField": "item_id",
                        "as": "parent_objects",
                        "depthField": "depth"
                    }
                },
                {
                    "$addFields":{
                        "max_depth_ancestor": {
                            "$reduce": {
                                "input": "$parent_objects",
                                "initialValue": {
                                    "item_id": None, 
                                    "depth": -1
                                },
                                "in": {
                                    "$cond": {
                                        "if": {"$gt": ["$$this.depth", "$$value.depth"]},
                                        "then": {"item_id": "$$this.item_id", "depth": "$$this.depth"},
                                        "else": "$$value"
                                    }
                                }
                            }
                        }
                    }
                },
                {
                    "$set": {
                        "ancestor_id": "$max_depth_ancestor.item_id"
                    }
                },
                {
                    "$project": {
                        "parent_objects": 0,
                        "max_depth_ancestor": 0,
                    }
                },
                {
                    "$merge": {
                        "into": COLLECTION_NAME,
                        "on": "_id",
                        "whenMatched": "merge",
                        "whenNotMatched": "discard"
                    }
                }
            ]
        )
