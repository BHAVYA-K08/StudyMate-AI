from src.qa import retrieve_context

questions = [
    "What is inertia?",
    "Explain Newton's laws of motion.",
    "What is the capital of India?"
]

for question in questions:

    print(f"\nQuestion: {question}")

    results = retrieve_context(
        question = question,
        document_id = "physics_handbook", 
        k = 10
    )

    if not results:
        print("No relevant PDF content found.")
        continue

    for doc in results:
        print(f"Page : {doc.metadata.get('page')}")
        print(f"Content : {doc.page_content}")
        print("-" * 40)