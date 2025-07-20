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

def line_completion_score(line):
    chunk_openings = []

    for char in line:
        if char in {'(', '[', '{', '<'}:
            chunk_openings.append(char)

        elif len(chunk_openings) > 0:
            opening_char = chunk_openings.pop()
            if check_pair(opening_char, char) == False:
                return 0
        else:
            return 0
    
    opening_to_closing = {'(': ')', '[': ']', '{': '}', '<': '>'}
    completion_list = []

    for opening in reversed(chunk_openings):
        completion_list.append(opening_to_closing[opening])

    score_mapping = {')': 1, ']': 2, '}': 3, '>': 4}
    score = 0

    for char in completion_list:
        score = 5 * score + score_mapping[char]
    
    return score


# Code

scores = []

for line in input_data:
    line_score = line_completion_score(line)
    
    if line_score != 0:
        scores.append(line_score)
    
scores.sort()

print(scores[(len(scores)-1)//2])
