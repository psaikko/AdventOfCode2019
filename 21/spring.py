import itertools
from collections import defaultdict, deque
from random import randint

import sys # https://stackoverflow.com/a/45874916/12214508
sys.path.append("..")
from IntCode import Program

with open("input",'r') as f:
    code = list(map(int, f.readline().strip().split(',')))

# PART 1
script = """\
NOT A J
NOT C T
AND D T
OR T J
WALK
"""

# PART 2
script = """\
NOT C J
AND D J
OR E T
OR H T
AND T J
NOT A T
OR T J
OR B T
OR E T
NOT T T
OR T J
RUN
"""

scriptlines = script.split("\n")
print(scriptlines)

ascii_input = list(map(ord, script))

p = Program(code)
p.run(ascii_input)

print(p.wait_f, p.halt_f)

print("".join(list(map(chr, p.outputs[:-1]))))
print(p.outputs[-1])
