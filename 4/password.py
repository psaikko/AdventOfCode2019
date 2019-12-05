start = 359282
end = 820401

def check(v):
    s = str(v)
    if len(set(s)) == 6: return False
    for i in range(5):
        if int(s[i]) > int(s[i+1]):
            return False
    return True

c = 0
for v in range(start,end+1):
    if check(v):
        c += 1

print(c)