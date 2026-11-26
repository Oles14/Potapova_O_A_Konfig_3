import argparse
import xml.etree.ElementTree as ET

from src.commands import LOAD, READ, WRITE, OPCODE_MASK
from src.commands import get_spec, decode_command

ADDRESS_BITS = 12
MEMORY_SIZE = 1 << ADDRESS_BITS


def check_address(address):
    """Check that the address belongs to memory."""
    if not 0 <= address < MEMORY_SIZE:
        raise ValueError(f"Invalid address: {address}")


def execute_command(memory, command):
    """Execute a decoded memory instruction."""
    opcode = command[0]

    if opcode == LOAD:
        _, b, c = command
        memory[c] = b

    elif opcode == READ:
        _, b, c, d = command
        address = memory[d] + c
        check_address(address)
        memory[b] = memory[address]

    elif opcode == WRITE:
        _, b, c = command
        memory[b] = memory[c]

    else:
        raise ValueError(f"Unsupported opcode: {opcode}")


def run_program(data):
    """Load and execute machine code in unified memory."""
    if len(data) > MEMORY_SIZE:
        raise ValueError("Program is too large")

    memory = [0] * MEMORY_SIZE
    memory[:len(data)] = data
    pc = 0

    while pc < len(data):
        opcode = memory[pc] & OPCODE_MASK
        _, _, size = get_spec(opcode)

        if pc + size > len(data):
            raise ValueError("Incomplete command")

        command = decode_command(bytes(memory[pc:pc + size]))
        pc += size
        execute_command(memory, command)

    return memory


def save_dump(memory, filename, start, end):
    """Save an inclusive range of memory addresses to XML."""
    check_address(start)
    check_address(end)

    if start > end:
        raise ValueError("Invalid address range")

    root = ET.Element("memory")

    for address in range(start, end + 1):
        cell = ET.SubElement(root, "cell", address=str(address))
        cell.text = str(memory[address])

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(filename, encoding="utf-8", xml_declaration=True)


def main():
    """Run the interpreter."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    args = parser.parse_args()

    try:
        with open(args.input, "rb") as file:
            data = file.read()

        memory = run_program(data)
        save_dump(memory, args.output, args.start, args.end)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print("Execution completed")
    print(f"Memory dump: {args.output}")


if __name__ == "__main__":
    main()