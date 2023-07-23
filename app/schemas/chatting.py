from typing import List

from pydantic import BaseModel

class MessageEvent(BaseModel):
    sender: str = None
    message: str | List[str]
    message_type: str
    receiver: str = None
