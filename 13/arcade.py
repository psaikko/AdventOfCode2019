import itertools
from collections import defaultdict
from matplotlib import pyplot as plt
from matplotlib import animation

import sys # https://stackoverflow.com/a/45874916/12214508
sys.path.append("..")
from IntCode import Program

with open("input",'r') as f:
    code = list(map(int, f.readline().strip().split(',')))

code[0] = 2
ball_x = None
paddle_x = None
score = 0

command = 0
p = Program(code)
p.run([])

while True:
    
    ids = p.outputs[2::3]
    xs = p.outputs[0::3]
    ys = p.outputs[1::3]

    xmax = max(xs)
    ymax = max(ys)

    field = [[0] * (xmax+1) for _ in range(ymax+1)]

    for (x,y,i) in zip(xs,ys,ids):
        if x >= 0:
            field[y][x] = i
        else: score = i
        if i == 4: ball_x = x
        elif i == 3: paddle_x = x

    if ball_x % 2 == 0:
        plt.cla()
        plt.imshow(field, cmap="summer")
        plt.pause(0.01)

    if ball_x < paddle_x: command = -1
    elif ball_x > paddle_x: command = 1
    else: command = 0
 
    if p.halt_f: break
    p.run([command])
print(score)