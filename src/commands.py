OPCODE_BITS = 4

COMMANDS = {
    "LOAD": (4, (21, 12), 5),
    "READ": (9, (12, 6, 12), 5),
    "WRITE": (0, (12, 12), 4),
    "SHR": (3, (12, 12, 12), 5),
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