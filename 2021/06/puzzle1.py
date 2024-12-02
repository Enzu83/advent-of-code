# Custom input
input_data = """3,4,3,1,2"""
input_data = input_data.split(',')


# Input from file
# input_data = open("input.txt").read().split('\n')
# input_data = input_data[0].split(',')


# Functions

def print_fish(fish, day):
    if day == 0:
        message = "Initial state: "
    elif day == 1:
        message = "After  " + str(day) + " day:  "
    elif day < 10:
        message = "After  " + str(day) + " days: "
    else:
        message = "After " + str(day) + " days: "
    
    for i in range(len(fish)):
        if i == 0:
            message += str(fish[i])
        else:
            message += "," + str(fish[i])
    
    print(message)
        

def update_fish(fish):
    for i in range(len(fish)):
        if fish[i] == 0:
            fish[i] = 6
            fish.append(8)
        else:
            fish[i] -= 1

# Code

fish = [int(data) for data in input_data]

total_days = 80

for day in range(total_days):
    print("Day " + str(day) + "...")
    #print_fish(fish, day)
    update_fish(fish)

#print_fish(fish, total_days)
print("Day " + str(total_days) + "...")
print(len(fish))