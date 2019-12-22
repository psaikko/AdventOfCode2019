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
#p.run([])

droid_x = 0
droid_y = 0

def neighbors(x,y):
    return [(x,y-1),(x+1,y),(x,y+1),(x-1,y)]

visited = set()
unknown = set()
visited.add((droid_x,droid_y))
tile_kb = defaultdict(int)

def explored_bitmap():
    global visited, tile_kb
    xs = [p[0] for p in visited]
    ys = [p[1] for p in visited]

    min_x = min(xs)-1
    max_x = max(xs)+1

    min_y = min(ys)-1
    max_y = max(ys)+1

    bitmap = [[0] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]
    for (x,y) in visited:
        bitmap[y-min_y][x-min_x] = tile_kb[(x,y)]
    for (x,y) in unknown:
        bitmap[y-min_y][x-min_x] = MAP_FOG
    bitmap[droid_y-min_y][droid_x-min_x] = MAP_DROID

    return bitmap

def step_to_unknown(x,y):
    """Perform breadth-first search from given point to find the closest unknown tile.
    Backtrack from this tile and return the point to step to from (x,y)."""
    seen = set()
    q = deque()
    q.append((0,x,y))

    backtrack = dict()

    while len(q) > 0:
        d, tx, ty = q.popleft()
        seen.add((tx,ty))
        for (nx, ny) in neighbors(tx, ty):
            if (nx, ny) in seen:
                continue
            backtrack[(nx,ny)] = (tx,ty)
            if tile_kb[(nx,ny)] == MAP_UNKNOWN:
                while backtrack[(nx,ny)] != (x,y):
                    nx, ny = backtrack[(nx,ny)]
                return (nx,ny)
            elif tile_kb[(nx,ny)] == MAP_FREE:
                q.append((d+1,nx,ny))
    return None

def distance(from_x,from_y,to_x,to_y):
    """Compute the shortest distance (from_x,from_y) -> (to_x,to_y)"""
    seen = set()
    q = deque()
    q.append((0,from_x,from_y))

    while len(q) > 0:
        d, tx, ty = q.popleft()
        seen.add((tx,ty))
        for (nx, ny) in neighbors(tx, ty):
            if (nx, ny) in seen:
                continue
            if (nx, ny) == (to_x,to_y):
                return d+1
            elif tile_kb[(nx,ny)] == MAP_FREE:
                q.append((d+1,nx,ny))
    return None

def fill_time(from_x,from_y):
    """Perform breadth-first search and return the distance of the furthest
    tile from (from_x,from_y)"""
    filled = set()
    q = deque()
    d = 0
    q.append((d,from_x,from_y))
    while len(q) > 0:
        d, tx, ty = q.popleft()
        filled.add((tx,ty))
        for (nx, ny) in neighbors(tx, ty):
            if (nx, ny) in filled:
                continue
            elif tile_kb[(nx,ny)] == MAP_FREE:
                q.append((d+1,nx,ny))
    return d 

def direction(from_x,from_y,to_x,to_y):
    """Assuming (from_x,from_y) and (to_x,to_y) are adjacent,
    return direction code to step to (to_x,to_y)."""
    if to_y < from_y:
        return MOVE_NORTH
    if to_y > from_y:
        return MOVE_SOUTH
    if to_x < from_x:
        return MOVE_EAST
    else: # to_x > from_x
        return MOVE_WEST


goal_x, goal_y = None, None

while True:

    for adj in neighbors(droid_x, droid_y):
        if adj not in visited:
            unknown.add(adj)

    res = step_to_unknown(droid_x,droid_y)
    if res == None:
        # All squares explored
        break
    else:
        nx,ny = res

    print((droid_x,droid_y),"to",(nx,ny))

    cmd = direction(droid_x,droid_y,nx,ny) # randint(1,4)

    target = None
    if cmd == MOVE_NORTH:
        target = (droid_x, droid_y-1)
    if cmd == MOVE_SOUTH:
        target = (droid_x, droid_y+1)        
    if cmd == MOVE_WEST:
        target = (droid_x+1, droid_y)
    if cmd == MOVE_EAST:
        target = (droid_x-1, droid_y)

    p.run([cmd])
    result = p.outputs.pop()
    visited.add(target)

    if target in unknown:
        unknown.remove(target)

    if result == CODE_WALL:
        tile_kb[target] = MAP_WALL
    elif result == CODE_MOVE:
        tile_kb[target] = MAP_FREE
        droid_x = target[0]
        droid_y = target[1]
    elif result == CODE_GOAL:
        tile_kb[target] = MAP_GOAL
        droid_x = goal_x = target[0]
        droid_y = goal_y = target[1]

    if result == CODE_MOVE and ((droid_x + droid_y) % 2) == 0:
        bitmap = explored_bitmap()
        plt.cla()
        plt.imshow(bitmap, cmap="summer")
        plt.pause(0.001)

print("Commands required:", distance(0,0,goal_x,goal_y))

print("Filled in:", fill_time(goal_x,goal_y))