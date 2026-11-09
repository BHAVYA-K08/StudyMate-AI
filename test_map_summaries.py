from src.summarizer import map_summaries

sample_chunks = [
    {
        "page": 1,
        "chunk": 1,
        "text": "Python is a high-level programming language."
    },
    {
        "page": 2,
        "chunk": 1,
        "text": "Python supports object-oriented programming."
    }
]

results = map_summaries(sample_chunks)


for result in results:
    print(f"\nPage: {result['page']}")
    print(f"Summary: {result['summary']}")


assert len(results) == 2
assert all(result["summary"].strip() for result in results)

print("\nMap stage test successful...!!!")