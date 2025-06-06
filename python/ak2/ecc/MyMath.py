def mod_inv(k, mod):
    if k == 0:
        return 0 % mod
    return pow(k, -1, mod)
