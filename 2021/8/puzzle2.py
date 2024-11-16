# Custom input
input_data = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

input_data = input_data.split('\n')

# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Functions

def digit_to_number(correct_digit):
    if len(correct_digit) == 2:
        return '1'
    elif len(correct_digit) == 3:
        return '7'
    elif len(correct_digit) == 4:
        return '4'
    elif len(correct_digit) == 5: # 2, 3, 5
        if 'b' in correct_digit:
            return '5'
        elif 'e' in correct_digit:
            return '2'
        else:
            return '3'
    elif len(correct_digit) == 6: # 0, 6, 9
        if 'd' not in correct_digit:
            return '0'
        if 'e' in correct_digit:
            return '6'
        else:
            return '9'
    elif len(correct_digit) == 7:
        return '8'
    else:
        return ''

def digits_to_number(correct_digits):
    number = ""

    for digit in correct_digits:
        number += digit_to_number(digit)
    
    return int(number)


def put_trivial_digit(digits, digit_mapping):
    for digit in digits:
        if len(digit) == 2 and 1 not in digit_mapping: # 1
            digit_mapping[1] = digit
        elif len(digit) == 3 and 7 not in digit_mapping: # 7
            digit_mapping[7] = digit
        elif len(digit) == 4 and 4 not in digit_mapping: # 4
            digit_mapping[4] = digit
        elif len(digit) == 7 and 8 not in digit_mapping: # 8
            digit_mapping[8] = digit

def full_digit_sets(digits, five_letters_digit, six_letters_digit):
    for digit in digits:
        if len(digit) == 6 and digit not in six_letters_digit: # 0, 6, 9
            six_letters_digit.add(digit)

        elif len(digit) == 5 and digit not in five_letters_digit: # 2, 3, 5
            five_letters_digit.add(digit)

def get_desired_occurrence(letters_set, desired_amount):
    letters_occurrence = {}

    for string in letters_set:
        for char in string:
            if char not in letters_occurrence:
                letters_occurrence[char] = 1
            else:
                letters_occurrence[char] += 1
    
    desired_letters = set()

    for letter in letters_occurrence:
        if letters_occurrence[letter] == desired_amount:
            desired_letters.add(letter)
    
    return desired_letters

def find_mapping(digits):
    # Returns mapping of current letters to new one : 'altered_letter': 'correct_letter'
    mapping = {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': ''}

    # Find 1, 4, 7, 8, {0, 6, 9}, {2, 3, 5}

    digit_segments = {} # number: 7-seg letters

    put_trivial_digit(digits, digit_segments) # 1, 4, 7, 8

    five_letters_digit = set() # {2, 3, 5}
    six_letters_digit = set() # {0, 6, 9}

    full_digit_sets(digits, five_letters_digit, six_letters_digit)

    # 1. Find 'x' => 'a'
    for letter in digit_segments[7]:
        if letter not in digit_segments[1]:
            mapping[letter] = 'a'
            break

    # 2. Get altered 'cde'
    cde = get_desired_occurrence(six_letters_digit, 2)

    # 3. Find 'c'
    for letter in cde:
        if letter in digit_segments[1]:
            mapping[letter] = 'c'
            break

    # 4. Find 'e'
    for letter in cde:
        if letter not in digit_segments[4]:
            mapping[letter] = 'e'
            break

    # 5. Find 'f'
    for letter in digit_segments[1]:
        if mapping[letter] != 'c':
            mapping[letter] = 'c'
            break

    # 6. Find 'd'
    for letter in cde:
        if mapping[letter] != 'c' and mapping[letter] != 'e':
            mapping[letter] = 'd'
            break

    # 7. Get altered 'bd'
    bd = get_desired_occurrence({digit_segments[1], digit_segments[4]}, 1)

    # 8. Find 'b'
    for letter in bd:
        if mapping[letter] != 'd':
            mapping[letter] = 'b'
            break
    
    # 9. Get altered 'adg'
    adg = get_desired_occurrence(five_letters_digit, 3)

    # 10. Find 'g'
    for letter in adg:
        if mapping[letter] != 'a' and mapping[letter] != 'd':
            mapping[letter] = 'g'
            break

    return mapping


def digit_correction(altered_digit, mapping):
    digit = ""

    for char in altered_digit:
        digit += mapping[char]
    
    return digit

def digits_correction(altered_digits, mapping):
    correct_digits = []

    for altered_digit in altered_digits:
        correct_digits.append(digit_correction(altered_digit, mapping))
    
    return correct_digits

# Formatting

test_digits = [data.split(' | ')[0].split(' ') for data in input_data]
output_digits = [data.split(' | ')[1].split(' ') for data in input_data]


# Find 1, 4, 7 and 8

numbers_sum = 0

for i in range(len(test_digits)):
    print(output_digits[i])

    mapping = find_mapping(test_digits[i])
    print(mapping)

    correct_output = digits_correction(output_digits[i], mapping)
    print(correct_output)

    number = int(digits_to_number(correct_output))
    print(number)

    print('')

    numbers_sum += number

print("Total sum: " + str(numbers_sum))

    


