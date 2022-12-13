import HelperFunctions as hf
import HelperClasses as hc
import collections
import copy
import numpy as np
import time
import ast

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
    currentDir = ""
    subdirs = {}
    files = {}

    for line in input:
        if line[0] == '$':
            cmd = line.split(' ')
            
            if cmd[1] == "cd":
                if cmd[2] == '/':
                    currentDir = "/"
                elif cmd[2] == "..":
                    parentEnd = currentDir.rfind('/', 0, -1)
                    currentDir = currentDir[:parentEnd + 1]
                else:
                    currentDir += cmd[2] + "/"
            elif cmd[1] == "ls":
                subdirs[currentDir] = []
                files[currentDir] = []
        else:
            # ls list
            item = line.split(' ')
            if item[0] == "dir":
                subdirs[currentDir].append(currentDir+item[1]+"/")
            else:
                files[currentDir].append((item[0], item[1]))

    sizes = {}
    hf.RecCalculateDirSizes("/", sizes, subdirs, files)
    
    totalSizeSmallDirs = 0
    for dir, size in sizes.items():
        if size <= 100000:
            totalSizeSmallDirs += size

    # part 2
    neededSpace = 30000000
    neededSpace -= 70000000 - sizes["/"]
    
    smallestDirSize = sizes["/"]
    for size in sizes.values():
        if size >= neededSpace and size < smallestDirSize:
            smallestDirSize = size


    return totalSizeSmallDirs, smallestDirSize

def day8(input):
    h = len(input)
    w = len(input[0])

    top = []
    right = []
    bottom = []
    left = []
    
    # calc visibilities
    for column in range(w):
        # from top
        top.append([])
        blockedHeight = -1
        for row in range(h):
            height = int(str(input[row])[column])
            if height > blockedHeight:
                top[column].append(True)
                blockedHeight = height
            else:
                top[column].append(False)
        # from bottom
        bottom.append([])
        blockedHeight = -1
        for row in reversed(range(h)):
            height = int(str(input[row])[column])
            if height > blockedHeight:
                bottom[column].append(True)
                blockedHeight = height
            else:
                bottom[column].append(False)
    for row in range(h):
        # from left
        left.append([])
        blockedHeight = -1
        for column in range(w):
            height = int(str(input[row])[column])
            if height > blockedHeight:
                left[row].append(True)
                blockedHeight = height
            else:
                left[row].append(False)
        # from right
        right.append([])
        blockedHeight = -1
        for column in reversed(range(w)):
            height = int(str(input[row])[column])
            if height > blockedHeight:
                right[row].append(True)
                blockedHeight = height
            else:
                right[row].append(False)

    numVisibleTrees = 0
    for y in range(h):
        revY  = h - y - 1
        for x in range(w):
            revX = w - x - 1
            if top[x][y] or bottom[x][revY] or left[y][x] or right[y][revX]:
                # print("Tree at", x, y, "is visible")
                numVisibleTrees += 1

    highestScenicScore = 0

    for y in range(h):
        for x in range(w):
            height = input[y][x]
            sLeft = 0
            sRight = 0
            sTop = 0
            sBottom = 0
            
            i = x - 1
            while i >= 0:
                sLeft += 1
                if input[y][i] >= height:
                    break
                i -= 1
            i = x + 1
            while i < w:
                sRight += 1
                if input[y][i] >= height:
                    break
                i += 1
            i = y - 1
            while i >= 0:
                sTop += 1
                if input[i][x] >= height:
                    break
                i -= 1
            i = y + 1
            while i < h:
                sBottom += 1
                if input[i][x] >= height:
                    break
                i += 1
            
            score = sLeft * sRight * sTop * sBottom
            if score > highestScenicScore:
                highestScenicScore = score

    return numVisibleTrees, highestScenicScore

def day9(input):

    currentHead = (0, 0)
    currentTail = (0, 0)
    tails = []
    for i in range(9):
        tails.append((0, 0))
    visited = set()
    visited2 = set()
    for line in input:
        dir = line[0]
        num = int(line[2:])

        for i in range(num):
            result = hf.MoveRope(currentHead, currentTail, dir)
            currentHead = result[0]
            currentTail = result[1]
            visited.add(currentTail)

            # part 2 longer rope
            tails[0] = result[1]
            for i in range(8):
                result = hf.MoveRope(tails[i], tails[i+1], '')
                tails[i+1] = result[1]
            visited2.add(tails[8])

    return len(visited), len(visited2)

def day10(input):
    cycle = 0
    regX = 1
    signalStrengths = []
    pixels = []
    for line in input:
        cycle += 1

        if cycle == 20 or cycle / 20 % 2 == 1:
            signalStrengths.append(regX * cycle)
            # print(cycle, regX)
        pixels.append('#' if abs(regX - (cycle - 1)  % 40) <= 1 else '.')
        # print(cycle, regX, pixels[-1])
        
        cmd = line.split(' ')
        if cmd[0] == "noop":
            pass
        elif cmd[0] == "addx":
            cycle += 1
            value = int(cmd[1])
            if cycle == 20 or cycle / 20 % 2 == 1:
                signalStrengths.append(regX * cycle)
                # print(cycle, regX)
            pixels.append('#' if abs(regX - (cycle - 1) % 40) <= 1 else '.')
            # print(cycle, regX, pixels[-1])
            regX += value
        
    for y in range(6):
        drawnLine = ""
        for x in range(40):
            drawnLine += pixels[y * 40 + x]
        print(drawnLine)

    total = sum(signalStrengths)
    return total, -1

