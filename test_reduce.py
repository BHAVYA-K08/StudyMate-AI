from src.summarizer import reduce_summaries

sample_summaries = sample_summaries = [
    {
        "page": 1,
        "chunk": 1,
        "summary": "Python is a high-level programming language."
    },
    {
        "page": 2,
        "chunk": 1,
        "summary": "Python supports object-oriented programming."
    },
    {
        "page": 3,
        "chunk": 1,
        "summary": "Python is used in AI, web development and automation."
    }
]

final_summary = reduce_summaries(sample_summaries)

print("\nFinal Study Notes:\n")
print(final_summary)

assert final_summary.strip()

print("\nReduce stage test successful...!!!")