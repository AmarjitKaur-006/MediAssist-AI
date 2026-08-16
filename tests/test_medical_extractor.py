from src.extraction.medical_extractor import extract_medical_findings


def test_medical_extraction():

    text = """
    MEDICAL LABORATORY REPORT
    Patient Name: Sample Patient
    Age: 25

    COMPLETE BLOOD COUNT

    Hemoglobin: 11.2 g/dL
    Reference Range: 12.0 - 16.0 g/dL

    WBC Count: 8,500 /uL
    Reference Range: 4,000 - 11,000 /uL

    Platelet Count: 250,000 /uL
    Reference Range: 150,000 - 450,000 /uL

    Vitamin D: 18 ng/mL
    Reference Range: 30 - 100 ng/mL
    """

    findings = extract_medical_findings(text)

    print("\n========== EXTRACTED MEDICAL FINDINGS ==========\n")

    for finding in findings:
        print(finding)

    # We expect four laboratory findings
    assert len(findings) == 4

    # Hemoglobin
    assert findings[0].test_name == "Hemoglobin"
    assert findings[0].value == 11.2
    assert findings[0].unit == "g/dL"
    assert findings[0].reference_min == 12.0
    assert findings[0].reference_max == 16.0
    assert findings[0].status == "Low"
    assert findings[0].finding_type == "numeric"

    # WBC
    assert findings[1].test_name == "WBC Count"
    assert findings[1].value == 8500
    assert findings[1].status == "Normal"
    assert findings[1].finding_type == "numeric"

    # Platelets
    assert findings[2].test_name == "Platelet Count"
    assert findings[2].value == 250000
    assert findings[2].status == "Normal"
    assert findings[2].finding_type == "numeric"

    # Vitamin D
    assert findings[3].test_name == "Vitamin D"
    assert findings[3].value == 18
    assert findings[3].unit == "ng/mL"
    assert findings[3].reference_min == 30
    assert findings[3].reference_max == 100
    assert findings[3].status == "Low"
    assert findings[3].finding_type == "numeric"

    print("\nMedical extraction test passed! ✓")


def test_reference_range_dash_variations():

    test_cases = [
        "Hemoglobin: 11.2 g/dL\nReference Range: 12.0 - 16.0 g/dL",
        "Hemoglobin: 11.2 g/dL\nReference Range: 12.0 – 16.0 g/dL",
        "Hemoglobin: 11.2 g/dL\nReference Range: 12.0 — 16.0 g/dL",
    ]

    print("\n========== DASH VARIATION TEST ==========\n")

    for text in test_cases:

        findings = extract_medical_findings(text)

        assert len(findings) == 1
        assert findings[0].reference_min == 12.0
        assert findings[0].reference_max == 16.0
        assert findings[0].status == "Low"
        assert findings[0].finding_type == "numeric"

        print(findings[0])

    print("\nDash variation test passed! ✓")

def test_missing_reference_range():

    text = """
    Some Test: 25 mg/dL
    """

    findings = extract_medical_findings(text)

    print("\n========== MISSING REFERENCE RANGE TEST ==========\n")
    print(findings)

    assert len(findings) == 1
    assert findings[0].test_name == "Some Test"
    assert findings[0].value == 25
    assert findings[0].unit == "mg/dL"
    assert findings[0].reference_min is None
    assert findings[0].reference_max is None
    assert findings[0].status == "Unknown"
    assert findings[0].finding_type == "numeric"

    print("\nMissing reference range test passed! ✓")

def test_non_lab_lines_are_ignored():

    text = """
    MEDICAL LABORATORY REPORT
    Patient Name: Sample Patient
    Age: 25
    Report Date: 15/08/2026

    Hemoglobin: 11.2 g/dL
    Reference Range: 12.0 - 16.0 g/dL
    """

    findings = extract_medical_findings(text)

    print("\n========== NON-LAB LINE TEST ==========\n")

    for finding in findings:
        print(finding)

    # Only Hemoglobin should be extracted.
    assert len(findings) == 1

    assert findings[0].test_name == "Hemoglobin"
    assert findings[0].value == 11.2
    assert findings[0].status == "Low"

    # Patient/report metadata must not become findings.
    assert all(
        finding.test_name.lower()
        not in {"patient name", "age", "report date"}
        for finding in findings
    )

    print("\nNon-laboratory line test passed! ✓")

def test_qualitative_findings():

    text = """
    URINALYSIS

    Protein: Negative
    Nitrite: Positive
    Blood: Trace
    Bacteria: Present
    """

    findings = extract_medical_findings(text)

    print("\n========== QUALITATIVE FINDING TEST ==========\n")

    for finding in findings:
        print(finding)

    # Four qualitative findings should be extracted.
    assert len(findings) == 4

    # Protein
    assert findings[0].test_name == "Protein"
    assert findings[0].value == "Negative"
    assert findings[0].unit == ""
    assert findings[0].reference_min is None
    assert findings[0].reference_max is None
    assert findings[0].status == "Unknown"
    assert findings[0].finding_type == "qualitative"

    # Nitrite
    assert findings[1].test_name == "Nitrite"
    assert findings[1].value == "Positive"
    assert findings[1].finding_type == "qualitative"

    # Blood
    assert findings[2].test_name == "Blood"
    assert findings[2].value == "Trace"
    assert findings[2].finding_type == "qualitative"

    # Bacteria
    assert findings[3].test_name == "Bacteria"
    assert findings[3].value == "Present"
    assert findings[3].finding_type == "qualitative"

    print("\nQualitative finding test passed! ✓")


def test_unrecognized_text_is_not_extracted_as_qualitative():

    text = """
    Patient Status: Stable
    Report Type: Laboratory
    Department: Pathology
    """

    findings = extract_medical_findings(text)

    print("\n========== QUALITATIVE FILTER TEST ==========\n")
    print(findings)

    # None of these lines use a recognized qualitative result.
    assert len(findings) == 0

    print("\nQualitative filter test passed! ✓")

if __name__ == "__main__":
    test_medical_extraction()
    test_reference_range_dash_variations()
    test_missing_reference_range()
    test_non_lab_lines_are_ignored()
    test_qualitative_findings()
    test_unrecognized_text_is_not_extracted_as_qualitative()