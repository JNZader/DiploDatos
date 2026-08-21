#!/usr/bin/env python3
"""Deterministically split the canonical DiploDatos guide into MkDocs pages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SHA256 = "6117a7f38316943c701529ce2c2195a9e439a76ab370c124c0701d1dc28ac04c"
EXPECTED_WORDS = 85_050
EXPECTED_LINES = 12_349
EXPECTED_HEADINGS = 1_201


@dataclass(frozen=True)
class PageSpec:
    path: str
    boundary: str | None


PAGE_SPECS: tuple[PageSpec, ...] = (
    PageSpec("docs/index.md", None),
    PageSpec("docs/materias/01-analisis-visualizacion.md", "# Materia 1 — Análisis y Visualización de Datos"),
    PageSpec("docs/materias/02-exploracion-curacion.md", "# Materia 2 — Análisis Exploratorio y Curación de Datos"),
    PageSpec("docs/materias/03-introduccion-aprendizaje.md", "# Materia 3 — Introducción al Aprendizaje Automático"),
    PageSpec("docs/materias/04-aprendizaje-supervisado.md", "# Materia 4 — Aprendizaje Supervisado"),
    PageSpec("docs/materias/05-aprendizaje-no-supervisado.md", "# Materia 5 — Aprendizaje No Supervisado"),
    PageSpec("docs/materias/06-etica-practica.md", "# Materia 6 — Ética Práctica en Ciencia de Datos"),
    PageSpec("docs/proyecto-integrador.md", "# Proyecto integrador — búsqueda semántica y RAG"),
    PageSpec("docs/apendice.md", "# Apéndice opcional — Trazabilidad de materiales"),
)


class GuideStructureError(ValueError):
    """Raised when the source cannot be partitioned without guessing."""


def source_metrics(raw: bytes) -> dict[str, int | str]:
    text = raw.decode("utf-8")
    return {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "words": len(re.findall(r"\S+", text)),
        "lines": len(text.splitlines()),
        "headings": len(re.findall(r"(?m)^#{1,6}\s+", text)),
    }


def validate_canonical_metrics(metrics: dict[str, int | str]) -> None:
    expected = {
        "sha256": EXPECTED_SHA256,
        "words": EXPECTED_WORDS,
        "lines": EXPECTED_LINES,
        "headings": EXPECTED_HEADINGS,
    }
    mismatches = [
        f"{name}={metrics[name]} (expected {value})"
        for name, value in expected.items()
        if metrics[name] != value
    ]
    if mismatches:
        raise GuideStructureError("Canonical source counts do not match: " + ", ".join(mismatches))


def read_generated_pages(destination: Path = PROJECT_ROOT) -> bytes:
    """Reconstruct the canonical bytes from the committed page set."""
    return b"".join((destination / spec.path).read_bytes() for spec in PAGE_SPECS)


def _boundary_positions(text: str, specs: Sequence[PageSpec] = PAGE_SPECS) -> list[int]:
    positions: list[int] = []
    for spec in specs[1:]:
        assert spec.boundary is not None
        pattern = re.compile(rf"(?m)^{re.escape(spec.boundary)}(?=\r?$)")
        matches = list(pattern.finditer(text))
        if not matches:
            raise GuideStructureError(f"Missing boundary: {spec.boundary}")
        if len(matches) > 1:
            raise GuideStructureError(f"Duplicate boundary: {spec.boundary}")
        positions.append(matches[0].start())

    if positions != sorted(positions):
        raise GuideStructureError("Canonical boundaries are out of order")
    return positions


def partition_text(text: str, specs: Sequence[PageSpec] = PAGE_SPECS) -> list[str]:
    starts = [0, *_boundary_positions(text, specs)]
    ends = [*starts[1:], len(text)]
    pages = [text[start:end] for start, end in zip(starts, ends, strict=True)]
    if len(pages) != len(specs) or "".join(pages) != text:
        raise GuideStructureError("Partition failed exact reconstruction")
    return pages


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def write_generated_pages(source: Path, destination: Path = PROJECT_ROOT) -> dict[str, object]:
    raw = source.read_bytes()
    text = raw.decode("utf-8")
    metrics = source_metrics(raw)
    pages = partition_text(text)

    mapping: list[dict[str, object]] = []
    offset = 0
    for spec, page in zip(PAGE_SPECS, pages, strict=True):
        page_bytes = page.encode("utf-8")
        target = destination / spec.path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(page_bytes)
        mapping.append(
            {
                "path": spec.path.removeprefix("docs/"),
                "boundary": spec.boundary,
                "start_line": _line_number(text, offset),
                "end_line": _line_number(text, offset + max(len(page) - 1, 0)),
                "bytes": len(page_bytes),
                "sha256": hashlib.sha256(page_bytes).hexdigest(),
            }
        )
        offset += len(page)

    generated_raw = read_generated_pages(destination)
    reconstruction_match = generated_raw == raw
    if not reconstruction_match:
        raise GuideStructureError("Generated pages do not reconstruct the source byte-for-byte")

    manifest: dict[str, object] = {
        "source": {
            "filename": source.name,
            **metrics,
        },
        "generated_pages": mapping,
        "reconstruction_match": reconstruction_match,
    }
    manifest_path = destination / "source-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Canonical UTF-8 Markdown guide")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.source.is_file():
        raise SystemExit(f"Source file does not exist: {args.source}")

    raw = args.source.read_bytes()
    metrics = source_metrics(raw)
    try:
        validate_canonical_metrics(metrics)
        manifest = write_generated_pages(args.source)
    except (GuideStructureError, UnicodeDecodeError) as error:
        raise SystemExit(f"ERROR={error}") from error

    print(f"SOURCE_SHA256={manifest['source']['sha256']}")
    print(f"SOURCE_WORDS={manifest['source']['words']}")
    print(f"SOURCE_LINES={manifest['source']['lines']}")
    print(f"SOURCE_HEADINGS={manifest['source']['headings']}")
    print(f"GENERATED_PAGES={len(manifest['generated_pages'])}")
    print("RECONSTRUCTION_MATCH=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
