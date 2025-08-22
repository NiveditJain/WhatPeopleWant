import boto3
import os
from dotenv import load_dotenv

from exospherehost import BaseNode
from pydantic import BaseModel

load_dotenv()

class SendAnalysisNode(BaseNode):
    class Inputs(BaseModel):
        insight: str
        thread_id: str

    class Outputs(BaseModel):
        pass

    async def execute(self) -> Outputs:
        ses = boto3.client(
            "ses",
            region_name=os.getenv("AWS_SES_REGION"),
            aws_access_key_id=os.getenv("AWS_SES_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SES_SECRET_KEY"),
        )

        self.inputs.insight += "\n Source: https://news.ycombinator.com/item?id=" + self.inputs.thread_id
        
        ses.send_email(
            Source=os.getenv("AWS_SES_EMAIL"),
            Destination={
                "ToAddresses": [email.strip() for email in os.getenv("TO_EMAILS").split(",")],
            },
            Message={
                "Subject": {
                    "Data": f"HN Analysis for {self.inputs.thread_id}",
                    "Charset": "UTF-8",
                },
                "Body": {
                    "Text": {
                        "Data": self.inputs.insight,
                        "Charset": "UTF-8",
                    },
                    "Html": {
                        "Data": "\n".join([f"<p>{line.strip()}</p>" for line in self.inputs.insight.split("\n")]),
                        "Charset": "UTF-8",
                    },
                },
            },
        )