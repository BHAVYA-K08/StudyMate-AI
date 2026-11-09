from src.summarizer import summarize_text

sample_text = """
Python is a high-level, interpreted programming language.
It supports object-oriented, procedural, and functional programming.
Python is widely used in web development, data science, artificial  intelligence
and automation.
"""

summary = summarize_text(sample_text)

print("\n Generated Summary:\n")
print(summary)

assert summary.strip()
print("\nSummarizer test successful...!!!")