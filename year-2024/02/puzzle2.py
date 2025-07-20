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
    bad_level = False

    for i in range(1, len(report)):
        if increasing is None:
            increasing = report[i-1] < report[i]

        if safeCondition(report[i-1], report[i], increasing) is False:
            # removing the last doesn't change the safety of the report
            if i == len(report)-1:
                return bad_level is False

            # if there is not already a bad level
            elif bad_level is False:
                bad_level = True

                # we can remove either (i-1)th or (i)th
                # if the unsafety remains unsafe for both removing : unsafe
                if safeCondition(report[i-1], report[i+1], increasing) is False and safeCondition(report[i], report[i+1], increasing) is False:
                    return False
                
                # else if the bad level is the current one : take the previous one
                elif safeCondition(report[i], report[i+1], increasing) is False:
                    report[i] = report[i-1]

            # already a bad level : unsafe
            else:
                return False
    
    return True


def getSafeReports(reports):
    return sum([1 for report in reports if safeReport(report)])


# Code

print(getSafeReports(reports))