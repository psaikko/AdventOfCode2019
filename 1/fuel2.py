import math
lines = [line.strip() for line in open("input", 'r')]
masses = [int(line) for line in lines if line]

def mass2fuel(m):
    return math.floor(m / 3) - 2

def rocket_fuel(m):
    f_total = 0
    f_mass = mass2fuel(m)
    while f_mass > 0:
        f_total += f_mass
        f_mass = mass2fuel(f_mass)
    return f_total

fuels = [rocket_fuel(m) for m in masses]
print(sum(fuels))

print(rocket_fuel(100756))