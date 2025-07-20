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
while index < len(input_data) - 5:
    board = [[0 for _ in range(5)] for _ in range(5)]

    for i in range(5):
        row = input_data[index + i]
        row = row.split(' ')
        board[i] = [int(number) for number in row if number != '']

    boards.append([[[board[i][j], False] for j in range(5)] for i in range(5)])
    index += 6

# Code

current_number = 0
board = []
win_sequence = None

i = 0

while win_sequence == None:
    current_number = int(number_sequence[i])

    board_index = 0

    while board_index < len(boards):
        board = boards[board_index]
        update_board(board, current_number)

        win_sequence = get_winning_row_or_column(board)

        if win_sequence != None:
            break
        else:
            board_index +=  1
    
    
    i += 1

print(win_sequence)
print(current_number)

unmarked_sum = board_unmarked_sum(board)

print(unmarked_sum * current_number)
