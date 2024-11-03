import logging
from fastapi import APIRouter, HTTPException
from schemas.agent import PromptRequest, PromptResponse
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import utilities.config as config

router = APIRouter(prefix="/agent", tags=["agents"])

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# FIXME: thread_idはAgent側で生成してもらい、それをもとに作成することにする
# {
#     "summary": "初期生成のみ",
#     "thread_id": "同じく初期生成時のみ"
#     "response": "response",
# }
# TODO: 初期生成時のAPIと既存スレッド上の会話は分けた方が良いかも？また、生成ロジックは統一させ、叩くAPIだけ変えればラクに実装できそう
@router.post("/", response_model=PromptResponse)
async def generate_response(request: PromptRequest):
    try:
        logger.info("Request received")

        system_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Please respond to the user's request only based on the given context.",
                ),
                ("user", "Question: {prompt}"),
            ]
        )

        logger.info("Prompt template created")

        llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=config.OPENAI_API_KEY)

        chain = system_template | llm

        res = chain.invoke({"prompt": request.prompt})

        logger.info(f"Response from LLM: {res}")

        return {"response": res.content, "summary": request.prompt}

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
