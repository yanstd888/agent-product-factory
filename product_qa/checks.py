import json
import os
from pathlib import Path
import re

from .product_checks import check_product_type
from .report import Finding, Report


MAX_FILES = 5_000
# ponytail: fixed limits cap offline scans; add streaming scanners if real products exceed them.
MAX_TEXT_BYTES = 4 * 1024 * 1024
MAX_TOTAL_TEXT_BYTES = 16 * 1024 * 1024
METADATA_FIELDS = ("title", "author", "version", "license")
PLACEHOLDERS = (
    ("TODO", re.compile(r"\bTODO\b", re.IGNORECASE)),
    ("lorem ipsum", re.compile(r"\blorem ipsum\b", re.IGNORECASE)),
    ("{{...}}", re.compile(r"{{[^{}]+}}")),
    ("[ISI]", re.compile(r"\[ISI\]", re.IGNORECASE)),
)
TEXT_SUFFIXES = {".csv", ".html", ".json", ".md", ".txt", ".xml", ".yaml", ".yml"}


def check_product(product_path: str | Path, product_type: str) -> Report:
    try:
        product = Path(product_path)
        if product.is_symlink():
            return _blocked(product, product_type, "Product path must not be a symlink.")
        if not product.exists():
            return _blocked(product, product_type, "Product path does not exist.")
        product = product.resolve(strict=True)
    except (OSError, ValueError):
        return _blocked(Path(product_path), product_type, "Product path cannot be opened.")

    files, findings = _files_in(product)
    if not files:
        findings.append(Finding("product-files", "fail", "blocker", "Product has no files."))
    else:
        findings.append(
            Finding("product-path", "pass", "blocker", "Product path is available.")
        )

    contents: dict[Path, bytes] = {}
    text_bytes = 0
    unreadable = False
    for file_path in files:
        try:
            size = file_path.stat().st_size
            with file_path.open("rb") as product_file:
                product_file.read(1)
        except OSError:
            unreadable = True
            findings.append(
                Finding(
                    "file-readable",
                    "fail",
                    "blocker",
                    "File cannot be opened.",
                    _display_path(product, file_path),
                )
            )
            continue

        if not _is_text_file(file_path):
            continue
        if size > MAX_TEXT_BYTES or text_bytes + size > MAX_TOTAL_TEXT_BYTES:
            findings.append(
                Finding(
                    "text-scan-limit",
                    "fail",
                    "blocker",
                    "Text content exceeds the offline scan limit.",
                    _display_path(product, file_path),
                )
            )
            continue
        try:
            contents[file_path] = file_path.read_bytes()
            text_bytes += size
        except OSError:
            unreadable = True
            findings.append(
                Finding(
                    "file-readable",
                    "fail",
                    "blocker",
                    "File cannot be opened.",
                    _display_path(product, file_path),
                )
            )

    if not unreadable:
        findings.append(
            Finding("file-readable", "pass", "blocker", "All product files can be opened.")
        )

    findings.extend(_placeholder_findings(product, contents, product_type))
    findings.extend(_metadata_findings(product, contents))
    findings.extend(check_product_type(product, product_type))
    return Report(_display_product(product), product_type, findings)


def _blocked(product: Path, product_type: str, message: str) -> Report:
    return Report(
        _display_product(product),
        product_type,
        [Finding("product-path", "fail", "blocker", message)],
    )


def _files_in(product: Path) -> tuple[list[Path], list[Finding]]:
    if product.is_file():
        return [product], []

    files: list[Path] = []
    findings: list[Finding] = []

    def walk_error(_: OSError) -> None:
        findings.append(
            Finding("product-walk", "fail", "blocker", "Product files cannot be listed.")
        )

    for directory, directories, names in os.walk(
        product, topdown=True, followlinks=False, onerror=walk_error
    ):
        current = Path(directory)
        allowed_directories = []
        for name in sorted(directories, key=str.casefold):
            candidate = current / name
            if candidate.is_symlink():
                findings.append(
                    Finding(
                        "symlink",
                        "fail",
                        "blocker",
                        "Product symlinks are not supported.",
                        _display_path(product, candidate),
                    )
                )
            else:
                allowed_directories.append(name)
        directories[:] = allowed_directories

        for name in sorted(names, key=str.casefold):
            candidate = current / name
            if candidate.is_symlink():
                findings.append(
                    Finding(
                        "symlink",
                        "fail",
                        "blocker",
                        "Product symlinks are not supported.",
                        _display_path(product, candidate),
                    )
                )
            elif candidate.is_file():
                files.append(candidate)
                if len(files) > MAX_FILES:
                    findings.append(
                        Finding(
                            "file-count-limit",
                            "fail",
                            "blocker",
                            "Product exceeds the offline file-count limit.",
                        )
                    )
                    return files[:MAX_FILES], findings

    return sorted(files, key=lambda path: (path.as_posix().casefold(), path.as_posix())), findings


def _placeholder_findings(
    product: Path, contents: dict[Path, bytes], product_type: str
) -> list[Finding]:
    findings: list[Finding] = []
    for file_path, content in contents.items():
        placeholders = (
            tuple((label, pattern) for label, pattern in PLACEHOLDERS if label != "{{...}}")
            if product_type == "prompt-pack" and file_path.name == "prompts.json"
            else PLACEHOLDERS
        )
        text = _text_content(content)
        if text is None:
            findings.append(
                Finding(
                    "text-encoding",
                    "fail",
                    "blocker",
                    "Text file cannot be decoded.",
                    _display_path(product, file_path),
                )
            )
            continue
        for label, pattern in placeholders:
            for match in pattern.finditer(text):
                line_number = text.count("\n", 0, match.start()) + 1
                findings.append(
                    Finding(
                        "placeholder",
                        "fail",
                        "blocker",
                        f"Found placeholder {label} on line {line_number}.",
                        _display_path(product, file_path),
                    )
                )
    if product_type not in {"xlsx", "ebook"} and not any(finding.id == "placeholder" for finding in findings):
        findings.append(
            Finding("placeholder", "pass", "blocker", "No text placeholders found.")
        )
    return findings


def _is_text_file(file_path: Path) -> bool:
    return file_path.suffix.lower() in TEXT_SUFFIXES


def _text_content(content: bytes) -> str | None:
    encodings = ("utf-16",) if content.startswith((b"\xff\xfe", b"\xfe\xff")) else ("utf-8-sig", "latin-1")
    for encoding in encodings:
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    return None


def _metadata_findings(product: Path, contents: dict[Path, bytes]) -> list[Finding]:
    root = product if product.is_dir() else product.parent
    manifest = root / "product.json"
    content = contents.get(manifest)
    if content is None:
        return [
            Finding(
                "metadata",
                "fail",
                "warning",
                "Missing product.json with title, author, version, and license.",
            )
        ]

    try:
        metadata = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return [
            Finding("metadata", "fail", "warning", "product.json is not valid UTF-8 JSON.")
        ]

    missing = [
        field
        for field in METADATA_FIELDS
        if not isinstance(metadata, dict) or not str(metadata.get(field, "")).strip()
    ]
    if missing:
        return [
            Finding(
                "metadata",
                "fail",
                "warning",
                f"product.json is missing: {', '.join(missing)}.",
                "product.json",
            )
        ]
    return [
        Finding("metadata", "pass", "warning", "Required metadata is present.", "product.json")
    ]


def _display_product(product: Path) -> str:
    return product.name or "."


def _display_path(product: Path, file_path: Path) -> str:
    if product.is_file():
        return file_path.name
    try:
        return file_path.relative_to(product).as_posix()
    except ValueError:
        return file_path.name
