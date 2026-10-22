import json
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1] / "examples"
ZIP_EPOCH = (1980, 1, 1, 0, 0, 0)
METADATA = {
    "title": "Digital Product Factory example",
    "author": "Digital Product Factory",
    "version": "1.0.0",
    "license": "CC0-1.0",
}


def write_json(path: Path, data: dict[str, object]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_zip(archive: zipfile.ZipFile, name: str, content: str, compression: int = zipfile.ZIP_DEFLATED) -> None:
    entry = zipfile.ZipInfo(name, ZIP_EPOCH)
    entry.compress_type = compression
    archive.writestr(entry, content)


def prompt_pack() -> None:
    product = ROOT / "prompt-pack"
    product.mkdir(parents=True, exist_ok=True)
    write_json(product / "product.json", {**METADATA, "title": "Launch planner prompts"})
    write_json(
        product / "prompts.json",
        {
            "prompts": [
                {
                    "id": "launch-plan",
                    "template": "Create a three-step launch plan for {{audience}}.",
                    "variables": ["audience"],
                    "example": {
                        "input": {"audience": "indie creators"},
                        "output": "1. Define offer. 2. Prepare landing page. 3. Announce launch.",
                    },
                }
            ]
        },
    )
    (product / "README.md").write_text("# Launch planner prompts\n\nA verified prompt-pack example.\n", encoding="utf-8")


def spreadsheet() -> None:
    product = ROOT / "xlsx"
    product.mkdir(parents=True, exist_ok=True)
    write_json(
        product / "product.json",
        {**METADATA, "title": "Budget template", "input_cells": ["Budget!B2"]},
    )
    with zipfile.ZipFile(product / "budget.xlsx", "w", zipfile.ZIP_DEFLATED) as workbook:
        write_zip(
            workbook,
            "[Content_Types].xml",
            """<?xml version='1.0' encoding='UTF-8'?>
<Types xmlns='http://schemas.openxmlformats.org/package/2006/content-types'>
<Default Extension='rels' ContentType='application/vnd.openxmlformats-package.relationships+xml'/>
<Default Extension='xml' ContentType='application/xml'/>
<Override PartName='/xl/workbook.xml' ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml'/>
<Override PartName='/xl/worksheets/sheet1.xml' ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml'/>
<Override PartName='/xl/worksheets/sheet2.xml' ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml'/>
</Types>""",
        )
        write_zip(
            workbook,
            "_rels/.rels",
            "<Relationships xmlns='http://schemas.openxmlformats.org/package/2006/relationships'><Relationship Id='rId1' Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument' Target='xl/workbook.xml'/></Relationships>",
        )
        write_zip(
            workbook,
            "xl/workbook.xml",
            "<workbook xmlns='http://schemas.openxmlformats.org/spreadsheetml/2006/main' xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships'><sheets><sheet name='Instructions' sheetId='1' r:id='rId1'/><sheet name='Budget' sheetId='2' r:id='rId2'/></sheets></workbook>",
        )
        write_zip(
            workbook,
            "xl/_rels/workbook.xml.rels",
            "<Relationships xmlns='http://schemas.openxmlformats.org/package/2006/relationships'><Relationship Id='rId1' Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet' Target='worksheets/sheet1.xml'/><Relationship Id='rId2' Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet' Target='worksheets/sheet2.xml'/></Relationships>",
        )
        write_zip(
            workbook,
            "xl/worksheets/sheet1.xml",
            "<worksheet xmlns='http://schemas.openxmlformats.org/spreadsheetml/2006/main'><sheetData><row r='1'><c r='A1' t='inlineStr'><is><t>Enter values in marked input cells.</t></is></c></row></sheetData></worksheet>",
        )
        write_zip(
            workbook,
            "xl/worksheets/sheet2.xml",
            "<worksheet xmlns='http://schemas.openxmlformats.org/spreadsheetml/2006/main'><sheetData><row r='1'><c r='A1' t='inlineStr'><is><t>Sample budget</t></is></c></row><row r='2'><c r='B2'><v>100</v></c></row></sheetData></worksheet>",
        )


def write_pdf(path: Path) -> None:
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length 45 >>\nstream\nBT /F1 18 Tf 72 720 Td (Tiny ebook) Tj ET\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    chunks = [b"%PDF-1.4\n"]
    offsets = [0]
    for index, body in enumerate(objects, start=1):
        offsets.append(sum(len(chunk) for chunk in chunks))
        chunks.append(f"{index} 0 obj\n".encode() + body + b"\nendobj\n")
    startxref = sum(len(chunk) for chunk in chunks)
    xref = [f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()]
    xref.extend(f"{offset:010d} 00000 n \n".encode() for offset in offsets[1:])
    chunks.extend(xref)
    chunks.append(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{startxref}\n%%EOF\n".encode())
    path.write_bytes(b"".join(chunks))


def ebook() -> None:
    product = ROOT / "ebook"
    product.mkdir(parents=True, exist_ok=True)
    write_json(product / "product.json", {**METADATA, "title": "Tiny ebook"})
    with zipfile.ZipFile(product / "book.epub", "w") as archive:
        write_zip(archive, "mimetype", "application/epub+zip", zipfile.ZIP_STORED)
        write_zip(archive, "META-INF/container.xml", "<container xmlns='urn:oasis:names:tc:opendocument:xmlns:container' version='1.0'><rootfiles><rootfile full-path='OEBPS/content.opf' media-type='application/oebps-package+xml'/></rootfiles></container>")
        write_zip(archive, "OEBPS/content.opf", "<package xmlns='http://www.idpf.org/2007/opf' version='3.0' unique-identifier='book'><metadata xmlns:dc='http://purl.org/dc/elements/1.1/'><dc:identifier id='book'>tiny-ebook</dc:identifier><dc:title>Tiny ebook</dc:title><dc:language>en</dc:language><meta property='dcterms:modified'>2026-10-20T00:00:00Z</meta></metadata><manifest><item id='nav' href='nav.xhtml' media-type='application/xhtml+xml' properties='nav'/><item id='chapter' href='chapter.xhtml' media-type='application/xhtml+xml'/></manifest><spine><itemref idref='chapter'/></spine></package>")
        write_zip(archive, "OEBPS/nav.xhtml", "<!DOCTYPE html><html xmlns='http://www.w3.org/1999/xhtml'><head><title>Contents</title></head><body><nav epub:type='toc' xmlns:epub='http://www.idpf.org/2007/ops'><ol><li><a href='chapter.xhtml'>Chapter</a></li></ol></nav></body></html>")
        write_zip(archive, "OEBPS/chapter.xhtml", "<!DOCTYPE html><html xmlns='http://www.w3.org/1999/xhtml'><head><title>Tiny ebook</title></head><body><h1 id='start'>Tiny ebook</h1><p>A verified example.</p></body></html>")
    write_pdf(product / "book.pdf")


def main() -> None:
    prompt_pack()
    spreadsheet()
    ebook()


if __name__ == "__main__":
    main()
