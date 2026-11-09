from src.pdf_processor import extract_pdf_text, chunk_pdf_text

pdf_path = r"D:\ALLEN KOTA ENGLISH MEDIUM STUDY MATERIALS-20230609T123029Z-001\ALLEN KOTA ENGLISH MEDIUM STUDY MATERIALS\ALLEN NEET UG PARAKH 2021\CHEM_Chemical kinetics 1.pdf"

pages = extract_pdf_text(pdf_path)
chunks = chunk_pdf_text(pages)

for chunk in chunks:
    print(f"\n Page: {chunk['page']}")
    print(f"\n Chunk: {chunk['chunk']}")
    print(f"\n Length of Characters: {len(chunk['text'])}")

    print (chunk['text'][:200])

assert len(chunks) > 0

assert all(chunk['page'] >= 1 for chunk in chunks)

assert all(chunk['text'].strip() for chunk in chunks)
        
