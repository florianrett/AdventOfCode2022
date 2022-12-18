import collections
import copy

# Rock = 0, Paper = 1, Scissors = 2
def PlayRockPaperScissors(PlayerA, PlayerB):
    Score = PlayerA + 1
    if PlayerA == PlayerB:
        # draw
        return Score + 3

    if PlayerA == (PlayerB + 1) % 3:
        # win
        return Score + 6
    else:
        # lose
        return Score

# recursive calc dir sizes
def RecCalculateDirSizes(dir, sizes = {}, subdirs = {}, files = {}):
    dirSize = 0
    for subdir in subdirs[dir]:
        RecCalculateDirSizes(subdir, sizes, subdirs, files)
        dirSize += sizes[subdir]
    
    for file in files[dir]:
        dirSize += int(file[0])

    sizes[dir] = dirSize

# move rope head and tail one step
def MoveRope(head, tail, dir):
    # update head
    newHead = head
    if dir == 'R':
        newHead = (head[0] + 1, head[1])
    elif dir == 'L':
        newHead = (head[0] - 1, head[1])
    elif dir == 'U':
        newHead = (head[0], head[1] + 1)
    elif dir == 'D':
        newHead = (head[0], head[1] - 1)
    
    # update tail
    dX = newHead[0] - tail[0]
    dY = newHead[1] - tail[1]
    moveX = 0
    moveY = 0
    if dX == 0 and abs(dY) > 1:
        moveY = 1 if dY > 0 else -1
    elif dY == 0 and abs(dX) > 1:
        moveX = 1 if dX > 0 else -1
    elif abs(dX) + abs(dY) > 2:
        moveX = 1 if dX > 0 else -1
        moveY = 1 if dY > 0 else -1
    newTail = (tail[0] + moveX, tail[1] + moveY)

    return newHead, newTail

# day 13 compare packets recursively
def ComparePackets(packet1, packet2) -> int:
    # print("comparing", packet1, "vs", packet2)
    bLeftIsInt = isinstance(packet1, int)
    bRightIsInt = isinstance(packet2, int)

    if bLeftIsInt and bRightIsInt:
        if packet1 < packet2:
            return 1
        elif packet1 == packet2:
            return 0
        else:
            return -1
    
    if not bLeftIsInt and not bRightIsInt:
        # both are lists
        for i in range(len(packet1)):
            if i >= len(packet2):
                # right ran out of items
                return -1
            comp = ComparePackets(packet1[i], packet2[i])
            if comp == 0:
                continue
            else:
                return comp
        if len(packet1) == len(packet2):
            return 0
        return 1
        
    
    # mismatched types
    if bLeftIsInt:
        return ComparePackets([packet1], packet2)
    if bRightIsInt:
        return ComparePackets(packet1, [packet2])

    print("This should never be reached")
    return -1

# day 15 is in sensor range
def IsInSensorRange(point, sensorPos, dist) -> bool:
    return abs(point[0] - sensorPos[0]) + abs(point[1] - sensorPos[1]) <= dist

def CheckLine(y, sensors, minX, maxX) -> int:    
    blocks = []
    for sensor in sensors:
        pos = sensor[0]
        dist = sensor[1]
        width = dist - abs(pos[1] - y)
        if width >= 0:
            # print("sensor", pos, "blocking from", pos[0] - width, "to", pos[0] + width)
            blocks.append((pos[0] - width, pos[0] + width))
    blocks.sort(key=lambda x: x[0])
    
    numOccupied = 0
    lastBlockUpper = minX - 1
    for b in blocks:
        start = max(b[0], lastBlockUpper + 1)
        end = min(b[1], maxX)
        if end < start:
            continue
        uniqueWidth = end - start + 1
        numOccupied += uniqueWidth
        lastBlockUpper = b[1]
        
    return numOccupied