def day11(input):

    Monkeys = []
    Monkeys2 = []
    for i in range(0, len(input), 7):
        items = [np.int64(x) for x in input[i+1].split(": ")[1].split(", ")]
        operation = input[i+2].split("= ")[1]
        test = input[i+3].split(' ')[-1]
        test = int(test)
        testTrue = input[i+4].split(' ')[-1]
        testTrue = int(testTrue)
        testFalse = input[i+5].split(' ')[-1]
        testFalse = int(testFalse)

        Monkeys.append(hc.Monkey(items.copy(), operation, test, testTrue, testFalse))
        Monkeys2.append(hc.Monkey(items.copy(), operation, test, testTrue, testFalse, False))
    
    for i in range(20):
        for m in Monkeys:
            throws = m.TakeTurn()
            for t in throws:
                Monkeys[t[1]].items.append(t[0])
        
        # print("After turn", i)
        # for j in range(len(Monkeys)):
        #     print("Monkey", j, ":", Monkeys[j].items)

    inspected = []
    for m in Monkeys:
        inspected.append(m.timesInspected)
    inspected.sort()
    inspected.reverse()
    MonkeyBusiness = inspected[0] * inspected[1]

    testProduct = np.prod([m.test for m in Monkeys2])
    for i in range(10000):
        for m in Monkeys2:
            throws = m.TakeTurn()
            for t in throws:
                Monkeys2[t[1]].items.append(t[0] % testProduct)
        
        # if i % 1000 == 0:
        #     print("After turn", i)
        #     for j in range(len(Monkeys2)):
        #         print("Monkey", j, " inspected", Monkeys2[j].timesInspected)
    
    inspected.clear()
    for m in Monkeys2:
        inspected.append(m.timesInspected)
    inspected.sort()
    inspected.reverse()
    MonkeyBusiness2 = inspected[0] * inspected[1]
    
    return MonkeyBusiness, MonkeyBusiness2

def day12(input):

    current = ()
    target = ()
    numX = len(input[0])
    numY = len(input)
    map = {}
    for x in range(numX):
        for y in range(numY):
            height = input[y][x]
            if height == 'S':
                height = 'a'
                current = (x, y)
            elif height == 'E':
                height = 'z'
                target = (x, y)
            map[(x, y)] = ord(height)

    # helper lambdas
    validX = lambda x : x >= 0 and x < numX
    validY = lambda y : y >= 0 and y < numY

    # depth first search
    visited = set()
    steps = {}
    steps[current] = 0
    candidates = []
    
    while current != target:
        visited.add(current)
        currentSteps = steps[current]
        # print(current, currentSteps)
        for offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = (current[0] + offset[0], current[1] + offset[1])
            if validX(neighbor[0]) and validY(neighbor[1]):
                # print("neighbor:", neighbor, "dist:", map[neighbor] - map[current])
                if map[neighbor] - map[current] <= 1:
                    if neighbor in visited:
                        continue
                    if neighbor not in steps:
                        steps[neighbor] = currentSteps + 1
                        candidates.append(neighbor)
                    elif steps[neighbor] <= currentSteps + 1:
                        # 
                        pass
                    else:
                        print("This should never be reached!")
        # print("candidates: ", candidates)
        current = candidates.pop(0)
    shortestPath = steps[target]

    # part 2 depth first search
    current = target
    visited.clear()
    steps.clear()
    steps[current] = 0
    candidates = []
    candidates.append(target)
    shortestHikingPath = numX * numY
    
    while len(candidates) > 0:        
        current = candidates.pop(0)
        visited.add(current)
        currentSteps = steps[current]
        # print(current)
        if map[current] == ord('a'):
            if currentSteps < shortestHikingPath:
                shortestHikingPath = currentSteps
        # print(current, currentSteps)
        for offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = (current[0] + offset[0], current[1] + offset[1])
            if validX(neighbor[0]) and validY(neighbor[1]):
                # print("neighbor:", neighbor, "dist:", map[neighbor] - map[current])
                if map[neighbor] - map[current] >= -1:
                    # print(neighbor)
                    if neighbor in visited:
                        continue
                    if neighbor not in steps:
                        steps[neighbor] = currentSteps + 1
                        candidates.append(neighbor)                        
                    elif steps[neighbor] <= currentSteps + 1:
                        # 
                        pass
                    else:
                        print("This should never be reached!")
        # print("candidates: ", candidates)

    return shortestPath, shortestHikingPath

def day13(input):

    pairInd = 0
    sum = 0
    packets = []
    for i in range(0, len(input), 3):
        pairInd += 1
        packet1 = ast.literal_eval(input[i])
        packet2 = ast.literal_eval(input[i+1])
        packets.append(packet1.copy())
        packets.append(packet2.copy())

        if hf.ComparePackets(packet1, packet2) == 1:
            sum += pairInd

    # part 2, sort packages
    sortedPackages = []
    for p in packets:
        bInserted = False
        for i in range(len(sortedPackages)):
            if hf.ComparePackets(p, sortedPackages[i]) == 1:
                sortedPackages.insert(i, p)
                bInserted = True
                break
        if not bInserted:
            sortedPackages.append(p)
    
    bFirstPacketInserted = False
    DecoderKey = 1
    for i in range(len(sortedPackages)):
        if not bFirstPacketInserted:
            if hf.ComparePackets([[2]], sortedPackages[i]) == 1:
                sortedPackages.insert(i, p)
                bFirstPacketInserted = True
                DecoderKey = i + 1
        else:
            if hf.ComparePackets([[6]], sortedPackages[i]) == 1:
                sortedPackages.insert(i, p)
                DecoderKey *= (i + 1)
                break

    return sum, DecoderKey

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