from src.summarizer import summarize_chunks

sample_chunks = [
    {
        "page": i + 1,
        "chunk": 1,
        "text": f"Important Python programming concept number {i + 1}. "
                "Python is used in software development and automation."
    }
    for i in range(12)
]

final_summary = summarize_chunks(sample_chunks)

print("\nFINAL STUDY NOTES\n")
print(final_summary)

assert  final_summary.strip()

print("\nComplete Summarization pipeline successful...!!!")