# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting


# Functions
def getO2(diagnostic):
    oxygen = diagnostic.copy()
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

    return int(oxygen[0], 2)

def getCO2(diagnostic):
    co2 = diagnostic.copy()
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

    return int(co2[0], 2)

# Code

o2 = getO2(input_data)
co2 = getCO2(input_data)

print(o2 * co2)