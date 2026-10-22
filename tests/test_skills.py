import filecmp
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
ALLOWED_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


class SkillPackageTests(unittest.TestCase):
    def test_skill_frontmatter_is_portable(self) -> None:
        for skill in sorted(path for path in SKILLS.iterdir() if path.is_dir()):
            skill_md = skill / "SKILL.md"
            self.assertTrue(skill_md.is_file(), skill)
            lines = skill_md.read_text(encoding="utf-8").splitlines()
            self.assertEqual(lines[0], "---", skill)
            end = lines.index("---", 1)
            fields = {
                key: value.strip()
                for key, _, value in (line.partition(":") for line in lines[1:end])
            }
            self.assertEqual(fields["name"], skill.name)
            self.assertTrue(fields["description"])
            self.assertLessEqual(len(fields["name"]), 64)
            self.assertLessEqual(len(fields["description"]), 1024)
            self.assertTrue(set(fields).issubset(ALLOWED_FIELDS))
            self.assertLess(len(lines), 500)

    def test_bundled_product_qa_matches_source_and_runs(self) -> None:
        source = ROOT / "product_qa"
        bundled = SKILLS / "product-qa" / "scripts" / "product_qa"
        comparison = filecmp.dircmp(source, bundled)
        self.assertFalse(comparison.left_only)
        self.assertFalse(comparison.right_only)
        self.assertFalse(comparison.diff_files)

        with tempfile.TemporaryDirectory() as temporary_directory:
            report = Path(temporary_directory) / "report.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILLS / "product-qa" / "scripts" / "run_qa.py"),
                    "check",
                    str(ROOT / "examples" / "prompt-pack"),
                    "--type",
                    "prompt-pack",
                    "--json-out",
                    str(report),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Product QA: PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
