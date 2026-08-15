from src.ingestion.image_loader import extract_text_from_image


image_path = "data/raw/sample_medical_report.png"

text = extract_text_from_image(image_path)

print("\n========== EXTRACTED TEXT ==========\n")
print(text)