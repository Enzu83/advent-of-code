# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

input_data = [line.split('-') for line in input_data]


# Functions

def create_graph(data):
    nodes = set()
    neighbors = {}

    for edge in data:
        for i in range(2):
            nodes.add(edge[i])

            if edge[i] not in neighbors:
                neighbors[edge[i]] = {edge[1-i]}
            else:
                neighbors[edge[i]].add(edge[1-i])
    
    return nodes, neighbors
            
def is_big_cave(node):
    for char in node:
        if char.islower():
            return False
    
    return True

def get_available_neighbor(graph, node, path, all_paths):
    for neighbor in graph[1][node]:
        if path + [neighbor] not in all_paths and (is_big_cave(neighbor) or neighbor not in path):
            return neighbor
    
    return ''
    

def find_all_paths(graph, start, end):
    all_paths = []

    path = [start]

    while len(path) > 0:
        node = path[-1]

        best_neighbor = get_available_neighbor(graph, node, path, all_paths)

        if best_neighbor == '':
            path.pop()

        elif best_neighbor == end:
            all_paths.append(path + [end])

        else:
            path.append(best_neighbor)
            all_paths.append(path.copy())
    
    return [path for path in all_paths if end in path]


# Code

graph = create_graph(input_data)

paths = find_all_paths(graph, 'start', 'end')

for path in paths:
    print(path)

one_small_cave_paths = 0

for path in paths:
    if sum([1 for cave in path if is_big_cave(cave) == False and cave not in {'start', 'end'}]):
        one_small_cave_paths += 1

print(one_small_cave_paths)