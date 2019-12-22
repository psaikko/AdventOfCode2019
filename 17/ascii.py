import itertools
from collections import defaultdict, deque
from matplotlib import pyplot as plt
from matplotlib import animation
from random import randint

import sys # https://stackoverflow.com/a/45874916/12214508
sys.path.append("..")
from IntCode import Program

with open("input",'r') as f:
    code = list(map(int, f.readline().strip().split(',')))

CODE_WALL = 0
CODE_MOVE = 1
CODE_GOAL = 2

MOVE_NORTH = 1
MOVE_SOUTH = 2
MOVE_WEST = 3
MOVE_EAST = 4

MAP_UNKNOWN = 0
MAP_FOG = 1
MAP_FREE = 2
MAP_WALL = 3
MAP_GOAL = 4
MAP_DROID = 5

p = Program(code)
p.run([])

s = "".join(list(map(chr, p.outputs)))
print(s)

M = [[c for c in l] for l in s.split()]

w = len(M[0])
h = len(M)

def is_intersection(x,y):
    return M[y][x] == '#' and M[y-1][x] == '#' and M[y+1][x] == '#' and M[y][x-1] == '#' and M[y][x+1] == '#'

def alignment_parameter(x,y):
    return x*y

s = 0
c = 0

for y in range(1,h-1):
    for x in range(1,w-1):
        if is_intersection(x,y):
            print(x,y)
            M[y][x] = 'O'
            s += alignment_parameter(x,y)
            c += 1

print("\n".join(["".join(l) for l in M]))

print(s)
print(c)

