"""Secret scanning utilities for CI/CD pipeline steps."""

import re
from typing import Dict, List


SECRET_PATTERNS: Dict[str, str] = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "GitHub Token": r"ghp_[0-9A-Za-z]{36}",
    "Generic Password": r"(?i)password\s*=\s*['\"][^'\"]+['\"]",
    "JWT": r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
    "Private Key Block": r"-----BEGIN( RSA)? PRIVATE KEY-----",
}


class SecretFinding:
    """Represents a detected secret within a pipeline step."""

    def __init__(self, step_name: str, secret_type: str, snippet: str) -> None:
        self.step_name = step_name
        self.secret_type = secret_type
        self.snippet = snippet

    def __repr__(self) -> str:  # pragma: no cover - simple repr
        return (
            f"SecretFinding(step_name={self.step_name!r}, "
            f"secret_type={self.secret_type!r}, snippet={self.snippet!r})"
        )


class SecretScanner:
    """Provides utilities to scan pipeline steps for potential secrets."""

    @staticmethod
    def scan_step(step: Dict) -> List[SecretFinding]:
        """Scan a single pipeline step for secret patterns."""
        script: str = step.get("script", "")
        env: Dict[str, str] = step.get("env", {}) or {}
        env_text = "\n".join(f"{key}={value}" for key, value in env.items())
        text = f"{script}\n{env_text}" if env_text else script

        findings: List[SecretFinding] = []
        step_name: str = step.get("name", "")

        for name, pattern in SECRET_PATTERNS.items():
            for match in re.finditer(pattern, text):
                findings.append(
                    SecretFinding(
                        step_name=step_name,
                        secret_type=name,
                        snippet=match.group(0),
                    )
                )

        return findings

    @staticmethod
    def scan_all(steps: List[Dict]) -> List[SecretFinding]:
        """Scan a list of pipeline steps for potential secrets."""
        all_findings: List[SecretFinding] = []
        for step in steps:
            all_findings.extend(SecretScanner.scan_step(step))
        return all_findings
