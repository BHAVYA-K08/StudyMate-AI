from src.reranker import get_reranker

model = get_reranker()

question = "Explain Newton's laws of motion."

documents = [
    "Newton's law of gravitation describes the gravitational force between two masses.",
    "Newton's first law states that an object remains at rest or in uniform motion unless acted upon by an external force.",
    "Newton's second law states that force is equal to mass multiplied by acceleration.",
    "The capital of India is New Delhi."
]

pairs = [[question, document] for document in documents]

scores = model.predict(pairs)

for document, score in zip(documents, scores):
    print(f"\n Score: {score:.4f}")
    print(f"Document: {document}")

