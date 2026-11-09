from src.pdf_processor import extract_pdf_text
from pathlib import Path

print("\n Test 1: Checking missing PDF:")

try:
    extract_pdf_text("missing_file.pdf")
except FileNotFoundError as error:
    print(f"Expected error caught: {error}")


print("\n Test 2: Checking empty PDF:")

empty_pdf = Path("empty_pdf")
empty_pdf.touch()

try:
    extract_pdf_text(empty_pdf)
except ValueError as error:
    print(f"Expected error caught: {error}")

finally:
    empty_pdf.unlink()


print("\n Test 3: Checking Corrupted PDF:")

corrupted_pdf = Path("corrupted_pdf.pdf")
corrupted_pdf.write_text("This is not a valid pdf file...")

try:
    extract_pdf_text(corrupted_pdf)

except ValueError as error:
    print(f"Expected error caught: {error}")

finally:
    corrupted_pdf.unlink(missing_ok = True)


print("\n All error handling tests completed successfully...")

