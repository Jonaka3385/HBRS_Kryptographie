def mod_inv(k, mod):
    if k == 0:
        raise ZeroDivisionError('Division durch Null')
    return pow(k, -1, mod)
