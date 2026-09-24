from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

reranker = CrossEncoder(MODEL_NAME)


def rerank_chunks(
    question: str,
    chunks: list[str],
    top_k: int = 3,
) -> list[tuple[str, float]]:
    """
    Rerank retrieved chunks based on their relevance to the question.

    Returns:
        List of (chunk_text, score) sorted from most relevant
        to least relevant.
    """

    pairs = [
        (question, chunk)
        for chunk in chunks
    ]

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(chunks, scores),
        key=lambda item: float(item[1]),
        reverse=True,
    )

    return [
        (chunk, float(score))
        for chunk, score in ranked[:top_k]
    ]