# AI Study Notes Assistant

## Problem statement
Students often need to read lengthy PDFs, find specific concepts, and prepare revision notes. Doing this manually can be time-consuming.

## Objective
Build an AI-powered application that accepts PDF study material, answers questions based on the uploaded documents, and generates summaries of short and long PDFs.

## Target users
Students, learners, and people who need to understand lengthy documents.

## Core features
1. PDF upload and validation.
2. PDF text extraction with page tracking.
3. Text chunking and local embeddings.
4. Vector storage and semantic retrieval.
5. Question-answering using RAG.
6. Short-document summarization.
7. Hierarchical summarization for long documents.
8. Source references for answers.
9. Error handling and a user-friendly Streamlit interface.

## Technology stack
Python, Streamlit, PyMuPDF, LangChain, Sentence Transformers, ChromaDB, Groq API, Git, and pytest.

## Constraints
- The first version processes text-based PDFs.
- Scanned PDFs may require OCR, which can be added later.
- Large PDFs must be processed in batches rather than sent to the LLM in one request.
- Answers should be grounded in the uploaded documents.
- API keys must not be exposed in source code or GitHub.