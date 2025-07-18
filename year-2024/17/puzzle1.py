# Custom input
input_data = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

instructions = []
register = {}

for line in input_data:
    # register values
    if line.startswith("Register A"):
        register['A'] = int(line.split(": ")[1])
    elif line.startswith("Register B"):
        register['B'] = int(line.split(": ")[1])
    elif line.startswith("Register C"):
        register['C'] = int(line.split(": ")[1])

    # instructions
    elif line.startswith("Program"):
        instructions = list(map(int, line.split(": ")[1].split(",")))
        

# Functions

def getComboOperand(literal_operand, register):
    if literal_operand == 4:
        return register['A']
    elif literal_operand == 5:
        return register['B']
    elif literal_operand == 6:
        return register['C']
    else:
        return literal_operand
    

def performInstruction(instructions, pointer, register):
    # instructions parameters
    opcode = instructions[pointer]
    literal_operand = instructions[pointer+1]
    combo_operand = getComboOperand(literal_operand, register)

    # output print
    output = None

    # LO: literal operand
    # CO: combo operand

    # adv: A // 2^CO -> A
    if opcode == 0:
        register['A'] = register['A'] // 2**combo_operand
        pointer += 2

    # bxl: B XOR LO -> B
    elif opcode == 1:
        register['B'] = register['B'] ^ literal_operand
        pointer += 2

    # bst: CO % 8 -> B
    elif opcode == 2:
        register['B'] = combo_operand % 8
        pointer += 2

    # jnz: A != 0 => goto LO
    elif opcode == 3:
        if register['A'] != 0:
            pointer = literal_operand
        else:
            pointer += 2

    # bxc: B XOR C -> B
    elif opcode == 4:
        register['B'] = register['B'] ^ register['C']
        pointer += 2

    # out: print(CO % 8)
    elif opcode == 5:
        output = combo_operand % 8
        pointer += 2

    # bdv: A // 2^CO -> B
    elif opcode == 6:
        register['B'] = register['A'] // 2**combo_operand
        pointer += 2

    # cdv: A // 2^CO -> C
    elif opcode == 7:
        register['C'] = register['A'] // 2**combo_operand
        pointer += 2

    
    return output, pointer
    

def readInstructions(instructions, register):
    pointer = 0

    full_output = []

    while pointer < len(instructions)-1:
        output, pointer = performInstruction(instructions, pointer, register)

        if output is not None:
            full_output.append(output)

    
    return ",".join(map(str, full_output))

# Code

print(readInstructions(instructions, register))