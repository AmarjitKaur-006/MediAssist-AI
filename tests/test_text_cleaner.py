from src.preprocessing.text_cleaner import clean_medical_text


sample_text = """
MEDICAL LABORATORY REPORT

Patient Name: Sample Patient
Age: 25

COMPLETE BLOOD COUNT

Hemoglobin:     11.2 g/dl
Reference Range: 12.0 - 16.0 g/dl.

WBC Count:      8,500 /ul
Reference Range: 4,000 - 11,000 /ul.

Platelet Count: 250,000 /uL
Reference Range: 150,000 - 450,000 /uL

Vitamin D: 18 ng/ml
Reference Range: 30 - 100 ng/ml
"""


cleaned_text = clean_medical_text(sample_text)

print("\n========== CLEANED TEXT ==========\n")
print(cleaned_text)