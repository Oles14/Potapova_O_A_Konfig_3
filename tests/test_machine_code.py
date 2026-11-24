import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.assembler import assemble_program, parse_program
from src.commands import encode_command


EXPECTED = [
    bytes.fromhex("E4 18 00 4E 03"),
    bytes.fromhex("F9 31 05 21 00"),
    bytes.fromhex("E0 32 63 01"),
    bytes.fromhex("43 14 58 71 10"),
]


class TestMachineCode(unittest.TestCase):
    """Check machine code against the specification."""

    def test_load(self):
        """Check LOAD bytes."""
        self.assertEqual(encode_command((4, 398, 423)), EXPECTED[0])

    def test_read(self):
        """Check READ bytes."""
        self.assertEqual(encode_command((9, 799, 5, 132)), EXPECTED[1])

    def test_write(self):
        """Check WRITE bytes."""
        self.assertEqual(encode_command((0, 814, 355)), EXPECTED[2])

    def test_shr(self):
        """Check SHR bytes."""
        self.assertEqual(encode_command((3, 324, 344, 263)), EXPECTED[3])

    def test_program(self):
        """Check all instructions in the CSV file."""
        program = parse_program("tests/specification.csv")
        self.assertEqual(assemble_program(program), EXPECTED)

    def test_binary_file(self):
        """Check the binary file created by the CLI."""
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "program.bin"
            subprocess.run([
                sys.executable, "-m", "src.assembler",
                "--input", "tests/specification.csv",
                "--output", str(output),
            ], check=True, capture_output=True)

            self.assertEqual(output.read_bytes(), b"".join(EXPECTED))