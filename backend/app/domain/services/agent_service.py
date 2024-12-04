import asyncio
import json
import logging
from pathlib import Path
from sqlalchemy.exc import SQLAlchemyError
from typing import AsyncGenerator, List, Dict
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from application.usecase.agent_usecase import AgentUseCase
from infrastructure.database.models.chat_session import ChatSession
from infrastructure.database.models.message import Message
from infrastructure.cache.redis.redis_keys import (
    get_messages_list_key,
    get_sessions_list_key,
)
import utilities.config as config

logger = logging.getLogger(__name__)


class AgentService(AgentUseCase):
    async def delete_cache(self, redis_key: str) -> None:
        try:
            self._redis.delete([redis_key])
        except Exception as e:
            logger.warning(f"Failed to delete cache for key {redis_key}: {str(e)}")

    async def create_chat_session(self, user_id: int, message_content: str) -> int:
        try:
            new_chat_session = ChatSession(
                user_id=user_id,
                summary=message_content,
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow()
                + timedelta(days=int(config.DEFAULT_SESSION_EXPIRATION_DAY)),
            )
            self._db.add(new_chat_session)
            self._db.commit()
            self._db.refresh(new_chat_session)
            return new_chat_session.id
        except Exception as e:
            logger.error(f"Error creating chat session: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating chat session.",
            )

    async def get_conversation_history(
        self, session_id: int, limit: int = 10
    ) -> List[Dict[str, str]]:
        try:
            conversation_histories = (
                self._db.query(Message)
                .filter(Message.session_id == session_id)
                .order_by(Message.id.desc())
                .limit(limit)
                .all()
            )
            return [
                {
                    "role": "user" if msg.is_user else "agent",
                    "content": msg.content,
                }
                for msg in conversation_histories
            ]
        except Exception as e:
            logger.error(f"Error fetching conversation history: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error fetching conversation history.",
            )

    async def process_message(
        self,
        message_content: str,
        session_id: int,
        context: List[Dict[str, str]],
    ) -> AsyncGenerator[str, None]:
        try:
            async for chunk in self._process_llm(message_content, session_id, context):
                yield chunk
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing message.",
            )

    async def _process_llm(
        self, prompt: str, session_id: int, context: List[Dict[str, str]] = []
    ) -> AsyncGenerator[str, None]:
        """
        Processes the LLM request and streams the response in chunks.

        Args:
            prompt (str): The user's message.
            session_id (int): The session ID.
            context (List[Dict[str, str]]): Conversation history.

        Yields:
            str: Chunks of the response from the LLM.
        """
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.5,
            streaming=True,
            openai_api_key=config.OPENAI_API_KEY,
        )

        # System prompt loaded from the file
        system_prompt = self._load_system_prompt()
        system_template = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(system_prompt),
                HumanMessagePromptTemplate.from_template(
                    "Context Analysis:\n{context}\n\nEngineer's Adaptive Task: {prompt}"
                ),
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

        # MEMO: 本当はこの時点でfull_responseをapplication層に返し、application層のサービスとかでDB保存は行うべき
        if full_response:
            await self._save_messages_to_db(session_id, prompt, full_response)

    async def _save_messages_to_db(
        self, session_id: int, user_message_content: str, agent_message_content: str
    ) -> None:
        """
        Saves user and agent messages to the database using the MessageRepository.

        Args:
            session_id (int): Session ID.
            user_message_content (str): The user's message.
            agent_message_content (str): The agent's message.
        """
        cache_key_pattern = get_messages_list_key(session_id)
        await self.delete_cache(cache_key_pattern)

        try:
            user_message = self.message_repository.create_message(
                session_id=session_id,
                content=user_message_content,
                is_user=True,
            )
            agent_message = self.message_repository.create_message(
                session_id=session_id,
                content=agent_message_content,
                is_user=False,
            )

            if user_message is None or agent_message is None:
                logger.error("Failed to save messages to the database.")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to save messages to the database.",
                )

        except Exception as e:
            logger.error(
                f"Unexpected error while saving messages for session {session_id}: {str(e)}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error while saving messages for session {session_id}: {str(e)}",
            )

    @staticmethod
    def _load_system_prompt() -> str:
        """
        Loads the system prompt from a file in the assets directory.

        Args:
            filename (str): Filename of the system prompt.

        Returns:
            str: The system prompt content.

        Raises:
            HTTPException: If the file is not found or cannot be read.
        """
        project_root = Path(__file__).resolve().parents[2]
        system_prompt_path = project_root / "assets" / "system_prompt.txt"

        with system_prompt_path.open("r", encoding="utf-8") as file:
            return file.read()
