# Custom input
input_data = """029A
980A
179A
456A
379A"""
input_data = input_data.split('\n')


# Input from file
# input_data = open("input.txt").read().split('\n')
# input_data.pop()


# Formatting

num_grid = [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], [None, '0', 'A']]
dir_grid = [[None, '^', 'A'], ['<', 'v', '>']]

dir_to_delta = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0)
}

# Functions

"""def getSequence(start, end, grid):
    # grid info
    start = findPositionInGrid(start, grid)
    end = findPositionInGrid(end, grid)

    delta = (end[0] - start[0], end[1] - start[1])

    # build sequence
    sequence = "" # vertical first
    sequence2 = "" # horizontal first

    # horizontal movement
    if delta[0] > 0:
        sequence += 'v' * delta[0]
    elif delta[0] < 0:
        sequence += '^' * (-delta[0])

    # vertical movement
    if delta[1] > 0:
        sequence2 = '>' * delta[1] + sequence
        sequence += '>' * delta[1]
    elif delta[1] < 0:
        sequence2 = '<' * (-delta[1]) + sequence
        sequence += '<' * (-delta[1])
        
    
    if validSequence(sequence, start, grid):
        return sequence
    else:
        return sequence2


def getCodeSequence(code, grid):
    code = 'A' + code
    sequence = ""

    for i in range(len(code)-1):
        sequence += getSequence(code[i], code[i+1], grid) + 'A'
    
    return sequence

def getFullSequence(code):
    sequence = getCodeSequence(code, num_grid)

    for _ in range(2):
        sequence = getCodeSequence(sequence, dir_grid)
    
    return sequence"""

def checkSequence(grid, sequence, start, end):
    for dir in sequence:
        if dir != 'A':
            delta = dir_to_delta[dir]
            start = (start[0] + delta[0], start[1] + delta[1])

            if not(0 <= start[0] < len(grid) and 0 <= start[1] < len(grid[0]) and grid[start[0]][start[1]] is not None):
                return False
    
    return start == end

def findPositionInGrid(grid, key):
    for x in range(len(grid)):
        for y, grid_key in enumerate(grid[x]):
            if key == grid_key:
                return (x, y)
    
    return None

def getSequence(start, end):
    delta = (end[0] - start[0], end[1] - start[1])
    moves = ""

    # horizontal moves
    if delta[1] == 0:
        if delta[0] > 0:
            moves = 'v' * delta[0]
        elif delta[0] < 0:
            moves = '^' * (-delta[0])

    # vertical moves
    elif delta[0] == 0:
        if delta[1] > 0:
            moves = '>' * delta[1]
        elif delta[1] < 0:
            moves = '<' * (-delta[1])
    
    return moves

def buildSequence(num_start, num_end):
    # get info about the sequence
    start = findPositionInGrid(num_grid, num_start)
    end = findPositionInGrid(num_grid, num_end)
    num_moves = getSequence(start, end)

    # find the best valid sequence that minimize the moves
    num_sequence = ""
    dir_sequences = ["", "", ""]

    minimum_moves = float("inf")

    for possible_num_sequence in zip(list(num_moves), list(num_moves)):
        if checkSequence(num_grid, possible_num_sequence, start, end):
            possible_num_sequence = num_start + possible_num_sequence

            still_valid = True

            while still_valid:
                for i in range(len(possible_num_sequence)-1):
                    dir_sequences[0] = 0


    return num_sequence + dir_sequences

def getMove(delta):
    if delta == (0, 1):
        return '>'
    
    if delta == (0, -1):
        return '<'
    
    if delta == (1, 0):
        return 'v'
    
    if delta == (-1, 0):
        return '^'

def getDelta(move):
    if move == '>':
        return (0, 1)
    
    if move == '<':
        return (0, -1)
    
    if move == 'v':
        return (1, 0)
    
    if move == '^':
        return (-1, 0)

def decodeSequence(sequence):
    # sequence = getDirSequence(
    #           getDirSequence(
    #               getNumSequence(code)
    #           )
    #        )

    sequence_indexes = []
    code = ""

    # initial positions are set at 'A' for all robots
    num_pos = findPositionInGrid(num_grid, 'A')
    dir_pos1 = findPositionInGrid(dir_grid, 'A')
    dir_pos2 = findPositionInGrid(dir_grid, 'A')

    for i, dir_move2 in enumerate(sequence):
        if dir_move2 != 'A':
            delta = getDelta(dir_move2)
            dir_pos2 = (dir_pos2[0] + delta[0], dir_pos2[1] + delta[1])

        # dir robot 2 pressed 'A': dir robot 1 moves
        else:
            dir_move1 = dir_grid[dir_pos2[0]][dir_pos2[1]]

            if dir_move1 != 'A':
                delta = getDelta(dir_move1)
                dir_pos1 = (dir_pos1[0] + delta[0], dir_pos1[1] + delta[1])

            # dir robot 1 pressed 'A': num robot moves
            else:
                num_move = dir_grid[dir_pos1[0]][dir_pos1[1]]

                if num_move != 'A':
                    delta = getDelta(num_move)
                    num_pos = (num_pos[0] + delta[0], num_pos[1] + delta[1])
                
                # num robot pressed 'A': new code digit
                else:
                    sequence_indexes.append(i)
                    code += num_grid[num_pos[0]][num_pos[1]]
    
    digit_sequences = [sequence[0:sequence_indexes[0]+1]] + [sequence[sequence_indexes[i-1]+1:sequence_indexes[i]+1] for i in range(1, len(sequence_indexes))]

    return code, digit_sequences


# Code

start = findPositionInGrid(num_grid, '4')
end = findPositionInGrid(num_grid, '6')

print(decodeSequence("<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"))
