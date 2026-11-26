import sys
import os

# Destination codes
DEST = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

# Jump codes
JUMP = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}


# Computation codes
COMP = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",

    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}


# Predefined symbols
SYMBOLS = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}

# Add R0 to R15
for i in range(16):
    SYMBOLS[f"R{i}"] = i


# Convert A-instruction into 16-bit binary
def assemble_a_instruction(instruction, line_number, labels):

    value = instruction[1:]

    if value in labels:
        address = labels[value]

    elif value in SYMBOLS:
        address = SYMBOLS[value]

    else:
        try:
            address = int(value)
        except ValueError:
            raise ValueError(
                f"Line {line_number}: Invalid A-instruction '{instruction}'"
            )

    if address < 0 or address > 32767:
        raise ValueError(
            f"Line {line_number}: Address out of range '{instruction}'"
        )

    return format(address, "016b")


# Convert C-instruction into 16-bit binary
def assemble_c_instruction(instruction, line_number):

    dest = ""
    jump = ""

    # Separate destination from computation
    if "=" in instruction:
        dest, instruction = instruction.split("=")

    # Separate computation from jump
    if ";" in instruction:
        instruction, jump = instruction.split(";")

    # Validate instruction components
    if instruction not in COMP:
        raise ValueError(
            f"Line {line_number}: Invalid computation"
        )

    if dest not in DEST:
        raise ValueError(
            f"Line {line_number}: Invalid destination"
        )

    if jump not in JUMP:
        raise ValueError(
            f"Line {line_number}: Invalid jump"
        )

    return "111" + COMP[instruction] + DEST[dest] + JUMP[jump]



# First pass: Identify labels
def first_pass(lines):

    labels = {}
    rom_address = 0

    for line_number, line in enumerate(lines, start=1):

        line = line.split("//")[0].strip()

        if not line:
            continue

        # Check for label declaration
        if line.startswith("(") and line.endswith(")"):

            label = line[1:-1]

            if not label:
                raise ValueError(
                    f"Line {line_number}: Empty label"
                )

            if label in labels or label in SYMBOLS:
                raise ValueError(
                    f"Line {line_number}: Duplicate label '{label}'"
                )

            labels[label] = rom_address

        else:
            rom_address += 1

    return labels



# Second pass: Convert instructions and resolve variables
def second_pass(lines, labels):

    machine_code = []
    next_variable_address = 16
    variables = {}

    for line_number, line in enumerate(lines, start=1):

        line = line.split("//")[0].strip()

        if not line or (line.startswith("(") and line.endswith(")")):
            continue

        if line.startswith("@"):

            symbol = line[1:]

            if (not symbol.isdigit()
                and symbol not in SYMBOLS
                and symbol not in labels):

                if symbol not in variables:
                    variables[symbol] = next_variable_address
                    next_variable_address += 1

                SYMBOLS[symbol] = variables[symbol]

            machine_code.append(
                assemble_a_instruction(line, line_number, labels)
            )

        else:
            machine_code.append(
                assemble_c_instruction(line, line_number)
            )

    return machine_code




# Main assembler function
def assemble(input_file):

    with open(input_file, "r") as file:
        lines = file.readlines()

    # Pass 1: Find labels
    labels = first_pass(lines)

    # Pass 2: Generate machine code
    machine_code = second_pass(lines, labels)

    # Create output filename
    output_file = os.path.splitext(input_file)[0] + ".hack"

    with open(output_file, "w") as file:
        for instruction in machine_code:
            file.write(instruction + "\n")

    print(f"Assembly successful! Output: {output_file}")


# Program entry point
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python assembler.py <file.asm>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        assemble(input_file)

    except (ValueError, OSError) as error:
        print("Assembler Error:", error)
        sys.exit(1)