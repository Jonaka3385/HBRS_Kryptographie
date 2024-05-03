"""
Uebung2
"""
from dataclasses import dataclass
from gmpy2 import mpz


@dataclass
class PointXYZ:
    """
    Point mit x, y, z
    """
    x: mpz
    y: mpz
    z: mpz


@dataclass
class PointXY:
    """
    Point mit x, y
    """
    x: mpz
    y: mpz


def on_courve(point):
    """
    :param point:
    :return: True, False
    """
    # E: y^2 = x^3 + 16x + 7  GF(31)
    if isinstance(point, PointXY):
        sum1 = (point.y ** 2) % 31
        sum2 = ((point.x ** 3) + (16 * point.x) + 7) % 31
    elif isinstance(point, PointXYZ):
        sum1 = ((point.y ** 2) * point.z) % 31
        sum2 = ((point.x ** 3) + ((16 * point.x) * (point.z ** 2)) + (7 * (point.z ** 3))) % 31
    else:
        return False
    return sum1 == sum2


if __name__ == '__main__':
    a = PointXY(mpz(28), mpz(26))
    b = PointXY(mpz(28), mpz(5))
    c = PointXY(mpz(121), mpz(-5))
    d = PointXY(mpz(0), mpz(0))
    e = PointXYZ(mpz(0), mpz(1), mpz(0))
    f = PointXYZ(mpz(28), mpz(5), mpz(1))
    g = PointXY(mpz(0), mpz(10))
    h = PointXYZ(mpz(56), mpz(52), mpz(2))
    s_a = on_courve(a)
    s_b = on_courve(b)
    s_c = on_courve(c)
    s_d = on_courve(d)
    s_e = on_courve(e)
    s_f = on_courve(f)
    s_g = on_courve(g)
    s_h = on_courve(h)
    print(s_a, s_b, s_c, s_d, s_e, s_f, s_g, s_h, sep='\n')
