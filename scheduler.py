import asyncio
from exospherehost import StateManager, TriggerState
from dotenv import load_dotenv
from datetime import time

load_dotenv()

def trigger_scrape_hacker_news():
    asyncio.run(
        StateManager(
            namespace="WhatPeopleWant"
        ).trigger(
            graph_name="ScrapeYC",
            state=TriggerState(
                identifier="GetMaxItem",
                inputs={}
            )
        )
    )

trigger_scrape_hacker_news()