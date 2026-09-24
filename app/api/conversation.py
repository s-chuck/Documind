from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.user import User
from app.schema.conversation import (
    ConversationCreate,
    ConversationResponse,
    MessageResponse,
)
from app.services.conversation_service import (
    get_user_conversation,
    get_conversation_messages,
)


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post(
    "/",
    response_model=ConversationResponse,
)
def create_conversation(
    data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    now = datetime.now(timezone.utc)

    conversation = Conversation(
        user_id=current_user.id,
        title=data.title,
        created_at=now,
        updated_at=now,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


@router.get(
    "/",
    response_model=list[ConversationResponse],
)
def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversations = (
        db.query(Conversation)
        .filter(
            Conversation.user_id == current_user.id
        )
        .order_by(
            Conversation.updated_at.desc()
        )
        .all()
    )

    return conversations


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id,
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return conversation


@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
def get_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = get_user_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return get_conversation_messages(
        db=db,
        conversation_id=conversation_id,
    )


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id,
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    # Delete messages belonging to this conversation first.
    db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).delete(
        synchronize_session=False
    )

    # Then delete the conversation itself.
    db.delete(conversation)

    db.commit()

    return None

@router.patch(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def rename_conversation(
    conversation_id: int,
    data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id,
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    title = data.title.strip()

    if not title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Conversation title cannot be empty",
        )

    conversation.title = title
    conversation.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(conversation)

    return conversation