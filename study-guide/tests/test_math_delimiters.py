"""Regression guard for batch D1: broken math delimiters in the study guide.

Broken patterns this batch fixed in materias 03 and 04 (the pages it owns):
  1. Display math written as bare lines `[` / `]` — pymdownx.arithmatex
     (generic) does NOT recognise a lone bracket; the block never renders.
  2. Inline math written as plain `(...)` containing LaTeX (backslash
     commands, `_`, `^`, `{`) — arithmatex only converts `$...$`, `$$...$$`,
     `\(...\)` and `\[...\]`; a plain paren group stays literal text.
  3. Raw `\(...\)` (mangled `\bar M\)` at 03:880) normalised to `$...$`.

Not broken, and deliberately NOT flagged:
  - `\(...\)` / `\[...\]`: native arithmatex (generic) syntax, verified in
    the built HTML as `<span class="arithmatex">…</span>`.
  - `[^...]` footnotes (footnotes extension is enabled) — never touched.
  - Prose parentheticals and inline code / fenced code blocks.

Calibration discovery (resolved in batch D2): pages 05, 06 and 08 carried the same
`(...)`-LaTeX style (05: ~72 hits, 06: ~12, 08: 1) and were reported out of scope by
this batch. D2 fixed them, so the expected out-of-scope set is now empty; the scan
still reports any future page that regresses to the broken style.
"""

from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATERIAS = sorted((ROOT / "docs" / "materias").glob("*.md"))

# Files this batch fixed. Hard assertions apply to these only.
BATCH_FILES = {"03-introduccion-aprendizaje.md", "04-aprendizaje-supervisado.md"}
# Pages that still carry the broken style, out of scope for this batch.
# Batch D2 fixed 05/06/08, so the set is empty; the scan above keeps
# reporting any future regression and this assertion fails loudly.
EXPECTED_OUT_OF_SCOPE: set[str] = set()

INLINE_MATH_RE = re.compile(r"\$[^$\n]+\$")
CODE_SPAN_RE = re.compile(r"`[^`]*`")
PAREN_LATEX_RE = re.compile(r"[\\_{}]")
DISPLAY_MARKERS = {"$$", "\\[", "\\]"}


def scan_page(path: Path) -> list[tuple[int, str, str]]:
    """Return [(line, kind, snippet)] broken-math findings for one page.

    kind is "display-bracket" (bare `[`/`]` line) or "paren-latex"
    (plain `(...)` group whose content is LaTeX). Fenced code, `$$...$$`
    and `\[...\]` display blocks, inline `$...$` and `` `code` `` spans,
    and raw `\(...\)` are all skipped.
    """
    findings: list[tuple[int, str, str]] = []
    in_fence = False
    in_display = False
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if in_display:
            if stripped in DISPLAY_MARKERS:
                in_display = False
            continue
        if stripped in DISPLAY_MARKERS:
            in_display = True
            continue
        if stripped in ("[", "]"):
            findings.append((lineno, "display-bracket", stripped))
            continue
        masked = INLINE_MATH_RE.sub("\x00MATH\x00", raw)
        masked = CODE_SPAN_RE.sub("\x00CODE\x00", masked)
        i, n = 0, len(masked)
        while i < n:
            if masked[i] != "(":
                i += 1
                continue
            depth = 0
            j = i
            while j < n:
                if masked[j] == "(":
                    depth += 1
                elif masked[j] == ")":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if j >= n:
                i += 1
                continue
            content = masked[i + 1 : j]
            # Raw \(...\) is legit arithmatex syntax: backslash glued to the
            # opener and to the closer.
            legit_raw = i > 0 and masked[i - 1] == "\\" and content.endswith("\\")
            if not legit_raw and PAREN_LATEX_RE.search(content):
                findings.append((lineno, "paren-latex", masked[i : j + 1][:60]))
            i = j + 1
    return findings


