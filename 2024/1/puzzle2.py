# Custom input
input_data = """3   4
4   3
2   5
1   3
3   9
3   3"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting
left_list = []
right_list = []

for line in input_data:
    left, right = line.split()
    left_list.append(int(left))
    right_list.append(int(right))


# Functions
def getSimilarityScore(left_list, right_list):
    score = 0

    right_occurences = {}

    # right list numbers occurences
    for num in right_list:
        if num not in right_occurences:
            right_occurences[num] = 1
        else:
            right_occurences[num] += 1
    
    # score
    for num in left_list:
        if num in right_occurences:
            score += num * right_occurences[num]
    
    return score

# Code

print(getSimilarityScore(left_list, right_list))