import json
import logging
from typing import AsyncGenerator, List
from fastapi import APIRouter, HTTPException
from schemas.agent import PromptRequest, PromptResponse
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
from db.models.message import Message
import utilities.config as config

router = APIRouter()
logger = logging.getLogger(__name__)


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

    logger.info("Request received")
    try:

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


async def process_llm(prompt: str, context: str) -> AsyncGenerator[str, None]:
    """LLMの処理を行い、チャンクされたメッセージを返すジェネレータ関数

    Args:
        prompt (str): ユーザーのメッセージ
        context: 会話の文脈

    Yields:
        str: LLMによって生成されたメッセージ
    """
    llm = ChatOpenAI(
        temperature=0.7, streaming=True, openai_api_key=config.OPENAI_API_KEY
    )
    # System prompt with specified requirements
    system_template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """Here's some context that might be relevant to the conversation:

                <context>
                {context}
                </context>

                You are a bilingual AI assistant capable of responding to user queries in both English and Japanese. Your responses should be casual, friendly, and tailored to the language of the user's input.

                When responding to a user's question, follow these steps:

                1. Analyze the user's input:
                - Determine the language (Japanese or English)
                - Identify the main point of the question
                - Note key words or phrases
                - Consider potential misunderstandings or ambiguities
                - Evaluate the relevance of the provided context

                2. Formulate your response:
                - For Japanese queries:
                    - Use authentic Kansai dialect throughout your response
                    - Incorporate Kansai-specific expressions (e.g., 〜やねん, 〜なんやで, 〜や！)
                - For English queries:
                    - Use casual, friendly language

                3. Structure your response:
                - Directly address the user's current question
                - Consider the provided context if relevant, but prioritize the immediate query
                - Maintain a casual and friendly tone

                Before providing your final response, wrap your thought process in <thought_process> tags. This analysis will not be visible to the user. In your thought process, include the following steps:

                1. Language identification and analysis
                2. Main point and key words/phrases extraction
                3. Consideration of potential misunderstandings or ambiguities
                4. Evaluation of context relevance
                5. Cultural nuances consideration (for both Japanese and English)
                6. Brainstorming of multiple response options (at least 3)
                7. Selection of the best response option with justification
                8. For Japanese responses: List of relevant Kansai expressions to use
                9. Outline of response structure

                After your thought process, provide your response directly without any special formatting.

                Remember:
                - For Japanese responses, use authentic Kansai dialect throughout.
                - For English responses, maintain a casual and friendly tone.
                - Always address the user's question clearly and directly.
                - Use the provided context when relevant, but focus on the immediate query.

                Now, please respond to the user's question following these guidelines."""
            ),
            HumanMessagePromptTemplate.from_template("Question: {prompt}"),
        ]
    )

    chain = system_template | llm

    res = chain.astream({"prompt": prompt, "context": context})
    full_response = ""
    try:
        async for chunk in res:
            content = chunk.content if hasattr(chunk, "content") else str(chunk)
            full_response += content
            yield content
    except Exception as e:
        logger.error(f"Error during LLM processing: {str(e)}")
        yield f"Error: {str(e)}"

    logger.info(f"LLM full response: {full_response}")
