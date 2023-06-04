def rsa_encrypt(re_msg, re_e, re_n):
    re_cipher = pow(re_msg, re_e, re_n)
    return re_cipher


def rsa_decrypt(re_cipher, re_d, re_n):
    re_msg = pow(re_cipher, re_d, re_n)
    return re_msg


if __name__ == '__main__':
    e = 7
    n = 187
    d = 23
    msg = 10
    print(msg)
    cipher = rsa_encrypt(msg, e, n)
    print(cipher)
    new_msg = rsa_decrypt(cipher, d, n)
    print(new_msg)
