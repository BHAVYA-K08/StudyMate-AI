
from langchain_chroma import Chroma
from src.embeddings import get_embedding_model


def get_vector_store(persist_directory="chroma_db"):
    """CREATE A CHROMADB VECTOR STORE FOR PDF CHUNKS."""

    embedding_model = get_embedding_model()

    vector_store = Chroma(
        embedding_function=embedding_model,
        collection_name="study_notes",
        persist_directory=str(persist_directory)
    )

    return vector_store


def add_documents(
    chunks,
    document_id,
    filename,
    user_id,
    persist_directory="chroma_db",
    file_hash=None
):
    """ADD PDF CHUNKS WITH USER OWNERSHIP METADATA."""

    if not chunks:
        raise ValueError("No chunks provided.")

    if not document_id:
        raise ValueError("Document ID is required.")

    if not user_id:
        raise ValueError("User ID is required.")

    vector_store = get_vector_store(persist_directory)

    texts = [chunk["text"] for chunk in chunks]

    metadatas = [
        {
            "user_id": str(user_id),
            "document_id": document_id,
            "filename": filename,
            "page": chunk["page"],
            "chunk": chunk["chunk"],
            "file_hash": file_hash or ""
        }
        for chunk in chunks
    ]

    ids = [
        f"{document_id}_page_{chunk['page']}_chunk_{chunk['chunk']}"
        for chunk in chunks
    ]

    vector_store.add_texts(
        texts=texts,
        metadatas=metadatas,
        ids=ids
    )

    return vector_store


def search_documents(
    query,
    user_id,
    document_id=None,
    k=4,
    persist_directory="chroma_db",
    max_distance=1.3
):
    """SEARCH ONLY DOCUMENTS BELONGING TO THE SPECIFIED USER."""

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if not user_id:
        raise ValueError("User ID is required.")

    vector_store = get_vector_store(persist_directory)

    user_filter = {
        "user_id": str(user_id)
    }

    if document_id:
        search_filter = {
            "$and": [
                user_filter,
                {"document_id": document_id}
            ]
        }
    else:
        search_filter = user_filter

    results = vector_store.similarity_search_with_score(
        query,
        k=k,
        filter=search_filter
    )

    relevant_docs = [
        doc
        for doc, score in results
        if score <= max_distance
    ]

    return relevant_docs


def get_document_chunks(
    document_id,
    user_id,
    persist_directory="chroma_db"
):
    """RETRIEVE CHUNKS ONLY IF THE DOCUMENT BELONGS TO THE USER."""

    if not document_id:
        raise ValueError("Document ID is required.")

    if not user_id:
        raise ValueError("User ID is required.")

    vector_store = get_vector_store(persist_directory)

    data = vector_store.get(
        where={
            "$and": [
                {"user_id": str(user_id)},
                {"document_id": document_id}
            ]
        },
        include=["documents", "metadatas"]
    )

    chunks = []

    for text, metadata in zip(
        data["documents"],
        data["metadatas"]
    ):
        chunks.append({
            "text": text,
            "page": metadata["page"],
            "chunk": metadata["chunk"]
        })

    chunks.sort(
        key=lambda item: (
            item["page"],
            item["chunk"]
        )
    )

    return chunks
