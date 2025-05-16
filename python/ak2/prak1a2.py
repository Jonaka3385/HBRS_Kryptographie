"""
Praktikum 1 Aufgabe 2
p_ = Übergebener Parameter
"""
from random import randrange
from hashlib import sha256
# gmpy2 xmpz, mpz = different type of numeric values (xmpz is mutable, mpz not)
from gmpy2 import xmpz, to_binary, invert, powmod, is_prime


def generate_p_q(p_l, p_n):
    """
    :param p_l: l
    :param p_n: n
    :return generated_p, generated_q: die generierten p, q
    """
    g = p_n  # g >= 160
    n2 = (p_l - 1) // g
    b = (p_l - 1) % g
    while True:
        # generate q
        while True:
            # noinspection PyArgumentList
            s = xmpz(randrange(1, 2 ** g))
            a = sha256(to_binary(s)).hexdigest()
            zz = (s + 1) % (2 ** g)
            z = sha256(to_binary(zz)).hexdigest()
            u = int(a, 16) ^ int(z, 16)
            mask = 2 ** (p_n - 1) + 1  # nn-1 und niedrigste Bit auf 1 setzen rest 0
            q = u | mask  # u OR mask
            if is_prime(q, 20):
                break
        # generate p
        i = 0  # counter
        j = 2  # offset
        while i < 4096:
            v = []
            for counter in range(n2 + 1):
                arg = (s + j + counter) % (2 ** g)
                zzv = sha256(to_binary(arg)).hexdigest()
                v.append(int(zzv, 16))
            w = 0
            for counter2 in range(0, n2):
                w += v[counter2] * 2 ** (160 * counter2)
            w += (v[n2] % 2 ** b) * 2 ** (160 * n2)
            xx = w + 2 ** (p_l - 1)
            c = xx % (2 * q)
            p = xx - c + 1  # p = x - (c-1)
            if p >= 2 ** (p_l - 1):
                if is_prime(p, 10):
                    return p, q
            i += 1
            j += n2 + 1


def generate_alpha(p_p, p_q):
    """
    :param p_p: p
    :param p_q: q
    :return generated_alpha: alpha
    """
    while True:
        h = randrange(2, p_p - 1)
        exp = (p_p - 1) // p_q
        alpha = powmod(h, exp, p_p)
        if alpha > 1:
            break
    return alpha


def generate_params(p_length, p_n):
    """
    :param p_length: Schlüssellänge
    :param p_n: n
    :return: p, q, alpha
    """
    p, q = generate_p_q(p_length, p_n)
    alpha = generate_alpha(p, q)
    return p, q, alpha


def generate_keys(p_g, p_p, p_q):
    """
    :param p_g: g
    :param p_p: p
    :param p_q: q
    :return: x, y
    """
    x = randrange(2, p_q)  # x < q
    y = powmod(p_g, x, p_p)
    return x, y


def validate_params(p_p, p_q, p_alpha):
    """
    :param p_p: p
    :param p_q: q
    :param p_alpha: alpha
    :return: boolean-Ergebnis der validierung
    """
    if is_prime(p_p) and is_prime(p_q):
        if powmod(p_alpha, p_q, p_p) == 1 and p_alpha > 1 and \
                ((p_p - 1) % p_q) == 0:
            return True
    return False


def validate_sign(p_gamma, p_delta, p_q):
    """
    :param p_gamma: gamma
    :param p_delta: delta
    :param p_q: q
    :return: boolean-Ergebnis der validierung von der Signatur
    """
    if 0 > p_gamma > p_q:
        return False
    if 0 > p_delta > p_q:
        return False
    return True


def sign(p_msg, p_p, p_q, p_alpha, p_privkey):
    """
    :param p_msg: message to sign
    :param p_p: p
    :param p_q: q
    :param p_alpha: alpha
    :param p_privkey: private key
    :return: gamma, delta, k
    """
    if not validate_params(p_p, p_q, p_alpha):
        raise Exception('Invalid params')
    while True:
        k = randrange(2, p_q)  # k < q
        gamma = powmod(p_alpha, k, p_p) % p_q
        m = int(sha256(p_msg).hexdigest(), 16)
        try:
            delta = (invert(k, p_q) * (m + p_privkey * gamma)) % p_q
            return gamma, delta, k
        except ZeroDivisionError:
            pass


