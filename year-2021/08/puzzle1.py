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
input_data = [data.split(' | ')[1] for data in input_data]
input_data = [data.split(' ') for data in input_data]

# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Functions

def dict_sum_value(dic):
    res = 0

    for key in dic:
        res += dic[key]

    return res

# Code

digit_occurrences = {'1': 0, '4': 0, '7': 0, '8': 0}

for output_digits in input_data:
    for digit in output_digits:
        if len(digit) == 2:
            digit_occurrences['1'] += 1
        elif len(digit) == 3:
            digit_occurrences['7'] += 1
        elif len(digit) == 4:
            digit_occurrences['4'] += 1
        elif len(digit) == 7:
            digit_occurrences['8'] += 1

print(dict_sum_value(digit_occurrences))
        