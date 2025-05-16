def lfsr(lfsr_seed, laenge, p):
    x = [0] * len(lfsr_seed)
    for i in range(len(lfsr_seed)):
        x[i] = lfsr_seed[i]

    print(x)
    result = ''
    for i in range(laenge):
        result += str(x[16])
        tmp = 0
        for j in range(1, len(lfsr_seed)):
            tmp += x[j] * p[j]
            tmp %= 2
        for j in range(len(lfsr_seed) - 1, 0, -1):
            x[j] = x[j - 1]
        x[0] = tmp
        print(x)

    print(result)


if __name__ == '__main__':
    seed = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    # polynom:(1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17)
    polynom = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    lfsr(seed, 64, polynom)
