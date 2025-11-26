import argparse
import os

from pipeline_parser import PipelineParser
from secret_scanner import SecretScanner
from risky_step_checker import RiskyStepChecker
from best_practice_checker import BestPracticeChecker
from score_calculator import ScoreCalculator
from report import Reporter


def main() -> None:
    """Entry point CLI for the CI/CD Security Checker tool."""
    parser = argparse.ArgumentParser(
        description="CI/CD Security Checker - Demo tool for pipeline security analysis"
    )
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="Path to CI/CD pipeline YAML file (.gitlab-ci.yml, GitHub Actions workflow, etc.)",
    )
    parser.add_argument(
        "--json-report",
        help="Optional path to save the security report as a JSON file",
    )
    args = parser.parse_args()

    pipeline_path = args.file
    if not os.path.exists(pipeline_path):
        print(f"Error: file '{pipeline_path}' does not exist.")
        return

    parser_obj = PipelineParser(pipeline_path)
    try:
        parser_obj.load()
    except Exception as exc:
        print(f"Error parsing pipeline file: {exc}")
        return

    steps = parser_obj.steps

    secrets = SecretScanner.scan_all(steps)
    risky = RiskyStepChecker.scan_all(steps)
    best = BestPracticeChecker.analyze(steps)
    score = ScoreCalculator.calculate(
        secrets=secrets,
        risky_steps=risky,
        best_practice=best,
    )

    Reporter.print_human_readable(
        score=score,
        secrets=secrets,
        risky=risky,
        best=best,
    )

    if args.json_report:
        Reporter.to_json(
            path=args.json_report,
            score=score,
            secrets=secrets,
            risky=risky,
            best=best,
        )
        print(f"\nJSON report saved to: {args.json_report}")


if __name__ == "__main__":
    main()
