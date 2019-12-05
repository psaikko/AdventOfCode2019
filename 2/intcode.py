with open("input",'r') as f:
    mem = list(map(int, f.readline().strip().split(',')))

PC = 0

ops = {
    1 : lambda a, b : a + b,
    2 : lambda a, b : a * b
    }

ARG1 = 1
ARG2 = 2
RES  = 3
HALT = 99

mem[1] = 12
mem[2] = 2

while mem[PC] != HALT:
    print(mem[PC:PC+4])
    arg1_ptr = mem[PC+ARG1]
    arg2_ptr = mem[PC+ARG2]
    res_ptr = mem[PC+RES]
    mem[res_ptr] = ops[mem[PC]](mem[arg1_ptr],mem[arg2_ptr])
    print(mem)
    PC += 4

print(mem[0])