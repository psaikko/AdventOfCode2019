def parse_direction(s):
    return (s[0],int(s[1:]))

def read_wire(line):
    return [parse_direction(t) for t in line.strip().split(',')]

with open("input",'r') as f:
    wire1 = read_wire(f.readline())
    wire2 = read_wire(f.readline())

# wire1 = read_wire("R8,U5,L5,D3")
# wire2 = read_wire("U7,R6,D4,L4")

def trace_wire(l):
    trace = set()
    p = (0,0)
    #trace.add(p)
    for (d,n) in l:
        if d == 'U':
            for _ in range(n):
                p = (p[0],p[1]+1)
                trace.add(p)
        elif d == 'D':
            for _ in range(n):
                p = (p[0],p[1]-1)
                trace.add(p)
        elif d == 'L':  
            for _ in range(n):
                p = (p[0]-1,p[1])
                trace.add(p)
        elif d == 'R':
            for _ in range(n):
                p = (p[0]+1,p[1])
                trace.add(p)
    return trace

s1 = trace_wire(wire1)
s2 = trace_wire(wire2)

crosses = list(s1.intersection(s2))
dists = list(map(lambda p : abs(p[0])+abs(p[1]), crosses))

print(min(dists))
