import itertools
from collections import defaultdict, deque
from random import randint

import sys # https://stackoverflow.com/a/45874916/12214508
sys.path.append("..")
from IntCode import Program

with open("input",'r') as f:
    code = list(map(int, f.readline().strip().split(',')))


n = 1700
skip = 12 # beam has consistent behavior after row 12
edges = [(None,None) for _ in range(skip)]
box_width = 100

def in_beam(x,y):
    p = Program(code)
    p.run([x,y])
    return p.outputs[0]

## testing
# skip = 1
# edges = [(None,None)]
# box_width = 10
# grid = [[c for c in line.strip()] for line in open("test", 'r').readlines()]
# n = len(grid[0])
# print(grid)

# def in_beam(x,y):
#     if grid[y][x] == '.':
#         return 0
#     return 1

for y in range(skip,n): 
    left, right = None, None

    start = 0
    if edges[-1][0]: start = edges[-1][0] - 1

    # find rising edge
    prev = 0
    for x in range(start, n):
        val = in_beam(x,y)
        if prev == 0 and val == 1:
            left = x
            break
        prev = val
    
    if edges[-1][1]: start = edges[-1][1] - 1

    # find falling edge
    prev = 0
    right = n
    for x in range(start, n):
        val = in_beam(x,y)
        if prev == 1 and val == 0:
            right = x - 1
            break
        prev = val

    edges.append((left,right))

    # if beam is 100-wide check for square fit
    print(y, left, right)
    if right - left + 1 >= box_width:
        top_left, top_right = edges[-box_width]
        if top_right - top_left + 1 >= box_width:
            #print(i, right - left + 1, top_right - top_left - 1)
            if top_right >= left + box_width - 1:
                print("fits")
                x = left
                y = (y - (box_width - 1))
                print(x * 10000 + y)
                break
    
    

#print("\n".join(["".join(list(map(str, l))) for l in grid]))
