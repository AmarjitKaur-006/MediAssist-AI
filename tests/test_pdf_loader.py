from src.ingestion.pdf_loader import extract_text_from_pdf


pdf_path = "data/raw/sample_medical_report.pdf"

text = extract_text_from_pdf(pdf_path)

print("\n========== EXTRACTED TEXT ==========\n")
print(text)