# Custom input
input_data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""
input_data = input_data.split('\n')


# Input from file
# input_data = open("input.txt").read().split('\n')
# input_data.pop()


# Formatting
sequence = []
instructions = {}


for i in range(len(input_data)):
    line = input_data[i]

    if i == 0:
        sequence = line
    elif i > 1:
        pair, res = line.split(' -> ')
        instructions[pair] = res


# Functions

def find_new_sequence(sequence, instructions):
    if len(sequence) == 1:
        return sequence
    
    elif len(sequence) == 2:
        return sequence[:len(sequence)//2] + instructions[sequence] + sequence[len(sequence)//2:]
    
    elif sequence in instructions:
        return instructions[sequence]
    
    else:
        new_sequence = find_new_sequence(sequence[:len(sequence)//2], instructions) + instructions[sequence[len(sequence)//2-1] + sequence[len(sequence)//2]] + find_new_sequence(sequence[len(sequence)//2:], instructions)

        instructions[sequence] = new_sequence

        return new_sequence


def get_sequence_result(sequence):
    occurrences = {}

    for letter in sequence:
        if letter not in occurrences:
            occurrences[letter] = 1
        else:
            occurrences[letter] += 1
    
    min_occurrence = min(occurrences.values())
    max_occurrence = max(occurrences.values())

    return max_occurrence - min_occurrence


# Code

for step in range(10):
    print(sequence)
    sequence = find_new_sequence(sequence, instructions)
    
print(sequence)
print(get_sequence_result(sequence))