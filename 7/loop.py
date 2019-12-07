import itertools

with open("input",'r') as f:
    code = list(map(int, f.readline().strip().split(',')))

nargs = {
    1 : 2,  2 : 2,  3 : 0,
    4 : 1,  5 : 2,  6 : 2,
    7 : 2,  8 : 2,  99: 0
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
    while len(modes) < nargs[op]:
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

    def __init__(self, code):
        self.mem = code[:]
        self.PC = 0
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
            99: lambda self : self.op_halt()
        }

    def memread(self):
        val = self.mem[self.PC]
        self.PC += 1
        return val

    def get_args(self, modes):
        args = []
        for m in modes:
            if m == 1:
                val = self.memread()
                #print("=%d" % val,end=" ")
            else: 
                ptr = self.memread()
                val = self.mem[ptr]
                #print("@%d" % ptr,end=" ")
            args += [val]
        return args

    def run(self, inputs):
        self.inputs = inputs
        if self.wait_f:
            self.wait_f = False
            # rewind to start of input instruction
            self.PC -= 1
        while not self.halt_f and not self.wait_f:
            v = self.memread()
            op, modes = parse_opcode(v)
            #print("%d(%d)" % (op,v), end=" ")
            #print(modes,end=" ")
            args = self.get_args(modes)
            #print(args)
            res = self.ops[op](*([self] + args))
            if res != None:        
                resaddr = self.memread()
                #print("->","@%d" % resaddr)
                self.mem[resaddr] = res

amps = "ABCDE"
setting_values = [5,6,7,8,9]

max_out = -float('inf')
max_set = None

for settings in itertools.permutations(setting_values, 5):

    output = 0
    programs = [Program(code) for a in amps]

    for prog, setting in zip(programs, settings):
        prog.run([setting])

    i = 0
    while True:
        prog = programs[i]
        if prog.halt_f: break
        prog.run([output])
        output = prog.outputs[-1]
        i = (i+1)%len(programs)
        
    if output > max_out:
        max_out = output
        max_set = settings
print(max_out, max_set)
