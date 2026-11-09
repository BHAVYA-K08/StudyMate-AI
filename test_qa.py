from src.qa import retrieve_context

results = retrieve_context(
    question = "Explain Newton's laws of motion."
)

for result in results:
    print(f"Page: {result.metadata['page']}")
    print(f"Content: {result.page_content[:300]}")
    print("-" * 50)

