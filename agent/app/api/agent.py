from time import sleep
from fastapi import APIRouter
from schemas.agent import PromptRequest, PromptResponse

router = APIRouter(prefix="/agent", tags=["agents"])


# FIXME: thread_idはAgent側で生成してもらい、それをもとに作成することにする
# {
#     "summary": "初期生成のみ",
#     "thread_id": "同じく初期生成時のみ"
#     "response": "response",
# }
# TODO: 初期生成時のAPIと既存スレッド上の会話は分けた方が良いかも？また、生成ロジックは統一させ、叩くAPIだけ変えればラクに実装できそう
@router.post("/", response_model=PromptResponse)
async def generate_response(request: PromptRequest):
    sleep(10)
    generated_response = f"Agent response to: {request.prompt}"
    summary = f"Summary of the response to: {request.prompt}"
    return {"response": generated_response, "summary": summary}
