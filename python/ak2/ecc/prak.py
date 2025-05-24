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

            s = int(((y2 - y1) / (x2 - x1)) % p)

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
        if self == xy_neutral:
            return xy_neutral
        else:
            x = self.x
            y = self.y

            s = int(((3 * (x ** 2) + a) / (2 * y)) % p)

            x3 = ((s ** 2) - (2 * x)) % p
            y3 = ((s * (x - x3)) - y) % p

            return PointXY(x3, y3)

    def to_xyz(self):
        return PointXYZ(self.x, self.y, 1)

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
            x = self.x
            y = self.y
            z = self.z

            b_a = (a * z ** 2 + 3 * x ** 2) % p
            b_b = (y * z) % p
            b_c = (x * y * b_b) % p
            b_d = (b_a ** 2 - 8 * b_c) % p

            x3 = (2 * b_b * b_d) % p
            y3 = (b_a * (4 * b_c - b_d) - 8 * y ** 2 * b_b ** 2) % p
            z3 = (8 * b ** 3) % p

            return PointXYZ(x3, y3, z3)

    def to_xy(self):
        if self.z == 0:
            return xy_neutral
        else:
            new_x = int(self.x / self.z)
            new_y = int(self.y / self.z)
            return PointXY(new_x, new_y)

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

xyz_neutral = PointXYZ(0, 1, 0)
xy_neutral = PointXY(None, None)

p = 0
a = 0
b = 0

def on_short_weierstrass(point: PointXY):
    x = point.x
    y = point.y

    left = (y**2) % p
    right = (x**3 + a*x + b) % p

    return left == right

def on_homogenised_weierstrass(point: PointXYZ):
    x = point.x
    y = point.y
    z = point.z

    left = (y**2 * z) % p
    right = (x**3 + a * x * z**2 + b * z**3) % p

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


"""
main() Methode
"""
if __name__ == "__main__":
    # Y^2*Z = X^3 + a*X*Z^2 + b*Z^3
    # y^2 = x^3 + a*X + b
    p = int(0xA9FB57DBA1EEA9BC3E660A909D838D726E3BF623D52620282013481D1F6E5377)
    a = int(0x7D5A0975FC2C3057EEF67530417AFFE7FB8055C126DC5C6CE94A4B44F330B5D9)
    b = int(0x26DC5C6CE94A4B44F330B5D9BBD77CBF958416295CF7E1CE6BCCDC18FF8C07B6)

    """
    point_p = PointXYZ(60306380415904663168568911239273826053144841234228559299517684417361346433053,
                 74653857005150983469598545140707432309023702960881435319026826228339031179596, 1)
    p_val = on_homogenised_weierstrass(point_p)
    p2 = point_p.dbl()
    p3 = point_p * 9
    pq = point_p + p2
    print(f'point: {point_p}, valid: {p_val}', f'p2 {p2}', f'p3 {p3}', f'pq {pq}', sep='\n')
    """

    """
    point_p = PointXY(60306380415904663168568911239273826053144841234228559299517684417361346433053,
                 74653857005150983469598545140707432309023702960881435319026826228339031179596)
    p_val = on_short_weierstrass(point_p)
    p2 = point_p.dbl()
    p3 = point_p * 9
    pq = point_p + p2
    print(f'point: {point_p}, valid: {p_val}', f'p2 {p2}', f'p3 {p3}', f'pq {pq}', sep='\n')
    """

    #DH
    Gf = PointXY(0, 0)
