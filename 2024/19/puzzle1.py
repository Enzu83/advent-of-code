# Custom input
input_data = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

patterns = set()
designs = set()

for line in input_data:
    if ',' in line:
        patterns |= line.split(', ')

    elif len(line) > 0:
        designs.add(line)


# Functions

"""def addPatterns(patterns, parts, new_part):
    for part in parts:
        patterns.add(part + new_part)

def designPossible(design, patterns):
    idx = 0
    part_length = len(design)

    design_parts = []

    # iterate over all colors of the design
    while idx < len(design):
        print(len(patterns))
        # check if the current part of the design is a pattern
        # if not, increase the size of the pattern to search for new ones
        while part_length > 0 and design[idx:idx + part_length] not in patterns:
            part_length -= 1

        # if a matching pattern has been found, add it to the list of the parts
        if design[idx:idx + part_length] in patterns:
            addPatterns(patterns, design_parts, design[idx:idx + part_length]) # update the possible patterns

            design_parts.append(design[idx:idx + part_length])
            idx += part_length
            part_length = len(design) - idx

        # else, search for smaller previous part
        elif len(design_parts) > 0:
            previous_part = design_parts.pop()

            idx -= len(previous_part)
            part_length = len(previous_part) - 1
    
        # if there's no previous part, the design is not possible
        else:
            return False
    
    return sum(len(part) for part in design_parts) == len(design) """

def designPossible(desired_design, patterns):
    current_designs = {pattern for pattern in patterns if desired_design.startswith(pattern)}

    while len(current_designs) > 0 and desired_design not in current_designs:
        new_designs = set()

        for design in current_designs:
            


def countPossibleDesigns(designs, patterns):
    return sum(1 for design in designs if designPossible(design, patterns))


# Code

print(patterns)
#print(designPossible("gwruuugwgbbgbwrwgubbbuguwwgrruubwbrgugbgwwbwbbbrgwbubr", patterns))
print(countPossibleDesigns(designs, patterns))