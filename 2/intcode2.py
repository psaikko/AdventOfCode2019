with open("input",'r') as f:
    program = list(map(int, f.readline().strip().split(',')))

ops = {
    1 : lambda a, b : a + b,
    2 : lambda a, b : a * b
    }

ARG1 = 1
ARG2 = 2
RES  = 3
HALT = 99

def run(noun,verb):
    mem = program[:]
    PC = 0

    mem[1] = noun
    mem[2] = verb

    while mem[PC] != HALT:

        arg1_ptr = mem[PC+ARG1]
        arg2_ptr = mem[PC+ARG2]
        res_ptr = mem[PC+RES]
        mem[res_ptr] = ops[mem[PC]](mem[arg1_ptr],mem[arg2_ptr])
        PC += 4

    return mem[0]

for noun in range(0,100):
    for verb in range(0,100):
        res = run(noun,verb)
        if res == 19690720:
            print(100 * noun + verb)
            exit(0)
