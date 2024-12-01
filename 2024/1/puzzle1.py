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

left_list.sort()
right_list.sort()

# Functions
def getMinDifferences(left_list, right_list):
    distance = 0

    while len(left_list) > 0 and len(right_list) > 0:
        left_min = left_list.pop(0)
        right_min = right_list.pop(0)

        distance += abs(left_min - right_min)
    
    return distance

# Code

print(getMinDifferences(left_list, right_list))