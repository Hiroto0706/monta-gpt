from typing import List, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    content: str = Field(..., alias="content")
    is_user: bool = Field(..., alias="isUser")
    created_at: str = Field(..., alias="createdAt")

    class Config:
        allow_population_by_field_name = True


class PromptRequest(BaseModel):
    prompt: str = Field(..., alias="prompt")
    conversation: Optional[List[ChatMessage]] = Field(
        default=None, alias="conversation"
    )


class PromptResponse(BaseModel):
    response: str = Field(..., alias="response")
    summary: str = Field(..., alias="summary")
