input_data = open("input.txt").read().split('\n')


increase_measurement = 0


previous_sum = int(input_data[0]) + int(input_data[1]) + int(input_data[2])

i = 3

while input_data[i] != "":
    current_sum = int(input_data[i-2]) + int(input_data[i-1]) + int(input_data[i])

    if current_sum > previous_sum:
        increase_measurement += 1

    previous_sum = current_sum
    i += 1

print(increase_measurement)
