
import uuid
import hashlib
import shutil

from pathlib import Path

from src.pdf_processor import extract_pdf_text, chunk_pdf_text
from src.vector_store import add_documents, get_vector_store


UPLOAD_DIR = Path("data/uploads")


def generate_document_id():
    """GENERATE A UNIQUE ID FOR EACH UPLOADED PDF."""

    return str(uuid.uuid4())


def process_and_store_pdf(pdf_path, filename, user_id):
    """PROCESS AND STORE A PDF FOR A SPECIFIC USER."""

    if not user_id:
        raise ValueError("User ID is required.")

    user_id = str(user_id)

    source_path = Path(pdf_path)

    if not source_path.exists():
        raise FileNotFoundError("Uploaded PDF file not found.")

    file_hash = calculate_file_hash(source_path)

    existing_document = find_duplicate_document(
        file_hash,
        user_id
    )

    if existing_document:
        return {
            "duplicate": True,
            "document_id": existing_document["document_id"],
            "filename": existing_document["filename"]
        }

    document_id = generate_document_id()

    safe_filename = Path(filename).name

    # CREATE A SEPARATE FOLDER FOR THIS USER AND DOCUMENT

    document_dir = UPLOAD_DIR / user_id / document_id

    document_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    stored_pdf_path = document_dir / safe_filename

    # COPY THE PDF INTO ITS USER-SPECIFIC FOLDER

    try:

        if source_path.resolve() != stored_pdf_path.resolve():
            shutil.copy2(source_path, stored_pdf_path)

        pages = extract_pdf_text(stored_pdf_path)

        chunks = chunk_pdf_text(pages)

        add_documents(
            chunks=chunks,
            document_id=document_id,
            filename=safe_filename,
            user_id=user_id,
            file_hash=file_hash
        )

    except Exception:

        if stored_pdf_path.exists():
            stored_pdf_path.unlink()

        if document_dir.exists():
            shutil.rmtree(document_dir)

        raise

    return {
        "duplicate": False,
        "document_id": document_id,
        "filename": safe_filename,
        "total_pages": len(pages),
        "total_chunks": len(chunks)
    }


def list_documents(user_id):
    """RETURN ONLY THE LOGGED-IN USER'S PDF DOCUMENTS."""

    if not user_id:
        raise ValueError("User ID is required.")

    vector_store = get_vector_store()

    data = vector_store.get(
        where={
            "user_id": str(user_id)
        },
        include=["metadatas"]
    )

    documents = {}

    for metadata in data["metadatas"]:

        document_id = metadata["document_id"]

        if document_id not in documents:

            documents[document_id] = {
                "document_id": document_id,
                "filename": metadata["filename"],
                "pages": set(),
                "total_chunks": 0
            }

        documents[document_id]["pages"].add(
            metadata["page"]
        )

        documents[document_id]["total_chunks"] += 1

    result = []

    for document in documents.values():

        result.append({
            "document_id": document["document_id"],
            "filename": document["filename"],
            "total_pages": len(document["pages"]),
            "total_chunks": document["total_chunks"]
        })

    return result


def delete_document(document_id, user_id):
    """DELETE A DOCUMENT ONLY IF IT BELONGS TO THE USER."""

    if not document_id:
        raise ValueError("Document ID is required.")

    if not user_id:
        raise ValueError("User ID is required.")

    user_id = str(user_id)

    vector_store = get_vector_store()

    document_filter = {
        "$and": [
            {"user_id": user_id},
            {"document_id": document_id}
        ]
    }

    data = vector_store.get(
        where=document_filter,
        include=["metadatas"]
    )

    if not data["ids"]:
        return False

    filename = data["metadatas"][0]["filename"]

    # DELETE ONLY THIS USER'S DOCUMENT CHUNKS

    vector_store.delete(
        where=document_filter
    )

    # DELETE THE PDF FROM THIS USER'S FOLDER

    document_dir = (
        UPLOAD_DIR
        / user_id
        / document_id
    )

    pdf_path = document_dir / Path(filename).name

    if pdf_path.exists():
        pdf_path.unlink()

    if document_dir.exists():
        shutil.rmtree(document_dir)

    return True


def calculate_file_hash(file_path):
    """CALCULATE THE SHA-256 HASH OF A FILE."""

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        for chunk in iter(
            lambda: file.read(8192),
            b""
        ):
            sha256.update(chunk)

    return sha256.hexdigest()


def find_duplicate_document(file_hash, user_id):
    """FIND DUPLICATES ONLY WITHIN THE SAME USER ACCOUNT."""

    if not file_hash:
        raise ValueError("File Hash is required.")

    if not user_id:
        raise ValueError("User ID is required.")

    vector_store = get_vector_store()

    data = vector_store.get(
        where={
            "$and": [
                {"user_id": str(user_id)},
                {"file_hash": file_hash}
            ]
        },
        include=["metadatas"]
    )

    if not data["ids"]:
        return None

    metadata = data["metadatas"][0]

    return {
        "document_id": metadata["document_id"],
        "filename": metadata["filename"]
    }
