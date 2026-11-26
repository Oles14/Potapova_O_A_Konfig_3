import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from src.assembler import assemble_program, parse_program
from src.commands import decode_command
from src.interpreter import run_program, save_dump


def execute(program):
    """Assemble and execute a test program."""
    return run_program(b"".join(assemble_program(program)))


class TestInterpreter(unittest.TestCase):
    """Check decoding, memory operations and XML."""

    def test_decode(self):
        """Decode all four specification examples."""
        examples = [
            ("E4 18 00 4E 03", (4, 398, 423)),
            ("F9 31 05 21 00", (9, 799, 5, 132)),
            ("E0 32 63 01", (0, 814, 355)),
            ("43 14 58 71 10", (3, 324, 344, 263)),
        ]
        for text, expected in examples:
            self.assertEqual(decode_command(bytes.fromhex(text)), expected)

    def test_load(self):
        """Load a constant into memory."""
        memory = execute([(4, 500, 100)])
        self.assertEqual(memory[100], 500)

    def test_read(self):
        """Read through a pointer with an offset."""
        program = [(4, 100, 90), (4, 42, 102), (9, 200, 2, 90)]
        self.assertEqual(execute(program)[200], 42)

    def test_write(self):
        """Copy a value to another address."""
        memory = execute([(4, 77, 100), (0, 200, 100)])
        self.assertEqual(memory[200], 77)

    def test_copy_array(self):
        """Copy an array without changing its source."""
        memory = execute(parse_program("tests/copy_array.csv"))
        self.assertEqual(memory[100:105], [10, 20, 30, 40, 50])
        self.assertEqual(memory[200:205], [10, 20, 30, 40, 50])

    def test_unified_memory(self):
        """Modify a byte of the next machine instruction."""
        memory = execute([(4, 164, 5), (4, 1, 100)])
        self.assertEqual(memory[5], 164)
        self.assertEqual(memory[100], 10)

    def test_xml_dump(self):
        """Check XML addresses and values."""
        memory = execute([(4, 50, 100), (4, 60, 101)])
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "dump.xml"
            save_dump(memory, path, 100, 101)
            root = ET.parse(path).getroot()
            self.assertEqual(root.tag, "memory")
            self.assertEqual(len(root), 2)
            self.assertEqual(root[0].get("address"), "100")
            self.assertEqual(root[0].text, "50")
            self.assertEqual(root[1].get("address"), "101")
            self.assertEqual(root[1].text, "60")

    def test_invalid_address(self):
        """Reject an invalid indirect address."""
        program = [(4, 4095, 90), (9, 100, 1, 90)]
        with self.assertRaises(ValueError):
            execute(program)

    def test_incomplete_command(self):
        """Reject a truncated instruction."""
        with self.assertRaises(ValueError):
            run_program(bytes.fromhex("E4 18"))