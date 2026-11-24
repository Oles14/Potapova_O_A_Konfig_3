import argparse
import csv

from src.commands import COMMANDS


def parse_command(row):
    """Convert a CSV row into a tuple of numbers."""
    name = row[0].strip().upper()

    if name not in COMMANDS:
        raise ValueError(f"Unknown command: {name}")

    opcode, widths = COMMANDS[name]
    arguments = [int(value) for value in row[1:]]

    if len(arguments) != len(widths):
        raise ValueError(f"Wrong number of arguments: {name}")

    for value, bits in zip(arguments, widths):
        if not 0 <= value < 2 ** bits:
            raise ValueError(f"Invalid argument: {value}")

    return (opcode, *arguments)


def parse_program(filename):
    """Read all commands from a CSV file."""
    program = []

    with open(filename, encoding="utf-8-sig", newline="") as file:
        for row in csv.reader(file):
            if row:
                program.append(parse_command(row))

    return program


def print_program(program):
    """Print instruction fields in test mode."""
    for command in program:
        fields = []

        for name, value in zip("ABCD", command):
            fields.append(f"{name}={value}")

        print(", ".join(fields))


def main():
    """Run the assembler."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    try:
        program = parse_program(args.input)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    if args.test:
        print_program(program)

    print(f"Instructions: {len(program)}")


if __name__ == "__main__":
    main()