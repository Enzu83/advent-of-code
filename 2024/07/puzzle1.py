# Custom input
input_data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting
equations = {}

for line in input_data:
    line = line.replace(':', '').split()

    equations[int(line[0])] = []

    for i in range(1, len(line)):
        equations[int(line[0])].append(int(line[i]))

# Functions
def getResult(numbers, operations):
    result = numbers[0]

    for i in range(len(operations)):
        if operations[i] == '+':
            result += numbers[i+1]
        elif operations[i] == '*':
            result *= numbers[i+1]
    
    return result

def findCombination(result, numbers):
    operations = ['+']
    
    previous_operations = set()

    while len(operations) > 0:
        if len(operations) == len(numbers)-1 and getResult(numbers, operations) == result:
            return True
        
        # if it's not the right result, try another combination
        if len(operations) < len(numbers)-1 and "".join(operations) + '+' not in previous_operations:
            operations.append('+')
        elif len(operations) < len(numbers)-1 and "".join(operations) + '*' not in previous_operations:
            operations.append('*')
        else:
            if len(operations) == 1 and '+' not in previous_operations:
                operations = ['+']
            elif len(operations) == 1 and '*' not in previous_operations:
                operations = ['*']
            else:
                operations.pop()

        previous_operations.add("".join(operations))

    return False


def totalCalibrationResult(equations):
    total_result = 0

    for result in equations:
        if findCombination(result, equations[result]):
            total_result += result

    return total_result

# Code

print(totalCalibrationResult(equations))