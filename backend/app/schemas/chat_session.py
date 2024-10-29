from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ChatSessionBase(BaseModel):
    summary: Optional[str] = None


class ChatSessionUpdate(ChatSessionBase):
    pass


class ChatSessionInDB(ChatSessionBase):
    id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    created_at: datetime
    updated_at: datetime


class ChatSessionResponse(ChatSessionBase):
    id: int
    user_id: int
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ChatSessionCreateRequest(BaseModel):
    prompt: str


class ChatSessionDeleteResponse(BaseModel):
    message: str
