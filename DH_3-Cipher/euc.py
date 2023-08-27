def extendedEuclidean(n, b):
    r1, r2 = n, b
    t1, t2 = 0, 1
    while r2:
        q = r1 // r2
        r = r1 - q * r2
        r1, r2 = r2, r
        t = t1 - q * t2
        t1, t2 = t2, t

    if r1 != 1:
        return 0
    if t1 < 0:
        t1 = n + t1
    return t1


p = 3573716833
q = 3671005097
e = 65537
phi = (p - 1) * (q - 1)
print(extendedEuclidean(phi, e))
