# Custom input
input_data = """2333133121414131402"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

diskmap = [int(digit) for line in input_data for digit in line]

# Functions

def diskmapToLayout(diskmap):
    layout = {}
    layout_idx = 0

    for i, length in enumerate(diskmap):
        # File
        if i % 2 == 0:
            for _ in range(length):
                layout[layout_idx] = i // 2 # file ID
                layout_idx += 1
        
        # free space
        else:
            for _ in range(length):
                layout[layout_idx] = None # None = free space
                layout_idx += 1

    return layout

def nextFreeSpace(layout, max_index, current_index=None):
    if current_index is None:
        current_index = 0
    else:
        current_index += 1
    
    for i in range(current_index, max_index):
        if layout[i] is None:
            return i
    
    return float("inf")

def nextFreeSpaceBlock(layout, max_index, current_index=None):
    first_index = nextFreeSpace(layout, max_index, current_index)

    # get the end of the free space block
    second_index = first_index

    while second_index < max_index - 1 and layout[second_index + 1] is None:
        second_index += 1
    
    return [first_index, second_index]

def nextFile(layout, current_index):
    current_index -= 1

    while layout[current_index] is None:
        current_index -= 1

    return current_index

def nextFileBlock(layout, current_index):
    second_index = nextFile(layout, current_index)

    # get the beginning of the file block
    first_index = second_index

    while layout[first_index - 1] is not None and layout[first_index - 1] == layout[second_index]:
        first_index -= 1

    return [first_index, second_index]

def reArrangeLayout(layout):
    free_space = nextFreeSpaceBlock(layout, len(layout))
    file = nextFileBlock(layout, len(layout))

    while free_space[0] != float("inf"): # while there is still free space large enough for the file block

        if free_space[1] - free_space[0] >= file[1] - file[0]: # if there is enough space to put the files
            for i in range(file[1] - file[0] + 1):
                free_space_idx = free_space[0] + i
                file_idx = file[1] - i

                layout[free_space_idx] = layout[file_idx]
                layout[file_idx] = None

            # get the next file and free space blocks
            file = nextFileBlock(layout, file[0])
            free_space = nextFreeSpaceBlock(layout, file[0])

        else: # iterate throught eachen free space blocks before the file block
            free_space = nextFreeSpaceBlock(layout, file[0], free_space[1])

        # if there is not possible free spaces for the file : indexes are set to infinity
        # if it happens, we need to take the next file block to see if this one can be compressed
        if free_space[0] == float("inf"):
            file = nextFileBlock(layout, file[0])
            free_space = nextFreeSpaceBlock(layout, file[0])


    return layout

def computeChecksum(layout):
    checksum = 0

    for idx, id in layout.items():

        if id is not None:
            checksum += idx * id

    return checksum

def printLayout(layout):
    for i in range(len(layout)):
        if layout[i] is not None:
            print(layout[i], end="")
        else:
            print('.', end="")
    
    print("")

# Code

layout = reArrangeLayout(diskmapToLayout(diskmap))
printLayout(layout)

print(computeChecksum(layout))