"""Pipeline parser for CI/CD configuration files."""

import os
from typing import Any, Dict, List

import yaml


class PipelineType:
    """Enumeration of supported pipeline types."""

    GITHUB = "github_actions"
    GITLAB = "gitlab_ci"
    UNKNOWN = "unknown"


class PipelineParser:
    """Parse CI/CD pipeline YAML files into normalized steps."""

    def __init__(self, path: str) -> None:
        self.path: str = path
        self.raw: Any = None
        self.pipeline_type: str = PipelineType.UNKNOWN
        self.steps: List[Dict[str, Any]] = []

    def load(self) -> None:
        """Load the YAML file, detect its type, and extract steps."""

        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path)

        with open(self.path, "r", encoding="utf-8") as file:
            self.raw = yaml.safe_load(file)

        self._detect_type()
        self._extract_steps()

    def _detect_type(self) -> None:
        """Detect the pipeline type based on loaded YAML content."""

        if isinstance(self.raw, dict):
            if "jobs" in self.raw and "on" in self.raw:
                self.pipeline_type = PipelineType.GITHUB
                return

            if any(isinstance(value, dict) and "script" in value for value in self.raw.values()):
                self.pipeline_type = PipelineType.GITLAB
                return

        self.pipeline_type = PipelineType.UNKNOWN

    def _extract_steps(self) -> None:
        """Extract normalized steps according to the detected pipeline type."""

        self.steps = []

        if self.pipeline_type == PipelineType.GITHUB:
            self._extract_github()
        elif self.pipeline_type == PipelineType.GITLAB:
            self._extract_gitlab()
        else:
            self._extract_unknown()

    def _extract_github(self) -> None:
        """Extract steps from a GitHub Actions workflow."""

        jobs = self.raw.get("jobs", {}) if isinstance(self.raw, dict) else {}

        if not isinstance(jobs, dict):
            return

        for job_name, job_conf in jobs.items():
            if not isinstance(job_conf, dict):
                continue

            job_env = job_conf.get("env", {})
            step_list = job_conf.get("steps", [])

            if not isinstance(step_list, list):
                continue

            for step in step_list:
                if not isinstance(step, dict):
                    continue

                name = step.get("name") or f"{job_name}_step"
                run_cmd = step.get("run", "")
                env: Dict[str, Any] = {}

                if isinstance(job_env, dict):
                    env.update(job_env)

                if isinstance(step.get("env"), dict):
                    env.update(step.get("env", {}))

                if run_cmd:
                    self.steps.append(
                        {
                            "name": str(name),
                            "script": str(run_cmd),
                            "env": env,
                        }
                    )

    def _extract_gitlab(self) -> None:
        """Extract steps from a GitLab CI pipeline configuration."""

        if not isinstance(self.raw, dict):
            return

        for job_name, job_conf in self.raw.items():
            if not isinstance(job_conf, dict):
                continue

            scripts = job_conf.get("script")

            if scripts is None:
                continue

            if isinstance(scripts, list):
                script_text = "\n".join(str(item) for item in scripts)
            else:
                script_text = str(scripts)

            env = job_conf.get("variables", {})

            if not isinstance(env, dict):
                env = {}

            self.steps.append(
                {
                    "name": str(job_name),
                    "script": script_text,
                    "env": env,
                }
            )

    def _extract_unknown(self) -> None:
        """Attempt to extract steps from an unknown pipeline format."""

        if not isinstance(self.raw, dict):
            return

        for value in self.raw.values():
            if not isinstance(value, dict):
                continue

            scripts = value.get("script")

            if scripts is None:
                continue

            if isinstance(scripts, list):
                script_text = "\n".join(str(item) for item in scripts)
            else:
                script_text = str(scripts)

            env = value.get("variables", {})

            if not isinstance(env, dict):
                env = {}

            self.steps.append(
                {
                    "name": str(value.get("name", "unknown_step")),
                    "script": script_text,
                    "env": env,
                }
            )
