from dataclasses import dataclass
from typing import Optional, List
import re


@dataclass
class MedicalFinding:
    """
    Represents one laboratory finding extracted
    from a medical report.

    A finding can be:
    - numeric: value is a number and may have a reference range
    - qualitative: value is a reported word such as Positive, Negative, Trace, etc.
    """

    test_name: str
    value: float | str
    unit: str
    reference_min: Optional[float]
    reference_max: Optional[float]
    status: str
    finding_type: str


def determine_status(
    value: float,
    reference_min: float | None,
    reference_max: float | None
) -> str:
    """
    Determine whether a numeric laboratory value is
    Low, Normal, High, or Unknown based on its
    reference range.
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
    Extract numeric and qualitative laboratory findings
    from cleaned medical report text.

    Numeric example:
        Hemoglobin: 11.2 g/dL
        Reference Range: 12.0 - 16.0 g/dL

    Qualitative examples:
        Protein: Negative
        Nitrite: Positive
        Blood: Trace

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

    # Only recognize a conservative set of qualitative result words.
    qualitative_values = {
        "positive",
        "negative",
        "trace",
        "present",
        "absent",
    }

    lines = text.splitlines()

    for i, line in enumerate(lines):

        current_line = line.strip()

        if not current_line:
            continue

        # ============================================================
        # 1. NUMERIC FINDING EXTRACTION
        # ============================================================

        numeric_match = re.match(
            r"^(.+?):\s*([\d,]+(?:\.\d+)?)\s*([A-Za-z/%]+)\s*$",
            current_line
        )

        if numeric_match:

            test_name = numeric_match.group(1).strip()

            if test_name.lower() in excluded_fields:
                continue

            value = float(
                numeric_match.group(2).replace(",", "")
            )

            unit = numeric_match.group(3).strip()

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
                status=status,
                finding_type="numeric"
            )

            findings.append(finding)

            continue

        # ============================================================
        # 2. QUALITATIVE FINDING EXTRACTION
        # ============================================================

        qualitative_match = re.match(
            r"^(.+?):\s*([A-Za-z]+)\s*$",
            current_line
        )

        if qualitative_match:

            test_name = qualitative_match.group(1).strip()
            qualitative_value = qualitative_match.group(2).strip()

            if test_name.lower() in excluded_fields:
                continue

            if qualitative_value.lower() not in qualitative_values:
                continue

            finding = MedicalFinding(
                test_name=test_name,
                value=qualitative_value,
                unit="",
                reference_min=None,
                reference_max=None,
                status="Unknown",
                finding_type="qualitative"
            )

            findings.append(finding)

    return findings