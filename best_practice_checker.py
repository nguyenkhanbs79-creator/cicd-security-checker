"""Check CI/CD steps for security best practices."""

from typing import Dict, List


DEP_SCAN_KEYWORDS: List[str] = [
    "npm audit",
    "yarn audit",
    "pip-audit",
    "safety",
    "dependency-check",
]

SECURITY_KEYWORDS: List[str] = [
    "bandit",
    "semgrep",
    "trivy",
    "sast",
    "dast",
    "zap-baseline",
]


class BestPracticeResult:
    """Represents whether best practice security checks are present in the pipeline."""

    def __init__(self, has_dependency_scan: bool, has_security_step: bool) -> None:
        self.has_dependency_scan = has_dependency_scan
        self.has_security_step = has_security_step


class BestPracticeChecker:
    """Analyze pipeline steps to identify security best practice coverage."""

    @staticmethod
    def analyze(steps: List[Dict]) -> BestPracticeResult:
        """Check if any step performs dependency scanning or security scanning.

        The analysis searches for known dependency and security scanning keywords
        inside the script contents of each step to set the corresponding flags.
        """

        has_dep_scan = False
        has_sec_step = False

        for step in steps:
            script = step.get("script", "")
            lower = script.lower()

            if any(keyword in lower for keyword in DEP_SCAN_KEYWORDS):
                has_dep_scan = True

            if any(keyword in lower for keyword in SECURITY_KEYWORDS):
                has_sec_step = True

        return BestPracticeResult(
            has_dependency_scan=has_dep_scan,
            has_security_step=has_sec_step,
        )
