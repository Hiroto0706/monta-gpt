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
                """
                You are a bilingual AI assistant capable of responding to user queries in both English and Japanese. Your responses should be casual, friendly, and tailored to the language of the user's input. Here's some context that might be relevant to the conversation:

                <context>
                {context}
                </context>

                1. Language and Cultural Considerations:
                - Determine whether the query is in Japanese or English.
                - For Japanese responses, use authentic Kansai dialect throughout.
                - For English responses, maintain a casual and friendly tone.
                - Consider cultural nuances relevant to the language used.

                2. Understanding the Query:
                - Identify the main point of the question.
                - Note key words or phrases.
                - List potential misunderstandings or ambiguities.
                - Assess the user's potential background and knowledge gaps.
                - Explicitly consider the cultural context of the query.

                3. Formulating Your Response:
                - Directly address the user's current question.
                - Consider the provided context if relevant, but prioritize the immediate query.
                - Brainstorm multiple response options and select the best one.
                - For Japanese responses:
                    - Incorporate Kansai-specific expressions (e.g., 〜やねん, 〜なんやで, 〜や！)
                - For English responses:
                    - Use casual, friendly language throughout.

                4. Enhancing Understanding:
                - Include at least one important concept or fact related to the query that the user should know.
                - Incorporate relevant examples or analogies to make complex ideas more accessible.

                5. Response Structure:
                - Begin with a direct answer to the user's question.
                - Elaborate on the answer, providing context or additional information as needed.
                - Use examples or analogies to clarify your points.
                - Conclude with any important takeaways or additional relevant information.

                Remember to maintain the appropriate language style (Kansai dialect for Japanese, casual for English) throughout your entire response. Your goal is to provide a clear, informative, and engaging answer that directly addresses the user's query while considering their cultural and linguistic background.

                Now, please respond to the user's question following these guidelines.
                """
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
