from src.pdf_processor import extract_pdf_text


pdf_path = r"D:\ALLEN KOTA ENGLISH MEDIUM STUDY MATERIALS-20230609T123029Z-001\ALLEN KOTA ENGLISH MEDIUM STUDY MATERIALS\ALLEN NEET UG PARAKH 2021\CHEM_Chemical kinetics 1.pdf"
pages = extract_pdf_text(pdf_path)

print("TOTAL PAGES EXTRACTED = ", len(pages))

for page in pages:
    print(f"\n--- Page {page['page']} ---")
    print(page["text"][:500])