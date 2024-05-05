"""
Uebung2
"""
from dataclasses import dataclass
from gmpy2 import mpz

gf = 0


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
    if isinstance(point, PointXY):
        # y^2 = x^3 + 16x + 7 mod GF(31)
        sum1 = (point.y ** 2) % gf
        sum2 = ((point.x ** 3) + (16 * point.x) + 7) % gf
    elif isinstance(point, PointXYZ):
        # y^2*z = x^3 + 16x*z^2 + 7*z^3 mod GF(31)
        sum1 = ((point.y ** 2) * point.z) % gf
        sum2 = ((point.x ** 3) + ((16 * point.x) * (point.z ** 2)) + (7 * (point.z ** 3))) % gf
    else:
        return False
    return sum1 == sum2


def is_congruent(point1, point2):
    """
    :param point1:
    :param point2:
    :return: is congruent
    """
    if isinstance(point1, PointXY):
        x1 = point1.x % gf
        y1 = point1.y % gf
    elif isinstance(point1, PointXYZ):
        x1 = point1.x / point1.z % gf
        y1 = point1.y / point1.z % gf
    else:
        return False
    if isinstance(point2, PointXY):
        x2 = point2.x % gf
        y2 = point2.y % gf
    elif isinstance(point2, PointXYZ):
        x2 = point2.x / point2.z % gf
        y2 = point2.y / point2.z % gf
    else:
        return False
    return x1 == x2 and y1 == y2


if __name__ == '__main__':
    gf = 31

    # 2.1
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
    print(s_a, s_b, s_c, s_d, s_e, s_f, s_g, s_h, '', sep='\n')
    a_c_con = is_congruent(a, c)
    a_h_con = is_congruent(c, h)
    b_f_con = is_congruent(b, f)
    print('congruent:', f'a zu c: {a_c_con}', f'a zu h: {a_h_con}', f'b zu f: {b_f_con}', sep='\n')

    # 2.2