def sign_with_k(p_msg, p_p, p_q, p_alpha, p_a, p_k):
    """
    :param p_msg: message to sign
    :param p_p: p
    :param p_q: q
    :param p_alpha: alpha
    :param p_a: a
    :param p_k: k
    :return: r, delta, k
    """
    if not validate_params(p_p, p_q, p_alpha):
        raise Exception('Invalid params')
    r = powmod(p_alpha, p_k, p_p) % p_q
    m = int(sha256(p_msg).hexdigest(), 16)
    try:
        delta = (invert(p_k, p_q) * (m + p_a * r)) % p_q
        return r, delta, p_k
    except ZeroDivisionError:
        pass


def verify(p_msg, p_gamma, p_delta, p_p, p_q, p_alpha, p_beta):
    """
    :param p_msg: message to verify
    :param p_gamma: gamma
    :param p_delta: delta
    :param p_p: p
    :param p_q: q
    :param p_alpha: alpha
    :param p_beta: beta
    :return: boolean-Ergebnis vom Verifizieren
    """
    if not validate_params(p_p, p_q, p_alpha):
        raise Exception('Invalid params')
    if not validate_sign(p_gamma, p_delta, p_q):
        return False
    try:
        w = invert(p_delta, p_q)
    except ZeroDivisionError:
        return False
    m = int(sha256(p_msg).hexdigest(), 16)
    u1 = (m * w) % p_q
    u2 = (p_gamma * w) % p_q
    v = (powmod(p_alpha, u1, p_p) * powmod(p_beta, u2, p_p)) % p_p % p_q
    if v == p_gamma:
        return True
    return False


def private_key_finder(p_msg1, p_msg2, p_delta1, p_delta2, p_q, p_gamma):
    """
    :param p_msg1: erste message
    :param p_msg2: zweite message
    :param p_delta1: delta der ersten message
    :param p_delta2: delta der zweiten message
    :param p_q: q
    :param p_gamma: gamma
    :return: nothing (private key will be printed in console)
    """
    h1 = int(sha256(p_msg1).hexdigest(), 16)
    h2 = int(sha256(p_msg2).hexdigest(), 16)

    delta1_inv = pow(p_delta1, -1, p_q)
    delta2_inv = pow(p_delta2, -1, p_q)
    x_calc = ((h1 * delta1_inv - h2 * delta2_inv) * pow(p_gamma, -1, p_q)
              * pow((delta2_inv - delta1_inv), -1, p_q)) % p_q

    print(f'Privater Schlüssel: {x_calc}')
    return


if __name__ == '__main__':
    key_n = 256
    key_length = 3072
    p, q, alpha = generate_params(key_length, key_n)
    priv_key, beta = generate_keys(alpha, p, q)

    text = 'Hallo, Welt!'
    msg = str.encode(text)
    gamma, delta, k = sign(msg, p, q, alpha, priv_key)
    b = False
    if verify(msg, gamma, delta, p, q, alpha, beta):
        print(f'All ok')
        b = True
    print(f'msg: {msg}', f'gamma: {gamma}', f'delta: {delta}', f'p: {p}', f'q: {q}', f'g: {alpha}', f'beta: {beta}',
          f'priv_key: {priv_key}', sep='\n')

    if b:
        text1 = text
        msg1, gamma1, delta1 = msg, gamma, delta
    else:
        print(f'Fehlerhafte Parameter')
        input(f'Trotzdem fortfahren?: ')
        text1 = text
        msg1, gamma1, delta1 = msg, gamma, delta

    # Next Text

    text = 'Hallo, Menschen!'
    msg = str.encode(text)
    gamma, delta, k = sign_with_k(msg, p, q, alpha, priv_key, k)
    b = False
    if verify(msg, gamma, delta, p, q, alpha, beta):
        print(f'All ok')
        b = True
    print(f'msg: {msg}', f'gamma: {gamma}', f'delta: {delta}', f'p: {p}', f'q: {q}', f'g: {alpha}', f'beta: {beta}',
          f'priv_key: {priv_key}', sep='\n')

    if b:
        text2 = text
        msg2, gamma2, delta2 = msg, gamma, delta
    else:
        print(f'Fehlerhafte Parameter')
        input(f'Trotzdem fortfahren?: ')
        text2 = text
        msg2, gamma2, delta2 = msg, gamma, delta

    # Faelschung erzeugen
    private_key_finder(msg1, msg2, delta1, delta2, q, gamma)
