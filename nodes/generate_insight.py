import openai
import os
import json

from exospherehost import BaseNode
from pydantic import BaseModel
from .utils import get_mongo_client


DATABASE_NAME = "WhatPeopleWant"
COLLECTION_NAME = "items"

PROMPT = """Consider yourself a VC analyst, you have only one job to study HackerNews portal and understand what people want and what you suggest entrepreneurs.  

I am giving you a thread from HackerNews where people are talking, I want you to generate a tweet thread on what do you think people want with reasoning. 

**CONVERSATION:**  
{conversation}

Output format: Give me new line separated tweets in order, I will use python string.split('\n') to get a list of tweets and post them in order. So please be sure you follow the same, nothing to be generated which is not a part of tweet. First thread should be of format, People want <1-3 words>, try to be specific, less verbose and do not increase size of one tweet of the thread more than 280 characters.

NOTE: Be professional , do not mention people on HN just mention people. No extra text apart from tweet content. Never tell anyone in tweet that actually you are a VC analyst.

Do not use long dashes — and emojis.
"""

def generate_prompt(message):
    return PROMPT.format(conversation=json.dumps(message, indent=2, ensure_ascii=False))

class GenerateInsightNode(BaseNode):
    class Inputs(BaseModel):
        thread_id: str
    
    class Outputs(BaseModel):
        insight: str
        thread_id: str

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

        client = openai.AsyncOpenAI(
            api_key=os.getenv("OPENAI_KEY"),
            base_url=os.getenv("OPENAI_ENDPOINT")
        )
        reponse = await client.chat.completions.create(
            model="openai-gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": generate_prompt(message)
                }
            ]
        )
        return self.Outputs(insight=reponse.choices[0].message.content, thread_id=str(thread_id))
