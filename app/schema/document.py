from pydantic import BaseModel

class DocumentCreate(BaseModel):
    name: str

class DocumentResponse(BaseModel):
    id: int
    name: str
    status: str


class DocumentListResponse(BaseModel):
    items: list[DocumentResponse]
    page: int
    limit: int
    total: int

class DocumentStatusUpdate(BaseModel):
    status: str


class DocumentSearchRequest(BaseModel):
    query: str
    document_id: int | None = None
    limit: int = 5

class QuestionRequest(BaseModel):
    question: str
    conversation_id: int
    document_id: int | None = None
    limit: int = 3

