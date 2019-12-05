with open("input",'r') as f:
    mem = list(map(int, f.readline().strip().split(',')))

PC = 0

ops = {
    1 : lambda a, b : a + b,
    2 : lambda a, b : a * b,
    3 : lambda : int(input(">> ")),
    4 : lambda x : print(">>",x),
    99: lambda : exit(0)
}

nargs = {
    1 : 2,
    2 : 2,
    3 : 0,
    4 : 1,
    99: 0
}

ARG1 = 1
ARG2 = 2
RES  = 3
HALT = 99

def memread():
    global PC
    val = mem[PC]
    PC += 1
    return val

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

def get_args(modes):
    global PC
    args = []
    for m in modes:
        if m == 1:
            val = memread()
            print("=%d" % val,end=" ")
        else: 
            ptr = memread()
            val = mem[ptr]
            print("@%d" % ptr,end=" ")
        args += [val]
    return args

while True:
    v = memread()
    op, modes = parse_opcode(v)
    print("%d(%d)" % (op,v), end=" ")
    print(modes,end=" ")
    args = get_args(modes)
    print(args)
    res = ops[op](*args)
    if res != None:        
        resaddr = memread()
        print("->","@%d" % resaddr)
        mem[resaddr] = res
    else:
        print()