import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, Dict, List
from application.services.user import get_user_payload
from utilities.dict import get_user_id_from_dict
from domain.services.chat_session_service import ChatSessionService
from infrastructure.cache.connection import get_redis_connection
from infrastructure.cache.redis.redis_repository import RedisRepository
from db.connection import get_db_connection
from schemas.v1.chat_session import ChatSessionResponse

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/", response_model=List[ChatSessionResponse])
async def get_chat_history(
    current_user: Dict[str, Any] = Depends(get_user_payload),
    db: Session = Depends(get_db_connection),
):
    """
    指定されたユーザーのチャットセッション履歴を取得します。

    Args:
        current_user (Dict[str, Any]): アクセストークンから取得したユーザーペイロード
        db (Session): データベースセッション
        redis (Redis): Redisクライアント

    Returns:
        List[ChatSessionResponse]: チャットセッションのリスト

    Raises:
        HTTPException: データ取得中にエラーが発生した場合
    """
    chat_session_service = ChatSessionService(db)
    user_id = get_user_id_from_dict(current_user)
    return await chat_session_service.get_chat_history(user_id)


# @router.post(
#     "/", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED
# )
# async def create_chat_session(
#     chat_session_request: ChatSessionCreateRequest,
#     current_user: Dict[str, Any] = Depends(get_user_payload),
#     db: Session = Depends(get_db_connection),
# ):
#     """
#     チャットトップページで、初めてのプロンプトを送信した際に叩かれるAPIです。
#     ユーザーからのプロンプトを受け取り、Agentの回答を生成し、両方をデータベースに保存します。
#     新しいセッションが作成され、プロンプトとレスポンスが保存された状態で返されます。
#     Agentのレスポンスに含まれるsummaryもセッションに保存されます。

#     Args:
#         chat_session_request (ChatSessionCreateRequest): ユーザーからの質問
#         current_user (Dict[str, Any]): 現在ログインしているユーザーの情報
#         db (Session): データベースセッション

#     Returns:
#         ChatSessionResponse: 作成されたチャットセッションの情報

#     Raises:
#         HTTPException: セッション作成中にエラーが発生した場合
#     """
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
#                 detail=f"Request error while contacting agent API: {str(e)}",
#             )

#     agent_response_data = response.json()
#     agent_response = agent_response_data.get("response")
#     agent_summary = agent_response_data.get("summary")

#     logger.info(f"agent_response: {agent_response}\n agent_summary: {agent_summary}\n")

#     if not agent_response or not agent_summary:
#         logger.error("Invalid response from agent API, missing response or summary.")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Invalid response from agent API, missing response or summary.",
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

#         db.add(new_chat_session)
#         db.commit()
#         db.refresh(new_chat_session)

#         user_message.session_id = new_chat_session.id
#         agent_message.session_id = new_chat_session.id

#         db.add(user_message)
#         db.add(agent_message)
#         db.commit()
#         db.refresh(user_message)
#         db.refresh(agent_message)

#         logger.info(
#             f"Chat session and messages inserted successfully for user {current_user.get('user_id')}"
#         )

#         response = ChatSessionResponse(
#             id=new_chat_session.id,
#             user_id=new_chat_session.user_id,
#             start_time=new_chat_session.start_time,
#             end_time=new_chat_session.end_time,
#             created_at=new_chat_session.created_at,
#             updated_at=new_chat_session.updated_at,
#             content=agent_message.content,
#         )
#         return new_chat_session
#     except SQLAlchemyError as db_error:
#         db.rollback()
#         logger.error(f"Database error during chat session creation: {str(db_error)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Database error during chat session creation: {str(db_error)}",
#         )
#     except Exception as e:
#         db.rollback()
#         logger.error(f"Unexpected error during chat session creation: {str(e)}")
#         # FIXME: ここのエラーは統一させたいので関数化させる
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Unexpected error during chat session creation: {str(e)}",
#         )


# @router.delete(
#     "/{session_id}",
#     response_model=ChatSessionDeleteResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def delete_chat_session(
#     session_id: int,
#     current_user: Dict[str, Any] = Depends(get_user_payload),
#     db: Session = Depends(get_db_connection),
# ):
#     """
#     指定されたチャットセッションと、そのセッションに関連するメッセージを削除します。

#     Args:
#         session_id (int): 削除対象のセッションID
#         current_user (Dict[str, Any]): アクセストークンから取得したユーザーペイロード
#         db (Session): データベースセッション

#     Returns:
#         ChatSessionDeleteResponse: 削除成功のメッセージを含むレスポンス

#     Raises:
#         HTTPException: セッションが見つからない、もしくは削除中にエラーが発生した場合
#     """
#     try:
#         chat_session = (
#             db.query(ChatSession).filter(ChatSession.id == session_id).first()
#         )
#         if chat_session is None:
#             logger.warning(f"Attempted to delete non-existent session {session_id}")
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Attempted to delete non-existent session {session_id}",
#             )

#         messages = db.query(Message).filter(Message.session_id == session_id).all()
#         for message in messages:
#             db.delete(message)

#         db.delete(chat_session)
#         db.commit()

#         logger.info(
#             f"Chat session {session_id} and related messages deleted successfully"
#         )

#         # TODO: Redisからも対象のセッションを削除する処理を追加

#         return ChatSessionDeleteResponse(message="Delete Successfully")

#     except SQLAlchemyError as db_error:
#         db.rollback()
#         logger.error(
#             f"Database error during deletion of session {session_id}: {str(db_error)}"
#         )
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Database error during deletion of session {session_id}: {str(db_error)}",
#         )

#     except Exception as e:
#         db.rollback()
#         logger.error(
#             f"Unexpected error during deletion of session {session_id}: {str(e)}"
#         )
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Unexpected error during deletion of session {session_id}: {str(e)}",
#         )


# @router.put("/{session_id}", response_model=ChatSessionResponse)
# async def update_chat_session(
#     session_id: int,
#     chat_session_update: ChatSessionUpdateRequest,
#     current_user: Dict[str, Any] = Depends(get_user_payload),
#     db: Session = Depends(get_db_connection),
# ):
#     """
#     指定されたチャットセッションを更新します。

#     Args:
#         session_id (int): 更新対象のセッションID
#         chat_session_update (ChatSessionUpdateRequest): 更新する内容
#         current_user (Dict[str, Any]): アクセストークンから取得したユーザーペイロード
#         db (Session): データベースセッション

#     Returns:
#         ChatSessionResponse: 更新されたセッションの詳細情報

#     Raises:
#         HTTPException: セッションが見つからない、もしくは更新中にエラーが発生した場合
#     """
#     chat_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
#     if chat_session is None:
#         logger.warning(f"Attempted to update non-existent session {session_id}")
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Attempted to update non-existent session {session_id}",
#         )
#     try:
#         chat_session.summary = chat_session_update.summary
#         chat_session.updated_at = datetime.utcnow()
#         db.commit()
#         db.refresh(chat_session)

#         logger.info(f"Chat session {session_id} updated successfully")

#         # TODO: redisの値も更新
#         return chat_session
#     except SQLAlchemyError as db_error:
#         db.rollback()
#         logger.error(
#             f"Database error during update of session {session_id}: {str(db_error)}"
#         )
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Database error during update of session {session_id}: {str(db_error)}",
#         )

#     except Exception as e:
#         db.rollback()
#         logger.error(
#             f"Unexpected error during update of session {session_id}: {str(e)}"
#         )
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Unexpected error during update of session {session_id}: {str(e)}",
#         )
