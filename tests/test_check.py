import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from product_qa.checks import check_product
from product_qa.report import Report


class ProductQaCheckTests(unittest.TestCase):
    def write_metadata(self, product: Path) -> None:
        (product / "product.json").write_text(
            json.dumps(
                {
                    "title": "Ready guide",
                    "author": "Digital Product Factory",
                    "version": "1.0.0",
                    "license": "CC0-1.0",
                }
            ),
            encoding="utf-8",
        )
        (product / "prompts.json").write_text(
            json.dumps(
                {
                    "prompts": [
                        {
                            "id": "ready",
                            "template": "Write a ready guide.",
                            "variables": [],
                            "example": {"input": {}, "output": "A ready guide."},
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )

    def test_complete_product_passes_and_has_a_versioned_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            product = Path(temporary_directory)
            (product / "guide.md").write_text("# Ready\n\nUseful content.", encoding="utf-8")
            self.write_metadata(product)

            report = check_product(product, "prompt-pack")

        self.assertEqual(report.exit_code, 0)
        self.assertEqual(report.to_dict()["schema_version"], "1.0")
        self.assertEqual(report.to_dict()["summary"]["blockers"], 0)

    def test_all_text_placeholders_and_latin1_text_are_blockers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            product = Path(temporary_directory)
            (product / "guide.md").write_text("TODO one\nTODO two\n[ISI]", encoding="utf-8")
            (product / "legacy.txt").write_bytes("TODO: café".encode("latin-1"))
            self.write_metadata(product)

            report = check_product(product, "prompt-pack")

        placeholders = [finding for finding in report.findings if finding.id == "placeholder"]
        self.assertEqual(report.exit_code, 1)
        self.assertEqual(len(placeholders), 4)

    def test_missing_and_unreadable_products_are_blockers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            product = Path(temporary_directory)
            file_path = product / "guide.md"
            file_path.write_text("Ready", encoding="utf-8")

            missing_report = check_product(product / "missing", "prompt-pack")
            with patch.object(Path, "read_bytes", side_effect=PermissionError):
                unreadable_report = check_product(product, "prompt-pack")

        self.assertEqual(missing_report.exit_code, 1)
        self.assertEqual(missing_report.findings[0].id, "product-path")
        self.assertEqual(unreadable_report.exit_code, 1)
        self.assertTrue(
            any(finding.id == "file-readable" for finding in unreadable_report.findings)
        )

    def test_empty_report_is_not_a_pass(self) -> None:
        self.assertEqual(Report("product", "prompt-pack", []).exit_code, 1)

    def test_cli_writes_json_outside_product_and_rejects_inside_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            workspace = Path(temporary_directory)
            product = workspace / "product"
            product.mkdir()
            output = workspace / "qa-report.json"
            inside_product = product / "qa-report.json"
            (product / "guide.md").write_text("[ISI]", encoding="utf-8")
            self.write_metadata(product)

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "product_qa",
                    "check",
                    str(product),
                    "--type",
                    "prompt-pack",
                    "--json-out",
                    str(output),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            rejected = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "product_qa",
                    "check",
                    str(product),
                    "--type",
                    "prompt-pack",
                    "--json-out",
                    str(inside_product),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            report = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(result.returncode, 1)
        self.assertIn("BLOCKED", result.stdout)
        self.assertEqual(report["summary"]["blockers"], 1)
        self.assertEqual(rejected.returncode, 2)
        self.assertFalse(inside_product.exists())


if __name__ == "__main__":
    unittest.main()
