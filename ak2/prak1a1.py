"""
Praktikum 1 Aufgabe 1
p_ = Übergebener Parameter
"""
import random

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def generate_key(p_bit_size, p_pub_exp):
    """
    :param p_bit_size:
    :param p_pub_exp:
    :return: private and public key (pem encoded)
    """
    priv_key = rsa.generate_private_key(
        public_exponent=p_pub_exp,
        key_size=p_bit_size,
        backend=default_backend()
    )

    # privater Schlüssel PEM-codiert als String
    priv_key_pem = priv_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    # öffentlicher Schlüssel PEM-kodiert als String
    pub_key_pem = priv_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    path_priv = '/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak2/prak1Files/priv_key.pem'
    path_pub = '/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak2/prak1Files/pub_key.pem'
    # privaten Schlüssel als PEM-Datei schreiben
    with open(path_priv, 'wb') as f:
        f.write(priv_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # öffentlichen Schlüssel als PEM-Datei schreiben
    with open(path_pub, 'wb') as f:
        f.write(priv_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    return priv_key_pem, pub_key_pem


def generate_key_only(p_bit_size, p_pub_exp):
    """
    :param p_bit_size:
    :param p_pub_exp:
    :return: rsa private key
    """
    return rsa.generate_private_key(
        public_exponent=p_pub_exp,
        key_size=p_bit_size,
        backend=default_backend()
    )


def key_to_pem_string(p_key):
    """
    :param p_key:
    :return: private and public key (pem encoded)
    """
    # privater Schlüssel PEM-kodiert als String
    priv_key_pem = p_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    # öffentlicher Schlüssel PEM-kodiert als String
    pub_key_pem = p_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    return priv_key_pem, pub_key_pem


def key_to_file(p_key, p_path_priv, p_path_pub):
    """
    :param p_key:
    :param p_path_priv:
    :param p_path_pub:
    """
    # privaten Schlüssel als PEM-Datei schreiben
    with open(p_path_priv, 'wb') as f:
        f.write(p_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # öffentlichen Schlüssel als PEM-Datei schreiben
    with open(p_path_pub, 'wb') as f:
        f.write(p_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))


def fast_modular_exponentation(p_a, p_b, p_n):
    """
    :param p_a:
    :param p_b:
    :param p_n:
    :return: Ergebnis der fast modular exponentation
    """
    result = 1
    while p_b > 0:
        if p_b % 2:
            result = (result * p_a) % p_n
        p_a = (p_a * p_a) % p_n
        p_b //= 2
    return result


def signatur(p_msg, p_n, p_d):
    """
    :param p_msg:
    :param p_n:
    :param p_d:
    :return: fme_result
    """
    return fast_modular_exponentation(p_msg, p_d, p_n)


def verifikation(p_signature, p_n, p_d):
    """
    :param p_signature:
    :param p_n:
    :param p_d:
    :return: fme_result
    """
    return fast_modular_exponentation(p_signature, p_d, p_n)


def universelle_faelschung(p_msg, p_n, p_e, p_d):
    """
    :param p_msg:
    :param p_n:
    :param p_e:
    :param p_d:
    :return: m
    """
    r = random.getrandbits(3000)
    s_strich = r * fast_modular_exponentation(p_msg, p_d, p_n)
    s = pow(r, -1, p_n) * s_strich % p_n
    m = fast_modular_exponentation(s, p_e, p_n)
    return m


if __name__ == '__main__':
    # path_priv = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak2/prak1Files/priv_key.pem"
    # path_pub = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak2/prak1Files/pub_key.pem"
    bit_size = 3000
    exp = 65537  # 2^16 + 1
    key = generate_key_only(bit_size, exp)
    priv_key, pub_key = key_to_pem_string(key)
    # key_to_file(key, path_priv, path_pub)
    print(f'Keys: ')
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
    print(n, e, d, sep='\n')
    print()

    message = 'Hallo, Welt!'
    message_bytes = message.encode()
    byte_menge = len(message_bytes)
    int_num = int.from_bytes(message_bytes, "big")

    signature = signatur(int_num, n, d)
    verifikation = verifikation(signature, n, d)
    faelschung = universelle_faelschung(int_num, n, e, d)
    print(f'Signature: \n{signature}', f'Verifikation: \n{verifikation}', f'Faelschung: \n{faelschung}', '',
          f'Original unveraendert: {message}',
          f'Original encoded, decoded: {int_num.to_bytes(byte_menge, "big").decode()}',
          f'Faelschung decoded: {faelschung.to_bytes(byte_menge, "big").decode()}', sep='\n')
