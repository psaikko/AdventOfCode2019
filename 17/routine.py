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

routine = ['B','C','B','A','B','C','A','C','A','C']
A = ['R',4,'L',4,'L',10,'L',10]
B = ['R',10,'R',10,'R',6,'R',4]
C = ['R',10,'R',10,'L',4]

# R,10,R,10,R,6,R,4,R,10,R,10,L,4,R,10,R,10,R,6,R,4,R,4,L,4,L,10,L,10,R,10,R,10,R,6,R,4,R,10,R,10,L,4,R,4,L,4,L,10,L,10,R,10,R,10,L,4,R,4,L,4,L,10,L,10,R,10,R,10,L,4

def make_command(l):
    s = ','.join(list(map(str, l))) + "\n"
    cs = [ord(c) for c in s]
    return cs

code[0] = 2
p = Program(code)
p.run(make_command(routine))
s = "".join(list(map(chr, p.outputs)))
print(s)
p.outputs.clear()

p.run(make_command(A))
s = "".join(list(map(chr, p.outputs)))
print(s)
p.outputs.clear()

p.run(make_command(B))
s = "".join(list(map(chr, p.outputs)))
print(s)
p.outputs.clear()

p.run(make_command(C))
s = "".join(list(map(chr, p.outputs)))
print(s)
p.outputs.clear()

p.run(make_command(['n']))
#s = "".join(list(map(chr, p.outputs)))
print(p.outputs)


