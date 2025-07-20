# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Functions

def check_pair(opening, closing):
    if opening + closing in {"()", "[]", "{}", "<>"}:
        return True
    else:
        return False


def check_line_validity(line):
    chunk_openings = []

    for char in line:
        if char in {'(', '[', '{', '<'}:
            chunk_openings.append(char)

        elif len(chunk_openings) > 0:
            opening_char = chunk_openings.pop()
            if check_pair(opening_char, char) == False:
                return (False, char)
        else:
            return (False, char)
    
    return (True, '')


# Code

score_mapping = {')': 3, ']': 57, '}': 1197, '>': 25137}

score = 0

for line in input_data:
    check, char = check_line_validity(line)

    if check == False:
        score += score_mapping[char]

print(score)
