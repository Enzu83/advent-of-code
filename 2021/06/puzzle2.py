# Custom input
input_data = """3,4,3,1,2"""
input_data = input_data.split(',')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data = input_data[0].split(',')


# Functions
        
def update_fish(fish):
    zero_fish = fish['0']

    for i in range(1, 9):
        fish[str(i-1)] = fish[str(i)]
    
    fish['8'] = zero_fish
    fish['6'] += zero_fish

def total_fish(fish):
    fish_number = 0
    for state in fish:
        fish_number += fish[state]
    
    return fish_number

# Code

fish = {str(i):0 for i in range(9)}

for data in input_data:
    fish[data] += 1
    
print(fish)

total_days = 256

for day in range(total_days):
    print("Day " + str(day) + "...")
    update_fish(fish)

print("Day " + str(total_days) + "...")
print(fish)
print(total_fish(fish))