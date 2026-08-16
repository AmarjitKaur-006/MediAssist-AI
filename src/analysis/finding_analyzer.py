from dataclasses import dataclass
from typing import List

from src.extraction.medical_extractor import MedicalFinding


@dataclass
class FindingAnalysis:      # output structure -> Instead of returning three separate lists, we package them together:
    #For example:
    #FindingAnalysis(abnormal_findings=[Hemoglobin, Vitamin D], normal_findings=[WBC, Platelet Count],unknown_findings=[])

    """
    Stores the categorized medical findings
    produced by the analysis layer.
    """

    abnormal_findings: List[MedicalFinding]
    normal_findings: List[MedicalFinding]
    unknown_findings: List[MedicalFinding]


def analyze_findings(
    findings: List[MedicalFinding]
) -> FindingAnalysis:
    """
    Categorize medical findings based on their status.

    Findings with status:
        Low / High  -> abnormal_findings
        Normal      -> normal_findings
        Unknown     -> unknown_findings
    """

    abnormal_findings = []
    normal_findings = []
    unknown_findings = []

    for finding in findings:

        if finding.status in {"Low", "High"}:
            abnormal_findings.append(finding)

        elif finding.status == "Normal":
            normal_findings.append(finding)

        else:
            unknown_findings.append(finding)

    return FindingAnalysis(
        abnormal_findings=abnormal_findings,
        normal_findings=normal_findings,
        unknown_findings=unknown_findings
    )