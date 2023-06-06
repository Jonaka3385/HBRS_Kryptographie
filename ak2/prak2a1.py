from random import randint
from time import time


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
    if number % 3 == 0:
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


def qft(qft_a, qft_n):
    qft_tmp = pow(qft_a, 1, qft_n)
    qft_i = 2
    while not pow(qft_a, qft_i, qft_n) == qft_tmp:
        qft_i += 1
    return qft_i-1


def shor():
    p = randint(100, 200)
    while not isPrime(p):
        p = randint(100, 200)
    q = randint(100, 200)
    while not isPrime(q) and not p == q:
        q = randint(100, 200)
    n = p*q
    print('\n\n', f'p: {p}', f'q: {q}', f'n: {n}', '', sep='\n')
    a = 2
    r = qft(a, n)
    while a < n and not r % 2 == 0:
        a += 1
        r = qft(a, n)
    print(f'r: {r}', sep='\n')
    if r % 2 == 0:
        x = pow(2, int(r/2), n)
        print(f'x: {x}', f'a: {a}', '', sep='\n')
    else:
        return False, False
    p_tmp = gcd(x-1, n)
    q_tmp = gcd(x+1, n)
    print(f'p_tmp: {p_tmp}', f'q_tmp: {q_tmp}', sep='\n')
    if not p_tmp * q_tmp == n:
        return False, False
    if not isPrime(p_tmp):
        return False, False
    if not isPrime(q_tmp):
        return False, False
    if (p_tmp == p or p_tmp == q) or (q_tmp == p or q_tmp == q):
        print('Success?\n')

    euler_n, d, e = get_rsa_params(p, q)
    msg = 10
    cipher = rsa_encrypt(msg, e, n)
    new_msg = rsa_decrypt(cipher, d, n)
    print(f'p: {p}', f'q: {q}', f'n: {n}', f'euler_n: {euler_n}', f'd: {d}', f'e: {e}', sep='\n')
    print()
    crypt_worked = msg == new_msg
    print(msg, cipher, new_msg, f'Crypt worked: {crypt_worked}', sep='\n')
    return True, crypt_worked


if __name__ == '__main__':
    start = time()
    worked = 0
    tries = 100
    crypt_worked = 0
    for i in range(tries - 1):
        sw, cw = shor()
        if sw:
            worked += 1
        if cw == 1:
            crypt_worked += 1

    end = time()
    print(f'\n\nTime passed:          {end - start}s')
    worked_pro = worked / (tries/100)
    print(f'worked:               {worked} out of {tries}; {worked_pro}%')
    crypt_worked_pro = crypt_worked / (tries / 100)
    print(f'worked with crypting: {crypt_worked} out of {tries}; {crypt_worked_pro}%')
