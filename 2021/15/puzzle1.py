import numpy as np

# Custom input
input_data = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

rows, cols = len(input_data), len(input_data[0])

grid = np.zeros((rows, cols))

for i in range(rows):
    for j in range(cols):
        grid[i, j] = input_data[i][j]


# Functions

def get_nearest_neighbor(frontier, distance):
    nearest_node = (0, 0)
    minimum_distance = float("inf")

    for node in frontier:
        if node in distance and distance[node] < minimum_distance:
            nearest_node = node
            minimum_distance = distance[node]
    
    return nearest_node

def get_neighbors(grid, node):
    i, j = node

    neighbors = set()

    if i > 0:
        neighbors.add((i-1, j))
    if i < len(grid)-1:
        neighbors.add((i+1, j))
    if j > 0:
        neighbors.add((i, j-1))
    if j < len(grid[0])-1:
        neighbors.add((i, j+1))

    return neighbors

def get_path(parent):
    current_node = (len(grid)-1, len(grid[0])-1)
    path = [current_node]

    while not parent [current_node] is None:
        current_node = parent[current_node]
        path.append(current_node)

    path.reverse()
    return path

def find_shortest_path(grid):
    start = (0, 0)
    end = (len(grid), len(grid[0]))

    frontier = {start}
    parent = {start: None}
    distance = {start: 0}

    while len(frontier) > 0:
        nearest_node = get_nearest_neighbor(frontier, distance)
        frontier.remove(nearest_node)


        for neighbor in get_neighbors(grid, nearest_node):
            if neighbor not in parent:
                frontier.add(neighbor)
            
            node_distance = distance[nearest_node] + grid[nearest_node]

            if neighbor not in distance or node_distance < distance[neighbor]:
                distance[neighbor] = node_distance
                parent[neighbor] = nearest_node

    return get_path(parent)

def get_risk(grid, path):
    risk = 0

    for node in path:
        if node != (0, 0):
            risk += int(grid[node])

    return risk


# Code

path = find_shortest_path(grid)

print(get_risk(grid, path))