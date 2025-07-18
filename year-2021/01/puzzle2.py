# Custom input
input_data = """199
200
208
210
200
207
240
269
260
263"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting
measurements = list(map(int, input_data))

# Functions
def getIncreaseMeasurements(measurements):
    increase_measurement = 0

    previous_sum = sum(measurements[:3])

    for i in range(3, len(measurements)):
        current_sum = sum(measurements[i-2:i+1])

        if current_sum > previous_sum:
            increase_measurement += 1

        previous_sum = current_sum
    
    return increase_measurement

# Code

print(getIncreaseMeasurements(measurements))