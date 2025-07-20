# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

rules = {}
updates = []

for line in input_data:
    if '|' in line:
        first, second = line.split('|')

        if first not in rules:
            rules[first] = [second]
        else:
            rules[first].append(second)
        
        if second not in rules:
            rules[second] = []
    
    elif ',' in line:
        updates.append(line.split(','))


# Functions

def getRightOrder(update, rules):
    order = []

    for num in update:
        inserted = False

        for i in range(len(order)):
            if order[i] in rules[num]:
                order = order[:i] + [num] + order[i:]
                inserted = True
                break
        
        if inserted is False:
            order.append(num)

    return order


def checkRightOrder(update, rules):
    for i, num in enumerate(update):
        for next_num in rules[num]:
            for j in range(i):
                if next_num == update[j]:
                    return False

    return True

def countRightUpdates(updates, rules):
    result = 0

    for update in updates:
        if checkRightOrder(update, rules) is False:
            update = getRightOrder(update, rules)

            result += int(update[len(update)//2])

    return result


# Code

print(countRightUpdates(updates, rules))