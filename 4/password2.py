from collections import Counter

start = 359282
end = 820401

def check(v):
    s = str(v)
    for i in range(5):
        if int(s[i]) > int(s[i+1]):
            return False
    c = Counter(s)
    if 2 not in c.values():
        return False
    return True

c = 0
for v in range(start,end+1):
    if check(v):
        c += 1

print(c)