import json
from typing import List

from rich.console import Console
from rich.table import Table

from best_practice_checker import BestPracticeResult
from risky_step_checker import RiskyStepFinding
from score_calculator import ScoreResult
from secret_scanner import SecretFinding

console = Console()


class Reporter:
    """Generate human-readable and JSON reports for CI/CD security analysis."""

    @staticmethod
    def print_human_readable(
        score: ScoreResult,
        secrets: List[SecretFinding],
        risky: List[RiskyStepFinding],
        best: BestPracticeResult,
    ) -> None:
        """Print a formatted console report summarizing security findings."""

        console.rule("[bold cyan]CI/CD Security Report")
        console.print(f"Security Score: {score.score} ({score.level})")

        bp_table = Table(title="Best Practice Summary")
        bp_table.add_column("Check")
        bp_table.add_column("Status")
        bp_table.add_row(
            "Has security step",
            "YES" if best.has_security_step else "NO",
        )
        bp_table.add_row(
            "Has dependency scan",
            "YES" if best.has_dependency_scan else "NO",
        )
        console.print(bp_table)

        console.print("[bold yellow]Secret Findings[/bold yellow]")
        if secrets:
            secret_table = Table()
            secret_table.add_column("Step")
            secret_table.add_column("Type")
            secret_table.add_column("Snippet")
            for finding in secrets:
                secret_table.add_row(
                    finding.step_name,
                    finding.secret_type,
                    finding.snippet,
                )
            console.print(secret_table)
        else:
            console.print("[green]No secrets detected.[/green]")

        console.print("[bold yellow]Risky Steps[/bold yellow]")
        if risky:
            risky_table = Table()
            risky_table.add_column("Step")
            risky_table.add_column("Rule")
            risky_table.add_column("Description")
            risky_table.add_column("Severity")
            for finding in risky:
                risky_table.add_row(
                    finding.step_name,
                    finding.rule_id,
                    finding.desc,
                    finding.severity,
                )
            console.print(risky_table)
        else:
            console.print("[green]No risky patterns detected.[/green]")

    @staticmethod
    def to_json(
        path: str,
        score: ScoreResult,
        secrets: List[SecretFinding],
        risky: List[RiskyStepFinding],
        best: BestPracticeResult,
    ) -> None:
        """Export the report to a JSON file at the given path."""

        data = {
            "score": {"value": score.score, "level": score.level},
            "best_practices": {
                "has_security_step": best.has_security_step,
                "has_dependency_scan": best.has_dependency_scan,
            },
            "secrets": [
                {
                    "step": finding.step_name,
                    "type": finding.secret_type,
                    "snippet": finding.snippet,
                }
                for finding in secrets
            ],
            "risky_steps": [
                {
                    "step": finding.step_name,
                    "rule": finding.rule_id,
                    "severity": finding.severity,
                    "description": finding.desc,
                }
                for finding in risky
            ],
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
