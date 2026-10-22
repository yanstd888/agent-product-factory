import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import create_examples


class ExampleGenerationTests(unittest.TestCase):
    def test_examples_are_byte_stable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            with patch.object(create_examples, "ROOT", root):
                create_examples.main()
                first = {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}
                create_examples.main()
                second = {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
