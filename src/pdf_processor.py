import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

#------------------------------------EXTRACTS THE TEXT FROM THE PDF------------------
def extract_pdf_text(pdf_path):

    pdf_path =  Path(pdf_path)

    #CHECKS IF THE FILE EXISTS OR NOT
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    #CHECKS IF THE SUPPLIED PATH IS A FILE OR NOT
    if not pdf_path.is_file():
        raise ValueError("Provide path is not a file.")

    #CHECKS WHETHER THE FILE IS EMPTY OR NOT
    if pdf_path.stat().st_size == 0:
        raise ValueError("The PDF file is empty.")

    with open(pdf_path, "rb") as file:
        file_signature = file.read(5)

    if file_signature != b"%PDF-":
        raise ValueError("Invalid PDF file. PDF signature not found.")


    pages = []

    try:
        with pymupdf.open(pdf_path) as doc:

            for page_number, page in enumerate(doc, start = 1):
                text = page.get_text("text").strip()

                pages.append({
                    "page": page_number,
                    "text": text
                })
    except ValueError:
        raise

    except Exception as error:
        raise ValueError(f"Unable to read PDF: {error}") from error

    if not any(page['text'] for page in pages):
        raise ValueError(
            "No extractable text found. This PDF may contain scanned pages."
        )


    return pages

#------------------------------------COBINES OR SPLITS THE  WHOLE TEXT INTO SMALLER CHUNKS------------------

def chunk_pdf_text(pages, chunk_size = 1000, chunk_overlap = 150):
    """"SPLITS EVERY PAGE'S TEXT INTO CHUNKS AND PRESERVES THE PAGE NUMBERS"""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        length_function = len,
        separators = ["\n\n", "\n", " ", ""]
    )

    chunks = []

    for page in pages:
        if not page["text"].strip():
            continue

        page_chunks = splitter.split_text(page["text"])

        for chunk_number, chunk_text in enumerate(page_chunks, start = 1):
            chunks.append({
                "page" : page["page"],
                "chunk" : chunk_number,
                "text" : chunk_text
            })

    return chunks