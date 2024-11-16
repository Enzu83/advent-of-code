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
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting
sequence = ""
instructions = {}

for i in range(len(input_data)):
    line = input_data[i]

    if i == 0:
        sequence = line
    elif i > 1:
        pair, res = line.split(' -> ')
        instructions[pair] = {pair[0] + res, res + pair[1]}

# Functions

def string_to_count(sequence):
    sequence_count = {"first": sequence[0], 'last': sequence[-1]}

    for i in range(len(sequence)-1):
        pair = sequence[i] + sequence[i+1]

        if pair not in sequence_count:
            sequence_count[pair] = 1
        else:
            sequence_count[pair] += 1
    
    return sequence_count

def next_count(sequence_count, instructions):
    new_sequence_count = {"first": sequence_count["first"], "last": sequence_count["last"]}

    for pair in sequence_count:
        if pair not in {"first", "last"}:
            for new_pair in instructions[pair]:
                if new_pair not in new_sequence_count:
                    new_sequence_count[new_pair] = sequence_count[pair]
                else:
                    new_sequence_count[new_pair] += sequence_count[pair]
        
    return new_sequence_count

def count_letters(sequence_count):
    letter_occurrences = {}

    for pair in sequence_count:
        if pair not in {"first", "last"}:
            for letter in pair:
                if letter not in letter_occurrences:
                    letter_occurrences[letter] = sequence_count[pair]
                else:
                    letter_occurrences[letter] += sequence_count[pair]
    
    for letter in letter_occurrences:
        letter_occurrences[letter] = letter_occurrences[letter] // 2
    
    letter_occurrences[sequence_count["first"]] += 1
    letter_occurrences[sequence_count["last"]] += 1

    return letter_occurrences

def get_result(letter_occurrences):
    min_occurrence = min(letter_occurrences.values())
    max_occurrence = max(letter_occurrences.values())

    return max_occurrence - min_occurrence


# Code

sequence_count = string_to_count(sequence)

total_steps = 40

for step in range(total_steps):
    print(f"Step {step}")
    print(sequence_count)
    sequence_count = next_count(sequence_count, instructions)

print(f"Step {total_steps}")
print(sequence_count)

print(get_result(count_letters(sequence_count)))