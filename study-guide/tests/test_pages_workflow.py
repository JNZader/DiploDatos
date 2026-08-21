from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_PATH = REPOSITORY_ROOT / ".github" / "workflows" / "pages.yml"


class PagesWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
        if not isinstance(cls.workflow, dict):
            raise AssertionError("Pages workflow must parse as a YAML mapping")

    def test_triggers_are_scoped_to_study_guide_on_main(self) -> None:
        triggers = self.workflow["on"]
        self.assertIn("workflow_dispatch", triggers)
        self.assertEqual(triggers["push"]["branches"], ["main"])
        self.assertEqual(
            set(triggers["push"]["paths"]),
            {"study-guide/**", ".github/workflows/pages.yml"},
        )

    def test_current_official_pages_actions_are_pinned(self) -> None:
        uses = [
            step["uses"]
            for job in self.workflow["jobs"].values()
            for step in job.get("steps", [])
            if "uses" in step
        ]
        checkout = next(value for value in uses if value.startswith("actions/checkout@"))
        match = re.fullmatch(r"actions/checkout@v(\d+)", checkout)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertGreaterEqual(int(match.group(1)), 6)
        self.assertIn("actions/configure-pages@v5", uses)
        self.assertIn("actions/upload-pages-artifact@v4", uses)
        self.assertIn("actions/deploy-pages@v4", uses)

    def test_build_and_upload_are_isolated_to_the_reader(self) -> None:
        build = self.workflow["jobs"]["build"]
        self.assertEqual(
            build["defaults"]["run"]["working-directory"],
            "study-guide",
        )
        self.assertEqual(build["env"]["SITE_DIR"], "${{ github.workspace }}/.pages-site")

        steps = {step["name"]: step for step in build["steps"]}
        self.assertIn(
            "python -m pip install --requirement requirements.txt",
            steps["Install dependencies"]["run"],
        )
        build_command = steps["Build strict site"]["run"]
        self.assertIn("python -m mkdocs build --strict", build_command)
        self.assertIn("--config-file mkdocs.yml", build_command)
        self.assertIn('--site-dir "$SITE_DIR"', build_command)
        self.assertIn(
            "python -m unittest discover -s tests -v",
            steps["Run focused tests"]["run"],
        )
        self.assertEqual(
            steps["Upload Pages artifact"]["with"]["path"],
            "${{ env.SITE_DIR }}",
        )

    def test_deploy_permissions_environment_and_smoke_check_are_bounded(self) -> None:
        deploy = self.workflow["jobs"]["deploy"]
        self.assertEqual(deploy["needs"], "build")
        self.assertEqual(deploy["environment"]["name"], "github-pages")
        self.assertEqual(deploy["permissions"]["pages"], "write")
        self.assertEqual(deploy["permissions"]["id-token"], "write")
        deployment = next(step for step in deploy["steps"] if step.get("id") == "deployment")
        self.assertEqual(deployment["uses"], "actions/deploy-pages@v4")

        smoke = self.workflow["jobs"]["smoke"]
        self.assertEqual(smoke["needs"], "deploy")
        command = smoke["steps"][0]["run"]
        self.assertIn("for attempt in 1 2 3 4 5", command)
        self.assertIn("curl --fail", command)
        self.assertIn("--connect-timeout 10", command)
        self.assertIn("--max-time 20", command)
        print("WORKFLOW_YAML=PASS")


if __name__ == "__main__":
    unittest.main()
