from exospherehost import BaseNode
from pydantic import BaseModel
from typing import List
from .utils import get_mongo_client
import json

DATABASE_NAME = "WhatPeopleWant"
COLLECTION_NAME = "keywords"

class FetchKeywordsNode(BaseNode):
    class Inputs(BaseModel):
        pass

    class Outputs(BaseModel):
        keywords: str

    async def execute(self) -> Outputs:
        # client = get_mongo_client()
        # db = client[DATABASE_NAME]
        # collection = db[COLLECTION_NAME]
        
        # # Fetch all keywords from the database
        # cursor = collection.find({})
        # documents = await cursor.to_list(length=None)
        
        # # Extract keywords from documents
        # # Assuming documents have a "keyword" field or similar
        # keywords = []
        # for doc in documents:
        #     if "keyword" in doc:
        #         keywords.append(doc["keyword"])
        #     elif "text" in doc:
        #         keywords.append(doc["text"])
        #     elif "name" in doc:
        #         keywords.append(doc["name"])

        keywords = ["multi-agent", "ai", "llm", "agentic", "agentic ai", "agentic llm", "agentic ai llm", "agentic ai llm", "agentic ai llm","distributed agentic ai", "parallel agentic ai"]

        keywords = ", ".join(keywords)
        return self.Outputs(keywords=json.dumps(keywords))

