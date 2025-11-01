import os
import openai
from dotenv import load_dotenv
from exospherehost import BaseNode, PruneSignal
from pydantic import BaseModel

load_dotenv()


from browseruse import Agent, Browser, ChatOpenAI, BrowserConfig


PRODUCT_MESSAGING_PROMPT = """You are crafting a reply to a Hacker News thread that is relevant to our product/keywords.

**Product Keywords:**
{keywords}

**Thread Context:**
{thread_context}

**Original Thread:**
{thread_text}

Craft a helpful, relevant reply that:
1. Provides value to the discussion
2. Naturally aligns with our product messaging/keywords without being overly promotional
3. Is professional and respectful
4. Addresses the key points in the thread
5. Does NOT explicitly advertise or mention our product directly unless it's a natural fit

Respond with ONLY the reply text, nothing else. Keep it concise and valuable (2-4 sentences)."""

class EngageWithThreadNode(BaseNode):
    class Inputs(BaseModel):
        thread_id: str
        relevance_score: float
        keywords: list[str]
    
    class Outputs(BaseModel):
        reply_sent: bool
        thread_id: str

    async def execute(self) -> Outputs:
        # Check if relevance score is above threshold
        if self.inputs.relevance_score <= 0.5:
            raise PruneSignal()
        
        # Get thread data to understand context
        from .utils import get_mongo_client
        
        DATABASE_NAME = "WhatPeopleWant"
        COLLECTION_NAME = "items"
        
        client = get_mongo_client()
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        
        thread_id = int(self.inputs.thread_id)
        thread_doc = await collection.find_one({"item_id": thread_id})
        
        if not thread_doc:
            raise PruneSignal()
        
        # Get thread text for context
        thread_text = thread_doc.get("text") or thread_doc.get("title", "")
        thread_context = f"Thread ID: {thread_id}\nTitle: {thread_doc.get('title', 'N/A')}"
        
        # Generate reply using OpenAI
        openai_client = openai.AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        
        reply_prompt = PRODUCT_MESSAGING_PROMPT.format(
            keywords="\n".join(f"- {keyword}" for keyword in self.inputs.keywords),
            thread_context=thread_context,
            thread_text=thread_text[:1000]  # Limit to first 1000 chars
        )
        
        reply_response = await openai_client.chat.completions.create(
            model="openai-gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": reply_prompt
                }
            ]
        )
        
        reply_text = reply_response.choices[0].message.content.strip()
        
        # Use browseruse to navigate to HN and reply
        hn_url = f"https://news.ycombinator.com/item?id={thread_id}"

        browser = Browser(headless=False)
    
        agent = Agent(
            task=f"""
            1. Go to {hn_url}
            2. Find the reply box
            3. Type this comment: {reply_text}
            4. Submit the comment
            """,
            browser=browser,
            llm=ChatOpenAI(model="gpt-4o-mini")
        )
        await agent.run()      
        
        return self.Outputs(
            reply_sent=True,
            thread_id=str(thread_id)
        )

