import sys
import os
import csv
import math
import numpy as np
import pickle
import numpy.linalg as linalg

class Logging:
    __slots__ = ['file', 'ws']
    def __init__(self, file):
        self.file = file
        self.ws = 0
    def __call__(self, *args, **kwargs):
        if self.ws > 0:
            print(' ' * (self.ws - 1), *args, file=self.file, **kwargs)
        else:
            print(*args, file=self.file, **kwargs)
    def enter(self):
        self.ws += 2
    def exit(self):
        self.ws -= 2

eprint = Logging(sys.stderr)

def read_csv(fn):
    with open(fn, "r") as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)

class Linear:
    __slots__ = ['__cx', '__cy', '__add']
    def __init__(self, __cx, __cy, __add):
        self.__cx, self.__cy, self.__add = __cx, __cy, __add
    def __call__(self, x, y):
        return self.__cx * x + self.__cy * y + self.__add
    def __str__(self):
        return "Linear(%.2f, %.2f, %.2f)" % (self.__cx, self.__cy, self.__add)
    def std(self, data):
        return np.sqrt(sum((self(p[0], p[1]) - p[2]) ** 2 for p in data) / len(data))

def ask(ques):
    while True:
        eprint(ques + ' (y/n) ', end='')
        ans = input().strip().lower()
        if ans in ['y', 'yes']:
            return True
        elif ans in ['n', 'no']:
            return False
