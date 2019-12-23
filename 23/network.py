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
IDLE_THRESHOLD = 10

ids = range(50)

ports = [[] for _ in ids]
nat = []

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
        global ports, nat
        if self.out_seq % 3 == 0:
            self.out_port = x
        if self.out_seq % 3 == 1:
            self.out_packet.append(x)
        if self.out_seq % 3 == 2:
            self.out_packet.append(x)
            if self.out_port == 255:
                nat = self.out_packet
            else:
                ports[self.out_port] += self.out_packet
            #print("%d: %s -> %d" % (self.id, repr(self.out_packet) ,self.out_port))
            self.out_packet = []
        self.out_seq += 1

    def op_input(self):
        global ports
        if self.in_seq == 0:
            self.in_seq += 1
            print("read id %d" % self.id)
            return self.id
        if len(ports[self.id]) == 0:
            self.in_seq += 1
            if self.in_seq > IDLE_THRESHOLD:
                self.idle = True
            return -1
        self.idle = False
        self.in_seq = 1
        x, ports[self.id] = ports[self.id][0], ports[self.id][1:]
        return x

    def op_relo(self, a):
        self.RELO += a

    def __init__(self, code, id):
        self.idle = False
        self.in_seq = 0
        self.out_seq = 0
        self.out_port = -1
        self.out_packet = []
        self.id = id
        self.mem = defaultdict(int)
        for i,v in enumerate(code): self.mem[i] = v
        #self.mem = code[:]
        self.PC = 0
        self.RELO = 0
        self.halt_f = False

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
                val = self.mem[ptr]
            else: # position
                ptr = self.memread()
                val = self.mem[ptr]
            args += [val]
        return args

    def tick(self):
        v = self.memread()
        op, modes = parse_opcode(v)
        args = self.get_args(modes[:-1])
        res = self.ops[op](*([self] + args))
        if res != None:        
            resaddr = self.memread()
            if modes[-1] == 2: resaddr += self.RELO
            self.mem[resaddr] = res

nodes = [Program(code, i) for i in ids]

prev_nat_y = -1

while True:
    for n in nodes:
        n.tick()
    
    if len([n for n in nodes if n.idle]) == len(nodes):
        print("idle", nat)
        if prev_nat_y == nat[1]:
            print(prev_nat_y)
            break
        prev_nat_y = nat[1]
        ports[0] += nat
        for n in nodes:
            n.in_seq = 1
            n.idle = False
    