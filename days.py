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

    TotalPrio = 0
    for line in input:
        num = int(len(line) / 2)
        items1 = set(line[:num])
        items2 = set(line[num:])
        
        matchedType = items1.intersection(items2).pop()
        if matchedType.isupper():
            TotalPrio += ord(matchedType) - 38
        else:
            TotalPrio += ord(matchedType) - 96

    TotalPrio2 = 0
    for i in range(len(input))[::3]:
        items1 = set(input[i])
        items2 = set(input[i+1])
        items3 = set(input[i+2])
        badge = items1.intersection(items2).intersection(items3).pop()
        
        if badge.isupper():
            TotalPrio2 += ord(badge) - 38
        else:
            TotalPrio2 += ord(badge) - 96

    return TotalPrio, TotalPrio2

def day4(input):

    FullOverlaps = 0
    PartialOverlaps = 0
    for pair in input:
        elf1 = pair.split(',')[0]
        elf2 = pair.split(',')[1]
        bounds1 = (int(elf1.split('-')[0]), int(elf1.split('-')[1]))
        bounds2 = (int(elf2.split('-')[0]), int(elf2.split('-')[1]))

        set1 = set(range(bounds1[0], bounds1[1]+1))
        set2 = set(range(bounds2[0], bounds2[1]+1))
        join = set1.union(set2)
        intersection = set1.intersection(set2)
        
        if len(join) == len(set1) or len(join) == len(set2):
            FullOverlaps += 1

        if len(intersection) > 0:
            PartialOverlaps += 1

    return FullOverlaps, PartialOverlaps

def day5(input):

    stacks = {}
    stacks2 = {}
    lineNr = 0
    while not input[lineNr].startswith(" 1"):
        # build initial stacks
        line = input[lineNr]
        stackIdx = 1
        for i in range(1, len(line), 4):
            if line[i] != ' ':
                if stackIdx not in stacks:
                    stacks[stackIdx] = []
                    stacks2[stackIdx] = []
                stacks[stackIdx].insert(0, line[i])
                stacks2[stackIdx].insert(0, line[i])
            stackIdx += 1

        lineNr += 1
    lineNr += 2
    
    while lineNr < len(input):
        move = input[lineNr].split(' ')
        num = int(move[1])
        fromS = int(move[3])
        toS = int(move[5])

        # puzzle 1 moving
        for i in range(num):
            stacks[toS].append(stacks[fromS].pop())

        # puzzle 2 moving
        lowestMovedIdx = len(stacks2[fromS]) - num        
        for i in range(num):
            stacks2[toS].append(stacks2[fromS].pop(lowestMovedIdx))
        lineNr += 1
        
    topCrates = ""
    topCrates2 = ""
    idx = 1
    while idx in stacks:
        topCrates += stacks[idx][-1]
        topCrates2 += stacks2[idx][-1]
        idx += 1

    return topCrates, topCrates2

def day6(input):
    signal = input[0]
    for i in range(3, len(signal)):
        marker = set(signal[i-3:i+1])
        if len(marker) == 4:
            startMarkerPos = i + 1 
            break

    startMessage = -1
    for j in range(13, len(signal)):
        marker = set(signal[j-13:j+1])
        if len(marker) == 14:
            startMessage = j + 1
            break

    return startMarkerPos, startMessage

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