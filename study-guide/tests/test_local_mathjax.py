from __future__ import annotations

from html.parser import HTMLParser
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit
import unittest


ROOT = Path(__file__).resolve().parents[1]
MKDOCS_CONFIG = ROOT / "mkdocs.yml"
LOCAL_RUNTIME = "assets/vendor/mathjax/es5/tex-mml-chtml.js"
REMOTE_RUNTIME_HOST = "unpkg.com"


class ExecutableResourceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.executable_resources: list[str] = []
        self.script_sources: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        attributes = dict(attrs)
        if tag == "script" and attributes.get("src"):
            source = attributes["src"]
            assert source is not None
            self.script_sources.append(source)
            self.executable_resources.append(source)
        if tag == "link" and attributes.get("href"):
            relationships = set((attributes.get("rel") or "").lower().split())
            if "stylesheet" in relationships:
                href = attributes["href"]
                assert href is not None
                self.executable_resources.append(href)


class LocalMathJaxTests(unittest.TestCase):
    def test_mathjax_runtime_is_vendored_and_built_pages_stay_local(self) -> None:
        config = MKDOCS_CONFIG.read_text(encoding="utf-8")
        self.assertNotIn(REMOTE_RUNTIME_HOST, config)
        self.assertIn(LOCAL_RUNTIME, config)

        runtime = ROOT / "docs" / LOCAL_RUNTIME
        license_path = ROOT / "docs" / "assets/vendor/mathjax/LICENSE"
        self.assertTrue(runtime.is_file())
        self.assertGreater(runtime.stat().st_size, 0)
        self.assertTrue(license_path.is_file())
        self.assertGreater(license_path.stat().st_size, 0)

        with tempfile.TemporaryDirectory() as temporary:
            site_dir = Path(temporary) / "site"
            environment = os.environ.copy()
            environment["NO_MKDOCS_2_WARNING"] = "1"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "mkdocs",
                    "build",
                    "--strict",
                    "--config-file",
                    str(MKDOCS_CONFIG),
                    "--site-dir",
                    str(site_dir),
                ],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            html_paths = sorted(site_dir.rglob("*.html"))
            self.assertTrue(html_paths)

            local_mathjax_references = 0
            third_party_resources: list[tuple[Path, str]] = []
            for html_path in html_paths:
                html = html_path.read_text(encoding="utf-8")
                self.assertNotIn(REMOTE_RUNTIME_HOST, html)
                parser = ExecutableResourceParser()
                parser.feed(html)
                local_mathjax_references += sum(
                    urlsplit(source).path.endswith(LOCAL_RUNTIME)
                    for source in parser.script_sources
                )
                third_party_resources.extend(
                    (html_path.relative_to(site_dir), resource)
                    for resource in parser.executable_resources
                    if urlsplit(resource).scheme.lower() in {"http", "https"}
                )

            self.assertEqual(local_mathjax_references, len(html_paths))
            self.assertEqual(third_party_resources, [])
            print(f"BUILT_HTML_COUNT={len(html_paths)}")
            print(f"REMOTE_RESOURCE_COUNT={len(third_party_resources)}")


if __name__ == "__main__":
    unittest.main()
