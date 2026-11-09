import pytest
import pymupdf
from pathlib import Path
from src.pdf_processor import extract_pdf_text, chunk_pdf_text

def test_missing_pdf():
    with pytest.raises(FileNotFoundError):
        extract_pdf_text("missing_file.pdf")

def test_empty_pdf(tmp_path):
    empty_pdf = tmp_path / "empty_pdf.pdf"
    empty_pdf.touch()

    with pytest.raises(ValueError):
        extract_pdf_text(empty_pdf)    
    
def test_corrupted_pdf(tmp_path):
    corrupted_pdf = tmp_path / "corrupted_pdf.pdf"
    corrupted_pdf.write_text("This is a corrupted pdf file.")

    with pytest.raises(ValueError):
        extract_pdf_text(corrupted_pdf)


def test_extract_pdf_text(tmp_path):

    #CREATING A TEMPORARY PDF
    pdf_path = tmp_path / "sample.pdf"
    doc = pymupdf.open()
    page = doc.new_page()

    page.insert_text(
        (72,72),
        "This is a sample PDF for testing text extraction...."
    )

    doc.save(pdf_path)
    doc.close()

    pages = extract_pdf_text(pdf_path)

    assert len(pages) == 1
    assert pages[0]["page"] == 1
    assert "sample PDF" in pages[0]["text"]

def test_chunk_pdf_text():

    #SAMPLE DATA

    pages = [
        {
            "page" : 1,
            "text" : "Python Programming is interesting."  * 100
        }
    ]

    #GENERATE CHUNKS
    chunks = chunk_pdf_text(pages)

    assert len(chunks) > 1
    assert all(chunk["page"] == 1 for chunk in chunks)
    assert all(chunk["text"].strip() for chunk in chunks)


def test_chunk_pdf_text_skips_empty_pages():
    pages = [
        {"page": 1, "text": ""},
        {"page": 2, "text": "This pdf contains interesting information"}
    ]

    chunks = chunk_pdf_text(pages)

    assert len(chunks) == 1
    assert chunks[0]["page"] == 2