import itertools
l1 = [1, 2, 3, 4]
l2 = [5, 6, 7, 8]
l3 = [9, 10, 11, 12]
L = [l1, l2, l3]
T = []
for i in range(1, 11):
    t = [x for x in range(i, i+10)]
    T.append(t)
size = len(L)
sizeT = len(T)
for l in range(2, size+1):
    for sub in itertools.combinations(L[0:size], l):
        L.append([sum(x) for x in zip(*list(sub))])
for p in range(2, sizeT+1):
    for sub in itertools.combinations(T[0:sizeT], p):
        T.append(([sum(x) for x in zip(*list(sub))]))
print L
print T
print len(T)

