import openai
import os
import json

from exospherehost import BaseNode
from pydantic import BaseModel
from .utils import get_mongo_client


DATABASE_NAME = "WhatPeopleWant"
COLLECTION_NAME = "items"

PROMPT = """
You are an entrepreneur-analyst. Your task is to study the attached forum conversation and extract real problems people mention. From those, generate venture ideas that could be built.  

**Important rules:**
- Only use what is in the conversation. Do not hallucinate.  
- Be careful: poor analysis may waste money and time.  
- If evidence is weak or unclear, mark the idea as Low confidence.  
- If an idea could cause harm, flag the risk.  

**Steps:**
1. **Extract signals** - pull out pain points, complaints, or unmet needs with short supporting quotes.  
2. **Cluster themes** - group signals into clear themes.  
3. **Define problems** - one line per theme that states the problem.  
4. **Generate ideas** - propose solutions directly tied to these problems.  
5. **Rank ideas** - score each idea (1-5) on: frequency, intensity, willingness to pay, urgency, feasibility. Show the total.  
6. **Validation** - suggest 1 lean steps to test top ideas.

**Output format:**
- A short summary with Idea, Problem, and Key Quote.
- A **detailed note** for top ideas: Idea, Problem, Target User, Solution, Quotes, Risks, Score breakdown, Validation steps.

**CONVERSATION:**  
{conversation}
"""

def generate_prompt(message):
    return PROMPT.format(conversation=json.dumps(message, indent=2, ensure_ascii=False))

class GenerateInsightNode(BaseNode):
    class Inputs(BaseModel):
        thread_id: str
    
    class Outputs(BaseModel):
        insight: str

    async def execute(self) -> Outputs:
        try:
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
                api_key=os.getenv("IO_NET_INFERENCE_KEY"),
                base_url="https://api.intelligence.io.solutions/api/v1/"
            )
            reponse = await client.chat.completions.create(
                model="Qwen/Qwen3-235B-A22B-Thinking-2507",
                messages=[
                    {
                        "role": "user",
                        "content": generate_prompt(message)
                    }
                ]
            )
            return self.Outputs(insight=reponse.choices[0].message.content)
        
        except Exception as _:
            raise
