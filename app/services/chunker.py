def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[str]:

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        # If adding this paragraph still fits,
        # keep it in the current chunk.
        if len(current_chunk) + len(paragraph) <= chunk_size:
            current_chunk += paragraph + "\n\n"
            continue

        # Save the current chunk
        if current_chunk:
            chunks.append(current_chunk.strip())

        # Create overlap using complete words
        words = current_chunk.strip().split()

        overlap_words = []
        overlap_length = 0
        #reversing the current_chunk bcs overlap ka kaam hi yehi ki old last info ko new chunk mai add krdo.
        for word in reversed(words):
            if overlap_length + len(word) + 1 > overlap:
                break

            overlap_words.insert(0, word)
            overlap_length += len(word) + 1

        overlap_text = " ".join(overlap_words)

        if overlap_text:
            current_chunk = overlap_text + "\n\n" + paragraph + "\n\n"
        else:
            current_chunk = paragraph + "\n\n"

    # Add final chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    print("\n" + "=" * 80)
    print("\n" + "=" * 80)
    print("CHUNKS")
    print("=" * 80)

    for i, chunk in enumerate(chunks):
        print(f"\n--- CHUNK {i} ---")
        print("Characters:", len(chunk))
        print(chunk)
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
