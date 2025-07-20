# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

wire_values = {} # "x00": 0
wire_relations = {} # z00: ("x00", "AND", "y00")

for line in input_data:
    if "->" in line:
        op, wire = line.split(" -> ")
        wire_relations[wire] = tuple(op.split(' '))
    
    elif len(line) > 0:
        wire, val = line.split(": ")
        wire_values[wire] = bool(int(val))

# Functions

def computeRelations(wire_values, wire_relations):
    # compute every possible relations
    for wire, (wire1, gate, wire2) in wire_relations.items():

        # check if all values of the relation are set
        if wire1 in wire_values and wire2 in wire_values:

            # different computation for each gate
            if gate == "AND":
                wire_values[wire] = wire_values[wire1] & wire_values[wire2]
            elif gate == "OR":
                wire_values[wire] = wire_values[wire1] | wire_values[wire2]
            elif gate == "XOR":
                wire_values[wire] = wire_values[wire1] ^ wire_values[wire2]


def getOutputWire(wire_values, wire_relations):
    output_wire_length = sum(1 for wire in wire_relations if wire[0] == 'z')

    # compute relations until all digits of 'z' are set
    while sum(1 for wire in wire_values if wire[0] == 'z') < output_wire_length:
        computeRelations(wire_values, wire_relations)
    
    # get digits of 'z' sorted in the correct order
    output_wire = sorted([(wire, str(int(wire_values[wire]))) for wire in wire_values if wire[0] == 'z'], key=lambda x: x[0], reverse=True)

    # only extract the binary value of the output wire
    return int(str().join([digit[1] for digit in output_wire]), 2)


# Code

print(getOutputWire(wire_values, wire_relations))
