import json
from typing import Dict, Any
from exospherehost import BaseNode
from pydantic import BaseModel
from .utils import get_mongo_client


DATABASE_NAME = "WhatPeopleWant"
COLLECTION_NAME = "items"


class GenerateThreadNode(BaseNode):
    class Inputs(BaseModel):
        thread_id: str
    
    class Outputs(BaseModel):
        thread_id: str
        message: str

    async def execute(self) -> Outputs:
        client = get_mongo_client()
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        thread_id = int(self.inputs.thread_id)
        thread_data = await(await collection.aggregate(
            [
                {
                    "$match": {
                        "item_id": thread_id
                    }
                },
                {
                    "$graphLookup": {
                        "from": COLLECTION_NAME,
                        "startWith": "$kids",
                        "connectFromField": "kids",
                        "connectToField": "item_id",
                        "as": "replies",
                        "depthField": "level"
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "item_id": 1,
                        "text": 1,
                        "kids": 1,
                        "title": 1,
                        "replies.item_id": 1,
                        "replies.text": 1,
                        "replies.title": 1,
                        "replies.level": 1,
                        "replies.kids": 1
                    }
                }
            ]
        )).to_list()

        look_up_table = {}
        for item in thread_data[0]["replies"]:
            look_up_table[item["item_id"]] = item

        look_up_table[thread_id] = thread_data[0].copy()
        look_up_table[thread_id].pop("replies")

        def dfs(item_id):
            if item_id not in look_up_table:
                return {}
                
            item = look_up_table[item_id]
            message = {
                "text": item["text"] if "text" in item else item["title"] if "title" in item else None
            }

            replies = []
            if "kids" in item:
                for reply in item["kids"]:
                    replies.append(dfs(reply))
                    
            if len(replies) > 0:
                message["replies"] = replies
                    
            return message

        message = dfs(thread_id)

        return self.Outputs(
            thread_id=str(thread_id),
            message=json.dumps(message)
        )

