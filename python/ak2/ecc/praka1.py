from dataclasses import dataclass


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

            s = int(((y2 - y1) / (x2 - x1)) % gf)

            x3 = ((s ** 2) - x1 - x2) % gf
            y3 = ((s * (x1 - x3)) - y1) % gf

            return PointXY(x3, y3)

    def dbl(self):
        if self == xy_neutral:
            return xy_neutral
        else:
            x = self.x
            y = self.y

            s = int(((3 * (x ** 2) + a) / (2 * y)) % gf)

            x3 = ((s ** 2) - (2 * x)) % gf
            y3 = ((s * (x - x3)) - y) % gf

            return PointXY(x3, y3)

    def to_xyz(self):
        return PointXYZ(self.x, self.y, 1)

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

            b_a = (y2 * z1 - y1 * z2) % gf
            b_b = (x2 * z1 - x1 * z2) % gf
            b_c = (b_a ** 2 * z1 * z2 - b_b ** 3 - 2 * b_b ** 2 * x1 * z2) % gf

            x3 = (b_b * b_c) % gf
            y3 = (b_a * (b_b ** 2 * x1 * z2 - b_c) - b_b ** 3 * y1 * z2) % gf
            z3 = (b_b ** 3 * z1 * z2) % gf

            return PointXYZ(x3, y3, z3)

    def dbl(self):
        if self == xyz_neutral:
            return xyz_neutral
        else:
            x = self.x
            y = self.y
            z = self.z

            b_a = (a * z ** 2 + 3 * x ** 2) % gf
            b_b = (y * z) % gf
            b_c = (x * y * b_b) % gf
            b_d = (b_a ** 2 - 8 * b_c) % gf

            x3 = (2 * b_b * b_d) % gf
            y3 = (b_a * (4 * b_c - b_d) - 8 * y ** 2 * b_b ** 2) % gf
            z3 = (8 * b ** 3) % gf

            return PointXYZ(x3, y3, z3)

    def to_xy(self):
        if self.z == 0:
            return xy_neutral
        else:
            new_x = int(self.x / self.z)
            new_y = int(self.y / self.z)
            return PointXY(new_x, new_y)

xyz_neutral = PointXYZ(0, 1, 0)
xy_neutral = PointXY(None, None)

gf = 0
a = 0
b = 0

if __name__ == "__main__":
    # Y^2*Z = X^3 + a*X*Z^2 + b*Z^3
    # y^2 = x^3 + a*X + b
    gf = 31
    a = 16
    b = 7
    print('')
