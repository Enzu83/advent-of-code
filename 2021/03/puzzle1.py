# Custom input
input_data = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""
input_data = input_data.split('\n')

# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

# Functions
def getO2(diagnostic):
    bit_frequency = {i: [0, 0] for i in range(len(diagnostic[0]))}

    for number in diagnostic:
        for i, bit in enumerate(map(int, number)):
            bit_frequency[i][bit] += 1
    
    o2 = ""
    epsilon = ""

    for i in bit_frequency:
        if bit_frequency[i][0] < bit_frequency[i][1]:
            o2 += '1'
            epsilon += '0'
        else:
            o2 += '0'
            epsilon += '1'

    return int(o2, 2) * int(epsilon, 2)


# Code

print(getO2(input_data))