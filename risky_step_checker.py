"""Check CI/CD steps for risky patterns in scripts."""

from typing import Dict, List


RISKY_PATTERNS: Dict[str, Dict[str, object]] = {
    "curl_bash": {
        "desc": "Download & execute script via curl | bash",
        "keywords": ["curl", "|", "bash"],
        "severity": "high",
    },
    "wget_bash": {
        "desc": "Download & execute script via wget | bash",
        "keywords": ["wget", "|", "bash"],
        "severity": "high",
    },
    "sudo_usage": {
        "desc": "Usage of sudo inside CI job",
        "keywords": ["sudo "],
        "severity": "medium",
    },
    "docker_privileged": {
        "desc": "Docker run with --privileged flag",
        "keywords": ["docker run", "--privileged"],
        "severity": "high",
    },
    "shell_injection": {
        "desc": "Potential shell injection via piping to sh",
        "keywords": ["|", "sh"],
        "severity": "medium",
    },
}


class RiskyStepFinding:
    """Represents a risky pattern finding in a pipeline step."""

    def __init__(self, step_name: str, rule_id: str, desc: str, severity: str) -> None:
        self.step_name = step_name
        self.rule_id = rule_id
        self.desc = desc
        self.severity = severity

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return (
            f"RiskyStepFinding(step_name={self.step_name!r}, rule_id={self.rule_id!r}, "
            f"severity={self.severity!r})"
        )


class RiskyStepChecker:
    """Provides utilities to scan pipeline steps for risky command patterns."""

    @staticmethod
    def scan_step(step: Dict) -> List[RiskyStepFinding]:
        """Scan a single step for risky patterns defined in ``RISKY_PATTERNS``."""

        script = step.get("script", "")
        lower = script.lower()
        findings: List[RiskyStepFinding] = []

        for rule_id, rule in RISKY_PATTERNS.items():
            keywords = rule.get("keywords", [])
            if all(str(keyword).lower() in lower for keyword in keywords):
                findings.append(
                    RiskyStepFinding(
                        step_name=step.get("name", ""),
                        rule_id=rule_id,
                        desc=str(rule.get("desc", "")),
                        severity=str(rule.get("severity", "")),
                    )
                )
        return findings

    @staticmethod
    def scan_all(steps: List[Dict]) -> List[RiskyStepFinding]:
        """Scan multiple steps and collect all risky pattern findings."""

        all_findings: List[RiskyStepFinding] = []
        for step in steps:
            all_findings.extend(RiskyStepChecker.scan_step(step))
        return all_findings

