"""
Praktikum 1 Aufgabe 2
p_ = Übergebener Parameter
"""
import time
import timeit
from dataclasses import dataclass
from random import randrange
from gmpy2 import xmpz, mpz, is_prime, invert, powmod, mpz_random, random_state, gcd
from sympy import primefactors


@dataclass
class PrivKey:
    """
    Private Key.
    """
    n: mpz
    d: mpz


@dataclass
class PubKey:
    """
    Private Key.
    """
    n: mpz
    e: mpz


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
    a = mpz((p - 1) * (q - 1))
    randstate = random_state(randrange(1, 2 ** p_bits))
    e = mpz_random(randstate, a - 1)
    while True:
        if gcd(e, a) == 1:
            break
        e = mpz_random(randstate, a - 1)
    d = invert(e, a)  # e*d mod a = 1
    if (e * d) % a == 1:
        return p, q, n, a, e, d
    else:
        print("false d, quitting code")
        quit()


def crypt(p_msg, p_x, p_n):
    """
    :param p_msg:
    :param p_x: e oder d
    :param p_n:
    :return: chiffrat
    """
    return powmod(p_msg, p_x, p_n)


def sign(p_msg, p_d, p_n):
    """
    :param p_msg:
    :param p_n:
    :param p_d:
    :return: signature
    """
    h = hash(p_msg)
    return crypt(h, p_d, p_n)


def verify(p_msg, p_signature, p_e, p_n):
    """
    :param p_msg:
    :param p_signature:
    :param p_e:
    :param p_n:
    :return: True or False
    """
    h = hash(p_msg)
    h2 = crypt(p_signature, p_e, p_n)
    return h == h2


def euler_totient(n):
    """
    :param n:
    :return:
    """
    print('try primefactors')
    factors = primefactors(n)
    result = xmpz(n)
    print('got primefactors', f'laenge: {len(factors)}')
    for factor in factors:
        result *= (1 - 1 / factor)
    return mpz(result)


def fake_it(p_msg, p_e, p_n, p_s):
    """
    :param p_s:
    :param p_msg:
    :param p_e:
    :param p_n:
    :return: gefaelschte Signatur 
    """
    print('try phi')
    phi_n = euler_totient(p_n)
    print('got phi, try invert')
    d = invert(p_e, phi_n)
    print('got invert')
    print(d)
    s = sign(p_msg, d, p_n)
    return s


if __name__ == '__main__':
    bit_len = 3000
    p, q, n, a, e, d = rsa_key(bit_len)
    priv_key = PrivKey(n, d)
    pub_key = PubKey(n, e)
    msg = mpz(42)
    chiffrat = crypt(msg, pub_key.e, pub_key.n)
    decrypt_msg = crypt(chiffrat, priv_key.d, priv_key.n)
    signature = sign(msg, priv_key.d, priv_key.n)
    verifikation = verify(msg, signature, pub_key.e, pub_key.n)
    faelschung = fake_it(msg, pub_key.e, pub_key.n, signature)
    new_verifikation = verify(msg, faelschung, pub_key.e, pub_key.n)
    print(f'p: {p}', f'q: {q}', f'n: {n}', f'a: {a}', f'e: {e}', f'd: {d}', f'msg: {msg}', f'chiffrat: {chiffrat}',
          f'decrypted msg: {decrypt_msg}', f'signature: {signature}', f'verifikation: {verifikation}',
          f'Faelschung: {faelschung}', f'Faelschung verify: {new_verifikation}', sep='\n')
