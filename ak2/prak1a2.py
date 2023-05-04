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


def generate_g(generate_g_p, generate_g_q):
    while True:
        generate_g_h = randrange(2, generate_g_p - 1)
        generate_g_exp = (generate_g_p - 1) // generate_g_q
        generated_g = powmod(generate_g_h, generate_g_exp, generate_g_p)
        if generated_g > 1:
            break
    return generated_g


def generate_params(generate_params_key_length, generate_params_n):
    generated_param_p, generated_param_q = generate_p_q(generate_params_key_length, generate_params_n)
    generated_param_g = generate_g(generated_param_p, generated_param_q)
    return generated_param_p, generated_param_q, generated_param_g


def generate_keys(generate_keys_g, generate_keys_p, generate_keys_q):
    generated_x = randrange(2, generate_keys_q)  # x < q
    generated_y = powmod(generate_keys_g, generated_x, generate_keys_p)
    return generated_x, generated_y


def validate_params(validate_params_p, validate_params_q, validate_params_g):
    if is_prime(validate_params_p) and is_prime(validate_params_q):
        if powmod(validate_params_g, validate_params_q, validate_params_p) == 1 and validate_params_g > 1 and \
                ((validate_params_p - 1) % validate_params_q) == 0:
            return True
    return False


def validate_sign(validate_sign_r, validate_sign_r_s, validate_sign_q):
    if 0 > validate_sign_r > validate_sign_q:
        return False
    if 0 > validate_sign_r_s > validate_sign_q:
        return False
    return True


def sign(sign_msg, sign_p, sign_q, sign_g, sign_x):
    if not validate_params(sign_p, sign_q, sign_g):
        raise Exception('Invalid params')
    while True:
        sign_k = randrange(2, sign_q)  # k < q
        sign_r = powmod(sign_g, sign_k, sign_p) % sign_q
        sign_m = int(sha256(sign_msg).hexdigest(), 16)
        try:
            sign_s = (invert(sign_k, sign_q) * (sign_m + sign_x * sign_r)) % sign_q
            return sign_r, sign_s, sign_k
        except ZeroDivisionError:
            pass


def sign_with_k(sign_w_k_msg, sign_w_k_p, sign_w_k_q, sign_w_k_g, sign_w_k_x, sign_w_k_k):
    if not validate_params(sign_w_k_p, sign_w_k_q, sign_w_k_g):
        raise Exception('Invalid params')
    while True:
        sign_w_k_r = powmod(sign_w_k_g, sign_w_k_k, sign_w_k_p) % sign_w_k_q
        sign_w_k_m = int(sha256(sign_w_k_msg).hexdigest(), 16)
        try:
            sign_w_k_delta = (invert(sign_w_k_k, sign_w_k_q) * (sign_w_k_m + sign_w_k_x * sign_w_k_r)) % sign_w_k_q
            return sign_w_k_r, sign_w_k_delta, sign_w_k_k
        except ZeroDivisionError:
            pass


def verify(verify_msg, verify_r, verify_s, verify_p, verify_q, verify_g, verify_y):
    if not validate_params(verify_p, verify_q, verify_g):
        raise Exception('Invalid params')
    if not validate_sign(verify_r, verify_s, verify_q):
        return False
    try:
        w = invert(verify_s, verify_q)
    except ZeroDivisionError:
        return False
    m = int(sha256(verify_msg).hexdigest(), 16)
    u1 = (m * w) % verify_q
    u2 = (verify_r * w) % verify_q
    v = (powmod(verify_g, u1, verify_p) * powmod(verify_y, u2, verify_p)) % verify_p % verify_q
    if v == verify_r:
        return True
    return False


def private_key_finder(p_k_f_msg1, p_k_f_msg2, p_k_f_delta1, p_k_f_delta2, p_k_f_q, p_k_f_gamma):
    h1 = int(sha256(p_k_f_msg1).hexdigest(), 16)
    h2 = int(sha256(p_k_f_msg2).hexdigest(), 16)

    p_k_f_delta1_inv = pow(p_k_f_delta1, -1, p_k_f_q)
    p_k_f_delta2_inv = pow(p_k_f_delta2, -1, p_k_f_q)
    x_calc = ((h1 * p_k_f_delta1_inv - h2 * p_k_f_delta2_inv) * pow(p_k_f_gamma, -1, p_k_f_q)
              * pow((p_k_f_delta2_inv - p_k_f_delta1_inv), -1, p_k_f_q)) % p_k_f_q

    print(f'Privater Schlüssel: {x_calc}')
    return


if __name__ == '__main__':
    key_n = 256
    key_length = 3072
    p, q, alpha = generate_params(key_length, key_n)
    x, y = generate_keys(alpha, p, q)

    text = 'Hallo, Welt!'
    msg = str.encode(text, 'utf-8')
    r, delta, k = sign(msg, p, q, alpha, x)
    b = False
    if verify(msg, r, delta, p, q, alpha, y):
        print('All ok')
        b = True
    print(f'msg: {msg}, ', f'r: {r}, ', f'delta: {delta}, ', f'p: {p}, ', f'q: {q}, ', f'g: {alpha}, ', f'y: {y}, ',
          f'x: {x}',
          sep='\n')

    if b:
        text1 = text
        msg1, r1, delta1 = msg, r, delta
    else:
        print('Fehlerhafte Parameter')
        input('Trotzdem fortfahren?: ')
        text1 = text
        msg1, r1, delta1 = msg, r, delta

    #
    # next Text

    text = 'Hallo, Menschen!'
    msg = str.encode(text, 'utf-8')
    r, delta, k = sign_with_k(msg, p, q, alpha, x, k)
    b = False
    if verify(msg, r, delta, p, q, alpha, y):
        print('All ok')
        b = True
    print(f'msg: {msg}, ', f'r: {r}, ', f's: {delta}, ', f'p: {p}, ', f'q: {q}, ', f'g: {alpha}, ', f'y: {y}, ',
          f'x: {x}',
          sep='\n')

    if b:
        text2 = text
        msg2, r2, delta2 = msg, r, delta
    else:
        print('Fehlerhafte Parameter')
        input('Trotzdem fortfahren?: ')
        text2 = text
        msg2, r2, delta2 = msg, r, delta

    #
    # faelschung erzeugen

    private_key_finder(msg1, msg2, delta1, delta2, q, r)

# g = alpha
# y = beta
# x = a
# p = p
# q = q
# public key = p,q,g,y
# private key = x
# r = gamma
# s = delta
