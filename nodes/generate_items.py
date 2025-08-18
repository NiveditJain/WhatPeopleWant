from exospherehost import BaseNode
from pydantic import BaseModel

class GenerateItemsNode(BaseNode):
    class Inputs(BaseModel):
        start_id: str
        end_id: str

    class Outputs(BaseModel):
        item_id: str

    async def execute(self) -> list[Outputs]:
        outputs = []
        for item_id in range(int(self.inputs.start_id), int(self.inputs.end_id) + 1):
            outputs.append(self.Outputs(item_id=str(item_id)))
        return outputs
