# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Functions

def dict_sum_value(dic):
    res = 0

    for key in dic:
        res += dic[key]

    return res

# Code

digit_occurrences = {'1': 0, '4': 0, '7': 0, '8': 0}

for output_digits in input_data:
    for digit in output_digits:
        if len(digit) == 2:
            digit_occurrences['1'] += 1
        elif len(digit) == 3:
            digit_occurrences['7'] += 1
        elif len(digit) == 4:
            digit_occurrences['4'] += 1
        elif len(digit) == 7:
            digit_occurrences['8'] += 1

print(dict_sum_value(digit_occurrences))
        