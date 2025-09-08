import asyncio
from exospherehost import StateManager
from dotenv import load_dotenv

load_dotenv()

def trigger_scrape_hacker_news():
    asyncio.run(
        StateManager(
            namespace="WhatPeopleWant"
        ).trigger(
            graph_name="ScrapeYC",
            start_delay=60
        )
    )

trigger_scrape_hacker_news()