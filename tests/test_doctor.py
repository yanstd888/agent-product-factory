import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from product_qa.doctor import check_tools, java_path


class DoctorTests(unittest.TestCase):
    def test_python_is_available_without_path_lookup(self) -> None:
        report = check_tools(("python",), search_path="")

        self.assertEqual(report.exit_code, 0)
        self.assertEqual(report.findings[0].id, "tool-python")
        self.assertEqual(report.findings[0].status, "pass")

    def test_tool_lookup_is_deterministic_and_missing_tools_block(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            tools = Path(temporary_directory)
            name = "pandoc.exe" if os.name == "nt" else "pandoc"
            executable = tools / name
            executable.write_text("", encoding="utf-8")
            executable.chmod(0o755)

            found = check_tools(("pandoc",), search_path=str(tools))
            missing = check_tools(("pandoc",), search_path="")

        self.assertEqual(found.exit_code, 0)
        self.assertEqual(found.findings[0].status, "pass")
        self.assertEqual(missing.exit_code, 1)
        self.assertEqual(missing.findings[0].id, "tool-pandoc")
        self.assertEqual(missing.findings[0].severity, "blocker")
    def test_java_home_is_used_when_path_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            home = Path(temporary_directory)
            executable = home / "bin" / ("java.exe" if os.name == "nt" else "java")
            executable.parent.mkdir()
            executable.write_text("", encoding="utf-8")
            with patch("product_qa.doctor.shutil.which", return_value=None), patch.dict(
                os.environ, {"JAVA_HOME": str(home)}
            ):
                found = java_path()

        self.assertEqual(found, str(executable))


if __name__ == "__main__":
    unittest.main()
