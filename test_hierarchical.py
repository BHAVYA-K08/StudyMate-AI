from src.summarizer import hierarchical_reduce_summaries

sample_summaries = [
    {
        "page": i + 1,
        "chunk": 1,
        "summary": f"Important concept number {i + 1} in Python programming."
    }
    for i in range(20)
]
final_summary = hierarchical_reduce_summaries(
    sample_summaries,
    batch_size = 5
)

print("\n Hierarchical Summary:\n")
print(final_summary)

assert final_summary.strip()

print("\nHierarchical summarization test successful...!!!")