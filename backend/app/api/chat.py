from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/")
async def get_chat_history():
    return {"message": "get chats history"}


@router.post("/send")
async def send_prompt():
    return {"message": "you sended prompt to agent"}
