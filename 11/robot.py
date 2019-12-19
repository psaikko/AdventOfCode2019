import itertools
from collections import defaultdict
from matplotlib import pyplot

import sys # https://stackoverflow.com/a/45874916/12214508
sys.path.append("..")
from IntCode import Program

with open("input",'r') as f:
    code = list(map(int, f.readline().strip().split(',')))

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Robot:
    def __init__(self, code):
        self.prog = Program(code)

    def move(self):
        if self.dir == UP:
            self.y += 1
        elif self.dir == RIGHT:
            self.x += 1
        elif self.dir == DOWN:
            self.y -= 1
        else: # self.dir == LEFT
            self.x -= 1

    def run(self): 
        self.dir = UP
        self.hull = defaultdict(lambda: 1)
        self.painted = set()
        self.x = 0
        self.y = 0

        while not self.prog.halt_f:
            pos = (self.x, self.y)
            color = self.hull[pos]
            self.prog.run([color])
            newcolor, turn = self.prog.outputs
            self.prog.outputs.clear()

            self.hull[pos] = newcolor
            self.painted.add(pos)

            if turn == 1:
                self.dir += 1
            if turn == 0:
                self.dir -= 1
            self.dir = self.dir % 4

            self.move()

        print(len(self.painted))

r = Robot(code)
r.run()

xmin, xmax, ymin, ymax = float('inf'), -float('inf'), float('inf'), -float('inf')
for (x,y) in r.painted:
    xmin = min(x, xmin)
    xmax = max(x, xmax)
    ymin = min(y, ymin)
    ymax = max(y, ymax)

bitmap = [[0]*(xmax - xmin + 1) for _ in range(ymax - ymin + 1)]

for x in range(xmin,xmax+1):
    for y in range(ymin,ymax+1):
        c = r.hull[(x,y)]
        bitmap[y-ymin][x-xmin] = c

bitmap.reverse()
pyplot.imshow(bitmap, cmap="gray")
pyplot.show()