import operator
from collections import Counter
from math import floor
from math import ceil
from typing import Sequence
import numpy as np

# day 11
class Monkey:

    items = []
    operation = None
    op = None
    operand = 0 # maybe invalid
    test = 1
    TestTrueMonkey = -1
    TestFalseMonkey = -1
    bRelief = True

    timesInspected = 0

    def __init__(self, StartingItems = [], Operation = "", Test = 1, TestTrueMonkey = -1, TestFalseMonkey = -1, bRelief = True) -> None:
        self.items = StartingItems
        self.operation = Operation
        self.test = Test
        self.TestTrueMonkey = TestTrueMonkey
        self.TestFalseMonkey = TestFalseMonkey
        self.timesInspected = 0
        self.bRelief = bRelief

        # parse operation lambda
        parts = Operation.split(' ')
        self.op = operator.add if parts[1] == '+' else operator.mul

        if parts[2] == "old":
            self.operation = lambda old: self.op(old, old)
        else:
            self.operand = int(parts[2])
            self.operation = lambda old: self.op(old, self.operand)
        
        pass


    def TakeTurn(self) -> list:
        Throws = [] # list of tuples (WorryLevel, TargetMonkey)

        for item in self.items:
            # inspect item
            item = self.operation(item)
            if self.bRelief:
                item = np.int64(np.floor(item / 3))
            self.timesInspected += 1
            
            throw = ()
            if item % self.test == 0:
                throw = (item, self.TestTrueMonkey)
            else:
                throw = (item, self.TestFalseMonkey)
            Throws.append(throw)
            
        self.items.clear()
        return Throws
