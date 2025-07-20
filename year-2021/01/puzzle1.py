# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting
measurements = list(map(int, input_data))

# Functions
def getIncreaseMeasurements(measurements):
    increase_measurement = 0

    for i in range(1, len(measurements)):
        if measurements[i-1] < measurements[i]:
            increase_measurement += 1
    
    return increase_measurement

# Code

print(getIncreaseMeasurements(measurements))