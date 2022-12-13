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