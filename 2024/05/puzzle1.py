# Custom input
input_data = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
input_data = input_data.split('\n')


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
        if checkRightOrder(update, rules):
            result += int(update[len(update)//2])
    
    return result


# Code

print(countRightUpdates(updates, rules))
