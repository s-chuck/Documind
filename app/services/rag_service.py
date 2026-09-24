from sqlalchemy.orm import Session

from app.services.search_service import search_similar_chunks
from app.services.reranker_service import rerank_chunks
from app.services.llm_service import generate_answer


def answer_question(
    db: Session,
    user_id: int,
    question: str,
    document_id: int,
    limit: int = 10,
) -> dict:

    # ---------------------------------------------------------
    # 1. Retrieve candidate chunks using vector search
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # 2. Prepare chunks for reranking
    # ---------------------------------------------------------

    chunks_for_reranking = [
        chunk.content
        for chunk, document_name, distance in results
    ]

    # ---------------------------------------------------------
    # 3. Rerank the candidates
    # ---------------------------------------------------------

    reranked = rerank_chunks(
        question=question,
        chunks=chunks_for_reranking,
        top_k=3,
    )

    print("\n===== RERANK DEBUG =====")

    for rank, (chunk_content, score) in enumerate(
        reranked,
        start=1,
    ):
        print(
            "RANK:",
            rank,
            "| SCORE:",
            score,
            "| CHUNK:",
            chunk_content[:150].replace("\n", " "),
        )

    print("===== END RERANK DEBUG =====\n")

    # ---------------------------------------------------------
    # 4. Build context using only reranked chunks
    # ---------------------------------------------------------

    context_parts = []
    sources = []

    for chunk_content, rerank_score in reranked:

        # Find the original result corresponding to this chunk.
        for chunk, document_name, distance in results:

            if chunk.content == chunk_content:

                context_parts.append(chunk.content)

                sources.append({
                    "document_id": chunk.document_id,
                    "document_name": document_name,
                    "chunk_id": chunk.id,
                    "chunk_index": chunk.chunk_index,
                    "distance": float(distance),
                    "rerank_score": rerank_score,
                })

                break

    # ---------------------------------------------------------
    # 5. Send only reranked context to the LLM
    # ---------------------------------------------------------

    context = "\n\n---\n\n".join(context_parts)

    answer = generate_answer(
        question=question,
        context=context,
    )

    return {
        "answer": answer,
        "sources": sources,
    }