import unittest

from src.assembler import assemble_program, parse_program
from src.interpreter import run_program


def run_shift(value, shift, address=200):
    """Assemble and execute a program with one SHR command."""
    program = [
        (4, value, 300),
        (4, shift, 301),
        (4, address, 302),
        (3, 301, 300, 302),
    ]
    return run_program(b"".join(assemble_program(program)))


class TestALU(unittest.TestCase):
    """Check the logical right shift instruction."""

    def test_shift(self):
        """Check operands and indirect result addressing."""
        memory = run_shift(40, 2)
        self.assertEqual(memory[200], 10)
        self.assertEqual(memory[300:303], [40, 2, 200])

    def test_zero_shift(self):
        """Check that a shift by zero preserves the value."""
        self.assertEqual(run_shift(100, 0)[200], 100)

    def test_large_shift(self):
        """Check that shifting out all bits produces zero."""
        self.assertEqual(run_shift(255, 32)[200], 0)

    def test_zero_value(self):
        """Check shifting zero."""
        self.assertEqual(run_shift(0, 3)[200], 0)

    def test_invalid_address(self):
        """Reject a result address outside memory."""
        with self.assertRaises(ValueError):
            run_shift(40, 2, 4096)

    def test_shift_program(self):
        """Check all six calculations in the CSV program."""
        program = parse_program("tests/shift.csv")
        memory = run_program(b"".join(assemble_program(program)))
        self.assertEqual(memory[200:206], [10, 7, 100, 0, 1048575, 0])