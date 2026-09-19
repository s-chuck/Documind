from sqlalchemy.orm import Session

from app.services.search_service import search_similar_chunks
from app.services.llm_service import generate_answer


def answer_question(
    db: Session,
    user_id: int,
    question: str,
    document_id: int,
    limit: int = 3,
) -> dict:

    results = search_similar_chunks(
        db=db,
        user_id=user_id,
        query=question,
        document_id=document_id,
        limit=limit,
    )

    if not results:
        return {
            "answer": "I couldn't find relevant information in your documents.",
            "sources": [],
        }

    context_parts = []
    sources = []

    for chunk, distance in results:

        context_parts.append(chunk.content)

        sources.append({
            "document_id": chunk.document_id,
            "chunk_id": chunk.id,
            "chunk_index": chunk.chunk_index,
            "distance": float(distance),
        })

    context = "\n\n---\n\n".join(context_parts)

    answer = generate_answer(
        question=question,
        context=context,
    )

    return {
        "answer": answer,
        "sources": sources,
    }