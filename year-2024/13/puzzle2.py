# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

claws = [[]]

for line in input_data:
    if line.startswith("Button"):
        line = line[12:].split(", ")
        claws[-1].append((int(line[0]), int(line[1][2:])))

    elif line.startswith("Prize"):
        line = line[9:].split(", ")
        claws[-1].append((int(line[0]), int(line[1][2:])))

    else:
        claws.append([])


# Functions

def getPrizeTokens(claw):
    """
    Claw movement matrix C :
    X[A] X[B]
    Y[A] Y[B]

    Prize Vector P :
    X[P]
    Y[P]

    If C is inversible, one solution S : S = C^(-1)*P
    """

    button_a, button_b, prize = claw
    prize = (prize[0] + 10000000000000, prize[1] + 10000000000000) # conversion error of measurements

    ## solution computation
    det = button_a[0] * button_b[1] - button_a[1] * button_b[0]

    # matrix is not inversible
    if det == 0:
        return 0
    
    token_a = (button_b[1] * prize[0] - button_b[0] * prize[1]) / det
    token_b = (button_a[0] * prize[1] - button_a[1] * prize[0]) / det

    ## check if solutions are integers
    if token_a == int(token_a) and token_b == int(token_b):
        return 3 * int(token_a) + int(token_b)
    else:
        return 0

def getAllPrizeTokens(claws):
    return sum(getPrizeTokens(claw) for claw in claws)

# Code

print(getAllPrizeTokens(claws))