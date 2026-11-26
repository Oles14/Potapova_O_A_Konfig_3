import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from src.assembler import assemble_program, parse_program
from src.interpreter import run_program, save_dump


class TestVectors(unittest.TestCase):
    """Check the three vector programs and their XML dumps."""

    def check_vector(self, filename, x, y, expected):
        """Check the machine code, input vectors and result."""
        program = parse_program(filename)
        data = b"".join(assemble_program(program))
        self.assertEqual(len(data), 180)
        memory = run_program(data)

        self.assertEqual(memory[300:309], x)
        self.assertEqual(memory[400:409], y)
        self.assertEqual(memory[500:509], expected)

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "vector.xml"
            save_dump(memory, path, 500, 508)
            root = ET.parse(path).getroot()
            self.assertEqual(root.tag, "memory")
            addresses = [int(cell.get("address")) for cell in root]
            values = [int(cell.text) for cell in root]
            self.assertEqual(addresses, list(range(500, 509)))
            self.assertEqual(values, expected)

    def test_vector1(self):
        """Check powers of two."""
        self.check_vector(
            "tests/vector1.csv",
            [8, 16, 32, 64, 128, 256, 512, 1024, 2048],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 4, 4, 4, 4, 4, 4, 4, 4],
        )

    def test_vector2(self):
        """Check odd numbers."""
        self.check_vector(
            "tests/vector2.csv",
            [15, 31, 63, 127, 255, 511, 1023, 2047, 4095],
            [1, 1, 2, 2, 3, 3, 4, 4, 5],
            [7, 15, 15, 31, 31, 63, 63, 127, 127],
        )

    def test_vector3(self):
        """Check zero and large shifts."""
        self.check_vector(
            "tests/vector3.csv",
            [0, 1, 2, 7, 100, 255, 1024, 65535, 2097151],
            [0, 0, 1, 3, 0, 8, 10, 16, 32],
            [0, 1, 1, 0, 100, 0, 1, 0, 0],
        )