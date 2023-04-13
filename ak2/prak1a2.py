from random import randrange
from hashlib import sha256
from gmpy2 import xmpz, to_binary, invert, powmod, is_prime
# gmpy2 für bessere Performance.
# z.B. xmpz = schnellerer, größerer int


def generate_p_q(key_length, nn):
    g = nn  # g >= 160
    n = (key_length - 1) // g
    b = (key_length - 1) % g
    while True:
        # generate q
        while True:
            s = xmpz(randrange(1, 2 ** g))
            a = sha256(to_binary(s)).hexdigest()
            zz = xmpz((s + 1) % (2 ** g))
            z = sha256(to_binary(zz)).hexdigest()
            u = int(a, 16) ^ int(z, 16)
            mask = 2 ** (nn - 1) + 1    # nn-1 und niedrigste Bit auf 1 setzen rest 0
            q = u | mask                # u OR mask
            if is_prime(q, 20):
                break
        # generate p
        i = 0  # counter
        j = 2  # offset
        while i < 4096:
            v = []
            for k in range(n + 1):
                arg = xmpz((s + j + k) % (2 ** g))
                zzv = sha256(to_binary(arg)).hexdigest()
                v.append(int(zzv, 16))
            w = 0
            for qq in range(0, n):
                w += v[qq] * 2 ** (160 * qq)
            w += (v[n] % 2 ** b) * 2 ** (160 * n)
            x = w + 2 ** (key_length - 1)
            c = x % (2 * q)
            p = x - c + 1  # p = x - (c-1)
            if p >= 2 ** (key_length - 1):
                if is_prime(p, 10):
                    return p, q
            i += 1
            j += n + 1


def generate_g(p, q):
    while True:
        h = randrange(2, p - 1)
        exp = xmpz((p - 1) // q)
        g = powmod(h, exp, p)
        if g > 1:
            break
    return g


def generate_params(key_length, nn):
    p, q = generate_p_q(key_length, nn)
    g = generate_g(p, q)
    return p, q, g


def generate_keys(g, p, q):
    x = randrange(2, q)  # x < q
    y = powmod(g, x, p)
    return x, y


def validate_params(p, q, g):
    if is_prime(p) and is_prime(q):
        return True
    if powmod(g, q, p) == 1 and g > 1 and (p - 1) % q:
        return True
    return False


def validate_sign(r, s, q):
    if 0 > r > q:
        return False
    if 0 > s > q:
        return False
    return True


def sign(msg, p, q, g, x):
    if not validate_params(p, q, g):
        raise Exception('Invalid params')
    while True:
        k = randrange(2, q)  # k < q
        r = powmod(g, k, p) % q
        m = int(sha256(msg).hexdigest(), 16)
        try:
            s = (invert(k, q) * (m + x * r)) % q
            return r, s, k
        except ZeroDivisionError:
            pass


def sign_with_k(msg, p, q, g, x, k):
    if not validate_params(p, q, g):
        raise Exception('Invalid params')
    while True:
        r = powmod(g, k, p) % q
        m = int(sha256(msg).hexdigest(), 16)
        try:
            s = (invert(k, q) * (m + x * r)) % q
            return r, s, k
        except ZeroDivisionError:
            pass


def verify(msg, r, s, p, q, g, y):
    if not validate_params(p, q, g):
        raise Exception('Invalid params')
    if not validate_sign(r, s, q):
        return False
    try:
        w = invert(s, q)
    except ZeroDivisionError:
        return False
    m = int(sha256(msg).hexdigest(), 16)
    u1 = (m * w) % q
    u2 = (r * w) % q
    # v = ((g ** u1 * y ** u2) % p) % q
    v = (powmod(g, u1, p) * powmod(y, u2, p)) % p % q
    if v == r:
        return True
    return False


def private_key_finder(msg1, msg2, s1, s2, p, q, g, r, y, k):
    h1 = int(sha256(msg1).hexdigest(), 16)
    h2 = int(sha256(msg2).hexdigest(), 16)

    # s = (invert(k, q) * (m + x * r)) % q
    # umkehrung für x=:
    # s = (invert(k, q) * (m + x * r)) - unb*q
    # s + unb*q = invert(k, q) * (m + x*r)
    # (s + unb*q) / invert(k, q) = m + x*r
    # ((s + unb * q) / invert(k, q)) - m = x*r
    # (((s + unb * q) / invert(k, q)) - m) / r = x

    m = h1
    s = s1
    unb = 0
    while True:
        raw_s = s + unb*q
        x = ((raw_s / invert(k, q)) - m) / r
        try:
            s1t = (invert(k, q) * (h1 + x * r)) % q
            s2t = (invert(k, q) * (h2 + x * r)) % q
            if xmpz(s1t) == s1 & xmpz(s2t) == s2:
                return x
            unb += 1
            if unb > 1000000:
                return 0
        except ZeroDivisionError:
            pass

    #

    print(f'Privater Schlüssel: {x}')
    return x


if __name__ == '__main__':
    nn = 160
    key_length = 1024
    p, q, g = generate_params(key_length, nn)
    x, y = generate_keys(g, p, q)

    text = 'Hallo, Welt!'
    msg = str.encode(text, 'utf-8')
    r, s, k = sign(msg, p, q, g, x)
    b = False
    if verify(msg, r, s, p, q, g, y):
        print('All ok')
        b = True
    print(f'msg: {msg}, ', f'r: {r}, ', f's: {s}, ', f'p: {p}, ', f'q: {q}, ', f'g: {g}, ', f'y: {y}, ', f'x: {x}', sep='\n')

    if b:
        text1 = text
        msg1, r1, s1, p1, q1, g1, y1, x1, k1 = msg, r, s, p, q, g, y, x, k
    else:
        print('Fehlerhafte Parameter')
        input('Trotzdem fortfahren?: ')
        text1 = text
        msg1, r1, s1, p1, q1, g1, y1, x1, k1 = msg, r, s, p, q, g, y, x, k

    #
    # next Text

    text = 'Hallo, Menschen!'
    msg = str.encode(text, 'utf-8')
    r, s, k = sign_with_k(msg, p, q, g, x, k)
    b = False
    if verify(msg, r, s, p, q, g, y):
        print('All ok')
        b = True
    print(f'msg: {msg}, ', f'r: {r}, ', f's: {s}, ', f'p: {p}, ', f'q: {q}, ', f'g: {g}, ', f'y: {y}, ', f'x: {x}', sep='\n')

    if b:
        text2 = text
        msg2, r2, s2, p2, q2, g2, y2, x2, k2 = msg, r, s, p, q, g, y, x, k
    else:
        print('Fehlerhafte Parameter')
        input('Trotzdem fortfahren?: ')
        text2 = text
        msg2, r2, s2, p2, q2, g2, y2, x2, k2 = msg, r, s, p, q, g, y, x, k

    #
    # faelschung erzeugen

    pk = private_key_finder(msg1, msg2, s1, s2, p, q, g, r, y, k)
    print(f'Private Key: {pk}')
