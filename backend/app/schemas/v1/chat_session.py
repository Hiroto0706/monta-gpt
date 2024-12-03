from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ChatSessionBase(BaseModel):
    summary: Optional[str] = Field(default=None, alias="summary")


class ChatSessionInDB(ChatSessionBase):
    id: int = Field(..., alias="id")
    user_id: int = Field(..., alias="userId")
    start_time: datetime = Field(..., alias="startTime")
    end_time: datetime = Field(..., alias="endTime")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    class Config:
        allow_population_by_field_name = True


class ChatSessionCreateRequest(BaseModel):
    prompt: str = Field(..., alias="prompt")


class ChatSessionUpdateRequest(BaseModel):
    summary: Optional[str] = Field(default=None, alias="summary")


class ChatSessionResponse(ChatSessionBase):
    id: int = Field(..., alias="id")
    user_id: int = Field(..., alias="userId")
    start_time: Optional[datetime] = Field(default=None, alias="startTime")
    end_time: Optional[datetime] = Field(default=None, alias="endTime")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    content: Optional[str] = Field(default=None, alias="content")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ChatSessionDeleteResponse(BaseModel):
    message: str = Field(..., alias="message")
