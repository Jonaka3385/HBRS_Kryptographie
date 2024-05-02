"""
Praktikum 1 Aufgabe 2
p_ = Übergebener Parameter
"""
from random import randrange
from gmpy2 import xmpz, mpz, is_prime, invert, powmod, mpz_random, random_state, gcd


def generate_prime(p_l):
    """
    :param p_l: length
    :return generated_p, generated_q: die generierten p, q
    """
    randstate = random_state(randrange(1, 2 ** p_l))
    while True:
        prime = mpz_random(randstate, (2 ** p_l))
        if is_prime(prime):
            break
    return prime


def rsa_key(p_bits):
    """
    :param p_bits:
    :return: priv_key: d, pub_e: e, pub_n: n
    """
    p = generate_prime(p_bits)
    q = generate_prime(p_bits)
    n = p * q
    # gcd(e, (p-1)*(q-1)) = 1
    a = mpz((p - 1) * (q - 1))
    e = xmpz(2)
    while True:
        if gcd(e, a) == 1:
            e = mpz(e)
            break
        e += 1
    # e*d mod a = 1
    d = invert(e, a)
    return p, q, n, e, d


if __name__ == '__main__':
    bit_len = 3000
    p, q, n, e, d = rsa_key(bit_len)
    print(f'p: {p}', f'q: {q}', f'n: {n}', f'e: {e}', f'd: {d}', sep='\n')
