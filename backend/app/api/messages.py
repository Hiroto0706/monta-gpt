from fastapi import APIRouter

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/")
async def get_message_by_session_id():
    return {"message": "get chats history"}


@router.post("/send")
async def send_prompt():
    return {"message": "you sended prompt to agent"}
