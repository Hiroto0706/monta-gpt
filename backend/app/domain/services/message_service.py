import logging
from typing import List

from fastapi import HTTPException, status

from application.usecase.message_usecase import MessageUseCase
from schemas.v1.message import MessageResponse


logger = logging.getLogger(__name__)


class MessageService(MessageUseCase):

    async def get_messages_by_session_id(self, session_id: int) -> List[MessageResponse]:
        """
        指定された `chat_session_id` に基づいてメッセージのリストを取得します。

        Args:
            chat_session_id (int): メッセージを取得するスレッドのID

        Returns:
            List[MessageResponse]: 指定されたスレッドに含まれるメッセージのリスト

        Raises:
            HTTPException: スレッドIDに関連するメッセージが見つからない場合
        """
        try:
            messages = self.message_repository.get_messages_by_session_id(session_id)
            if messages is None:
                return []
            return messages
        except Exception as e:
            logger.error(
                f"Error getting messages for session_id {session_id}: {str(e)}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving messages.",
            )
