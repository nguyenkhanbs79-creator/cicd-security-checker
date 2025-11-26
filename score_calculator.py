"""Compute security score for CI/CD pipelines based on scanning results."""

from typing import List

from best_practice_checker import BestPracticeResult
from risky_step_checker import RiskyStepFinding
from secret_scanner import SecretFinding


class ScoreResult:
    """Represents the overall security score and classification for a pipeline."""

    def __init__(self, score: int, level: str) -> None:
        self.score = score
        self.level = level


class ScoreCalculator:
    """Calculate a normalized security score from findings and best-practice checks."""

    @staticmethod
    def calculate(
        secrets: List[SecretFinding],
        risky_steps: List[RiskyStepFinding],
        best_practice: BestPracticeResult,
    ) -> ScoreResult:
        """Compute the pipeline security score (0-100) and categorize the risk level."""

        score = 100
        score -= min(len(secrets) * 10, 40)

        for finding in risky_steps:
            if finding.severity == "high":
                score -= 10
            else:
                score -= 5

        if best_practice.has_security_step:
            score += 10
        if best_practice.has_dependency_scan:
            score += 10

        if score > 100:
            score = 100
        if score < 0:
            score = 0

        if score >= 85:
            level = "GOOD"
        elif score >= 60:
            level = "MEDIUM"
        else:
            level = "BAD"

        return ScoreResult(score=score, level=level)
