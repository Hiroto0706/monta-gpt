from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class MessageBase(BaseModel):
    content: Optional[str] = Field(default=None, alias="content")
    is_user: Optional[bool] = Field(default=None, alias="isUser")

    class Config:
        allow_population_by_field_name = True


class MessageResponse(MessageBase):
    id: int = Field(..., alias="id")
    session_id: int = Field(..., alias="sessionID")
    content: str = Field(default=None, alias="content")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
