import openai
import os
import json
from typing import List, Dict, Any

from exospherehost import BaseNode
from pydantic import BaseModel

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

RELEVANCE_PROMPT = """You are evaluating whether a message is relevant to a given list of keywords.

**Keywords:**
{keywords}

**Message:**
{message}

Rate the relevance of the message to the keywords on a scale of 0 to 10, where:
- 0 means completely irrelevant
- 5 means somewhat relevant
- 10 means highly relevant

Respond with ONLY an integer between 0 and 10, nothing else."""

class GenerateInsightNode(BaseNode):
    class Inputs(BaseModel):
        thread_id: str
        message: str
        keywords: str
    
    class Outputs(BaseModel):
        thread_id: str
        relevance_score: str

    async def execute(self) -> Outputs:

        client = openai.AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        # reponse = await client.chat.completions.create(
        #     model="openai-gpt-oss-120b",
        #     messages=[
        #         {
        #             "role": "user",
        #             "content": generate_prompt(self.inputs.message)
        #         }
        #     ]
        # )
        # insight = reponse.choices[0].message.content

        # Check relevance of the insight to the keywords
        relevance_prompt = RELEVANCE_PROMPT.format(
            keywords=self.inputs.keywords,
            message=self.inputs.message
        )
        relevance_response = await client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "user",
                    "content": relevance_prompt
                }
            ]
        )
        
        # Parse the relevance score
        relevance_text = relevance_response.choices[0].message.content.strip()
        try:
            relevance_score = int(relevance_text)
            # Clamp score between 0.0 and 1.0
            relevance_score = max(0, min(10, relevance_score))
        except ValueError:
            # If parsing fails, default to 0.0
            relevance_score = 0

        return self.Outputs(
            thread_id=str(self.inputs.thread_id),
            relevance_score=str(relevance_score)
        )
