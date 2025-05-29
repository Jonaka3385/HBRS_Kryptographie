from dataclasses import dataclass


"""
Affiner Punkt
"""
@dataclass
class PointXY:
    x: int
    y: int

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __neg__(self):
        return PointXY(self.x, -self.y)

    def __add__(self, other):
        if not isinstance(other, PointXY):
            raise Exception("Point must be of type PointXY")
        if self == xy_neutral:
            return other
        elif other == xy_neutral:
            return self
        elif self == other:
            return self.dbl()
        elif self == -other:
            return xy_neutral
        else:
            x1 = self.x
            x2 = other.x
            y1 = self.y
            y2 = other.y

            s = int(((y2 - y1) * mod_inv(x2 - x1, p)) % p)

            x3 = ((s ** 2) - x1 - x2) % p
            y3 = ((s * (x1 - x3)) - y1) % p

            return PointXY(x3, y3)

    def __mul__(self, k: int):
        q = xy_neutral
        kb = bin(k)
        # k = 2  ->  kb = '0b10'
        j = len(kb)
        for i in range(2, j, +1):
            q = q.dbl()
            if kb[i] == '1':
                q = q + self
        return q

    def dbl(self):
        if self == xy_neutral or self.y == 0:
            return xy_neutral
        else:
            x1 = self.x
            y1 = self.y

            s = int(((3 * (x1 ** 2) + a) * mod_inv(2 * y1, p)) % p)

            x3 = ((s**2) - (2 * x1)) % p
            y3 = ((s * (x1 - x3)) - y1) % p

            return PointXY(x3, y3)

    def to_xyz(self):
        return PointXYZ(self.x, self.y, 1)

    def __str__(self):
        return f'({self.x}, {self.y})'

"""
Projektiver Punkt
"""
@dataclass
class PointXYZ:
    x: int
    y: int
    z: int

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        else:
            return False

    def __neg__(self):
        return PointXYZ(self.x, -self.y, self.z)

    def __add__(self, other):
        if not isinstance(other, PointXYZ):
            raise Exception("Point must be of type PointXYZ")
        if self == xyz_neutral:
            return other
        elif other == xyz_neutral:
            return self
        elif self == other:
            return self.dbl()
        elif self == -other:
            return xyz_neutral
        else:
            x1 = self.x
            x2 = other.x
            y1 = self.y
            y2 = other.y
            z1 = self.z
            z2 = other.z

            b_a = (y2 * z1 - y1 * z2) % p
            b_b = (x2 * z1 - x1 * z2) % p
            b_c = (b_a ** 2 * z1 * z2 - b_b ** 3 - 2 * b_b ** 2 * x1 * z2) % p

            x3 = (b_b * b_c) % p
            y3 = (b_a * (b_b ** 2 * x1 * z2 - b_c) - b_b ** 3 * y1 * z2) % p
            z3 = (b_b ** 3 * z1 * z2) % p

            return PointXYZ(x3, y3, z3)

    def __mul__(self, k: int):
        q = xyz_neutral
        kb = bin(k)
        # k = 2  ->  kb = '0b10'
        j = len(kb)
        for i in range(2, j, +1):
            q = q.dbl()
            if kb[i] == '1':
                q = q + self
        return q

    def dbl(self):
        if self == xyz_neutral:
            return xyz_neutral
        else:
            x1 = self.x
            y1 = self.y
            z1 = self.z

            b_a = (a * z1 ** 2 + 3 * x1 ** 2) % p
            b_b = (y1 * z1) % p
            b_c = (x1 * y1 * b_b) % p
            b_d = (b_a ** 2 - 8 * b_c) % p

            x3 = (2 * b_b * b_d) % p
            y3 = (b_a * (4 * b_c - b_d) - 8 * y1 ** 2 * b_b ** 2) % p
            z3 = (8 * b_b ** 3) % p

            return PointXYZ(x3, y3, z3)

    def to_xy(self):
        if self.z == 0:
            return xy_neutral
        else:
            z_inv = mod_inv(self.z, p)
            new_x = int(self.x * z_inv)
            new_y = int(self.y * z_inv)
            return PointXY(new_x, new_y)

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

