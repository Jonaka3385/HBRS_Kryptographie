import random

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def generate_key(gk_bit_size, gk_public_exponent):
    gk_private_key = rsa.generate_private_key(
        public_exponent=gk_public_exponent,
        key_size=gk_bit_size,
        backend=default_backend()
    )

    # privater Schlüssel PEM-kodiert als String
    gk_private_key_pem = gk_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    # öffentlicher Schlüssel PEM-kodiert als String
    gk_public_key_pem = gk_private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    gk_path_priv = '/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak2/prak1Files/priv_key.pem'
    gk_path_pub = '/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak2/prak1Files/pub_key.pem'
    # privaten Schlüssel als PEM-Datei schreiben
    with open(gk_path_priv, 'wb') as gk_f:
        gk_f.write(gk_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # öffentlichen Schlüssel als PEM-Datei schreiben
    with open(gk_path_pub, 'wb') as gk_f:
        gk_f.write(gk_private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    return gk_private_key_pem, gk_public_key_pem


def generate_key_only(gko_bit_size, gko_public_exponent):
    return rsa.generate_private_key(
        public_exponent=gko_public_exponent,
        key_size=gko_bit_size,
        backend=default_backend()
    )


def key_to_pem_string(ktps_key):
    # privater Schlüssel PEM-kodiert als String
    ktps_private_key_pem = ktps_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    # öffentlicher Schlüssel PEM-kodiert als String
    ktps_public_key_pem = ktps_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    return ktps_private_key_pem, ktps_public_key_pem


def key_to_file(ktf_key, ktf_path_priv, ktf_path_pub):
    # privaten Schlüssel als PEM-Datei schreiben
    with open(ktf_path_priv, 'wb') as ktf_f:
        ktf_f.write(ktf_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # öffentlichen Schlüssel als PEM-Datei schreiben
    with open(ktf_path_pub, 'wb') as ktf_f:
        ktf_f.write(ktf_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))


def fast_modular_exponentation(fme_a, fme_b, fme_n):
    fme_result = 1
    while fme_b > 0:
        if fme_b % 2:
            fme_result = (fme_result * fme_a) % fme_n
        fme_a = (fme_a * fme_a) % fme_n
        fme_b //= 2
    return fme_result


def signatur(signatur_message, signatur_n, signatur_d):
    return fast_modular_exponentation(signatur_message, signatur_d, signatur_n)


def verifikation(verifikation_signature, verifikation_n, verifikation_d):
    return fast_modular_exponentation(verifikation_signature, verifikation_d, verifikation_n)


def universelle_faelschung(uf_message, uf_n, uf_e, uf_d):
    uf_r = random.getrandbits(3000)
    uf_s_strich = uf_r * fast_modular_exponentation(uf_message, uf_d, uf_n)
    uf_s = pow(uf_r, -1, uf_n) * uf_s_strich % uf_n
    uf_m = fast_modular_exponentation(uf_s, uf_e, uf_n)
    return uf_m


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
    message_bytes = message.encode('utf-8')
    byte_menge = len(message_bytes)
    int_num = int.from_bytes(message_bytes, byteorder='big')

    signature = signatur(int_num, n, d)
    verifikationn = verifikation(signature, n, d)
    faelschung = universelle_faelschung(int_num, n, e, d)
    print(f'Signature: \n{signature}', f'Verifikation: \n{verifikationn}', f'Faelschung: \n{faelschung}', '',
          f'Original unveraendert: {message}',
          f'Original encoded, decoded: {int_num.to_bytes(byte_menge, byteorder="big").decode("utf-8")}',
          f'Faelschung decoded: {faelschung.to_bytes(byte_menge, byteorder="big").decode("utf-8")}', sep='\n')
