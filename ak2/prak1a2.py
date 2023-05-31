from random import randrange
from hashlib import sha256
from gmpy2 import xmpz, to_binary, invert, powmod, is_prime


def generate_p_q(gen_pq_l, gen_pq_n):
    gen_pq_g = gen_pq_n  # g >= 160
    gen_pq_n2 = (gen_pq_l - 1) // gen_pq_g
    gen_pq_b = (gen_pq_l - 1) % gen_pq_g
    while True:
        # generate q
        while True:
            # noinspection PyArgumentList
            s = xmpz(randrange(1, 2 ** gen_pq_g))
            a = sha256(to_binary(s)).hexdigest()
            zz = (s + 1) % (2 ** gen_pq_g)
            z = sha256(to_binary(zz)).hexdigest()
            u = int(a, 16) ^ int(z, 16)
            mask = 2 ** (gen_pq_n - 1) + 1  # nn-1 und niedrigste Bit auf 1 setzen rest 0
            generated_q = u | mask  # u OR mask
            if is_prime(generated_q, 20):
                break
        # generate p
        i = 0  # counter
        j = 2  # offset
        while i < 4096:
            v = []
            for counter in range(gen_pq_n2 + 1):
                arg = (s + j + counter) % (2 ** gen_pq_g)
                zzv = sha256(to_binary(arg)).hexdigest()
                v.append(int(zzv, 16))
            w = 0
            for counter2 in range(0, gen_pq_n2):
                w += v[counter2] * 2 ** (160 * counter2)
            w += (v[gen_pq_n2] % 2 ** gen_pq_b) * 2 ** (160 * gen_pq_n2)
            xx = w + 2 ** (gen_pq_l - 1)
            c = xx % (2 * generated_q)
            generated_p = xx - c + 1  # p = x - (c-1)
            if generated_p >= 2 ** (gen_pq_l - 1):
                if is_prime(generated_p, 10):
                    return generated_p, generated_q
            i += 1
            j += gen_pq_n2 + 1


def generate_alpha(generatealpha_p, generatealpha_q):
    while True:
        generatealpha_h = randrange(2, generatealpha_p - 1)
        generatealpha_exp = (generatealpha_p - 1) // generatealpha_q
        generated_alpha = powmod(generatealpha_h, generatealpha_exp, generatealpha_p)
        if generated_alpha > 1:
            break
    return generated_alpha


def generate_params(generate_params_key_length, generate_params_n):
    generated_param_p, generated_param_q = generate_p_q(generate_params_key_length, generate_params_n)
    generated_param_alpha = generate_alpha(generated_param_p, generated_param_q)
    return generated_param_p, generated_param_q, generated_param_alpha


def generate_keys(generate_keys_g, generate_keys_p, generate_keys_q):
    generated_x = randrange(2, generate_keys_q)  # x < q
    generated_y = powmod(generate_keys_g, generated_x, generate_keys_p)
    return generated_x, generated_y


def validate_params(validate_params_p, validate_params_q, validate_params_alpha):
    if is_prime(validate_params_p) and is_prime(validate_params_q):
        if powmod(validate_params_alpha, validate_params_q, validate_params_p) == 1 and validate_params_alpha > 1 and \
                ((validate_params_p - 1) % validate_params_q) == 0:
            return True
    return False


def validate_sign(validatesign_gamma, validatesign_delta, validatesign_q):
    if 0 > validatesign_gamma > validatesign_q:
        return False
    if 0 > validatesign_delta > validatesign_q:
        return False
    return True


def sign(sign_msg, sign_p, sign_q, sign_alpha, sign_privkey):
    if not validate_params(sign_p, sign_q, sign_alpha):
        raise Exception('Invalid params')
    while True:
        sign_k = randrange(2, sign_q)  # k < q
        sign_gamma = powmod(sign_alpha, sign_k, sign_p) % sign_q
        sign_m = int(sha256(sign_msg).hexdigest(), 16)
        try:
            sign_delta = (invert(sign_k, sign_q) * (sign_m + sign_privkey * sign_gamma)) % sign_q
            return sign_gamma, sign_delta, sign_k
        except ZeroDivisionError:
            pass


