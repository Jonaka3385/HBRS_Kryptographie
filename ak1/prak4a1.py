from prak4_aes import AESCipher


def lower_wo_blanks(raw):
    raw.lower()
    return raw.replace('\n', '').replace(' ', '')


if __name__ == '__main__':
    key = '00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f'
    text = '00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff'
    key = lower_wo_blanks(key)
    text = lower_wo_blanks(text)
    print(f'key: {key}\n'
          f'text: {text}\n')
    c = AESCipher(key)

    print('CBC: ')
    enc = c.encrypt_cbc(text)
    dec = c.decrypt_cbc(enc)
    print(f'encrypted: {enc.decode("utf-8")}')
    print(f'encrypted hex: {enc.hex()}')
    print(f'decrypted: {dec}')
    print(f'decrypted equals original text: {dec == text}')
    print()

    print('ECB: ')
    enc = c.encrypt_ecb(text)
    dec = c.decrypt_ecb(enc)
    print(f'encrypted: {enc.decode("utf-8")}')
    print(f'encrypted hex: {enc.hex()}')
    print(f'decrypted: {dec}')
    print(f'decrypted equals original text: {dec == text}')
    print()

    print('CTR: ')
    count = 0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    print(f'counter: {str(count).encode("utf-8")}')
    counter = count.to_bytes(len(count), "big")
    enc = c.encrypt_ctr(text, counter)
    counter = count.to_bytes(len(count), "big")
    dec = c.decrypt_ctr(enc, counter)
    print(f'encrypted: {enc.decode("utf-8")}')
    print(f'encrypted hex: {enc.hex()}')
    print(f'decrypted: {dec}')
    print(f'decrypted equals original text: {dec == text}')
    print()

    print()
    print()
    print()
