from src.extraction.medical_extractor import MedicalFinding
from src.analysis.finding_analyzer import analyze_findings


def test_finding_analysis():

    findings = [
        MedicalFinding(
            test_name="Hemoglobin",
            value=11.2,
            unit="g/dL",
            reference_min=12.0,
            reference_max=16.0,
            status="Low"
        ),

        MedicalFinding(
            test_name="WBC Count",
            value=8500,
            unit="/uL",
            reference_min=4000,
            reference_max=11000,
            status="Normal"
        ),

        MedicalFinding(
            test_name="Platelet Count",
            value=250000,
            unit="/uL",
            reference_min=150000,
            reference_max=450000,
            status="Normal"
        ),

        MedicalFinding(
            test_name="Vitamin D",
            value=18,
            unit="ng/mL",
            reference_min=30,
            reference_max=100,
            status="Low"
        )
    ]

    analysis = analyze_findings(findings)

    print("\n========== FINDING ANALYSIS ==========\n")

    print("Abnormal Findings:")
    for finding in analysis.abnormal_findings:
        print(finding)

    print("\nNormal Findings:")
    for finding in analysis.normal_findings:
        print(finding)

    print("\nUnknown Findings:")
    for finding in analysis.unknown_findings:
        print(finding)

    # Two findings should be abnormal.
    assert len(analysis.abnormal_findings) == 2

    # Two findings should be normal.
    assert len(analysis.normal_findings) == 2

    # No findings should be unknown.
    assert len(analysis.unknown_findings) == 0

    # Check abnormal findings.
    assert analysis.abnormal_findings[0].test_name == "Hemoglobin"
    assert analysis.abnormal_findings[1].test_name == "Vitamin D"

    # Check normal findings.
    assert analysis.normal_findings[0].test_name == "WBC Count"
    assert analysis.normal_findings[1].test_name == "Platelet Count"

    print("\nFinding analysis test passed! ✓")


def test_high_finding():

    findings = [
        MedicalFinding(
            test_name="Testosterone",
            value=120,
            unit="ng/dL",
            reference_min=20,
            reference_max=100,
            status="High"
        )
    ]

    analysis = analyze_findings(findings)

    print("\n========== HIGH FINDING TEST ==========\n")

    for finding in analysis.abnormal_findings:
        print(finding)

    assert len(analysis.abnormal_findings) == 1
    assert analysis.abnormal_findings[0].test_name == "Testosterone"
    assert analysis.abnormal_findings[0].status == "High"

    assert len(analysis.normal_findings) == 0
    assert len(analysis.unknown_findings) == 0

    print("\nHigh finding test passed! ✓")


def test_empty_findings():

    findings = []

    analysis = analyze_findings(findings)

    print("\n========== EMPTY FINDINGS TEST ==========\n")

    print("Abnormal:", analysis.abnormal_findings)
    print("Normal:", analysis.normal_findings)
    print("Unknown:", analysis.unknown_findings)

    assert analysis.abnormal_findings == []
    assert analysis.normal_findings == []
    assert analysis.unknown_findings == []

    print("\nEmpty findings test passed! ✓")


def test_unknown_findings():

    findings = [
        MedicalFinding(
            test_name="Some Test",
            value=25,
            unit="mg/dL",
            reference_min=None,
            reference_max=None,
            status="Unknown"
        )
    ]

    analysis = analyze_findings(findings)

    print("\n========== UNKNOWN FINDING TEST ==========\n")

    for finding in analysis.unknown_findings:
        print(finding)

    assert len(analysis.unknown_findings) == 1
    assert analysis.unknown_findings[0].test_name == "Some Test"

    assert len(analysis.abnormal_findings) == 0
    assert len(analysis.normal_findings) == 0

    print("\nUnknown finding test passed! ✓")


if __name__ == "__main__":
    test_finding_analysis()
    test_unknown_findings()
    test_high_finding()
    test_empty_findings()