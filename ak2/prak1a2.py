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

    return r, s


def veri(msg, p, q, g, y, r, s):
    hash_obj = SHA256.new(msg)
    h = int.from_bytes(hash_obj.digest(), byteorder='big')

    # Signatur-Verifikation
    w = pow(s, -1, q)
    u1 = (h * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q

    if v == r:
        print("Signatur ist gültig!")
    else:
        print("Signatur ist ungültig!")


def start():
    message = "Hallo, Welt!"
    message_bytes = message.encode('utf-8')

    p, q, g, x, y = get_pars()
    r, s = sign(message_bytes, p, q, g, x)
    print(f'r: {r}\ns: {s}')

    veri(message_bytes, p, q, g, y, r, s)
