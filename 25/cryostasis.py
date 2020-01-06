import itertools
from collections import defaultdict, deque
from random import randint

import sys # https://stackoverflow.com/a/45874916/12214508
sys.path.append("..")
from IntCode import Program

with open("input",'r') as f:
    code = list(map(int, f.readline().strip().split(',')))

p = Program(code)
ascii_inputs = []

while not p.halt_f:
    p.run(ascii_inputs)
    ascii_output = p.outputs
    print("".join(list(map(chr, ascii_output))))
    user_input = input()
    ascii_inputs = list(map(ord, user_input)) + [10]
    