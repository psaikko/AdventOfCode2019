import itertools
from collections import defaultdict, deque
from matplotlib import pyplot as plt
from matplotlib import animation
from random import randint

with open("input",'r') as f:
    code = list(map(int, f.readline().strip().split(',')))

nargs = {
    1 : 2,  2 : 2,  3 : 0,
    4 : 1,  5 : 2,  6 : 2,
    7 : 2,  8 : 2,  9 : 1, 99: 0
}

ARG1 = 1
ARG2 = 2
RES  = 3
HALT = 99

def parse_opcode(x):
    op = x % 100
    x //= 100
    modes = []
    while x:
        modes.append(x % 10)
        x //= 10
    while len(modes) <= nargs[op]:
        modes.append(0)
    return (op, modes)

class Program:
    def op_jt(self, a, b):
        if a != 0: self.PC = b

    def op_jf(self, a, b):
        if a == 0: self.PC = b

    def op_halt(self):
        self.halt_f = True

    def op_print(self, x):
        self.outputs.append(x)

    def op_input(self):
        if len(self.inputs) == 0:
            self.wait_f = True
            return
        x, self.inputs = self.inputs[0], self.inputs[1:]
        return x

    def op_relo(self, a):
        self.RELO += a

    def __init__(self, code):
        self.mem = defaultdict(int)
        for i,v in enumerate(code): self.mem[i] = v
        #self.mem = code[:]
        self.PC = 0
        self.RELO = 0
        self.halt_f = False
        self.wait_f = False
        self.outputs = []

        self.ops = {
            1 : lambda self, a, b : a + b,
            2 : lambda self, a, b : a * b,
            3 : lambda self : self.op_input(),
            4 : lambda self, x : self.op_print(x),
            5 : lambda self, a, b : self.op_jt(a, b),
            6 : lambda self, a, b : self.op_jf(a, b),
            7 : lambda self, a, b : 1 if (a < b) else 0,
            8 : lambda self, a, b : 1 if (a == b) else 0,
            9 : lambda self, a : self.op_relo(a),
            99: lambda self : self.op_halt()
        }

    def memread(self):
        val = self.mem[self.PC]
        self.PC += 1
        return val

    def get_args(self, modes):
        args = []
        for m in modes:
            if m == 1: # direct 
                val = self.memread()
            elif m == 2: # relative mode
                ptr = self.memread() + self.RELO
                # print("@%d+%d"%(ptr-self.RELO, self.RELO),end=" ")
                val = self.mem[ptr]
            else: # position
                ptr = self.memread()
                # print("@%d"%ptr,end=" ")
                val = self.mem[ptr]
            args += [val]
        return args

    def run(self, inputs):
        self.inputs = inputs
        if self.wait_f:
            self.wait_f = False
            # rewind to start of input instruction
            self.PC -= 1
        while not self.halt_f and not self.wait_f:
            pc = self.PC
            v = self.memread()
            op, modes = parse_opcode(v)
            # print("%d(%d)@%d" % (op,v,pc), end=" ")
            # print(modes,end=" ")
            args = self.get_args(modes[:-1])
            # print(args)
            res = self.ops[op](*([self] + args))
            if res != None:        
                resaddr = self.memread()
                if modes[-1] == 2: resaddr += self.RELO
                # print("->","%d@%d" % (res,resaddr))
                self.mem[resaddr] = res

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
        #print(tx,ty)
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
    seen = set()
    q = deque()
    q.append((0,from_x,from_y))

    while len(q) > 0:
        d, tx, ty = q.popleft()
        print(tx,ty)
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
        print(tx,ty)
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

    bitmap = explored_bitmap()
    plt.cla()
    plt.imshow(bitmap, cmap="summer")
    plt.pause(0.001)

print("Commands required:", distance(0,0,goal_x,goal_y))

print("Filled in:", fill_time(goal_x,goal_y))