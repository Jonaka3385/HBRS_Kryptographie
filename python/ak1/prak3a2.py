def is_ascii_bytes(bytes_array):
    try:
        bytes_array.decode('ascii')
        return True
    except UnicodeDecodeError:
        return False


def next_key(nextkey, lb=65, ub=90):
    # nextkey = bytearray(nextkey)
    laenge = len(nextkey)
    nextkey[0] += 1
    for i in range(laenge):
        my_byte = nextkey[i]
        if my_byte > ub and i < (laenge - 1):
            nextkey[i + 1] += 1
            nextkey[i] = lb
        if my_byte > ub and i == (laenge - 1):
            nextkey[i] = lb
            nextkey.append(lb)
    return nextkey


def brute_force_decrypt(brute_ciphertext, brute_key=b'A'):
    counter = 0
    brute_key = bytearray(brute_key)
    while True:
        print(f'Key: {brute_key}, Versuch: {counter}')
        brute_plaintext = crypt(brute_ciphertext, brute_key)
        brute_plainarray = bytearray(brute_plaintext)
        if is_ascii_bytes(brute_plainarray):
            return brute_plainarray, brute_key, counter
        else:
            counter += 1
            next_key(brute_key)


def crypt(crypt_cipher, crypt_key):
    S = list(range(256))
    j = 0
    out = bytearray()

    # KSA Phase
    for i in range(256):
        j = (j + S[i] + crypt_key[i % len(crypt_key)]) % 256
        S[i], S[j] = S[j], S[i]

    # PRGA Phase
    i = j = 0
    for char in crypt_cipher:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(char ^ S[(S[i] + S[j]) % 256])

    return bytes(out)


if __name__ == "__main__":
    path = '/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak1/prak3Files/encryptedbin.sec'
    with open(path, 'rb') as f:
        ciphertext = bytes(f.read())

    key = b'MySecretKey'
    key_array = bytearray(key)
    ciphertext_array = bytearray(ciphertext)
    decrypted = crypt(ciphertext_array, key_array)
    decrypted_array = bytearray(decrypted)
    encrypted = crypt(decrypted_array, key_array)

    plaintext, b_key, cc = brute_force_decrypt(ciphertext_array)
    print(f'Text: {plaintext}, Key: {b_key}, Versuch: {cc}')

    print('Original data:', ciphertext)
    print('Decrypted data:', decrypted)
    print('Encrypted data:', encrypted)
