import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import zipfile

from product_qa.checks import check_product


WORKBOOK = """<?xml version='1.0' encoding='UTF-8'?>
<workbook xmlns='http://schemas.openxmlformats.org/spreadsheetml/2006/main' xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships'>
  <sheets><sheet name='Instructions' sheetId='1' r:id='rId1'/><sheet name='Budget' sheetId='2' r:id='rId2'/></sheets>
</workbook>"""
RELS = """<?xml version='1.0' encoding='UTF-8'?>
<Relationships xmlns='http://schemas.openxmlformats.org/package/2006/relationships'>
  <Relationship Id='rId1' Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet' Target='worksheets/sheet1.xml'/>
  <Relationship Id='rId2' Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet' Target='worksheets/sheet2.xml'/>
</Relationships>"""


class SpreadsheetChecksTests(unittest.TestCase):
    def write_product(self, product: Path, formula_error: str = "") -> None:
        (product / "product.json").write_text(
            json.dumps(
                {
                    "title": "Budget template",
                    "author": "Digital Product Factory",
                    "version": "1.0.0",
                    "license": "CC0-1.0",
                    "input_cells": ["Budget!B2"],
                }
            ),
            encoding="utf-8",
        )
        with zipfile.ZipFile(product / "budget.xlsx", "w") as workbook:
            workbook.writestr("xl/workbook.xml", WORKBOOK)
            workbook.writestr("xl/_rels/workbook.xml.rels", RELS)
            workbook.writestr(
                "xl/worksheets/sheet1.xml",
                "<worksheet><sheetData><row r='1'><c r='A1' t='inlineStr'><is><t>Instructions</t></is></c></row></sheetData></worksheet>",
            )
            workbook.writestr(
                "xl/worksheets/sheet2.xml",
                "<worksheet><sheetData><row r='1'><c r='A1' t='inlineStr'><is><t>Sample</t></is></c></row><row r='2'><c r='B2'><v>100</v></c></row></sheetData>"
                f"{formula_error}</worksheet>",
            )

    def test_valid_xlsx_passes_with_available_formula_engine(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            product = Path(temporary_directory)
            self.write_product(product)
            with patch("product_qa.product_checks._xlsx_external_findings", return_value=[]):
                report = check_product(product, "xlsx")

        self.assertEqual(report.exit_code, 0)
        self.assertTrue(any(finding.id == "xlsx" and finding.status == "pass" for finding in report.findings))

    def test_xlsx_formula_error_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            product = Path(temporary_directory)
            self.write_product(product, "<row r='3'><c r='B3' t='e'><v>#VALUE!</v></c></row>")
            with patch("product_qa.product_checks._xlsx_external_findings", return_value=[]):
                report = check_product(product, "xlsx")

        self.assertEqual(report.exit_code, 1)
        self.assertTrue(any(finding.id == "xlsx-formula-error" for finding in report.findings))

    def test_xlsx_placeholder_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            product = Path(temporary_directory)
            self.write_product(product, "<row r='3'><c r='B3' t='inlineStr'><is><t>TODO fix me</t></is></c></row>")
            with patch("product_qa.product_checks._xlsx_external_findings", return_value=[]):
                report = check_product(product, "xlsx")

        self.assertEqual(report.exit_code, 1)
        self.assertTrue(any(finding.id == "placeholder" for finding in report.findings))
    def test_xlsx_external_adapter_rechecks_converted_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            product = Path(temporary_directory)
            self.write_product(product)

            def convert(command: list[str], **_: object) -> SimpleNamespace:
                output = Path(command[command.index("--outdir") + 1])
                shutil.copyfile(product / "budget.xlsx", output / "budget.xlsx")
                return SimpleNamespace(returncode=0)

            with patch("product_qa.product_checks.tool_path", return_value="soffice"), patch(
                "product_qa.product_checks.subprocess.run", side_effect=convert
            ):
                report = check_product(product, "xlsx")

        self.assertEqual(report.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
