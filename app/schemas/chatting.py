from typing import List

from pydantic import BaseModel

class MessageEvent(BaseModel):
    sender: str | None = None
    message: str | List[str] = None
    message_type: str
    receiver: str | None = None
