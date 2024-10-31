import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Any, Dict, List
from datetime import datetime, timedelta
from services.users import get_user_payload
from db.models.message import Message
from db.connection import get_db_connection
from db.models.chat_session import ChatSession
from schemas.chat_session import (
    ChatSessionCreateRequest,
    ChatSessionDeleteResponse,
    ChatSessionUpdate,
    ChatSessionResponse,
)
import utilities.config as config

router = APIRouter(prefix="/chat_sessions", tags=["chat_sessions"])


# TODO: user_idごとにchat_sessionsを取得するように修正
@router.get("/", response_model=List[ChatSessionResponse])
async def get_chat_history(
    current_user: Dict[str, Any] = Depends(get_user_payload),
    db: Session = Depends(get_db_connection),
):
    """
    指定されたユーザーのチャットセッション履歴を取得します。

    Args:
        user_id (int): ユーザーのID
        db (Session): データベースセッション

    Returns:
        List[ChatSessionResponse]: チャットセッションのリスト

    Raises:
        HTTPException: データ取得中にエラーが発生した場合
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token payload",
        )
    try:
        # TODO: DBから取得する前にredisから取得する処理を書く
        chat_sessions = (
            db.query(ChatSession)
            .filter(ChatSession.user_id == user_id)
            .order_by(ChatSession.id.desc())
            .all()
        )
        if not chat_sessions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No chat sessions found for user with ID {current_user.user_id}",
            )
    except SQLAlchemyError as db_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(db_error)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return chat_sessions


# TODO: userからのプロンプトもformDataから受け取る必要あり
@router.post(
    "/", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED
)
async def create_chat_session(
    chat_session_request: ChatSessionCreateRequest,
    current_user: Dict[str, Any] = Depends(get_user_payload),
    db: Session = Depends(get_db_connection),
):
    """
    チャットトップページで、初めてのプロンプトを送信した際に叩かれるAPIです。
    ユーザーからのプロンプトを受け取り、Agentの回答を生成し、両方をデータベースに保存します。
    新しいセッションが作成され、プロンプトとレスポンスが保存された状態で返されます。
    Agentのレスポンスに含まれるsummaryもセッションに保存されます。

    Args:
        prompt (str): ユーザーが送信した最初の質問
        user_id (int): ユーザーのID
        db (Session): データベースセッション

    Returns:
        ChatSessionResponse: 作成されたチャットセッションの情報

    Raises:
        HTTPException: セッション作成中にエラーが発生した場合
    """
    print("叩かれてるのこっちですよね")
    user_message = Message(
        session_id=None,
        content=chat_session_request.prompt,
        is_user=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, connect=10.0)) as client:
        try:
            response = await client.post(
                f"{config.AGENT_URL}api/agent/",
                json={"prompt": chat_session_request.prompt},
            )
            response.raise_for_status()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    agent_response_data = response.json()
    agent_response = agent_response_data.get("response")
    agent_summary = agent_response_data.get("summary")
    if not agent_response or not agent_summary:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid response from agent API",
        )

    try:
        agent_message = Message(
            session_id=None,
            content=agent_response,
            is_user=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        new_chat_session = ChatSession(
            user_id=current_user.get("user_id"),
            summary=agent_summary,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow()
            + timedelta(days=int(config.DEFAULT_SESSION_EXPIRATION_DAY)),
        )

        db.add(new_chat_session)
        db.commit()
        db.refresh(new_chat_session)

        user_message.session_id = new_chat_session.id
        agent_message.session_id = new_chat_session.id

        db.add(user_message)
        db.add(agent_message)
        db.commit()
        db.refresh(user_message)
        db.refresh(agent_message)

        response = ChatSessionResponse(
            id=new_chat_session.id,
            user_id=new_chat_session.user_id,
            start_time=new_chat_session.start_time,
            end_time=new_chat_session.end_time,
            created_at=new_chat_session.created_at,
            updated_at=new_chat_session.updated_at,
            content=agent_message.content,
        )
        return new_chat_session
    except SQLAlchemyError as db_error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(db_error)}",
        )
    except Exception as e:
        db.rollback()
        # FIXME: ここのエラーは統一させたいので関数化させる
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )

    # TODO: redisに追加したセッションを追加する処理


@router.delete(
    "/{session_id}",
    response_model=ChatSessionDeleteResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_chat_session(
    session_id: int, db: Session = Depends(get_db_connection)
):
    """
    指定されたチャットセッションと、そのセッションに関連するメッセージを削除します。

    Args:
        session_id (int): 削除対象のセッションID
        db (Session): データベースセッション

    Returns:
        ChatSessionDeleteResponse: 削除成功のメッセージを含むレスポンス

    Raises:
        HTTPException: セッションが見つからない、もしくは削除中にエラーが発生した場合
    """
    try:
        chat_session = (
            db.query(ChatSession).filter(ChatSession.id == session_id).first()
        )
        if chat_session is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found"
            )

        messages = db.query(Message).filter(Message.session_id == session_id).all()
        for message in messages:
            db.delete(message)

        db.delete(chat_session)
        db.commit()

        # TODO: Redisからも対象のセッションを削除する処理を追加

        return {"message": "Delete successfully"}

    except SQLAlchemyError as db_error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(db_error)}",
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@router.put("/{session_id}", response_model=ChatSessionResponse)
async def update_chat_session(
    session_id: int,
    chat_session_update: ChatSessionUpdate,
    db: Session = Depends(get_db_connection),
):
    """
    指定されたチャットセッションを更新します。

    Args:
        session_id (int): 更新対象のセッションID
        chat_session_update (ChatSessionUpdate): 更新する内容
        db (Session): データベースセッション

    Returns:
        ChatSessionResponse: 更新されたセッションの詳細情報

    Raises:
        HTTPException: セッションが見つからない、もしくは更新中にエラーが発生した場合
    """
    chat_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if chat_session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found"
        )
    try:
        chat_session.summary = chat_session_update.summary
        chat_session.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(chat_session)

        # TODO: redisの値も更新
        return chat_session
    except SQLAlchemyError as db_error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(db_error)}",
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )
