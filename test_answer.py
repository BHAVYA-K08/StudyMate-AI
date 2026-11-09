from src.qa import retrieve_context, generate_answer

# ASK A QUESTION

question = "What is Torque? Give an example."

# RETRIEVE RELEVANT CHUNKS FROM CHROMADB

retrieved_docs = retrieve_context(
    question = question,
    document_id = "physics_handbook",
    k = 4
)

print(f"\n Retrieved Documents: {len(retrieved_docs)}")

# GENERATE  AN ANSWER  USING GROQ

answer = generate_answer(
    question = question,
    retrieved_docs = retrieved_docs
)

print("ANSWER: ")
print("-" * 50)
print(answer)
print("-" * 50)

