from sqlalchemy.orm import Mapped, mapped_column,relationship
from datetime import datetime
from sqlalchemy import DateTime, String
from app.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.conversation import Conversation

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.now())

    documents: Mapped[list["Document"]] = relationship(back_populates="user")
    conversations: Mapped[list["Conversation"]] = relationship(
    back_populates="user",
    cascade="all, delete-orphan",
)