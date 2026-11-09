import pytest

from src.vector_store import get_vector_store, add_documents, search_documents

@pytest.fixture
def sample_chunks():
    """Provide sample PDF chunks for testing."""

    return[
        {
            "page" : 1,
            "chunk" : 1,
            "text" : "Python is a high-level programming language."
        },
        {
            "page" : 2,
            "chunk" : 1,
            "text" : "Python supports object-oriented programming."
        }

    ]

@pytest.fixture

def database_path(tmp_path):
    """Provide a temporary database directory."""

    return tmp_path / "test_chroma_db"

#TEST 1: DATABASE CONNECTION

def test_get_vector_store(database_path):
    vector_store = get_vector_store(database_path)

    assert vector_store is not None

#TEST 2: DOCUMENT INSERTION

def test_add_documents(sample_chunks, database_path):
    vector_store = add_documents(
        chunks = sample_chunks,
        document_id = "python_001",
        filename = "Python_notes.pdf",
        persist_directory = database_path
    )

    assert vector_store is not None

    results = vector_store.get(
        where = {"document_id" : "python_001"}
    )

    assert len(results["ids"]) == 2

#TEST 3: INDIVIDUAL PDF RETRIEVAL

def test_search_individual_documents(sample_chunks, database_path):
    add_documents(
        chunks = sample_chunks,
        document_id = "python_001",
        filename = "Python_notes.pdf",
        persist_directory = database_path
    )

    results = search_documents(
        query = "Python programming",
        document_id = "python_001",
        k = 4,
        persist_directory = database_path
    )

    assert len(results) > 0

    assert all(
        result.metadata["document_id"] == "python_001"
        for result in results
    )

def test_search_all_documents(database_path):
    python_chunks = [
        {
            "page" : 1,
            "chunk" : 1,
            "text" : "Python is a high-level programming language."
        }
    ]

    dbms_chunks = [
        {
            "page" : 1,
            "chunk" : 1,
            "text" : "Database Management Systems organize data."
        }
    ] 

    add_documents(
        python_chunks,
        "python_001",
        "Python_notes.pdf",
        database_path
    )

    add_documents(
        dbms_chunks,
        "dbms_001",
        "DBMS_notes.pdf",
        database_path
    )

    results = search_documents(
        query = "Programming and Database Management",
        k = 10,
        persist_directory = database_path
    )

    document_ids = {
        result.metadata["document_id"]
        for result in results
    }

    assert "python_001" in document_ids
    assert "dbms_001" in document_ids

#TEST 5: EMPTY CHUNKS SHOULD RAISE VALUE-ERROR

def test_add_empty_documents(database_path):
    with pytest.raises(ValueError):
        add_documents(
            chunks = [],
            document_id = "python_001",
            filename = "Python_notes.pdf",
            persist_directory = database_path
        )

#TEST 6: MISSING DOCUMENT ID SHOULD RAISE VALUE-ERROR

def test_missing_document_id(sample_chunks, database_path):
    with pytest.raises(ValueError):
        add_documents(
            chunks = [],
            document_id = "",
            filename = "Python_notes.pdf",
            persist_directory = database_path
        )

#TEST 7: EMPTY SEARCH QUERY SHOULD RAISE VALUE-ERROR

def test_empty_search_query(database_path):
    with pytest.raises(ValueError):
        search_documents(
            query = "",
            persist_directory = database_path
        )

#TEST 8: DATABASE PERSISTENCE

def test_database_persistence(sample_chunks, database_path):
    add_documents(
        chunks = sample_chunks,
        document_id = "python_001",
        filename = "Python_notes.pdf",
        persist_directory = database_path
    )
    vectore_store = get_vector_store(database_path)

    results = vectore_store.get(
        where = {"document_id" : "python_001"}
    )

    assert len(results["ids"]) == 2

