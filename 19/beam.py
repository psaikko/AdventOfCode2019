import itertools
from collections import defaultdict, deque
from random import randint

import sys # https://stackoverflow.com/a/45874916/12214508
sys.path.append("..")
from IntCode import Program

with open("input",'r') as f:
    code = list(map(int, f.readline().strip().split(',')))

statuses = []

for i in range(50):
    for j in range(50):
        p = Program(code)
        p.run([i,j])
        statuses += p.outputs
print(sum(statuses))