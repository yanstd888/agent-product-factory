import json
import tempfile
import unittest
from pathlib import Path

from product_qa.checks import check_product


class PromptPackChecksTests(unittest.TestCase):
    def write_product(self, product: Path, prompts: list[dict[str, object]]) -> None:
        (product / "README.md").write_text("# Prompt pack", encoding="utf-8")
        (product / "product.json").write_text(
            json.dumps(
                {
                    "title": "Prompt pack",
                    "author": "Digital Product Factory",
                    "version": "1.0.0",
                    "license": "CC0-1.0",
                }
            ),
            encoding="utf-8",
        )
        (product / "prompts.json").write_text(
            json.dumps({"prompts": prompts}), encoding="utf-8"
        )

    def test_valid_prompt_pack_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            product = Path(temporary_directory)
            self.write_product(
                product,
                [
                    {
                        "id": "launch-plan",
                        "template": "Create a plan for {{audience}}.",
                        "variables": ["audience"],
                        "example": {
                            "input": {"audience": "indie creators"},
                            "output": "A three-step launch plan.",
                        },
                    }
                ],
            )

            report = check_product(product, "prompt-pack")

        self.assertEqual(report.exit_code, 0)
        self.assertTrue(
            any(finding.id == "prompt-pack" and finding.status == "pass" for finding in report.findings)
        )

    def test_undeclared_prompt_variable_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            product = Path(temporary_directory)
            self.write_product(
                product,
                [
                    {
                        "id": "launch-plan",
                        "template": "Create a plan for {{audience}} and {{budget}}.",
                        "variables": ["audience"],
                        "example": {
                            "input": {"audience": "indie creators"},
                            "output": "A plan.",
                        },
                    }
                ],
            )

            report = check_product(product, "prompt-pack")

        self.assertEqual(report.exit_code, 1)
        self.assertTrue(
            any(finding.id == "prompt-variable" for finding in report.findings)
        )

    def test_prompt_placeholder_outside_manifest_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            product = Path(temporary_directory)
            self.write_product(
                product,
                [
                    {
                        "id": "launch-plan",
                        "template": "Create a plan for {{audience}}.",
                        "variables": ["audience"],
                        "example": {"input": {"audience": "creators"}, "output": "A plan."},
                    }
                ],
            )
            (product / "README.md").write_text("Fill {{title}}", encoding="utf-8")

            report = check_product(product, "prompt-pack")

        self.assertEqual(report.exit_code, 1)
        self.assertTrue(any(finding.id == "placeholder" for finding in report.findings))


if __name__ == "__main__":
    unittest.main()
