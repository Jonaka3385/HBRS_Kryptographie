from itertools import product
import string


def same_length(a, length):
    if len(a) < length:
        # füge Leerzeichen am Ende hinzu, bis die gewünschte Länge erreicht ist
        copied_string = (a * (length // len(a) + 1))[:length]
    elif len(a) > length:
        # schneide den String ab, bis die gewünschte Länge erreicht ist
        copied_string = a[:length]
    else:
        # der String hat bereits die gewünschte Länge
        copied_string = a

    return copied_string  # Ausgabe: 'ABC    '


def is_ascii_bytes(bytes_array):
    try:
        bytes_array.decode('ascii')
        return True
    except UnicodeDecodeError:
        return False


def is_valid(testtext):
    for letter in testtext:
        if not is_valid_char(letter):
            return False
    return True


def is_valid_char(c):
    return c.isalpha() or c in string.punctuation


def generate_bytearrays(length):
    byte_values = [i for i in range(65, 91)]
    byte_combinations = itertools.product(byte_values, repeat=length)
    return [bytes(combination) for combination in byte_combinations]


def decrypt(cipher0, cipher1, cipher2):
    key_length = 7
    cipher_length = len(cipher0)
    while key_length < 10:
        print(f'Trying length: {key_length}')
        letters = string.ascii_uppercase
        # combinations_list = list(product(letters, repeat=key_length))
        for combination in product(letters, repeat=key_length):
            str_key = ''.join(combination)
            str_key = same_length(str_key, cipher_length)
            key = str_key.encode('ascii')
            p0 = bytearray(cipher_length)
            for r in range(cipher_length):
                p0[r] = cipher0[r] ^ key[r]
            if is_valid(p0.decode('ascii')):
                p1 = bytearray(cipher_length)
                for s in range(cipher_length):
                    p1[s] = cipher1[s] ^ key[s]
                if is_valid(p1.decode('ascii')):
                    p2 = bytearray(cipher_length)
                    for t in range(cipher_length):
                        p2[t] = cipher2[t] ^ key[t]
                    if is_valid(p2.decode('ascii')):
                        print(f"p0: {p0},\n"
                              f"p0 decoded: {p0.decode('ascii')},\n\n"
                              f"p1: {p1},\n"
                              f"p1 decoded: {p1.decode('ascii')},\n\n"
                              f"p2: {p2},\n"
                              f"p2 decoded: {p2.decode('ascii')},\n\n"
                              f"key: {key}\n\n\n")
        key_length += 1
    print("Keine Ahnung")


if __name__ == '__main__':
    c0 = 'RKYUXFRFGFCTSSNNAVDCO'
    c1 = 'GKAUKGUVLOPTSJONYXXYC'
    c2 = 'QKJGVAFPCWLJDFUGNQXYG'

    c0b = c0.encode('ascii')
    c1b = c1.encode('ascii')
    c2b = c2.encode('ascii')

    print(f'1. Cipher: {c0}')
    print(f'2. Cipher: {c1}')
    print(f'3. Cipher: {c2}')
    print('\n\n\n')

    decrypt(c0b, c1b, c2b)
