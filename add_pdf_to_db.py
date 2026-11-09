from pathlib import Path

from src.pdf_processor import extract_pdf_text, chunk_pdf_text
from src.vector_store import add_documents

# 1. Locate the PDF
pdf_path = Path(r"D:\AI-STUDY-NOTES-ASSISTANT\data\uploads\Physics Handbook_Allen.pdf")

# 2. Extract text from the PDF
pages = extract_pdf_text(pdf_path)
print("Pages extracted:", len(pages))

# 3. Split the extracted text into chunks
chunks = chunk_pdf_text(pages)
print("Chunks created:", len(chunks))

# 4. Add the chunks to ChromaDB
vector_store = add_documents(
    chunks=chunks,
    document_id="physics_handbook",
    filename=pdf_path.name
)

print("PDF successfully added to ChromaDB!")