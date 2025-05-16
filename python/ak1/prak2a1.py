decoding = 'ascii'


def is_text_bytes(bytes_array):
    try:
        bytes_array.decode(decoding)
        return True
    except UnicodeDecodeError:
        return False


def decrypt():
    path = '/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak1/prak2Files/chiffratbin.sec'
    with open(path, 'rb') as f:
        ciphertext = bytearray(f.read())
    path = '/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak1/prak2Files/random.dat'
    with open(path, 'rb') as f:
        full_keystream = bytearray(f.read())

    N = len(ciphertext)

    for i in range(len(full_keystream) - N):
        partial_keystream = full_keystream[i:i + N]
        plaintext = bytearray(N)
        for j in range(N):
            plaintext[j] = ciphertext[j] ^ partial_keystream[j]
        if is_text_bytes(plaintext):
            print(f"Found potential keystream at index {i}")
            print(plaintext)
            print(plaintext.decode(decoding))


if __name__ == '__main__':
    decrypt()
