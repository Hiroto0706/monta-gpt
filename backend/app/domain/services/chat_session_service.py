import logging
from typing import List

from fastapi import HTTPException, status

from schemas.v1.chat_session import ChatSessionResponse
from application.usecase.chat_session_usecase import ChatSessionUseCase
from domain.value_objects.user import UserID

logger = logging.getLogger(__name__)


class ChatSessionService(ChatSessionUseCase):
    async def get_chat_history(self, user_id: UserID) -> List[ChatSessionResponse]:
        """
        指定されたユーザーのチャットセッション履歴を取得します。

        Args:
            current_user (Dict[str, Any]): アクセストークンから取得したユーザーペイロード

        Returns:
            List[ChatSessionResponse]: チャットセッションのリスト

        Raises:
            HTTPException: データ取得中にエラーが発生した場合
        """
        try:
            chat_sessions = self.chat_session_repository.get_chat_session_by_user_id(
                user_id
            )
            if chat_sessions is None:
                return []
            return chat_sessions
        except Exception as e:
            logger.error(f"Error getting chat history for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving chat history.",
            )

    # async def create_chat_session(
    #     self,
    #     chat_session_request: ChatSessionCreateRequest,
    #     current_user: Dict[str, Any],
    # ) -> ChatSessionResponse:
    #     user_message = Message(
    #         session_id=None,
    #         content=chat_session_request.prompt,
    #         is_user=True,
    #         created_at=datetime.utcnow(),
    #         updated_at=datetime.utcnow(),
    #     )
    #     timeout = httpx.Timeout(connect=15.0, read=60.0, write=60.0, pool=5.0)
    #     async with httpx.AsyncClient(timeout=timeout) as client:
    #         try:
    #             response = await client.post(
    #                 f"{config.AGENT_URL}agent/",
    #                 json={"prompt": chat_session_request.prompt},
    #             )
    #             response.raise_for_status()
    #         except httpx.RequestError as e:
    #             logger.error(f"Request error while contacting agent API: {str(e)}")
    #             raise HTTPException(
    #                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                 detail=f"Request error while contacting agent API.",
    #             )

    #     agent_response_data = response.json()
    #     agent_response = agent_response_data.get("response")
    #     agent_summary = agent_response_data.get("summary")

    #     logger.info(
    #         f"Agent response: {agent_response}\nAgent summary: {agent_summary}\n"
    #     )

    #     if not agent_response or not agent_summary:
    #         logger.error(
    #             "Invalid response from agent API, missing response or summary."
    #         )
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail="Invalid response from agent API.",
    #         )

    #     try:
    #         agent_message = Message(
    #             session_id=None,
    #             content=agent_response,
    #             is_user=False,
    #             created_at=datetime.utcnow(),
    #             updated_at=datetime.utcnow(),
    #         )

    #         new_chat_session = ChatSession(
    #             user_id=current_user.get("user_id"),
    #             summary=agent_summary,
    #             start_time=datetime.utcnow(),
    #             end_time=datetime.utcnow()
    #             + timedelta(days=int(config.DEFAULT_SESSION_EXPIRATION_DAY)),
    #         )

    #         self._db.add(new_chat_session)
    #         self._db.commit()
    #         self._db.refresh(new_chat_session)

    #         user_message.session_id = new_chat_session.id
    #         agent_message.session_id = new_chat_session.id

    #         self._db.add(user_message)
    #         self._db.add(agent_message)
    #         self._db.commit()
    #         self._db.refresh(user_message)
    #         self._db.refresh(agent_message)

    #         logger.info(
    #             f"Chat session and messages inserted successfully for user {current_user.get('user_id')}"
    #         )

    #         return ChatSessionResponse(
    #             id=new_chat_session.id,
    #             user_id=new_chat_session.user_id,
    #             start_time=new_chat_session.start_time,
    #             end_time=new_chat_session.end_time,
    #             created_at=new_chat_session.created_at,
    #             updated_at=new_chat_session.updated_at,
    #             content=agent_message.content,
    #         )
    #     except SQLAlchemyError as db_error:
    #         self._db.rollback()
    #         logger.error(
    #             f"Database error during chat session creation: {str(db_error)}"
    #         )
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail=f"Database error during chat session creation.",
    #         )
    #     except Exception as e:
    #         self._db.rollback()
    #         logger.error(f"Unexpected error during chat session creation: {str(e)}")
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail="Unexpected error during chat session creation.",
    #         )
