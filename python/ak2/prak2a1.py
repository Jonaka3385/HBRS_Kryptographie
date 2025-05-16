"""
prak2a1.py
"""
from random import randint
from time import time


def gcd(a, b):
    """

    :param a:
    :param b:
    :return:
    """
    if b == 0:
        return a
    return gcd(b, a % b)


def is_prime(number):
    """
    :param number:
    :return:
    """
    if number == 2 or number == 3:
        return True
    if number < 2 or number % 2 == 0:
        return False
    if number < 9:
        return True
    if number % 3 == 0:
        return False
    border = int(number ** 0.5)
    tmp = 5
    while tmp <= border - 4:
        if number % tmp == 0:
            return False
        if number % (tmp + 2) == 0:
            return False
        tmp += 6
    return True


def get_rsa_params(grp_p, grp_q):
    """

    :param grp_p:
    :param grp_q:
    :return:
    """
    grp_euler_n = (grp_p - 1) * (grp_q - 1)
    grp_e = 2
    grp_x = []
    while grp_e < grp_euler_n - 1:
        if gcd(grp_e, grp_euler_n) == 1:
            grp_x.append(grp_e)
        grp_e += 1
    for element in grp_x:
        if is_prime(element):
            grp_e = element
    grp_d = 1
    while not (grp_e * grp_d) % grp_euler_n == 1:
        grp_d += 1
    return grp_euler_n, grp_e, grp_d


def rsa_encrypt(re_msg, re_e, re_n):
    """

    :param re_msg:
    :param re_e:
    :param re_n:
    :return:
    """
    re_cipher = pow(re_msg, re_e, re_n)
    return re_cipher


def rsa_decrypt(re_cipher, re_d, re_n):
    """

    :param re_cipher:
    :param re_d:
    :param re_n:
    :return:
    """
    re_msg = pow(re_cipher, re_d, re_n)
    return re_msg


def qft(qft_a, qft_n):
    """

    :param qft_a:
    :param qft_n:
    :return:
    """
    qft_tmp = pow(qft_a, 1, qft_n)
    qft_i = 2
    while not pow(qft_a, qft_i, qft_n) == qft_tmp:
        qft_i += 1
    return qft_i - 1


def shor():
    """

    :return:
    """
    p = randint(100, 200)
    while not is_prime(p):
        p = randint(100, 200)
    q = randint(100, 200)
    while not is_prime(q) and not p == q:
        q = randint(100, 200)
    n = p * q
    print('\n\n', f'p: {p}', f'q: {q}', f'n: {n}', '', sep='\n')
    a = 2
    r = qft(a, n)
    while a < n and not r % 2 == 0:
        a += 1
        r = qft(a, n)
    print(f'r: {r}', sep='\n')
    if r % 2 == 0:
        x = pow(2, int(r / 2), n)
        print(f'x: {x}', f'a: {a}', '', sep='\n')
    else:
        return False, False
    p_tmp = gcd(x - 1, n)
    q_tmp = gcd(x + 1, n)
    print(f'p_tmp: {p_tmp}', f'q_tmp: {q_tmp}', sep='\n')
    if not p_tmp * q_tmp == n:
        return False, False
    if not is_prime(p_tmp):
        return False, False
    if not is_prime(q_tmp):
        return False, False
    if (p_tmp == p or p_tmp == q) or (q_tmp == p or q_tmp == q):
        print('Success?\n')

    euler_n, d, e = get_rsa_params(p, q)
    msg = 10
    cipher = rsa_encrypt(msg, e, n)
    new_msg = rsa_decrypt(cipher, d, n)
    print(f'p: {p}', f'q: {q}', f'n: {n}', f'euler_n: {euler_n}', f'd: {d}', f'e: {e}', sep='\n')
    print()
    crypting_worked = msg == new_msg
    print(msg, cipher, new_msg, f'Crypt worked: {crypting_worked}', sep='\n')
    return True, crypting_worked


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
    worked_pro = worked / (tries / 100)
    print(f'worked:               {worked} out of {tries}; {worked_pro}%')
    crypt_worked_pro = crypt_worked / (tries / 100)
    print(f'worked with crypting: {crypt_worked} out of {tries}; {crypt_worked_pro}%')
