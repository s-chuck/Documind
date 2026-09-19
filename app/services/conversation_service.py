from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.message import Message


def get_user_conversation(
    db: Session,
    conversation_id: int,
    user_id: int,
) -> Conversation | None:
    return (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        .first()
    )


def add_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str,
) -> Message:
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        created_at=datetime.now(timezone.utc),
    )

    db.add(message)

    return message


def get_conversation_messages(
    db: Session,
    conversation_id: int,
) -> list[Message]:
    return (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(Message.created_at.asc())
        .all()
    )