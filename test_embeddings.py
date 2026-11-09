from src.embeddings import get_embedding_model

embeddings = get_embedding_model()

text = "Python is a programming language."
vector = embeddings.embed_query(text)

print(f"Embeddings Dimension: {len(vector)}")
print(f"First 10 values:{vector[:10]}")

print("Embedding Test Successful...!!!!")