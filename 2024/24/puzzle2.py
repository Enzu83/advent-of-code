# Custom input
input_data = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

wire_values = {} # "x00": 0
wire_to_relation = {} # z00: ("x00", "AND", "y00")
relation_to_wire = {} # ("x00", "AND", "y00"): z00

for line in input_data:
    if "->" in line:
        op, wire = line.split(" -> ")
        wire1, gate, wire2 = op.split(' ')

        relation_to_wire[(wire1, gate, wire2)] = wire
        wire_to_relation[wire] = (wire1, gate, wire2)
    
    elif len(line) > 0:
        wire, val = line.split(": ")
        wire_values[wire] = int(val)

# Functions

def computeRelations(wire_values, wire_to_relation):
    # compute every possible relations
    for wire, (wire1, gate, wire2) in wire_to_relation.items():

        # check if all values of the relation are set
        if wire1 in wire_values and wire2 in wire_values:

            # different computation for each gate
            if gate == "AND":
                wire_values[wire] = wire_values[wire1] & wire_values[wire2]
            elif gate == "OR":
                wire_values[wire] = wire_values[wire1] | wire_values[wire2]
            elif gate == "XOR":
                wire_values[wire] = wire_values[wire1] ^ wire_values[wire2]

def getOutputWire(wire_values, wire_to_relation):
    output_wire_length = sum(1 for wire in wire_to_relation if wire[0] == 'z')

    # compute relations until all digits of 'z' are set
    while sum(1 for wire in wire_values if wire[0] == 'z') < output_wire_length:
        computeRelations(wire_values, wire_to_relation)
    
    # get digits of 'z' sorted in the correct order
    output_wire = sorted([(wire, str(int(wire_values[wire]))) for wire in wire_values if wire[0] == 'z'], key=lambda x: x[0], reverse=True)

    # only extract the binary value of the output wire
    return int(str().join([digit[1] for digit in output_wire]), 2)
          
def getWrongWires():
    wrong_wires = set()

    # wrong 'z' output computation (without XOR gate)
    for wire, relation in wire_to_relation.items():
        if wire[0] == 'z' and relation[1] != "XOR" and wire != "z45":
            wrong_wires.add(wire)

    # wrong gate after x XOR y and x AND y
    for relation, wire in relation_to_wire.items():
        if {relation[0][0], relation[2][0]} == {'x', 'y'} and int(relation[0][1:]) > 0:
            for relation2 in relation_to_wire:
                if wire in {relation2[0], relation2[2]} and ((relation[1] == "XOR" and relation2[1] == "OR") or relation[1] == "AND" and relation2[1] == "XOR"):
                    wrong_wires.add(wire)

    # double XOR impossible without a 'z output
    for relation, wire in relation_to_wire.items():
        if {relation[0][0], relation[2][0]} == {'x', 'y'}:
            for relation2, wire2 in relation_to_wire.items():
                if wire in {relation2[0], relation2[2]} and relation[1] == "XOR" and relation2[1] == "XOR" and wire2[0] != 'z':
                    wrong_wires.add(wire2)
    
    return ",".join(sorted(wrong_wires))

# Code

print(getWrongWires())