xyz_neutral = PointXYZ(0, 1, 0)
xy_neutral = PointXY(None, None)

p = 0
a = 0
b = 0

def on_short_weierstrass(point: PointXY):
    x1 = point.x
    y1 = point.y

    left = (y1**2) % p
    right = (x1**3 + a*x1 + b) % p

    return left == right

def on_homogenised_weierstrass(point: PointXYZ):
    x1 = point.x
    y1 = point.y
    z1 = point.z

    left = (y1**2 * z1) % p
    right = (x1**3 + a * x1 * z1**2 + b * z1**3) % p

    return left == right

def skalarmul(point: PointXY, k):
    point = point.to_xyz()
    q = xyz_neutral
    j = len(k)-1
    for i in range(j, -1, -1):
        q = q.dbl()
        if k[i] == '1':
            q = q + point
    return q.to_xy()

def mod_inv(k, mod):
    if k == 0:
        raise ZeroDivisionError('Division durch Null')
    return pow(k, -1, mod)


"""
main() Methode
"""
if __name__ == "__main__":
    # Y^2*Z = X^3 + a*X*Z^2 + b*Z^3
    # y^2 = x^3 + a*X + b
    p = int(0xA9FB57DBA1EEA9BC3E660A909D838D726E3BF623D52620282013481D1F6E5377)
    a = int(0x7D5A0975FC2C3057EEF67530417AFFE7FB8055C126DC5C6CE94A4B44F330B5D9)
    b = int(0x26DC5C6CE94A4B44F330B5D9BBD77CBF958416295CF7E1CE6BCCDC18FF8C07B6)

    point_p = PointXYZ(60306380415904663168568911239273826053144841234228559299517684417361346433053,
                 74653857005150983469598545140707432309023702960881435319026826228339031179596, 1)
    p_val = on_homogenised_weierstrass(point_p)
    p2 = point_p.dbl()
    p2_val = on_homogenised_weierstrass(p2)
    p3 = point_p * 9
    p3_val = on_homogenised_weierstrass(p3)
    pq = point_p + p2
    pq_val = on_homogenised_weierstrass(pq)
    print(f'point: {point_p}, valid: {p_val}', f'p2 {p2}, valid: {p2_val}', f'p3 {p3}, valid: {p3_val}',
          f'pq {pq}, valid: {pq_val}', f'', sep='\n')

    point_p = PointXY(60306380415904663168568911239273826053144841234228559299517684417361346433053,
                 74653857005150983469598545140707432309023702960881435319026826228339031179596)
    p_val = on_short_weierstrass(point_p)
    p2 = point_p.dbl()
    p2_val = on_short_weierstrass(p2)
    p3 = point_p * 9
    p3_val = on_short_weierstrass(p3)
    pq = point_p + p2
    pq_val = on_short_weierstrass(pq)
    print(f'point: {point_p}, valid: {p_val}', f'p2 {p2}, valid: {p2_val}', f'p3 {p3}, valid: {p3_val}',
          f'pq {pq}, valid: {pq_val}', f'', sep='\n')

    #DH
    Gf = PointXY(63243729749562333355292243550312970334778175571054726587095381623627144114786,
                 38218615093753523893122277964030810387585405539772602581557831887485717997975)
    x = 13
    y = 21
    xG = Gf * x
    yG = Gf * y
    y_xG = xG * y
    x_yG = yG * x
    print(f'Gf: {Gf}, {on_short_weierstrass(Gf)}',
          f'xG: {xG}, {on_short_weierstrass(xG)}', f'yG: {yG}, {on_short_weierstrass(yG)}',
          f'y_xG: {y_xG}, {on_short_weierstrass(y_xG)}', f'x_yG: {x_yG}, {on_short_weierstrass(x_yG)}',
          f'{y_xG == x_yG}', f'xyG == yxG: {y_xG == x_yG}', sep='\n')
