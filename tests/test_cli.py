import subprocess
import sys
import unittest


class ProductQaCliTests(unittest.TestCase):
    def test_help_is_available(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "product_qa", "--help"],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Product QA Gate", result.stdout)
        self.assertIn("--version", result.stdout)


if __name__ == "__main__":
    unittest.main()
