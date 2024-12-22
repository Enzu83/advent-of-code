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
towels = set()

for line in input_data:
    if ',' in line:
        patterns = set(line.split(', '))

    elif len(line) > 0:
        towels.add(line)


# Functions

def countPossibleDesigns(towel, patterns):
    designs = {pattern: 1 for pattern in patterns if towel.startswith(pattern)}
    designs[towel] = 0

    queue = list(designs.keys())

    while queue:
        queue.sort(key=len)
        design = queue.pop(0)

        for pattern in patterns:
            if towel.startswith(design + pattern):

                if design + pattern not in designs:
                    designs[design + pattern] = designs[design]
                    queue.append(design + pattern)
                else:
                    designs[design + pattern] += designs[design]

    return designs[towel]

def countAllPossibleDesigns(towels, patterns):
    return sum(countPossibleDesigns(towel, patterns) for towel in towels)


# Code

print(countAllPossibleDesigns(towels, patterns))