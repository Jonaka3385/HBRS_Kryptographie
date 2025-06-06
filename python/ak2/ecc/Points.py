from ak2.ecc.Weierstrass import WeierstrassCurve
from ak2.ecc.MyMath import mod_inv


"""
Affiner Punkt
"""
class PointXY:
    x: int
    y: int
    neutral = False
    curve: WeierstrassCurve

    def __init__(self, x: int, y: int, curve: WeierstrassCurve):
        self.x = x
        self.y = y
        self.curve = curve

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __neg__(self):
        return PointXY(self.x, -self.y, self.curve)

    def __add__(self, other):
        if not isinstance(other, PointXY):
            raise Exception("Point must be of type PointXY")
        elif self.neutral:
            return other
        elif other.neutral:
            return self
        elif not isinstance(other.curve, WeierstrassCurve):
            raise NotImplementedError
        elif not self.curve == other.curve:
            raise Exception('Different curve parameters')
        elif self == other:
            return self.dbl()
        elif self == -other:
            return xy_neutral
        else:
            p = self.curve.p
            x1, y1 = self.x, self.y
            x2, y2 = other.x, other.y

            s = ((y2 - y1) * mod_inv((x2 - x1) % p, p)) % p

            x3 = ((s ** 2) - x1 - x2) % p
            y3 = ((s * (x1 - x3)) - y1) % p

            return PointXY(x3, y3, self.curve)

    def __mul__(self, k: int):
        q = xy_neutral
        # while k < 0 + p ??? oder n ???
        kb = bin(k)
        # k = 2  ->  kb = '0b10'
        j = len(kb)
        for i in range(2, j, +1):
            q = q.dbl()
            if kb[i] == '1':
                q = q + self
        return q

    def __str__(self):
        return f'({self.x}, {self.y})'

    def dbl(self):
        if self.neutral:
            return xy_neutral
        else:
            a = self.curve.a
            p = self.curve.p
            x1, y1 = self.x, self.y

            s = ((3 * (x1 ** 2) + a) * mod_inv((2 * y1) % p, p)) % p

            x3 = ((s ** 2) - (2 * x1)) % p
            y3 = ((s * (x1 - x3)) - y1) % p

            return PointXY(x3, y3, self.curve)

    def to_xyz(self):
        if self.neutral:
            return xyz_neutral
        return PointXYZ(self.x, self.y, 1, self.curve)

    def on_curve(self):
        return self.curve.on_short(self)

"""
Projektiver Punkt
"""
class PointXYZ:
    x: int
    y: int
    z: int
    curve: WeierstrassCurve

    def __init__(self, x: int, y: int, z:int, curve: WeierstrassCurve):
        self.x = x
        self.y = y
        self.z = z
        self.curve = curve

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        else:
            return False

    def __neg__(self):
        return PointXYZ(self.x, -self.y, self.z, self.curve)

    def __add__(self, other):
        if not isinstance(other, PointXYZ):
            raise NotImplementedError
        elif self.is_neutral():
            return other
        elif other.is_neutral():
            return self
        elif not isinstance(other.curve, WeierstrassCurve):
            raise NotImplementedError
        elif not self.curve == other.curve:
            raise Exception('Different curve parameters')
        elif self == other:
            return self.dbl()
        elif self == -other:
            return xyz_neutral
        else:
            p = self.curve.p
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

            new_p = PointXYZ(x3, y3, z3, self.curve)
            if z1 == 1 and z2 == 1:
                new_p.normalise()
            return new_p

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

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def dbl(self):
        if self.is_neutral():
            return xyz_neutral
        else:
            a = self.curve.a
            p = self.curve.p
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

            new_p = PointXYZ(x3, y3, z3, self.curve)
            if z1 == 1:
                new_p.normalise()
            return new_p

    def to_xy(self):
        if self.z == 0:
            return xy_neutral
        else:
            z_inv = mod_inv(self.z, self.curve.p)
            new_x = self.x * z_inv
            new_y = self.y * z_inv
            return PointXY(new_x, new_y, self.curve)

    def normalise(self):
        tmp_point = self.to_xy()
        self.x = tmp_point.x
        self.y = tmp_point.y
        self.z = 1

    def is_neutral(self):
        return self.z == 0

    def on_curve(self):
        return self.curve.on_homogenised(self)

"""
Neutrale Punkte
"""
tmp = WeierstrassCurve(0, 0, 0)
xy_neutral = PointXY(0, 0, tmp)
xy_neutral.neutral = True
xyz_neutral = PointXYZ(0, 1, 0, tmp)

"""    
def skalarmul(self, point: PointXY, k):
    point = point.to_xyz()
    q = self.xyz_neutral
    j = len(k)-1
    for i in range(j, -1, -1):
        q = q.dbl()
        if k[i] == '1':
            q = q + point
    return q.to_xy()
"""
