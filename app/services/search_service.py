from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.models.document import Document
from app.services.embedding_service import generate_embeddings


def search_similar_chunks(
    db: Session,
    user_id: int,
    query: str,
    document_id: int | None = None,
    limit: int = 5,
):
    query_embedding = generate_embeddings([query])[0]

    distance = DocumentChunk.embedding.cosine_distance(
        query_embedding
    ).label("distance")

    statement = (
        select(DocumentChunk, distance)
        .join(Document,Document.id == DocumentChunk.document_id,)
        .where(Document.user_id == user_id)
    )

    if document_id is not None:
        statement = statement.where(
            DocumentChunk.document_id == document_id
        )

    statement = (
        statement
        .order_by(distance)
        .limit(limit)
    )

    return db.execute(statement).all()