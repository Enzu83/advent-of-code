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

def is_second_visit_available(path):
    small_caves_visit = {}

    for cave in path:
        if is_big_cave(cave) == False and cave not in {'start', 'end'}:
            if cave not in small_caves_visit:
                small_caves_visit[cave] = 1
            else:
                small_caves_visit[cave] += 1
    
    for cave in small_caves_visit:
        if small_caves_visit[cave] == 2:
            return False
    
    return True

def check_second_small_cave_visit(path, node):
    if node in {'start', 'end'}:
        return False
    else:
        return is_second_visit_available(path)

def is_path_already_in(path, path_tree):
    current_tree = path_tree

    for node in path:
        if node in current_tree:
            current_tree = current_tree[node]
        else:
            return False
    
    return True

def add_path(path, path_tree):
    current_tree = path_tree

    for node in path:
        if node not in current_tree:
            current_tree[node] = {}
        
        current_tree = current_tree[node]

def get_available_neighbor(graph, node, path, path_tree):
    for neighbor in graph[1][node]:

        if neighbor != 'start' and is_path_already_in(path + [neighbor], path_tree) == False and (is_big_cave(neighbor) or (neighbor not in path or check_second_small_cave_visit(path, node))):
            return neighbor
    
    return ''
    
def get_paths(path_tree, current_node, path=None):
    if path == None:
        path = []

    path.append(current_node)

    if current_node == 'end':
        return [path]
    else:
        paths = []

        for node in path_tree[current_node].keys():
            paths += get_paths(path_tree[current_node], node, path.copy())
    
    return paths

def find_path_tree(graph):
    path_tree = {}

    path = ['start']

    while len(path) > 0:
        node = path[-1]

        best_neighbor = get_available_neighbor(graph, node, path, path_tree)

        if best_neighbor == '':
            path.pop()

        elif best_neighbor == 'end':
            add_path(path + ['end'], path_tree)

    
        else:
            path.append(best_neighbor)
            add_path(path, path_tree)
        

    return get_paths(path_tree, 'start')


# Code

graph = create_graph(input_data)

paths = find_path_tree(graph)

print(len(paths))