from dataclasses import dataclass
from typing import Optional, List
import re


@dataclass
class MedicalFinding:
    """
    Represents one laboratory finding extracted
    from a medical report.
    """

    test_name: str
    value: float
    unit: str
    reference_min: Optional[float]
    reference_max: Optional[float]
    status: str


def determine_status(
    value: float,
    reference_min: float | None,
    reference_max: float | None
) -> str:
    """
    Determine whether a laboratory value is Low,
    Normal, High, or Unknown based on its reference range.
    """

    if reference_min is None or reference_max is None:
        return "Unknown"

    if value < reference_min:
        return "Low"

    if value > reference_max:
        return "High"

    return "Normal"

def extract_medical_findings(text: str) -> List[MedicalFinding]:
    """
    Extract laboratory findings from cleaned medical report text.

    Expected format:

        Test Name: Value Unit
        Reference Range: Minimum - Maximum Unit

    Returns:
        A list of MedicalFinding objects.
    """

    findings = []

    excluded_fields = {
    "patient name",
    "name",
    "age",
    "patient age",
    "date",
    "report date",
    "date of birth",
    "dob",
}

    lines = text.splitlines()

    for i, line in enumerate(lines):

        # Look for lines containing:
        # Test Name: Value Unit
        match = re.match(
            r"^(.+?):\s*([\d,]+(?:\.\d+)?)\s*([A-Za-z/%]+)\s*$",
            line.strip()
        )

        if not match:
            continue

        test_name = match.group(1).strip()
        if test_name.lower() in excluded_fields:
            continue


        value = float(match.group(2).replace(",", ""))
        unit = match.group(3).strip()

        reference_min = None
        reference_max = None

        # Look at the next line for the reference range.
        if i + 1 < len(lines):

            reference_match = re.search(
                r"Reference Range:\s*"
                r"([\d,]+(?:\.\d+)?)\s*"
                r"[-–—]\s*"
                r"([\d,]+(?:\.\d+)?)",
                lines[i + 1],
                flags=re.IGNORECASE
            )

            if reference_match:
                reference_min = float(
                    reference_match.group(1).replace(",", "")
                )

                reference_max = float(
                    reference_match.group(2).replace(",", "")
                )

        # Determine status
        status = determine_status(
            value,
            reference_min,
            reference_max
        )

        finding = MedicalFinding(
            test_name=test_name,
            value=value,
            unit=unit,
            reference_min=reference_min,
            reference_max=reference_max,
            status=status
        )

        findings.append(finding)

    return findings