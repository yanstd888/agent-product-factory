import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import zipfile

from product_qa.checks import check_product


class EbookChecksTests(unittest.TestCase):
    def write_product(
        self, product: Path, broken_link: bool = False, chapter_broken_link: bool = False,
        chapter_placeholder: bool = False,
    ) -> None:
        (product / "product.json").write_text(
            json.dumps(
                {
                    "title": "Tiny ebook",
                    "author": "Digital Product Factory",
                    "version": "1.0.0",
                    "license": "CC0-1.0",
                }
            ),
            encoding="utf-8",
        )
        with zipfile.ZipFile(product / "book.epub", "w") as ebook:
            ebook.writestr(
                zipfile.ZipInfo("mimetype"),
                "application/epub+zip",
                compress_type=zipfile.ZIP_STORED,
            )
            ebook.writestr(
                "META-INF/container.xml",
                "<container><rootfiles><rootfile full-path='OEBPS/content.opf'/></rootfiles></container>",
            )
            ebook.writestr(
                "OEBPS/content.opf",
                "<package><manifest><item id='nav' href='nav.xhtml' properties='nav'/><item id='chapter' href='chapter.xhtml'/></manifest><spine><itemref idref='chapter'/></spine></package>",
            )
            target = "missing.xhtml" if broken_link else "chapter.xhtml"
            ebook.writestr("OEBPS/nav.xhtml", f"<html><body><a href='{target}'>Chapter</a></body></html>")
            chapter_target = "<a href='missing.xhtml'>Missing</a>" if chapter_broken_link else ""
            chapter_body = "TODO finish" if chapter_placeholder else ""
            ebook.writestr("OEBPS/chapter.xhtml", f"<html><body><h1 id='start'>Chapter</h1>{chapter_target}{chapter_body}</body></html>")
        (product / "book.pdf").write_bytes(b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\n%%EOF\n")

    def test_valid_ebook_passes_with_available_tools(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            product = Path(temporary_directory)
            self.write_product(product)
            with patch("product_qa.product_checks._ebook_external_findings", return_value=[]):
                report = check_product(product, "ebook")

        self.assertEqual(report.exit_code, 0)
        self.assertTrue(any(finding.id == "ebook" and finding.status == "pass" for finding in report.findings))

    def test_broken_internal_link_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            product = Path(temporary_directory)
            self.write_product(product, broken_link=True)
            with patch("product_qa.product_checks._ebook_external_findings", return_value=[]):
                report = check_product(product, "ebook")

        self.assertEqual(report.exit_code, 1)
        self.assertTrue(any(finding.id == "ebook-link" for finding in report.findings))
    def test_broken_chapter_link_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            product = Path(temporary_directory)
            self.write_product(product, chapter_broken_link=True)
            with patch("product_qa.product_checks._ebook_external_findings", return_value=[]):
                report = check_product(product, "ebook")

        self.assertEqual(report.exit_code, 1)
        self.assertTrue(any(finding.id == "ebook-link" for finding in report.findings))
    def test_ebook_placeholder_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            product = Path(temporary_directory)
            self.write_product(product, chapter_placeholder=True)
            with patch("product_qa.product_checks._ebook_external_findings", return_value=[]):
                report = check_product(product, "ebook")

        self.assertEqual(report.exit_code, 1)
        self.assertTrue(any(finding.id == "placeholder" for finding in report.findings))

    def test_ebook_external_adapter_runs_epubcheck(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            product = Path(temporary_directory)
            self.write_product(product)
            with patch("product_qa.product_checks.tool_path", side_effect=["pandoc", "epubcheck"]), patch(
                "product_qa.product_checks.subprocess.run", return_value=SimpleNamespace(returncode=0)
            ):
                report = check_product(product, "ebook")

        self.assertEqual(report.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
