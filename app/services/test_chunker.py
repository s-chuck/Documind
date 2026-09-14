from app.services.chunker import chunk_text


text = """
PostgreSQL uses MVCC to handle concurrent transactions.

Readers can continue reading while writers modify rows.

Each transaction gets a snapshot of the database.
"""

chunks = chunk_text(text, chunk_size=100, overlap=20)

for index, chunk in enumerate(chunks):
    print(f"\n--- Chunk {index} ---")
    print(chunk)