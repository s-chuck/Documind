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
    print("🔥 SEARCH SERVICE CALLED", flush=True)
    print("LIMIT RECEIVED:", limit, flush=True)

    print("\n===== SEARCH DEBUG =====")
    print("USER ID:", user_id)
    print("DOCUMENT ID:", document_id)
    print("QUERY:", query)

    query_embedding = generate_embeddings([query])[0]

    distance = DocumentChunk.embedding.cosine_distance(
        query_embedding
    ).label("distance")

    statement = (
        select(DocumentChunk, Document.name, distance)
        .join(
            Document,
            Document.id == DocumentChunk.document_id,
        )
        .where(Document.user_id == user_id)
    )

    if document_id is not None:
        statement = statement.where(
            DocumentChunk.document_id == document_id
        )
    all_chunks = db.execute(
        select(DocumentChunk.id, DocumentChunk.document_id)
        .join(
            Document,
            Document.id == DocumentChunk.document_id,
        )
        .where(Document.user_id == user_id)
    ).all()

    print("===== USER DOCUMENT CHUNKS =====")
    print(all_chunks)
    print("===== END USER DOCUMENT CHUNKS =====")
    statement = (
        statement
        .order_by(distance)
        .limit(limit)
    )

    results = db.execute(statement).all()

    print("RESULT COUNT:", len(results))

    for chunk, document_name, distance_value in results:
        print(
            "DOCUMENT:",
            document_name,
            "| CHUNK:",
            chunk.id,
            "| DISTANCE:",
            float(distance_value),
        )

    print("===== END SEARCH DEBUG =====\n")

    return results