from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.services.chunker import chunk_text
from app.services.embedding_service import generate_embeddings


def save_chunks(
    db: Session,
    document_id: int,
    text: str,
) -> list[DocumentChunk]:

    chunks = chunk_text(text)

    if not chunks:
        raise ValueError("No chunks were generated")

    embeddings = generate_embeddings(chunks)

    document_chunks = []

    for index, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        document_chunk = DocumentChunk(
            document_id=document_id,
            chunk_index=index,
            content=chunk,
            embedding=embedding,
        )

        db.add(document_chunk)
        document_chunks.append(document_chunk)

    return document_chunks