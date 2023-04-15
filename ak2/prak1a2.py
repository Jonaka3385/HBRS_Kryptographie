from random import randrange
from hashlib import sha256
from gmpy2 import xmpz, to_binary, invert, powmod, is_prime


def generate_p_q(ll, nn):
    g = nn  # g >= 160
    n = (ll - 1) // g
    b = (ll - 1) % g
    while True:
        # generate q
        while True:
            # noinspection PyArgumentList
            s = xmpz(randrange(1, 2 ** g))
            a = sha256(to_binary(s)).hexdigest()
            zz = (s + 1) % (2 ** g)
            z = sha256(to_binary(zz)).hexdigest()
            u = int(a, 16) ^ int(z, 16)
            mask = 2 ** (nn - 1) + 1  # nn-1 und niedrigste Bit auf 1 setzen rest 0
            q = u | mask  # u OR mask
            if is_prime(q, 20):
                break
        # generate p
        i = 0  # counter
        j = 2  # offset
        while i < 4096:
            v = []
            for k in range(n + 1):
                arg = (s + j + k) % (2 ** g)
                zzv = sha256(to_binary(arg)).hexdigest()
                v.append(int(zzv, 16))
            w = 0
            for qq in range(0, n):
                w += v[qq] * 2 ** (160 * qq)
            w += (v[n] % 2 ** b) * 2 ** (160 * n)
            xx = w + 2 ** (ll - 1)
            c = xx % (2 * q)
            p = xx - c + 1  # p = x - (c-1)
            if p >= 2 ** (ll - 1):
                if is_prime(p, 10):
                    return p, q
            i += 1
            j += n + 1


def generate_g(p, q):
    while True:
        h = randrange(2, p - 1)
        exp = (p - 1) // q
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
        if powmod(g, q, p) == 1 and g > 1 and ((p - 1) % q) == 0:
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
            delta = (invert(k, q) * (m + x * r)) % q
            return r, delta, k
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
    v = (powmod(g, u1, p) * powmod(y, u2, p)) % p % q
    if v == r:
        return True
    return False


def private_key_finder(msg1, msg2, delta1, delta2, q, gamma):
    h1 = int(sha256(msg1).hexdigest(), 16)
    h2 = int(sha256(msg2).hexdigest(), 16)

    delta1_inv = pow(delta1, -1, q)
    delta2_inv = pow(delta2, -1, q)
    x_calc = ((h1 * delta1_inv - h2 * delta2_inv) * pow(gamma, -1, q) * pow((delta2_inv - delta1_inv), -1, q)) % q

    print(f'Privater Schlüssel: {x_calc}')
    return


if __name__ == '__main__':
    nn = 256
    ll = 3072
    p, q, alpha = generate_params(ll, nn)
    x, y = generate_keys(alpha, p, q)

    text = 'Hallo, Welt!'
    msg = str.encode(text, 'utf-8')
    r, delta, k = sign(msg, p, q, alpha, x)
    b = False
    if verify(msg, r, delta, p, q, alpha, y):
        print('All ok')
        b = True
    print(f'msg: {msg}, ', f'r: {r}, ', f'delta: {delta}, ', f'p: {p}, ', f'q: {q}, ', f'g: {alpha}, ', f'y: {y}, ',
          f'x: {x}',
          sep='\n')

    if b:
        text1 = text
        msg1, r1, delta1 = msg, r, delta
    else:
        print('Fehlerhafte Parameter')
        input('Trotzdem fortfahren?: ')
        text1 = text
        msg1, r1, delta1 = msg, r, delta

    #
    # next Text

    text = 'Hallo, Menschen!'
    msg = str.encode(text, 'utf-8')
    r, delta, k = sign_with_k(msg, p, q, alpha, x, k)
    b = False
    if verify(msg, r, delta, p, q, alpha, y):
        print('All ok')
        b = True
    print(f'msg: {msg}, ', f'r: {r}, ', f's: {delta}, ', f'p: {p}, ', f'q: {q}, ', f'g: {alpha}, ', f'y: {y}, ',
          f'x: {x}',
          sep='\n')

    if b:
        text2 = text
        msg2, r2, delta2 = msg, r, delta
    else:
        print('Fehlerhafte Parameter')
        input('Trotzdem fortfahren?: ')
        text2 = text
        msg2, r2, delta2 = msg, r, delta

    #
    # faelschung erzeugen

    private_key_finder(msg1, msg2, delta1, delta2, q, r)

# g = alpha
# y = beta
# x = a
# p = p
# q = q
# public key = p,q,g,y
# private key = x
# r = gamma
# s = delta
