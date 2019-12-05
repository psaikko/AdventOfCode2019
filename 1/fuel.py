import math
lines = [line.strip() for line in open("input", 'r')]
masses = [int(line) for line in lines if line]
fuels = [math.floor(m / 3) - 2 for m in masses]
print(sum(fuels))