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


# Code

# Oxygen
oxygen = input_data.copy()
position = 0

while len(oxygen) > 1 and position < len(oxygen[0]):
    zero_bits = 0
    one_bits = 0

    for number in oxygen:
        if number[position] == "0":
            zero_bits += 1
        else:
            one_bits += 1
    
    most_common_bit = int(one_bits >= zero_bits)

    # Next step
    oxygen = [data for data in oxygen if int(data[position]) == most_common_bit]
    position += 1

oxygen = int(oxygen[0], 2)

# CO2
co2 = input_data.copy()
position = 0

while len(co2) > 1 and position < len(co2[0]):
    zero_bits = 0
    one_bits = 0

    for number in co2:
        if number[position] == "0":
            zero_bits += 1
        else:
            one_bits += 1
    
    most_common_bit = int(one_bits >= zero_bits)

    # Next step
    co2 = [data for data in co2 if int(data[position]) != most_common_bit]
    position += 1

co2 = int(co2[0], 2)

print(oxygen * co2)