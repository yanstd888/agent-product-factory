import os
from pathlib import Path
import shutil
import sys

from .report import Finding, Report


TOOLS = ("python", "pandoc", "epubcheck", "soffice")


def check_environment() -> Report:
    return check_tools(TOOLS)


def check_tools(names: tuple[str, ...], search_path: str | None = None) -> Report:
    findings = [_tool_finding(name, search_path) for name in names]
    return Report("environment", "doctor", findings)


def _tool_finding(name: str, search_path: str | None) -> Finding:
    if name == "python":
        return Finding(
            "tool-python",
            "pass",
            "blocker",
            f"Python {sys.version_info.major}.{sys.version_info.minor} is available.",
        )
    if tool_path(name, search_path):
        return Finding(f"tool-{name}", "pass", "blocker", f"{name} is available.")
    return Finding(
        f"tool-{name}",
        "fail",
        "blocker",
        f"{name} is required but was not found.",
    )


def java_path(search_path: str | None = None) -> str | None:
    found = shutil.which("java", path=search_path)
    if found or search_path is not None:
        return found
    roots = [Path(os.environ["JAVA_HOME"])] if os.environ.get("JAVA_HOME") else []
    adoptium = Path(os.environ.get("ProgramFiles", "")) / "Eclipse Adoptium"
    if adoptium.is_dir():
        roots.extend(sorted(adoptium.glob("jdk-*"), reverse=True))
    for root in roots:
        for executable in (root / "bin" / "java.exe", root / "bin" / "java"):
            if executable.is_file():
                return str(executable)
    return None


def tool_path(name: str, search_path: str | None = None) -> str | None:
    if name == "python":
        return sys.executable
    candidates = {
        "pandoc": ("pandoc", "pandoc.exe"),
        "epubcheck": ("epubcheck", "epubcheck.bat"),
        "soffice": ("soffice", "soffice.com", "soffice.exe", "libreoffice"),
    }[name]
    for candidate in candidates:
        found = shutil.which(candidate, path=search_path)
        if found:
            return found
    if search_path is not None:
        return None

    if name == "epubcheck":
        jar = os.environ.get("EPUBCHECK_JAR")
        if jar and Path(jar).is_file() and java_path():
            return jar
        return None

    fallbacks = {
        "pandoc": (Path(os.environ.get("ProgramFiles", "")) / "Pandoc" / "pandoc.exe",),
        "soffice": (
            Path(os.environ.get("ProgramFiles", "")) / "LibreOffice" / "program" / "soffice.com",
            Path(os.environ.get("ProgramFiles", "")) / "LibreOffice" / "program" / "soffice.exe",
            Path(os.environ.get("ProgramFiles(x86)", "")) / "LibreOffice" / "program" / "soffice.com",
            Path(os.environ.get("ProgramFiles(x86)", "")) / "LibreOffice" / "program" / "soffice.exe",
        ),
    }
    for fallback in fallbacks.get(name, ()):
        if fallback.is_file():
            return str(fallback)
    return None
