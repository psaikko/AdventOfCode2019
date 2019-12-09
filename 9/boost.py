import itertools
from collections import defaultdict

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
                print("@%d+%d"%(ptr-self.RELO, self.RELO),end=" ")
                val = self.mem[ptr]
            else: # position
                ptr = self.memread()
                print("@%d"%ptr,end=" ")
                val = self.mem[ptr]
            args += [val]
        return args

    def run(self, inputs):
        self.inputs = inputs
        while not self.halt_f:
            pc = self.PC
            v = self.memread()
            op, modes = parse_opcode(v)
            print("%d(%d)@%d" % (op,v,pc), end=" ")
            print(modes,end=" ")
            args = self.get_args(modes[:-1])
            print(args)
            res = self.ops[op](*([self] + args))
            if res != None:        
                resaddr = self.memread()
                if modes[-1] == 2: resaddr += self.RELO
                print("->","%d@%d" % (res,resaddr))
                self.mem[resaddr] = res

p = Program(code)
p.run([2])
print(p.outputs)
