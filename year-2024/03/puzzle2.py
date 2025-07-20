# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Functions

def checkDo(string: str, state: int, enabled: bool):
    # d
    if state == 0 and string[0] != 'd':
        return "", 0, enabled
    
    # do
    elif state == 1 and string[1] != 'o':
        return "", 0, enabled
    
    # don / do(
    elif state == 2 and string[2] != 'n' and string[2] != '(':
        return "", 0, enabled
    
    # don' / do()
    elif state == 3:
        if string == "do()":
            return "", 0, True
    
        elif string[3] != "'":
            return "", 0, enabled

    # don't
    elif state == 4 and string[4] != 't':
        return "", 0, enabled
    
    # don't(
    elif state == 5 and string[5] != "(":
        return "", 0, enabled
    
    # don't()
    elif state == 6:
        if string[6] == ')':
            return "", 0, False
        else:
            return "", 0, enabled

    return string, state+1, enabled


# check if the string is the beginning of a mult string
def checkMult(string: str, state: int):
    # 'mul' '(' XXX ',' YYY ')'

    # m
    if state == 0 and string[0] != 'm':
        return "", 0

    # mu
    if state == 1 and string[1] != 'u':
        return "", 0

    # mul
    if state == 2 and string[2] != 'l':
        return "", 0
    
    # mul(
    if state == 3 and string[3] != '(':
        return "", 0
    
    # mul(XXX
    if state == 4:
        if string[len(string)-4:].isnumeric():
            return "", 0
        
        if string[-1] == ',' and string[4:len(string)-1].isnumeric():
            state += 1

        elif string[4:].isnumeric() is False:
            return "", 0
    
    # mul(XXX,
    if state == 5 and string[-1] != ',':
        return "", 0
    
    # mul(XXX,YYY
    if state == 6:
        comma = string.find(',')

        if len(string) - (comma+1) > 3 and string[comma+1:].isnumeric():
            return "", 0

        if string[-1] == ')' and string[comma+1:len(string)-1].isnumeric():
            state += 1

        elif string[comma+1:].isnumeric() is False:
            return "", 0

    # mul(XXX,YYY) 
    if state == 7 and string[-1] != ')':
        return "", 0


    if state != 4 and state != 6:
        state += 1

    return string, state


def computeMult(mult):
    #print(mult)
    # mult = mul(XXX,YYY)

    x, y = mult[4:len(mult)-1].split(',') # mul(XXX,YYY) -> XXX, YYY

    return int(x) * int(y)


def getMemoryResult(lines):
    result = 0
    enabled = True

    for line in lines:
        current_string = ""
        state = 0
        
        for char in line:
            current_string += char

            # multiplication
            if current_string[0] == 'm':
                current_string, state = checkMult(current_string, state)

                if state == 8:
                    if enabled:
                        result += computeMult(current_string)
                    current_string = ""
                    state = 0
            
            # do / don't
            else:
                current_string, state, enabled = checkDo(current_string, state, enabled)

    return result
            

# Code

print(getMemoryResult(input_data))