# day 16
def RecCalcPressure(valves, flowRates, distances, current, minutesLeft) -> int:
    CurrentPressure = flowRates[current] * minutesLeft
    MaxTotalPressure = 0

    for v in valves:
        time = distances[(current, v)] + 1 # walk there and open it
        if time > minutesLeft:
            continue
        newValves = valves.copy()
        newValves.remove(v)

        MaxTotalPressure = max(MaxTotalPressure, RecCalcPressure(newValves, flowRates, distances, v, minutesLeft - time))

    return CurrentPressure + MaxTotalPressure

def RecCalcPressure2(valves, flowRates, distances, minutesLeft, current1, current2, remainingWay1, remainingWay2, depth) -> int:

    # if depth <= 2:
    #     print(minutesLeft, current1, current2, remainingWay1, remainingWay2)
    print(valves, minutesLeft, current1, current2, remainingWay1, remainingWay2)

    MaxTotalPressure = 0
    ChildPath = ""
    
    if remainingWay1 == 0:
        CurrentPressure = flowRates[current1] * minutesLeft
        Path = "1("  + str(27 - minutesLeft) + "):" + current1 + "; "

        sortedValves = valves.copy()
        # sortedValves.sort(key=lambda x : (minutesLeft - distances[(current1, x)] - 1) * flowRates[x])
        # sortedValves.reverse()
        for v in sortedValves:
            dist = distances[(current1, v)] + 1 # distance + one minute for opening
            time = min(remainingWay2, dist)
            if time >= minutesLeft: # neither agent can reach his next destination in time
                continue
            newValves = sortedValves.copy()
            newValves.remove(v)

            # print("A:", time, dist, remainingWay2 - time)
            result = RecCalcPressure2(newValves, flowRates, distances, minutesLeft - time, v, current2, dist - time, remainingWay2 - time, depth + 1)
            if result[0] > MaxTotalPressure:
                # print("Found more efficient path for agent 1 at minute", 27 - minutesLeft, ":", v)
                MaxTotalPressure = result[0]
                ChildPath = result[1]
            break
                    
    elif remainingWay2 == 0:
        CurrentPressure = flowRates[current2] * minutesLeft
        Path = "2("  + str(27 - minutesLeft) + "):" + current2 + "; "

        sortedValves = valves.copy()
        # sortedValves.sort(key=lambda x : (minutesLeft - distances[(current2, x)] - 1) * flowRates[x])
        # sortedValves.reverse()
        for v in sortedValves:
            dist = distances[(current2, v)] + 1
            time = min(remainingWay1, dist)
            if time >= minutesLeft:
                continue
            newValves = sortedValves.copy()
            newValves.remove(v)

            # print("B:", time, remainingWay1 - time, dist)
            result = RecCalcPressure2(newValves, flowRates, distances, minutesLeft - time, current1, v, remainingWay1 - time, dist - time, depth + 1)
            if result[0] > MaxTotalPressure:
                # print("Found more efficient path for agent 2 at minute", 27 - minutesLeft, ":", v)
                MaxTotalPressure = result[0]
                ChildPath = result[1]
            break
    else:
        print("No agent arrived at his destination!")

    print(Path+ChildPath, MaxTotalPressure, valves)
    return CurrentPressure + MaxTotalPressure, Path + ChildPath

def CalcPressureFixedPath(valves, flowRates, distances, minutesLeft, current) -> int:

    TotalPressure = flowRates[current] * minutesLeft
    TotalPressure = 0

    while len(valves) > 0:
        next = valves.pop(0)
        dist = distances[(current, next)] + 1
        if dist >= minutesLeft:
            break
        minutesLeft -= dist
        TotalPressure += flowRates[next] * minutesLeft
        current = next

    return TotalPressure

# day 17
def IsRockPositionValid(RockPos, rock, rocks) -> bool:
    for offset in rock:
        pos = (RockPos[0] + offset[0], RockPos[1] + offset[1])
        if pos[0] < 0 or pos[0] >= 7 or pos in rocks:
            return False
    return True

