from dataclasses import dataclass
from typing import List

from src.extraction.medical_extractor import MedicalFinding


@dataclass
class FindingAnalysis:
    """
    Stores categorized medical findings produced
    by the analysis layer.
    """

    abnormal_findings: List[MedicalFinding]
    normal_findings: List[MedicalFinding]
    unknown_findings: List[MedicalFinding]
    qualitative_findings: List[MedicalFinding]


def analyze_findings(
    findings: List[MedicalFinding]
) -> FindingAnalysis:
    """
    Categorize medical findings based on finding type and status.

    Numeric findings:
        Low / High  -> abnormal_findings
        Normal      -> normal_findings
        Unknown     -> unknown_findings

    Qualitative findings:
        -> qualitative_findings
    """

    abnormal_findings = []
    normal_findings = []
    unknown_findings = []
    qualitative_findings = []

    for finding in findings:

        if finding.finding_type == "qualitative":
            qualitative_findings.append(finding)

        elif finding.status in {"Low", "High"}:
            abnormal_findings.append(finding)

        elif finding.status == "Normal":
            normal_findings.append(finding)

        else:
            unknown_findings.append(finding)

    return FindingAnalysis(
        abnormal_findings=abnormal_findings,
        normal_findings=normal_findings,
        unknown_findings=unknown_findings,
        qualitative_findings=qualitative_findings
    )