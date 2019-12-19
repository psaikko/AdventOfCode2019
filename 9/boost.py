import itertools
from collections import defaultdict

import sys # https://stackoverflow.com/a/45874916/12214508
sys.path.append("..")
from IntCode import Program

with open("input",'r') as f:
    code = list(map(int, f.readline().strip().split(',')))

p = Program(code)
p.run([2])
print(p.outputs)
