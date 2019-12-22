import itertools
from collections import defaultdict, deque
from random import randint

import sys # https://stackoverflow.com/a/45874916/12214508
sys.path.append("..")
from IntCode import Program

with open("input",'r') as f:
    code = list(map(int, f.readline().strip().split(',')))

script = """\
NOT A J
NOT C T
AND D T
OR T J
WALK
"""

scriptlines = script.split("\n")
print(scriptlines)

ascii_input = list(map(ord, script))

p = Program(code)
p.run(ascii_input)

print(p.wait_f, p.halt_f)

print("".join(list(map(chr, p.outputs[:-1]))))
print(p.outputs[-1])