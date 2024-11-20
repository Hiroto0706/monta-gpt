import asyncio
import logging
from datetime import datetime
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException, status
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.models.message import Message
import utilities.config as config

router = APIRouter()
logger = logging.getLogger(__name__)


async def process_llm(
    prompt: str, session_id: int, db: Session, context: str = ""
) -> AsyncGenerator[str, None]:
    """LLMの処理を行い、チャンクされたメッセージを返すジェネレータ関数

    Args:
        prompt (str): ユーザーのメッセージ
        context: 会話の文脈

    Yields:
        str: LLMによって生成されたメッセージ
    """
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.5,
        streaming=True,
        openai_api_key=config.OPENAI_API_KEY,
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
    accumulated_content = ""
    chunk_size = 25
    last_send_time = asyncio.get_event_loop().time()
    time_threshold = 1.0
    try:
        async for chunk in res:
            content = chunk.content if hasattr(chunk, "content") else str(chunk)
            full_response += content
            accumulated_content += content

            current_time = asyncio.get_event_loop().time()
            if (
                len(accumulated_content) >= chunk_size
                or (current_time - last_send_time) >= time_threshold
            ):
                yield accumulated_content
                accumulated_content = ""
                last_send_time = current_time
    except Exception as e:
        logger.error(f"Error during LLM processing: {str(e)}")
        yield f"Error: {str(e)}"

    if accumulated_content:
        yield accumulated_content

    logger.info(f"LLM full response: {full_response}")

    if full_response:
        user_message = Message(
            session_id=session_id,
            content=prompt,
            is_user=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        agent_message = Message(
            session_id=session_id,
            content=full_response,
            is_user=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        try:
            db.add(user_message)
            db.add(agent_message)
            db.commit()
            db.refresh(user_message)
            db.refresh(agent_message)
        except SQLAlchemyError as db_error:
            db.rollback()
            logger.error(
                f"Database error while saving messages for session {session_id}: {str(db_error)}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while saving messages for session {session_id}: {str(db_error)}",
            )
        except Exception as e:
            db.rollback()
            logger.error(
                f"Unexpected error while saving messages for session {session_id}: {str(e)}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error while saving messages for session {session_id}: {str(e)}",
            )
