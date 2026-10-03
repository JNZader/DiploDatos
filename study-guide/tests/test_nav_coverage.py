from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "sync_guide.py"
SPEC = importlib.util.spec_from_file_location("sync_guide", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
sync_guide = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync_guide
SPEC.loader.exec_module(sync_guide)

MKDOCS_PATH = ROOT / "mkdocs.yml"
UNVERIFIED = {
    "docs/materias/07-aws-ml-foundations.md",
    "docs/materias/08-llms-aplicaciones.md",
    "docs/materias/09-bigdata-spark.md",
}


def _iter_nav_targets(node: object):
    if isinstance(node, str):
        if node.endswith(".md"):
            yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from _iter_nav_targets(value)
    elif isinstance(node, (list, tuple)):
        for item in node:
            yield from _iter_nav_targets(item)


class NavCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        config = yaml.safe_load(MKDOCS_PATH.read_text(encoding="utf-8"))
        if not isinstance(config, dict) or "nav" not in config:
            raise AssertionError("mkdocs.yml must define a nav mapping")
        cls.targets = [f"docs/{target}" for target in _iter_nav_targets(config["nav"])]

    def test_nav_defines_markdown_targets(self) -> None:
        self.assertTrue(self.targets, "mkdocs.yml nav defines no Markdown targets")

    def test_every_nav_target_is_verified_or_explicitly_unverified(self) -> None:
        page_paths = {spec.path for spec in sync_guide.PAGE_SPECS}
        for target in self.targets:
            with self.subTest(target=target):
                self.assertTrue(
                    target in page_paths or target in UNVERIFIED,
                    f"Nav target not covered by PAGE_SPECS or UNVERIFIED: {target}",
                )

    def test_every_page_spec_is_reachable_from_nav(self) -> None:
        page_paths = {spec.path for spec in sync_guide.PAGE_SPECS}
        missing = sorted(page_paths - set(self.targets))
        self.assertEqual(
            missing,
            [],
            f"PAGE_SPECS paths missing from mkdocs.yml nav: {missing}",
        )


if __name__ == "__main__":
    unittest.main()
