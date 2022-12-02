import HelperFunctions as hf
import HelperClasses as hc
import collections
import copy
import numpy as np

def day1(input):
    
    elves = []

    current = 0
    for line in input:
        if line == "":
            elves.append(current)
            current = 0
        else:
            current += int(line)

    a = np.array(elves)
    largestInd = np.argpartition(a, -3)
    largest = a[largestInd[-3:]]

    return max(elves), sum(largest)

def day2(input):

    TotalScore = 0
    TotalScoreB = 0

    for line in input:
        left = line.split(' ')[0]
        right = line.split(' ')[1]

        if left == 'A':
            other = 0
        elif left == 'B':
            other = 1
        else:
            other = 2
        if right == 'X':
            self = 0
        elif right == 'Y':
            self = 1
        else:
            self = 2
        
        TotalScore += hf.PlayRockPaperScissors(self, other)

        if right == 'X':
            self = (other + 2) % 3
        elif right =='Y':
            self = other
        else:
            self = (other + 1) % 3
        
        TotalScoreB += hf.PlayRockPaperScissors(self, other)

    return TotalScore, TotalScoreB

def day3(input):

    return -1, -1

def day4(input):

    return -1, -1

def day5(input):

    return -1, -1

def day6(input):

    return -1, -1

def day7(input):

    return -1, -1


def day8(input):

    return -1, -1

def day9(input):

    return -1, -1

def day10(input):

    return -1, -1

def day11(input):

    return -1, -1

def day12(input):

    return -1, -1

def day13(input):

    return -1, -1

def day14(input):

    return -1, -1

def day15(input):

    return -1, -1

def day16(input):

    return -1, -1

def day17(input):

    return -1, -1

def day18(input):

    return -1, -1

def day19(input):

    return -1, -1

def day20(input):

    return -1, -1

def day21(input):

    return -1, -1

def day22(input):

    return -1, -1

def day23(input):

    return -1, -1

def day24(input):

    return -1, -1

def day25(input):

    return -1, "Merry Christmas!"