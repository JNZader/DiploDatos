from __future__ import annotations

import importlib.util
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "sync_guide.py"
SPEC = importlib.util.spec_from_file_location("sync_guide", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
sync_guide = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync_guide
SPEC.loader.exec_module(sync_guide)
ROOT = MODULE_PATH.parents[1]


class SyncGuideTests(unittest.TestCase):
    def canonical_shape(self, order: list[int] | None = None) -> str:
        indexes = order or list(range(1, len(sync_guide.PAGE_SPECS)))
        sections = ["# Guía de estudio\n\nApertura del libro.\n\n"]
        for index in indexes:
            spec = sync_guide.PAGE_SPECS[index]
            sections.append(f"{spec.boundary}\n\nContenido de prueba {index}.\n\n")
        return "".join(sections)

    def test_missing_boundary_is_rejected(self) -> None:
        text = self.canonical_shape().replace(
            sync_guide.PAGE_SPECS[3].boundary,
            "# Materia ausente",
            1,
        )
        with self.assertRaisesRegex(sync_guide.GuideStructureError, "Missing boundary"):
            sync_guide.partition_text(text)

    def test_duplicate_boundary_is_rejected(self) -> None:
        boundary = sync_guide.PAGE_SPECS[2].boundary
        text = self.canonical_shape() + f"{boundary}\nDuplicado.\n"
        with self.assertRaisesRegex(sync_guide.GuideStructureError, "Duplicate boundary"):
            sync_guide.partition_text(text)

    def test_out_of_order_boundaries_are_rejected(self) -> None:
        order = list(range(1, len(sync_guide.PAGE_SPECS)))
        order[2], order[3] = order[3], order[2]
        with self.assertRaisesRegex(sync_guide.GuideStructureError, "out of order"):
            sync_guide.partition_text(self.canonical_shape(order))

    def test_partition_reconstructs_source_exactly(self) -> None:
        text = self.canonical_shape()
        pages = sync_guide.partition_text(text)
        self.assertEqual(len(pages), 9)
        self.assertEqual("".join(pages), text)

    def test_generation_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source = base / "guide.md"
            source.write_text(self.canonical_shape(), encoding="utf-8", newline="\n")
            first = base / "first"
            second = base / "second"
            sync_guide.write_generated_pages(source, first)
            sync_guide.write_generated_pages(source, second)

            relative_files = [spec.path for spec in sync_guide.PAGE_SPECS] + ["source-manifest.json"]
            for relative in relative_files:
                self.assertEqual((first / relative).read_bytes(), (second / relative).read_bytes())

    def test_manifest_omits_absolute_source_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source = base / "private" / "guide.md"
            source.parent.mkdir()
            source.write_text(self.canonical_shape(), encoding="utf-8", newline="\n")
            destination = base / "site"
            sync_guide.write_generated_pages(source, destination)

            raw_manifest = (destination / "source-manifest.json").read_text(encoding="utf-8")
            manifest = json.loads(raw_manifest)
            self.assertEqual(manifest["source"]["filename"], "guide.md")
            self.assertNotIn(str(source.resolve()), raw_manifest)
            self.assertNotIn(str(base.resolve()), raw_manifest)

    def test_canonical_metric_mismatch_is_rejected(self) -> None:
        metrics = sync_guide.source_metrics(self.canonical_shape().encode("utf-8"))
        with self.assertRaisesRegex(sync_guide.GuideStructureError, "counts do not match"):
            sync_guide.validate_canonical_metrics(metrics)

    def test_committed_pages_reconstruct_verified_source_without_canonical_file(self) -> None:
        manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        reconstructed = sync_guide.read_generated_pages(ROOT)
        metrics = sync_guide.source_metrics(reconstructed)

        self.assertEqual(len(sync_guide.PAGE_SPECS), 9)
        self.assertEqual(metrics["sha256"], sync_guide.EXPECTED_SHA256)
        self.assertEqual(metrics["words"], sync_guide.EXPECTED_WORDS)
        self.assertEqual(metrics["lines"], sync_guide.EXPECTED_LINES)
        self.assertEqual(metrics["headings"], sync_guide.EXPECTED_HEADINGS)
        self.assertTrue(manifest["reconstruction_match"])
        self.assertEqual(
            manifest["source"],
            {
                "bytes": len(reconstructed),
                "filename": "GUIA_ESTUDIO_DIPLO_MENTORIA_SAIJ.md",
                **metrics,
            },
        )

        for spec, entry in zip(sync_guide.PAGE_SPECS, manifest["generated_pages"], strict=True):
            page = (ROOT / spec.path).read_bytes()
            self.assertEqual(entry["path"], spec.path.removeprefix("docs/"))
            self.assertEqual(entry["bytes"], len(page))
            self.assertEqual(entry["sha256"], hashlib.sha256(page).hexdigest())

        print(f"DOC_MD_COUNT={len(sync_guide.PAGE_SPECS)}")
        print(f"RECONSTRUCTION_SHA256={metrics['sha256']}")
        print(f"RECONSTRUCTION_WORDS={metrics['words']}")


if __name__ == "__main__":
    unittest.main()
