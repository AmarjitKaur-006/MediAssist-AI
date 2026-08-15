from src.preprocessing.text_cleaner import clean_medical_text


def test_numeric_ocr_correction():
    text = """
    Hemoglobin: 11.2 g/dl
    Reference Range: 12.@ - 16.0 g/dl
    Vitamin D: 18 ng/ml
    Reference Range: 3@ - 10@ ng/ml
    """

    cleaned = clean_medical_text(text)

    print("\n========== OCR CORRECTION TEST ==========\n")
    print(cleaned)

    # Verify OCR corrections
    assert "12.0 - 16.0" in cleaned
    assert "30 - 100" in cleaned

    # Verify other information is preserved
    assert "Hemoglobin: 11.2 g/dL" in cleaned
    assert "Vitamin D: 18 ng/mL" in cleaned


def test_patient_name_is_not_modified():
    text = """
    Patient Name: A@ron
    """

    cleaned = clean_medical_text(text)

    print("\n========== PATIENT NAME TEST ==========\n")
    print(cleaned)

    # The @ in a normal word should NOT be changed
    assert "Patient Name: A@ron" in cleaned


if __name__ == "__main__":
    test_numeric_ocr_correction()
    test_patient_name_is_not_modified()

    print("\nAll OCR correction tests passed! ✓")