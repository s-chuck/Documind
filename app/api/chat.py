from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schema.document import QuestionRequest
from app.services.conversation_service import (
    get_user_conversation,
    add_message,
)
from app.services.rag_service import answer_question
from datetime import datetime, timezone


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


# @router.post("/")
# def chat(
#     data: QuestionRequest,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     return answer_question(
#         db=db,
#         user_id=current_user.id,
#         question=data.question,
#         limit=data.limit,
#     )

@router.post("/")
def chat(
    data: QuestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = get_user_conversation(
        db=db,
        conversation_id=data.conversation_id,
        user_id=current_user.id,
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    # Save user's message
    user_message = add_message(
        db=db,
        conversation_id=conversation.id,
        role="user",
        content=data.question,
    )

    db.commit()
    db.refresh(user_message)

    # Generate answer using RAG
    result = answer_question(
        db=db,
        user_id=current_user.id,
        question=data.question,
        document_id=data.document_id,
        limit=data.limit,
    )

    # Save assistant's message
    assistant_message = add_message(
        db=db,
        conversation_id=conversation.id,
        role="assistant",
        content=result["answer"],
    )

    conversation.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(assistant_message)

    return result