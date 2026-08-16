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
            status="Low",
            finding_type="numeric"
        ),

        MedicalFinding(
            test_name="WBC Count",
            value=8500,
            unit="/uL",
            reference_min=4000,
            reference_max=11000,
            status="Normal",
            finding_type="numeric"
        ),

        MedicalFinding(
            test_name="Platelet Count",
            value=250000,
            unit="/uL",
            reference_min=150000,
            reference_max=450000,
            status="Normal",
            finding_type="numeric"
        ),

        MedicalFinding(
            test_name="Vitamin D",
            value=18,
            unit="ng/mL",
            reference_min=30,
            reference_max=100,
            status="Low",
            finding_type="numeric"
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

    print("\nQualitative Findings:")
    for finding in analysis.qualitative_findings:
        print(finding)

    # Two findings should be abnormal.
    assert len(analysis.abnormal_findings) == 2

    # Two findings should be normal.
    assert len(analysis.normal_findings) == 2

    # No numeric findings should be unknown.
    assert len(analysis.unknown_findings) == 0

    # No qualitative findings in this test.
    assert len(analysis.qualitative_findings) == 0

    # Check abnormal findings.
    assert analysis.abnormal_findings[0].test_name == "Hemoglobin"
    assert analysis.abnormal_findings[1].test_name == "Vitamin D"

    # Check normal findings.
    assert analysis.normal_findings[0].test_name == "WBC Count"
    assert analysis.normal_findings[1].test_name == "Platelet Count"

    print("\nFinding analysis test passed! ✓")


def test_unknown_findings():

    findings = [
        MedicalFinding(
            test_name="Some Test",
            value=25,
            unit="mg/dL",
            reference_min=None,
            reference_max=None,
            status="Unknown",
            finding_type="numeric"
        )
    ]

    analysis = analyze_findings(findings)

    print("\n========== UNKNOWN FINDING TEST ==========\n")

    for finding in analysis.unknown_findings:
        print(finding)

    assert len(analysis.unknown_findings) == 1

    assert analysis.unknown_findings[0].test_name == "Some Test"

    assert analysis.unknown_findings[0].value == 25

    assert analysis.unknown_findings[0].status == "Unknown"

    assert analysis.unknown_findings[0].finding_type == "numeric"

    assert len(analysis.abnormal_findings) == 0
    assert len(analysis.normal_findings) == 0
    assert len(analysis.qualitative_findings) == 0

    print("\nUnknown finding test passed! ✓")


def test_high_finding():

    findings = [
        MedicalFinding(
            test_name="Testosterone",
            value=120,
            unit="ng/dL",
            reference_min=20,
            reference_max=100,
            status="High",
            finding_type="numeric"
        )
    ]

    analysis = analyze_findings(findings)

    print("\n========== HIGH FINDING TEST ==========\n")

    for finding in analysis.abnormal_findings:
        print(finding)

    # High numeric findings should be grouped under abnormal.
    assert len(analysis.abnormal_findings) == 1

    assert analysis.abnormal_findings[0].test_name == "Testosterone"

    assert analysis.abnormal_findings[0].status == "High"

    assert analysis.abnormal_findings[0].finding_type == "numeric"

    assert len(analysis.normal_findings) == 0
    assert len(analysis.unknown_findings) == 0
    assert len(analysis.qualitative_findings) == 0

    print("\nHigh finding test passed! ✓")


def test_empty_findings():

    findings = []

    analysis = analyze_findings(findings)

    print("\n========== EMPTY FINDINGS TEST ==========\n")

    print("Abnormal:", analysis.abnormal_findings)
    print("Normal:", analysis.normal_findings)
    print("Unknown:", analysis.unknown_findings)
    print("Qualitative:", analysis.qualitative_findings)

    assert analysis.abnormal_findings == []
    assert analysis.normal_findings == []
    assert analysis.unknown_findings == []
    assert analysis.qualitative_findings == []

    print("\nEmpty findings test passed! ✓")


def test_qualitative_findings():

    findings = [
        MedicalFinding(
            test_name="Protein",
            value="Negative",
            unit="",
            reference_min=None,
            reference_max=None,
            status="Unknown",
            finding_type="qualitative"
        ),

        MedicalFinding(
            test_name="Nitrite",
            value="Positive",
            unit="",
            reference_min=None,
            reference_max=None,
            status="Unknown",
            finding_type="qualitative"
        ),

        MedicalFinding(
            test_name="Blood",
            value="Trace",
            unit="",
            reference_min=None,
            reference_max=None,
            status="Unknown",
            finding_type="qualitative"
        )
    ]

    analysis = analyze_findings(findings)

    print("\n========== QUALITATIVE ANALYSIS ==========\n")

    for finding in analysis.qualitative_findings:
        print(finding)

    # All three qualitative findings should be
    # stored in the qualitative category.
    assert len(analysis.qualitative_findings) == 3

    # Check Protein.
    assert analysis.qualitative_findings[0].test_name == "Protein"
    assert analysis.qualitative_findings[0].value == "Negative"
    assert analysis.qualitative_findings[0].finding_type == "qualitative"

    # Check Nitrite.
    assert analysis.qualitative_findings[1].test_name == "Nitrite"
    assert analysis.qualitative_findings[1].value == "Positive"
    assert analysis.qualitative_findings[1].finding_type == "qualitative"

    # Check Blood.
    assert analysis.qualitative_findings[2].test_name == "Blood"
    assert analysis.qualitative_findings[2].value == "Trace"
    assert analysis.qualitative_findings[2].finding_type == "qualitative"

    # Qualitative findings must NOT automatically
    # be classified as normal or abnormal.
    assert len(analysis.abnormal_findings) == 0
    assert len(analysis.normal_findings) == 0
    assert len(analysis.unknown_findings) == 0

    print("\nQualitative analysis test passed! ✓")


if __name__ == "__main__":

    test_finding_analysis()

    test_unknown_findings()

    test_high_finding()

    test_empty_findings()

    test_qualitative_findings()