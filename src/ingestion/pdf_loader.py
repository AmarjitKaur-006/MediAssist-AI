import pymupdf
from src.ingestion.image_loader import extract_text_from_image


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF.

    If the PDF contains little or no extractable text,
    OCR will be used as a fallback.
    """

    document = pymupdf.open(pdf_path)

    extracted_text = []

    for page in document:
        text = page.get_text().strip()

        if text:
            extracted_text.append(text)
        else:
            # Render the PDF page as an image
            pixmap = page.get_pixmap()

            image_bytes = pixmap.tobytes("png")

            with open("temp_page.png", "wb") as image_file:
                image_file.write(image_bytes)

            ocr_text = extract_text_from_image("temp_page.png")

            extracted_text.append(ocr_text)

    document.close()

    return "\n".join(extracted_text)