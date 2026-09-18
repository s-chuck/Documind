def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[str]:

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        # Normal paragraph fits in current chunk
        if len(current_chunk) + len(paragraph) <= chunk_size:
            current_chunk += paragraph + "\n\n"
            continue

        # Save current chunk
        if current_chunk:
            chunks.append(current_chunk.strip())

        # If one paragraph itself is too large,
        # split it by words.
        if len(paragraph) > chunk_size:
            words = paragraph.split()
            current_chunk = ""

            for word in words:
                candidate = (
                    f"{current_chunk} {word}"
                    if current_chunk
                    else word
                )

                if len(candidate) <= chunk_size:
                    current_chunk = candidate
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())

                    current_chunk = word
        else:
            current_chunk = paragraph + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


#1. Normal character chunking
# def simple_chunker(text: str, chunks_size: int = 100) -> list[str]:
#     #spliting text into byte size characters
#     chunks = []
#     for i in range(0,len(text), chunks_size):
#         chunk = text[i:i + chunks_size]
#         chunks.append(chunk)
#2. Iteration split by words
# def chunk_by_words(text: str, chunk_size=5) -> list[str]:
#     chunks = []
#     words = text.split()
#     for i in range(0, len(text), chunk_size):
#         chunk = " ".join(words[i:i+chunk_size])
#         chunks.append(chunk)
#     return chunks

# text = """The quick brown fox jumps over the lazy dog. 
# Python is a powerful programming language. 
# It is widely used in data science and web development."""

# chunks = chunk_by_words(text)
# for i, chunk in enumerate(chunks, 1):
#     print(f"Chunk {i}: '{chunk}'")
#3 Problem: what if a word is 500 characters long so it won't be idle to put in all in one word
#another problem is context can be changed of the new chunk if we don't provide previous context our model can think otherwise
# def chunk_with_overlap(text:str, chunk_size:int=5, overlap:int=2) -> list[str]:
#     if overlap >= chunk_size:
#         raise ValueError("overlap must be smaller than chunk_size")
#     words = text.split()

#     chunks = []

#     step = chunk_size - overlap

#     for i in range(0, len(words), step):
#         chunk = " ".join(words[i:i + chunk_size])
#         chunks.append(chunk)

#     return chunks
# text = """The quick brown fox jumps over the lazy dog. 
# Python is a powerful programming language. 
# It is widely used in data science and web development."""

# chunks = chunk_with_overlap(text)
# for i, chunk in enumerate(chunks, 1):
#     print(f"Chunk {i}: '{chunk}'")
# list_comprehension = the elements in new list are expressions who satisfies if condn.[expresssion for item in items if condn]
# paragraph = [p.strip() for p in text.split("\n\n") if p.strip()]
