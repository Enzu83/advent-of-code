# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting
reports = [[int(num) for num in report.split()] for report in input_data]


# Functions
def safeCondition(previous, next, increasing):
    if previous == next:
        return False
    
    if abs(previous - next) > 3:
        return False

    if increasing is True and previous > next:
        return False
    
    if increasing is False and previous < next:
        return False
    
    return True


def safeReport(report):
    increasing = None

    for i in range(1, len(report)):
        if increasing is None:
            increasing = report[i-1] < report[i]

        if safeCondition(report[i-1], report[i], increasing) is False:
            return False
    
    return True


def getSafeReports(reports):
    return sum([1 for report in reports if safeReport(report)])


# Code

print(getSafeReports(reports))