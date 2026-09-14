from app.services.embedding_service import generate_embedding


text = "PostgreSQL uses MVCC for concurrent transactions."

vector = generate_embedding(text)

print("Dimensions:", len(vector))
print(vector)