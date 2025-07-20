# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

patterns = set()
towels = set()

for line in input_data:
    if ',' in line:
        patterns = set(line.split(', '))

    elif len(line) > 0:
        towels.add(line)


# Functions

def isDesignPossible(towel, patterns):
    designs = {pattern for pattern in patterns if towel.startswith(pattern)}

    while len(designs) > 0 and towel not in designs:
        new_designs = set()

        for design in designs:
            for pattern in patterns:
                if towel.startswith(design + pattern):
                    new_designs.add(design + pattern)

        designs = new_designs

    return towel in designs

def countPossibleDesigns(towels, patterns):
    return sum(isDesignPossible(towel, patterns) for towel in towels)


# Code

print(countPossibleDesigns(towels, patterns))