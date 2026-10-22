import json
from pathlib import Path
import posixpath
import re
import subprocess
import tempfile
import zipfile
import xml.etree.ElementTree as ET

from .doctor import java_path, tool_path
from .report import Finding


VARIABLE = re.compile(r"{{\s*([^{}\s]+)\s*}}")
FORMULA_ERROR = re.compile(r"#\s?(REF!|NAME\?|DIV/0!|VALUE!|N/A|NUM!|NULL!)", re.IGNORECASE)
EMBEDDED_PLACEHOLDER = re.compile(r"\bTODO\b|\blorem ipsum\b|{{[^{}]+}}|\[ISI\]", re.IGNORECASE)


def check_product_type(product: Path, product_type: str) -> list[Finding]:
    if product_type == "prompt-pack":
        return _prompt_pack_findings(product)
    if product_type == "xlsx":
        return _xlsx_findings(product)
    if product_type == "ebook":
        return _ebook_findings(product)
    return []


def _prompt_pack_findings(product: Path) -> list[Finding]:
    root = product if product.is_dir() else product.parent
    prompts_path = root / "prompts.json"
    try:
        prompts_data = json.loads(prompts_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return [
            Finding(
                "prompt-pack",
                "fail",
                "blocker",
                "prompts.json is required and must be valid UTF-8 JSON.",
            )
        ]

    prompts = prompts_data.get("prompts") if isinstance(prompts_data, dict) else None
    if not isinstance(prompts, list) or not prompts:
        return [
            Finding("prompt-pack", "fail", "blocker", "prompts.json needs a non-empty prompts list.")
        ]

    findings: list[Finding] = []
    ids: set[str] = set()
    for index, prompt in enumerate(prompts, start=1):
        if not isinstance(prompt, dict):
            findings.append(_prompt_error(index, "Each prompt must be an object."))
            continue
        prompt_id = prompt.get("id")
        template = prompt.get("template")
        variables = prompt.get("variables")
        example = prompt.get("example")
        if not isinstance(prompt_id, str) or not prompt_id.strip() or prompt_id in ids:
            findings.append(_prompt_error(index, "Prompt id must be unique and non-empty."))
        else:
            ids.add(prompt_id)
        if not isinstance(template, str) or not template.strip():
            findings.append(_prompt_error(index, "Prompt template must be non-empty."))
            continue
        if not isinstance(variables, list) or not all(
            isinstance(variable, str) and variable for variable in variables
        ):
            findings.append(_prompt_error(index, "Prompt variables must be a list of names."))
            continue

        declared = set(variables)
        used = {match.group(1) for match in VARIABLE.finditer(template)}
        if len(declared) != len(variables) or declared != used:
            findings.append(
                Finding(
                    "prompt-variable",
                    "fail",
                    "blocker",
                    f"Prompt {index} variables must match its template placeholders.",
                    "prompts.json",
                )
            )
        if not isinstance(example, dict) or not isinstance(example.get("input"), dict) or not isinstance(
            example.get("output"), str
        ) or not example["output"].strip():
            findings.append(_prompt_error(index, "Prompt example needs input and non-empty output."))
        elif not declared.issubset(example["input"]):
            findings.append(_prompt_error(index, "Prompt example input is missing declared variables."))

    if not findings:
        return [Finding("prompt-pack", "pass", "blocker", "Prompt pack structure is valid.")]
    return findings


def _xlsx_findings(product: Path) -> list[Finding]:
    root = product if product.is_dir() else product.parent
    workbooks = sorted(root.glob("*.xlsx"), key=lambda path: path.name.casefold())
    if len(workbooks) != 1:
        return [
            Finding(
                "xlsx",
                "fail",
                "blocker",
                "Product must contain exactly one XLSX file.",
            )
        ]

    findings = _xlsx_structure_findings(workbooks[0], root)
    findings.extend(_xlsx_external_findings(workbooks[0]))
    if not any(finding.id == "placeholder" for finding in findings):
        findings.append(Finding("placeholder", "pass", "blocker", "No packaged placeholders found."))
    if not any(finding.status == "fail" and finding.severity == "blocker" for finding in findings):
        findings.append(Finding("xlsx", "pass", "blocker", "Spreadsheet checks passed."))
    return findings


def _xlsx_structure_findings(workbook: Path, root: Path) -> list[Finding]:
    try:
        with zipfile.ZipFile(workbook) as archive:
            sheet_names = _xlsx_sheet_names(archive)
            worksheet_paths = _xlsx_worksheets(archive)
            worksheet_text = {
                path: archive.read(path).decode("utf-8", "replace") for path in worksheet_paths
            }
    except (OSError, ValueError, zipfile.BadZipFile, KeyError, ET.ParseError, UnicodeDecodeError):
        return [Finding("xlsx", "fail", "blocker", "XLSX file is corrupt or incomplete.")]

    findings: list[Finding] = []
    if any(FORMULA_ERROR.search(text) for text in worksheet_text.values()):
        findings.append(
            Finding("xlsx-formula-error", "fail", "blocker", "Workbook contains formula errors.")
        )
    findings.extend(_embedded_placeholder_findings(worksheet_text))
    if not any(name.casefold() == "instructions" for name in sheet_names):
        findings.append(
            Finding("xlsx-instructions", "fail", "warning", "Workbook has no Instructions sheet.")
        )
    if not any("<v>" in text or "<t>" in text for text in worksheet_text.values()):
        findings.append(
            Finding("xlsx-sample-data", "fail", "warning", "Workbook has no sample data.")
        )
    if not _has_input_cells(root, worksheet_text, sheet_names):
        findings.append(
            Finding("xlsx-input-cells", "fail", "warning", "product.json has no valid input_cells markers.")
        )
    return findings


def _embedded_placeholder_findings(parts: dict[str, str]) -> list[Finding]:
    findings: list[Finding] = []
    for path, text in parts.items():
        for match in EMBEDDED_PLACEHOLDER.finditer(text):
            findings.append(
                Finding(
                    "placeholder",
                    "fail",
                    "blocker",
                    f"Found placeholder {match.group(0)} in packaged content.",
                    path,
                )
            )
    return findings


def _xlsx_sheet_names(archive: zipfile.ZipFile) -> list[str]:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    return [sheet.attrib.get("name", "") for sheet in workbook.findall(".//{*}sheet")]


def _xlsx_worksheets(archive: zipfile.ZipFile) -> list[str]:
    return sorted(
        name for name in archive.namelist() if name.startswith("xl/worksheets/") and name.endswith(".xml")
    )


def _has_input_cells(root: Path, worksheets: dict[str, str], sheet_names: list[str]) -> bool:
    try:
        metadata = json.loads((root / "product.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return False
    markers = metadata.get("input_cells") if isinstance(metadata, dict) else None
    if not isinstance(markers, list) or not markers:
        return False
    valid_sheets = {name.casefold() for name in sheet_names}
    for marker in markers:
        if not isinstance(marker, str) or "!" not in marker:
            return False
        sheet_name, cell = marker.split("!", 1)
        if sheet_name.casefold() not in valid_sheets or not re.fullmatch(r"[A-Z]+[1-9][0-9]*", cell):
            return False
        if not any(re.search(rf"r=[\"']{re.escape(cell)}[\"']", text) for text in worksheets.values()):
            return False
    return True


def _xlsx_external_findings(workbook: Path) -> list[Finding]:
    soffice = tool_path("soffice")
    if not soffice:
        return [
            Finding("tool-soffice", "fail", "blocker", "LibreOffice is required for XLSX formula evaluation.")
        ]
    with tempfile.TemporaryDirectory() as temporary_directory:
        output = Path(temporary_directory)
        try:
            result = subprocess.run(
                [soffice, "--headless", "--convert-to", "xlsx", "--outdir", str(output), str(workbook)],
                capture_output=True,
                check=False,
                text=True,
                timeout=60,
            )
        except (OSError, subprocess.TimeoutExpired):
            return [Finding("xlsx-recalculate", "fail", "blocker", "LibreOffice could not recalculate XLSX.")]
        converted = output / workbook.name
        if result.returncode != 0 or not converted.is_file():
            return [Finding("xlsx-recalculate", "fail", "blocker", "LibreOffice could not recalculate XLSX.")]
        return _xlsx_structure_findings(converted, workbook.parent)


def _ebook_findings(product: Path) -> list[Finding]:
    root = product if product.is_dir() else product.parent
    epubs = sorted(root.glob("*.epub"), key=lambda path: path.name.casefold())
    pdfs = sorted(root.glob("*.pdf"), key=lambda path: path.name.casefold())
    if len(epubs) != 1 or len(pdfs) != 1:
        return [
            Finding(
                "ebook",
                "fail",
                "blocker",
                "Product must contain exactly one EPUB and one PDF file.",
            )
        ]

    findings = _epub_structure_findings(epubs[0])
    findings.extend(_pdf_findings(pdfs[0]))
    findings.extend(_ebook_external_findings(epubs[0]))
    if not any(finding.id == "placeholder" for finding in findings):
        findings.append(Finding("placeholder", "pass", "blocker", "No packaged placeholders found."))
    if not any(finding.status == "fail" and finding.severity == "blocker" for finding in findings):
        findings.append(Finding("ebook", "pass", "blocker", "Ebook checks passed."))
    return findings


def _epub_structure_findings(epub: Path) -> list[Finding]:
    try:
        with zipfile.ZipFile(epub) as archive:
            infos = archive.infolist()
            if not infos or infos[0].filename != "mimetype" or infos[0].compress_type != zipfile.ZIP_STORED:
                return [Finding("epub", "fail", "blocker", "EPUB mimetype must be the first stored file.")]
            if archive.read("mimetype") != b"application/epub+zip":
                return [Finding("epub", "fail", "blocker", "EPUB mimetype is invalid.")]
            container = ET.fromstring(archive.read("META-INF/container.xml"))
            rootfile = container.find(".//{*}rootfile")
            if rootfile is None or not rootfile.attrib.get("full-path"):
                return [Finding("epub", "fail", "blocker", "EPUB container has no rootfile.")]
            opf_path = rootfile.attrib["full-path"]
            opf = ET.fromstring(archive.read(opf_path))
            items = [item for item in opf.findall(".//{*}item") if item.attrib.get("href")]
            nav_item = next(
                (item for item in items if "nav" in item.attrib.get("properties", "").split()),
                None,
            )
            if nav_item is None:
                return [Finding("ebook-toc", "fail", "blocker", "EPUB has no navigation document.")]
            names = set(archive.namelist())
            paths = [_archive_path(opf_path, item.attrib["href"]) for item in items]
            findings = [
                Finding("ebook-asset", "fail", "blocker", "EPUB manifest asset is missing.", path)
                for path in paths
                if path not in names
            ]
            nav_path = _archive_path(opf_path, nav_item.attrib["href"])
            if nav_path not in names:
                return findings + [Finding("ebook-toc", "fail", "blocker", "EPUB navigation document is missing.")]
            documents = [
                path
                for item, path in zip(items, paths)
                if path in names
                and (
                    item.attrib.get("media-type") in {"application/xhtml+xml", "text/html"}
                    or path.lower().endswith((".xhtml", ".html"))
                )
            ]
            return findings + _epub_link_findings(archive, documents)
    except (OSError, ValueError, zipfile.BadZipFile, KeyError, ET.ParseError):
        return [Finding("epub", "fail", "blocker", "EPUB file is corrupt or incomplete.")]


def _epub_link_findings(archive: zipfile.ZipFile, document_paths: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    names = set(archive.namelist())
    contents: dict[str, str] = {}
    for document_path in sorted(document_paths):
        try:
            content = archive.read(document_path).decode("utf-8")
            document = ET.fromstring(content)
        except (KeyError, UnicodeDecodeError, ET.ParseError):
            findings.append(Finding("ebook-content", "fail", "blocker", "EPUB content document is invalid.", document_path))
            continue
        contents[document_path] = " ".join(document.itertext())
        for link in document.findall(".//{*}a"):
            href = link.attrib.get("href", "").strip()
            if not href or "://" in href or href.startswith("mailto:"):
                continue
            target, separator, fragment = href.partition("#")
            target_path = document_path if not target else _archive_path(document_path, target)
            if target_path not in names:
                findings.append(Finding("ebook-link", "fail", "blocker", "EPUB has a broken internal link.", document_path))
                continue
            if separator and fragment:
                try:
                    target_text = archive.read(target_path).decode("utf-8")
                except (KeyError, UnicodeDecodeError):
                    findings.append(Finding("ebook-link", "fail", "blocker", "EPUB link target is unreadable.", document_path))
                    continue
                if f'id="{fragment}"' not in target_text and f"id='{fragment}'" not in target_text:
                    findings.append(Finding("ebook-link", "fail", "blocker", "EPUB link target is missing.", document_path))
    findings.extend(_embedded_placeholder_findings(contents))
    return findings


def _archive_path(base: str, href: str) -> str:
    return posixpath.normpath(posixpath.join(posixpath.dirname(base), href))


def _pdf_findings(pdf: Path) -> list[Finding]:
    try:
        content = pdf.read_bytes()
    except OSError:
        return [Finding("pdf", "fail", "blocker", "PDF file cannot be opened.")]
    if not content.startswith(b"%PDF-") or b"%%EOF" not in content[-1024:]:
        return [Finding("pdf", "fail", "blocker", "PDF file is invalid.")]
    return []


def _ebook_external_findings(epub: Path) -> list[Finding]:
    pandoc = tool_path("pandoc")
    epubcheck = tool_path("epubcheck")
    findings: list[Finding] = []
    if not pandoc:
        findings.append(Finding("tool-pandoc", "fail", "blocker", "Pandoc is required for ebook builds."))
    if not epubcheck:
        findings.append(Finding("tool-epubcheck", "fail", "blocker", "EPUBCheck is required for EPUB validation."))
    if findings:
        return findings

    command = [epubcheck, str(epub)]
    if epubcheck.endswith(".jar"):
        java = java_path()
        if not java:
            return [Finding("tool-epubcheck", "fail", "blocker", "Java is required for EPUBCheck.")]
        command = [java, "-jar", epubcheck, str(epub)]
    try:
        result = subprocess.run(command, capture_output=True, check=False, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return [Finding("epubcheck", "fail", "blocker", "EPUBCheck could not validate EPUB.")]
    if result.returncode != 0:
        return [Finding("epubcheck", "fail", "blocker", "EPUBCheck rejected EPUB.")]
    return []


def _prompt_error(index: int, message: str) -> Finding:
    return Finding("prompt-pack", "fail", "blocker", f"Prompt {index}: {message}", "prompts.json")
