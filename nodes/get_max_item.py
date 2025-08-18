from exospherehost import BaseNode
from pydantic import BaseModel
from aiohttp import ClientSession

MAX_ITEM_ENDPOINT = "https://hacker-news.firebaseio.com/v0/maxitem.json"

class GetMaxItemNode(BaseNode):
    
    class Inputs(BaseModel):
        pass

    class Outputs(BaseModel):
        max_item: str

    async def _get_max_item(self) -> int:
        async with ClientSession() as session:
            async with session.get(MAX_ITEM_ENDPOINT) as response:
                return await response.json()

    async def execute(self) -> Outputs:
        max_item = await self._get_max_item()
        return self.Outputs(max_item= str(max_item))
