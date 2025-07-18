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

def nextFile(layout, current_index):
    current_index -= 1

    while layout[current_index] is None:
        current_index -= 1

    return current_index


def reArrangeLayout(layout):
    free_space_idx = nextFreeSpace(layout, len(layout)) # next in non decreasing order
    file_idx = nextFile(layout, len(layout)) # next in decreasing order

    while free_space_idx < file_idx: # while there is still free space to compress the string
        layout[free_space_idx] = layout[file_idx]
        layout[file_idx] = None

        # next free space and file index for the compression
        free_space_idx = nextFreeSpace(layout, len(layout), free_space_idx)
        file_idx = nextFile(layout, file_idx)

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

#printLayout(layout)

print(computeChecksum(layout))