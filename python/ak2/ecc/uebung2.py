"""
Uebung2
"""
from dataclasses import dataclass
from gmpy2 import mpz

gf = 0
a = 0
b = 0


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
        sum2 = ((point.x ** 3) + (a * point.x) + b) % gf
    elif isinstance(point, PointXYZ):
        # y^2*z = x^3 + 16x*z^2 + 7*z^3 mod GF(31)
        sum1 = ((point.y ** 2) * point.z) % gf
        sum2 = ((point.x ** 3) + ((a * point.x) * (point.z ** 2)) + (b * (point.z ** 3))) % gf
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


def point_add(point1, point2):
    if isinstance(point1, PointXY) and isinstance(point2, PointXY):
        x1 = point1.x
        y1 = point1.y
        x2 = point2.x
        y2 = point2.y
        if x1 == x2 or x1 == -x2:
            return point_double(point1)
        else:
            s = ((y2 - y1) / (x2 - x1)) % gf
            x3 = ((s ** 2) - x1 - x2) % gf
            y3 = ((s * (x1 - x3)) - y1) % gf
            point3 = PointXY(mpz(x3), mpz(y3))
            return point3
    else:
        raise Exception("Points must be of type PointXY")


def point_double(point1):
    if point1.x == 0:
        raise Exception("Points must be of type PointXY")
    else:
        x1 = point1.x
        y1 = point1.y
        s = ((3 * (x1 ** 2) + a) / (2 * y1)) % gf
        x3 = ((s ** 2) - (2 * x1)) % gf
        y3 = ((s * (x1 - x3)) - y1) % gf
        point3 = PointXY(mpz(x3), mpz(y3))
        return point3


if __name__ == '__main__':
    gf = 31
    a = 16
    b = 7

    # 2.1
    p_a = PointXY(mpz(28), mpz(26))
    p_b = PointXY(mpz(28), mpz(5))
    p_c = PointXY(mpz(121), mpz(-5))
    p_d = PointXY(mpz(0), mpz(0))
    p_e = PointXYZ(mpz(0), mpz(1), mpz(0))
    p_f = PointXYZ(mpz(28), mpz(5), mpz(1))
    p_g = PointXY(mpz(0), mpz(10))
    p_h = PointXYZ(mpz(56), mpz(52), mpz(2))
    s_a = on_courve(p_a)
    s_b = on_courve(p_b)
    s_c = on_courve(p_c)
    s_d = on_courve(p_d)
    s_e = on_courve(p_e)
    s_f = on_courve(p_f)
    s_g = on_courve(p_g)
    s_h = on_courve(p_h)
    print(s_a, s_b, s_c, s_d, s_e, s_f, s_g, s_h, '', sep='\n')
    a_c_con = is_congruent(p_a, p_c)
    a_h_con = is_congruent(p_c, p_h)
    b_f_con = is_congruent(p_b, p_f)
    print('congruent:', f'a zu c: {a_c_con}', f'a zu h: {a_h_con}', f'b zu f: {b_f_con}', sep='\n')

    # 2.2
