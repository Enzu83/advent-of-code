# Custom input
input_data = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')

# Vent positions list

vent_positions = []

for line in input_data:
    begin, end = line.split(' -> ')

    begin = [int(pos) for pos in begin.split(',')]
    end = [int(pos) for pos in end.split(',')]

    vent_positions.append([begin, end])

# Grid creation

x_max = 0
y_max = 0

for vent in vent_positions:
    [x_begin, y_begin], [x_end, y_end] = vent

    if x_begin == x_end or y_begin == y_end:
        if x_begin > x_max:
            x_max = x_begin
        elif x_end > x_max:
            x_max = x_end

        if y_begin > y_max:
            y_max = y_begin
        elif y_end > y_max:
            y_max = y_end

grid = [[0 for _ in range(y_max+1)] for _ in range(x_max+1)]

# Put vents in grid

for vent in vent_positions:
    [x_begin, y_begin], [x_end, y_end] = vent

    if x_begin == x_end:
        x = x_begin

        if y_end < y_begin:
            y_begin, y_end = y_end, y_begin
        
        for y in range(y_begin, y_end+1):
            grid[x][y] += 1

    elif y_begin == y_end:
        y = y_begin

        if x_end < x_begin:
            x_begin, x_end = x_end, x_begin
        
        for x in range(x_begin, x_end+1):
            grid[x][y] += 1


# Count overlap

overlap = 0

for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] > 1:
            overlap += 1

print(overlap)
