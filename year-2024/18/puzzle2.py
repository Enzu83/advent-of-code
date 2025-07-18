# Custom input
input_data = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

corrupted_bytes = [tuple(map(int, byte.split(','))) for byte in input_data]


# Functions

def getNeighbors(byte, size, corrupted_bytes):
    x, y = byte

    neighbors = set()

    if y > 0 and (x, y - 1) not in corrupted_bytes:
        neighbors.add((x, y - 1))
    
    if x > 0 and (x - 1, y) not in corrupted_bytes:
        neighbors.add((x - 1, y))
    
    if y < size and (x, y + 1) not in corrupted_bytes:
        neighbors.add((x, y + 1))
    
    if x < size and (x + 1, y) not in corrupted_bytes:
        neighbors.add((x + 1, y))

    return neighbors


def getMinimumCostByte(bytes, costs):
    return min(bytes, key=lambda byte: costs[byte])

def getShortestPathLength(corrupted_bytes, size):

    # graph
    remaining_bytes = {(x, y) for x in range(size + 1) for y in range(size + 1) if (x, y) not in corrupted_bytes}
    costs = {byte: float("inf") for byte in remaining_bytes}

    costs[(0, 0)] = 0

    # exploration
    while remaining_bytes:
        current = getMinimumCostByte(remaining_bytes, costs)
        remaining_bytes.remove(current)

        for neighbor in getNeighbors(current, size, corrupted_bytes):
            if neighbor in remaining_bytes:
                if costs[current] + 1 < costs[neighbor]:
                    costs[neighbor] = costs[current] + 1

    
    return costs[(size, size)]

def getFirstByteWithNoExit(corrupted_bytes, size):
    lower = 0
    upper = len(corrupted_bytes)-1

    while abs(upper - lower) > 1:
        middle = (upper + lower) // 2

        if getShortestPathLength(set(corrupted_bytes[:middle]), size) == float("inf"):
            upper = middle
        else:
            lower = middle
    
    return corrupted_bytes[lower]

def printGrid(size, corrupted_bytes):
    for x in range(size + 1):
        for y in range(size + 1):
            if (x, y) in corrupted_bytes:
                print('#', end="")
            else:
                print('.', end="")

        print("")
    
    print("")


# Code

grid_size = 70

print(getFirstByteWithNoExit(corrupted_bytes, grid_size))