def gcd(gcd_a, gcd_b):
    if gcd_b == 0:
        return gcd_a
    return gcd(gcd_b, gcd_a % gcd_b)


def isPrime(number):
    if number == 2 or number == 3:
        return True
    if number < 2 or number % 2 == 0:
        return False
    if number < 9:
        return True
    if n % 3 == 0:
        return False
    border = int(number**0.5)
    tmp = 5
    while tmp <= border:
        if number % tmp == 0:
            return False
        if number % (tmp + 2) == 0:
            return True
        tmp += 6
    return True


def get_rsa_params(grp_p, grp_q):
    grp_euler_n = (grp_p-1) * (grp_q-1)
    grp_e = 2
    grp_x = []
    while grp_e < grp_euler_n-1:
        if gcd(grp_e, grp_euler_n) == 1:
            grp_x.append(grp_e)
        grp_e += 1
    for element in grp_x:
        if isPrime(element):
            grp_e = element
    grp_d = 1
    while not (grp_e * grp_d) % grp_euler_n == 1:
        grp_d += 1
    return grp_euler_n, grp_e, grp_d


def rsa_encrypt(re_msg, re_e, re_n):
    re_cipher = pow(re_msg, re_e, re_n)
    return re_cipher


def rsa_decrypt(re_cipher, re_d, re_n):
    re_msg = pow(re_cipher, re_d, re_n)
    return re_msg


def qft(qft_n, qft_a):
    qft_tmp = pow(qft_a, 1, qft_n)
    qft_i = 2
    while not pow(qft_a, qft_i, qft_n) == qft_tmp:
        qft_i += 1
    return qft_i-1


if __name__ == '__main__':
    n = 143
    a = 2
    r = qft(n, a)
    print(r)
    if r % 2 == 0:
        x = pow(2, int(r/2), n)
        print(x)
    else:
        x = 0
    p = gcd(x-1, n)
    q = gcd(x+1, n)
    assert p * q == n
    print(p)
    print(q)
    print()

    euler_n, d, e = get_rsa_params(p, q)
    msg = 10
    cipher = rsa_encrypt(msg, e, n)
    new_msg = rsa_decrypt(cipher, d, n)
    print(f'p: {p}', f'q: {q}', f'n: {n}', f'euler_n: {euler_n}', f'd: {d}', f'e: {e}', sep='\n')
    print()
    print(msg, cipher, new_msg, sep='\n')
