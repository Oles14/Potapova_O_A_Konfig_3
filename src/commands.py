OPCODE_BITS = 4
OPCODE_MASK = (1 << OPCODE_BITS) - 1

LOAD = 4
READ = 9
WRITE = 0
SHR = 3

COMMANDS = {
    "LOAD": (LOAD, (21, 12), 5),
    "READ": (READ, (12, 6, 12), 5),
    "WRITE": (WRITE, (12, 12), 4),
    "SHR": (SHR, (12, 12, 12), 5),
}


def get_spec(opcode):
    """Find the command specification by opcode."""
    for spec in COMMANDS.values():
        if spec[0] == opcode:
            return spec

    raise ValueError(f"Unknown opcode: {opcode}")


def encode_command(command):
    """Convert an instruction tuple into machine bytes."""
    opcode, widths, size = get_spec(command[0])
    word = opcode
    offset = OPCODE_BITS

    for value, bits in zip(command[1:], widths):
        word |= value << offset
        offset += bits

    return word.to_bytes(size, byteorder="little")


def decode_command(data):
    """Convert machine bytes into an instruction tuple."""
    word = int.from_bytes(data, byteorder="little")
    opcode = word & OPCODE_MASK
    _, widths, size = get_spec(opcode)

    if len(data) != size:
        raise ValueError("Incomplete command")

    fields = [opcode]
    offset = OPCODE_BITS

    for bits in widths:
        mask = (1 << bits) - 1
        value = (word >> offset) & mask
        fields.append(value)
        offset += bits

    return tuple(fields)