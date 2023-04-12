from Cryptodome.Util.number import getPrime
from Cryptodome.Util.number import getRandomRange
from Cryptodome.Hash import SHA256


def get_pars():
    # key_length = 3072 dauert viel zu lange
    key_length = 32

    q = getPrime(key_length // 2)
    while True:
        p = getPrime(key_length)
        if (p - 1) % q == 0:
            break
    while True:
        g = getRandomRange(2, p - 1)
        if pow(g, q, p) == 1 and pow(g, 2, p) != 1:
            break

    x = getRandomRange(1, q - 1)

    y = pow(g, x, p)

    print("p:", p)
    print("q:", q)
    print("g:", g)
    print("x:", x)
    print("y:", y)

    return p, q, g, x, y


def inverse(a, m):
    r, prev_r = m, a
    x, prev_x = 0, 1

    while r != 0:
        quotient = prev_r // r
        prev_r, r = r, prev_r - quotient * r
        prev_x, x = x, prev_x - quotient * x

    if prev_r != 1:
        raise ValueError("Inverse existiert nicht")

    return prev_x % m


def sign(message, p, q, g, x):
    hash_obj = SHA256.new(message)
    h = int.from_bytes(hash_obj.digest(), byteorder='big')

    k = getRandomRange(1, q - 1)

    r = pow(g, k, p) % q
    s = (inverse(k, q) * (h + x * r % q)) % q

    return r, s, k


def sign_with_k_r(message, q, x, k, r):
    hash_obj = SHA256.new(message)
    h = int.from_bytes(hash_obj.digest(), byteorder='big')

    s = (inverse(k, q) * (h + x * r % q)) % q

    return r, s, k


def veri(msg, p, q, g, y, r, s):
    hash_obj = SHA256.new(msg)
    h = int.from_bytes(hash_obj.digest(), byteorder='big')

    s = int(s)
    q = int(q)
    # Signatur-Verifikation
    w = pow(s, -1, q)
    u1 = (h * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q

    if v == r:
        print("Signatur ist gültig!")
        return True
    else:
        print("Signatur ist ungültig!")
        return False


def extended_euclidean_algorithm(a, b):
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def schluessel_berechnung(message_bytes1, message_bytes2, s1, s2, q):
    hash_obj = SHA256.new(message_bytes1)
    h1 = int.from_bytes(hash_obj.digest(), byteorder='big')
    hash_obj = SHA256.new(message_bytes2)
    h2 = int.from_bytes(hash_obj.digest(), byteorder='big')

    ds = s1 - s2
    dh = inverse(h1 - h2, q)
    kx = ds * inverse(dh, q) % q
    x = (s1 * kx - h1) * inverse(kx, q) % q

    print(f'Privater Schlüssel: {x}')
    return x


def start():
    message = "Hallo, Welt!"
    message_bytes = message.encode('utf-8')

    p, q, g, x, y = get_pars()
    r, s, k = sign(message_bytes, p, q, g, x)
    print(f'r: {r}\ns: {s}')

    if veri(message_bytes, p, q, g, y, r, s):
        message_bytes1 = message_bytes
        s1 = s
    else:
        print("Fail!")
        return

    message = "Hallo, Menschen!"
    message_bytes = message.encode('utf-8')

    r, s, k = sign_with_k_r(message_bytes, q, x, k, r)
    print(f'r: {r}\ns: {s}')

    if veri(message_bytes, p, q, g, y, r, s):
        message_bytes2 = message_bytes
        s2 = s
    else:
        print("Fail!")
        return
    print(f'\nk: {k}\n')

    pk = schluessel_berechnung(message_bytes1, message_bytes2, s1, s2, q)
    print(pk)
