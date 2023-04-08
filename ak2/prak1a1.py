from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


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

    path_priv = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak2/prak1Files/priv_key.pem"
    path_pub = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak2/prak1Files/pub_key.pem"
    # privaten Schlüssel als PEM-Datei schreiben
    with open(path_priv, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # öffentlichen Schlüssel als PEM-Datei schreiben
    with open(path_pub, "wb") as f:
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
    with open(path_priv, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # öffentlichen Schlüssel als PEM-Datei schreiben
    with open(path_pub, "wb") as f:
        f.write(key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))


def start():
    # path_priv = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak2/prak1Files/priv_key.pem"
    # path_pub = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak2/prak1Files/pub_key.pem"
    bit_size = 3000
    exp = 65537  # 2^16 + 1
    key = generate_key_only(bit_size, exp)
    priv_key, pub_key = key_to_pem_string(key)
    # key_to_file(key, path_priv, path_pub)
    print("Key: ")
    print(priv_key)
    print()
    print(pub_key)
    print()
    print(f"Bitlänge: {bit_size}")
    print(f"Öffentlicher Exponent: {exp}")
