import argparse
import csv

from src.commands import COMMANDS, encode_command


def parse_command(row):
    """Convert a CSV row into a tuple of numbers."""
    name = row[0].strip().upper()

    if name not in COMMANDS:
        raise ValueError(f"Unknown command: {name}")

    opcode, widths, _ = COMMANDS[name]
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


def assemble_program(program):
    """Convert a program into a list of machine instructions."""
    result = []

    for command in program:
        result.append(encode_command(command))

    return result


def print_program(program):
    """Print machine instructions in hexadecimal format."""
    for command in program:
        values = []

        for byte in command:
            values.append(f"0x{byte:02X}")

        print(", ".join(values))


def main():
    """Run the assembler."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    try:
        program = parse_program(args.input)
        machine_code = assemble_program(program)
        data = b"".join(machine_code)

        with open(args.output, "wb") as file:
            file.write(data)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    if args.test:
        print_program(machine_code)

    print(f"Binary size: {len(data)} bytes")


if __name__ == "__main__":
    main()