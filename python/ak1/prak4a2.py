from prak4_aes import AESCipher


def lower_wo_blanks(raw):
    raw.lower()
    return raw.replace('\n', '').replace(' ', '')


if __name__ == '__main__':
    key_end = 'FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF'
    text = '00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff'
    text = lower_wo_blanks(text)
    print(f'key: {key}\n'
          f'text: {text}\n')

    # Später mit Schleife durchprobieren
    # Schleifen begin
    key_begin = 'AA AA '
    key = key_begin + key_end
    key = lower_wo_blanks(key)
    c = AESCipher(key)

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
    # Schleifen Ende