def sign_with_k(signwk_msg, signwk_p, signwk_q, signwk_alpha, signwk_a, signwk_k):
    if not validate_params(signwk_p, signwk_q, signwk_alpha):
        raise Exception('Invalid params')
    while True:
        signwk_r = powmod(signwk_alpha, signwk_k, signwk_p) % signwk_q
        signwk_m = int(sha256(signwk_msg).hexdigest(), 16)
        try:
            signwk_delta = (invert(signwk_k, signwk_q) * (signwk_m + signwk_a * signwk_r)) % signwk_q
            return signwk_r, signwk_delta, signwk_k
        except ZeroDivisionError:
            pass


def verify(verify_msg, verify_gamma, verify_delta, verify_p, verify_q, verify_alpha, verify_beta):
    if not validate_params(verify_p, verify_q, verify_alpha):
        raise Exception('Invalid params')
    if not validate_sign(verify_gamma, verify_delta, verify_q):
        return False
    try:
        w = invert(verify_delta, verify_q)
    except ZeroDivisionError:
        return False
    m = int(sha256(verify_msg).hexdigest(), 16)
    u1 = (m * w) % verify_q
    u2 = (verify_gamma * w) % verify_q
    v = (powmod(verify_alpha, u1, verify_p) * powmod(verify_beta, u2, verify_p)) % verify_p % verify_q
    if v == verify_gamma:
        return True
    return False


def private_key_finder(pkf_msg1, pkf_msg2, pkf_delta1, pkf_delta2, pkf_q, pkf_gamma):
    pkf_h1 = int(sha256(pkf_msg1).hexdigest(), 16)
    pkf_h2 = int(sha256(pkf_msg2).hexdigest(), 16)

    pkf_delta1_inv = pow(pkf_delta1, -1, pkf_q)
    pkf_delta2_inv = pow(pkf_delta2, -1, pkf_q)
    x_calc = ((pkf_h1 * pkf_delta1_inv - pkf_h2 * pkf_delta2_inv) * pow(pkf_gamma, -1, pkf_q)
              * pow((pkf_delta2_inv - pkf_delta1_inv), -1, pkf_q)) % pkf_q

    print(f'Privater Schlüssel: {x_calc}')
    return


if __name__ == '__main__':
    key_n = 256
    key_length = 3072
    p, q, alpha = generate_params(key_length, key_n)
    priv_key, beta = generate_keys(alpha, p, q)

    text = 'Hallo, Welt!'
    msg = str.encode(text, 'utf-8')
    gamma, delta, k = sign(msg, p, q, alpha, priv_key)
    b = False
    if verify(msg, gamma, delta, p, q, alpha, beta):
        print(f'All ok')
        b = True
    print(f'msg: {msg}', f'gamma: {gamma}', f'delta: {delta}', f'p: {p}', f'q: {q}', f'g: {alpha}', f'beta: {beta}',
          f'priv_key: {priv_key}', sep='\n')

    if b:
        text1 = text
        msg1, gamma1, delta1 = msg, gamma, delta
    else:
        print(f'Fehlerhafte Parameter')
        input(f'Trotzdem fortfahren?: ')
        text1 = text
        msg1, gamma1, delta1 = msg, gamma, delta

    #
    # next Text

    text = 'Hallo, Menschen!'
    msg = str.encode(text, 'utf-8')
    gamma, delta, k = sign_with_k(msg, p, q, alpha, priv_key, k)
    b = False
    if verify(msg, gamma, delta, p, q, alpha, beta):
        print(f'All ok')
        b = True
    print(f'msg: {msg}', f'gamma: {gamma}', f'delta: {delta}', f'p: {p}', f'q: {q}', f'g: {alpha}', f'beta: {beta}',
          f'priv_key: {priv_key}', sep='\n')

    if b:
        text2 = text
        msg2, gamma2, delta2 = msg, gamma, delta
    else:
        print(f'Fehlerhafte Parameter')
        input(f'Trotzdem fortfahren?: ')
        text2 = text
        msg2, gamma2, delta2 = msg, gamma, delta

    #
    # faelschung erzeugen
    private_key_finder(msg1, msg2, delta1, delta2, q, gamma)

# g = alpha
# y = beta
# x = a
# p = p
# q = q
# public key = p,q,g,y
# private key = x
# r = gamma
# s = delta
