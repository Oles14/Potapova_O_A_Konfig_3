import unittest

from src.assembler import parse_command, parse_program


class TestAssembler(unittest.TestCase):
    """Tests for the first stage of the assembler."""

    def test_load(self):
        result = parse_command(["LOAD", "398", "423"])
        self.assertEqual(result, (4, 398, 423))

    def test_read(self):
        result = parse_command(["READ", "799", "5", "132"])
        self.assertEqual(result, (9, 799, 5, 132))

    def test_write(self):
        result = parse_command(["WRITE", "814", "355"])
        self.assertEqual(result, (0, 814, 355))

    def test_shr(self):
        result = parse_command(["SHR", "324", "344", "263"])
        self.assertEqual(result, (3, 324, 344, 263))

    def test_program(self):
        result = parse_program("tests/specification.csv")
        self.assertEqual(result, [
            (4, 398, 423),
            (9, 799, 5, 132),
            (0, 814, 355),
            (3, 324, 344, 263),
        ])

    def test_unknown_command(self):
        with self.assertRaises(ValueError):
            parse_command(["UNKNOWN"])

    def test_wrong_count(self):
        with self.assertRaises(ValueError):
            parse_command(["LOAD", "10"])

    def test_invalid_argument(self):
        with self.assertRaises(ValueError):
            parse_command(["READ", "100", "64", "90"])