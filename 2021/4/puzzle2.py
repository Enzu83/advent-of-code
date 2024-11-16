# Custom input
input_data = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Functions
def update_board(board, number):
    for i in range(5):
        for j in range(5):
            if board[i][j][0] == number:
                board[i][j][1] = True 

def check_win(row_or_column):
    for element in row_or_column:
        if element[1] == False:
            return False
    
    return True

def get_winning_row_or_column(board):
    # Rows
    for i in range(5):
        row = [board[i][j] for j in range(5)]

        if check_win(row):
            return [element[0] for element in row]

    # Columns
    for j in range(5):
        column = [board[i][j] for i in range(5)]
        if check_win(column):
            return [element[0] for element in column]
    
    return None

def board_unmarked_sum(board):
    unmarked_sum = 0

    for i in range(5):
        for j in range(5):
            element = board[i][j]
            if element[1] == False:
                unmarked_sum += element[0]
    
    return unmarked_sum

# Input formatting

number_sequence = input_data[0].split(',')

boards = []

index = 2
while index < len(input_data)-5:
    board = [[0 for _ in range(5)] for _ in range(5)]

    for i in range(5):
        row = input_data[index + i]
        row = row.split(' ')
        board[i] = [int(number) for number in row if number != '']

    boards.append([[[board[i][j], False] for j in range(5)] for i in range(5)])
    index += 6


# Code

last_board = []

cleared_board = []

for number in number_sequence:
    for i in range(len(boards)):
        if i not in cleared_board:
            update_board(boards[i], int(number))

            if get_winning_row_or_column(boards[i]) != None:
                cleared_board.append(i)
    
    if len(boards) - len(cleared_board) == 1:
        break


# Get last board

last_board = []

for i in range(len(boards)):
        if i not in cleared_board:
            last_board = boards[i]



# Solve last board

win_sequence = []
current_number = 0

for number in number_sequence:
    current_number = int(number)

    update_board(last_board, current_number)

    win_sequence = get_winning_row_or_column(last_board)

    if win_sequence != None:
        break

unmarked_sum = board_unmarked_sum(last_board)

print(win_sequence)
print(unmarked_sum, current_number)
print(unmarked_sum * current_number)
