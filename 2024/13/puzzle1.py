# Custom input
input_data = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

claws = [[]]

for line in input_data:
    if line.startswith("Button A") or line.startswith("Button B"):
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