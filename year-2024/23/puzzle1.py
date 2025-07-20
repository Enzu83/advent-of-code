# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

connections = {}
pairs = set()

for line in input_data:
    computer1, computer2 = line.split('-')

    pairs.add((computer1, computer2))

    if computer1 not in connections:
        connections[computer1] = {computer2}
    else:
        connections[computer1].add(computer2)
    
    if computer2 not in connections:
        connections[computer2] = {computer1}
    else:
        connections[computer2].add(computer1)


# Functions

def getConnectedTriplets(connections, pairs):
    triplets = set()

    for computer, linked_computers in connections.items():
        for computer1, computer2 in pairs:
            if computer != computer1 and computer != computer2 and (computer1 in linked_computers and computer2 in linked_computers):
                triplets.add(tuple(sorted([computer, computer1, computer2])))
    
    return triplets

def sumTripletsWithComputer(triplets, computer_name):
    return sum(1 for triplet in triplets if any(computer[0] == computer_name for computer in triplet))

# Code

triplets = getConnectedTriplets(connections, pairs)

print(sumTripletsWithComputer(triplets, 't'))
