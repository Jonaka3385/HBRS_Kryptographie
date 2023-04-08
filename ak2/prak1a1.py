import random

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def schluessel_generierung(bit_size):
    priv_key = ''
    pub_key = ''
    # Algorithmus einfügen
    return priv_key, pub_key


def generate_key(bit_size, public_exponent):
    private_key = rsa.generate_private_key(
        public_exponent=public_exponent,
        key_size=bit_size,
        backend=default_backend()
    )

    # privater Schlüssel PEM-kodiert als String
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    # öffentlicher Schlüssel PEM-kodiert als String
    public_key_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    path_priv = '/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak2/prak1Files/priv_key.pem'
    path_pub = '/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak2/prak1Files/pub_key.pem'
    # privaten Schlüssel als PEM-Datei schreiben
    with open(path_priv, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # öffentlichen Schlüssel als PEM-Datei schreiben
    with open(path_pub, 'wb') as f:
        f.write(private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    return private_key_pem, public_key_pem


def generate_key_only(bit_size, public_exponent):
    private_key = rsa.generate_private_key(
        public_exponent=public_exponent,
        key_size=bit_size,
        backend=default_backend()
    )
    return private_key


def key_to_pem_string(key):
    # privater Schlüssel PEM-kodiert als String
    private_key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    # öffentlicher Schlüssel PEM-kodiert als String
    public_key_pem = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    return private_key_pem, public_key_pem


def key_to_file(key, path_priv, path_pub):
    # privaten Schlüssel als PEM-Datei schreiben
    with open(path_priv, 'wb') as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # öffentlichen Schlüssel als PEM-Datei schreiben
    with open(path_pub, 'wb') as f:
        f.write(key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))


def fast_modular_exponentation(a, b, n):
    result = 1
    while b > 0:
        if b % 2:
            result = (result * a) % n
        a = (a * a) % n
        b //= 2
    return result


def signatur(message, n, d):
    return fast_modular_exponentation(message, d, n)


def verifikation(signature, n, d):
    return fast_modular_exponentation(signature, d, n)


def universelle_faelschung(message, n, e, d):
    r = random.getrandbits(3000)
    s_strich = r * fast_modular_exponentation(message, d, n)
    s = pow(r, -1, n)*s_strich % n
    m = fast_modular_exponentation(s, e, n)
    return m


def start():
    # path_priv = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak2/prak1Files/priv_key.pem"
    # path_pub = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak2/prak1Files/pub_key.pem"
    bit_size = 3000
    exp = 65537  # 2^16 + 1
    key = generate_key_only(bit_size, exp)
    priv_key, pub_key = key_to_pem_string(key)
    # key_to_file(key, path_priv, path_pub)
    print('Key: ')
    print(priv_key)
    print()
    print(pub_key)
    print()
    print(f'Bitlänge: {bit_size}')
    print(f'Öffentlicher Exponent: {exp}')
    print()
    print()

    n = key.public_key().public_numbers().n
    e = key.public_key().public_numbers().e
    d = key.private_numbers().d
    print(f'{n}\n{e}\n{d}\n')

    message = "Hallo, Welt!"
    message = message.encode('utf-8').decode('utf-8')
    binary = ''.join(format(ord(c), '08b') for c in message)
    int_num = int(binary, 2)

    signature = signatur(int_num, n, d)
    print('Signature: \n', signature)
    verifikatione = verifikation(signature, n, d)
    print('Verifikation: \n', verifikatione)
    faelschung = universelle_faelschung(int_num, n, e, d)
    print('Faelschung: \n', faelschung)

    binary = bin(int_num)[2:]
    text = ''.join(chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8)).encode('utf-8').decode('utf-8')
    print('Text1: \n', text)
    binary = bin(faelschung)[2:]
    text = ''.join(chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8)).encode('utf-8').decode('utf-8')
    print('Text2: \n', text)
    print('Text1 Ergebnis aus Ursprung; Text2 aus Faelschung \nFormatierungsprobleme')
