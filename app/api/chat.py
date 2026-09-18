from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schema.document import QuestionRequest
from app.services.rag_service import answer_question



router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/")
def chat(
    data: QuestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return answer_question(
        db=db,
        user_id=current_user.id,
        question=data.question,
        limit=data.limit,
    )