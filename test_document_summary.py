from src.document_manager import list_documents
from src.vector_store import get_document_chunks

documents = list_documents()

for document in documents:
    chunks = get_document_chunks(document["document_id"])

    print(f"\nPDF: {document['filename']}")
    print(f"Total chunks retrieved: {len(chunks)}")

    if chunks:
        print(f"First chunk page: {chunks[0]['page']}")
        print(f"First chunk text: {chunks[0]['text'][:150]}")