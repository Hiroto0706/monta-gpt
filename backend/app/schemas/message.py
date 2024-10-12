from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageBase(BaseModel):
    content: Optional[str] = None
    is_user: Optional[bool] = None


class MessageUpdate(MessageBase):
    pass


class MessageInDB(MessageBase):
    id: int
    session_id: int
    content: str
    timestamp: datetime
    is_user: bool
    created_at: datetime

    class Config:
        orm_mode = True


class MessageCreateRequest(BaseModel):
    session_id: int
    prompt: str


class MessageResponse(MessageBase):
    id: int
    session_id: int
    content: str
    timestamp: datetime
    is_user: bool
    created_at: datetime

    class Config:
        orm_mode = True
