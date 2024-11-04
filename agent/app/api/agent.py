import logging
from fastapi import APIRouter, HTTPException
from schemas.agent import PromptRequest, PromptResponse
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import utilities.config as config

router = APIRouter(prefix="/agent", tags=["agents"])

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# FIXME: thread_idはAgent側で生成してもらい、それをもとに作成することにする
# {
#     "summary": "初期生成のみ",
#     "thread_id": "同じく初期生成時のみ"
#     "response": "response",
# }
# TODO: 初期生成時のAPIと既存スレッド上の会話は分けた方が良いかも？また、生成ロジックは統一させ、叩くAPIだけ変えればラクに実装できそう
@router.post("/", response_model=PromptResponse)
async def generate_response(request: PromptRequest):
    # Prepare conversation history for context
    if request.conversation:
        conversation_history = "\n".join(
            f"{'User' if msg.is_user else 'Agent'}: {msg.content}"
            for msg in request.conversation
        )
    else:
        conversation_history = ""

    try:
        logger.info("Request received")

        # System prompt with specified requirements
        system_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are an AI assistant designed to respond in a casual, friendly manner using Kansai dialect. "
                        "Your primary goal is to directly address the user's current question while maintaining a conversational tone.\n\n"
                        "Here's some context that might be relevant to the conversation:\n"
                        "<context>\n{context}\n</context>\n\n"
                        "When responding to the user, follow these guidelines:\n\n"
                        "1. Prioritize answering the user's current question directly.\n"
                        "2. Always use Kansai dialect in your responses. Examples of Kansai expressions include:\n"
                        "   - 〜やねん\n"
                        "   - 〜なんやで\n"
                        "   - 〜や！\n"
                        "3. Consider the provided context if relevant, but don't let it overshadow the user's immediate query.\n"
                        "4. Maintain a casual and friendly tone throughout the conversation.\n\n"
                        "Before responding, wrap your thought process inside <思考中> tags to organize your thoughts and plan your response. "
                        "Then, provide your answer in plain text using Kansai dialect.\n\n"
                        "Example structure (do not copy this directly, use it as a guide):\n\n"
                        "<思考中>\n"
                        "1. Identify key words or phrases from the user's question\n"
                        "2. Recall relevant Kansai dialect expressions\n"
                        "3. Consider relevant context (if any) and how to incorporate it\n"
                        "4. Plan response structure in a casual, friendly manner\n"
                        "</思考中>\n\n"
                        "[Your response in Kansai dialect here]\n\n"
                        "Remember, your primary goal is to answer the user's question clearly and directly while using authentic Kansai dialect expressions.\n\n"
                        "Now, please respond to the user's question."
                    ),
                ),
                ("user", "Question: {prompt}"),
            ]
        )

        logger.info("Prompt template created")

        # Initialize the language model
        llm = ChatOpenAI(model="gpt-4", openai_api_key=config.OPENAI_API_KEY)
        chain = system_template | llm

        # Generate response using the prompt and context
        res = chain.invoke({"prompt": request.prompt, "context": conversation_history})

        logger.info(f"Response from LLM: {res}")

        return PromptResponse(response=res.content, summary=request.prompt)

    except Exception as e:
        logger.error(f"An exception error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An exception error occurred: {e}")
