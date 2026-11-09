from src.document_manager import generate_document_id
from src.document_manager import process_and_store_pdf
from src.vector_store import search_documents, get_vector_store
from src.document_manager import list_documents, delete_document, calculate_file_hash, process_and_store_pdf, find_duplicate_document
# result = process_and_store_pdf(
#     pdf_path = r"D:\AI-STUDY-NOTES-ASSISTANT\data\uploads\Physics Handbook_Allen.pdf",
#     filename = "physics_handbook.pdf"
# )

# print("\nPDF PROCESSING RESULT:")
# print(result)

# results = search_documents(
#     query = "What is newton's first law of motion?",
#     document_id = result['document_id'],
#     k = 4
# )
# print(f"\nRetrieved chunks: {len(results)}")


# for doc in results:
#     print("Page:", doc.metadata["page"])
#     print("Content:", doc.page_content[:200])
#     print("-" * 40)

# vectore_store = get_vector_store()

# data = vectore_store.get(
#     include = ["metadatas"]
# )

# print(data["metadatas"][:5])

# print("\n ALL UPLOADED DOCUMENTS: ")

# documents = list_documents()

# for doc in documents:
#     print(doc)

# documents_before = list_documents()

# print("\nDOCUMENTS BEFORE DELETION:")
# for doc in documents_before:
#     print(doc)


# document_id = "7a28cba2-43eb-4aa0-92e8-98224fb7569a"

# delete_document(document_id)
# documents_after = list_documents()

# print("\nDOCUMENTS AFTER DELETION:")
# for doc in documents_before:
#     print(doc)
from src.document_manager import delete_document

delete_document("3e3170f4-d402-416b-b16b-f61759d347bd")

print("Invalid test document deleted.")