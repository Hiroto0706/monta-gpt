from typing import List, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    content: str
    is_user: bool
    created_at: str


class PromptRequest(BaseModel):
    prompt: str
    conversation: Optional[List[ChatMessage]] = None


class PromptResponse(BaseModel):
    response: str
    summary: str