class MathDelimiterTests(unittest.TestCase):
    def test_batch_pages_have_no_broken_math_delimiters(self) -> None:
        """Regression guard: fails on the pre-fix style of materias 03/04."""
        for path in MATERIAS:
            if path.name not in BATCH_FILES:
                continue
            findings = scan_page(path)
            self.assertEqual(
                findings,
                [],
                f"{path.name} still has broken math delimiters: {findings[:5]}",
            )

    def test_out_of_scope_pages_are_reported(self) -> None:
        """Scan every materia page; report (not assert) the out-of-scope ones."""
        out_of_scope: dict[str, list[tuple[int, str, str]]] = {}
        for path in MATERIAS:
            if path.name in BATCH_FILES:
                continue
            findings = scan_page(path)
            if findings:
                out_of_scope[path.name] = findings
        for name, findings in sorted(out_of_scope.items()):
            print(f"OUT_OF_SCOPE_FINDING {name}: {len(findings)} hits")
            for lineno, kind, snippet in findings[:5]:
                print(f"  L{lineno} [{kind}] {snippet}")
        self.assertEqual(
            set(out_of_scope),
            EXPECTED_OUT_OF_SCOPE,
            "Out-of-scope pages changed: update EXPECTED_OUT_OF_SCOPE (or fix the pages "
            "in the follow-up batch).",
        )

    def test_detector_flags_pre_fix_style(self) -> None:
        """The broken style must be detected (fails = detector works)."""
        pre_fix = (
            "[\n"
            "X = \\begin{bmatrix}x_{11} & x_{12}\\end{bmatrix}\n"
            "]\n"
            "- (x_i) es la entrada del caso (i);\n"
            "- (mathcal{X}) es el espacio;\n"
            "- (P(y=c\\mid x)): posterior;\n"
            "- (\\bar M\\) resume.\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "page.md"
            page.write_text(pre_fix, encoding="utf-8")
            findings = scan_page(page)
        kinds = sorted({kind for _, kind, _ in findings})
        self.assertIn("display-bracket", kinds)
        self.assertIn("paren-latex", kinds)
        self.assertGreaterEqual(len(findings), 4)

    def test_detector_accepts_post_fix_style(self) -> None:
        """The fixed style must be clean (passes = detector does not overreach)."""
        post_fix = (
            "$$\n"
            "X = \\begin{bmatrix}x_{11} & x_{12}\\end{bmatrix}\n"
            "$$\n"
            "- $x_i$ es la entrada del caso $i$;\n"
            "- $\\mathcal{X}$ es el espacio;\n"
            "- $P(y=c\\mid x)$: posterior;\n"
            "- $\\bar M$ resume.\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "page.md"
            page.write_text(post_fix, encoding="utf-8")
            findings = scan_page(page)
        self.assertEqual(findings, [])

    def test_raw_arithmatex_delimiters_are_not_flagged(self) -> None:
        """\(...\) and \[...\] are legit arithmatex syntax — never flagged."""
        legit = (
            "- \\(\\bar M\\) resume el desempeño promedio.\n"
            "\\[\n"
            "z = b + w_1x_1\n"
            "\\]\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "page.md"
            page.write_text(legit, encoding="utf-8")
            findings = scan_page(page)
        self.assertEqual(findings, [])

    def test_footnote_syntax_is_never_flagged(self) -> None:
        """`[^...]` footnotes must not be mistaken for display brackets."""
        with_footnote = (
            "Un texto con nota al pie[^1].\n"
            "\n"
            "[^1]: La referencia, nunca tocada.\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "page.md"
            page.write_text(with_footnote, encoding="utf-8")
            findings = scan_page(page)
        self.assertEqual(findings, [])

    def test_prose_parens_are_not_flagged(self) -> None:
        """Plain prose parentheticals (no LaTeX) are never flagged."""
        prose = (
            "El caso (cursada 2026) se cita así (ver sección 2).\n"
            "La fecha (2026) y el número (4) no son matemática.\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "page.md"
            page.write_text(prose, encoding="utf-8")
            findings = scan_page(page)
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()