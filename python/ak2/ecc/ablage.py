"""
def add(point1, point2):
    if isinstance(point1, PointXY) and isinstance(point2, PointXY):
        return xy_add(point1, point2)
    elif isinstance(point1, PointXYZ) and isinstance(point2, PointXYZ):
        return xyz_add(point1, point2)
    else:
        exception('not implemented')
        return None

def xy_add(point1: PointXY, point2: PointXY):
    if point1 == xy_neutral:
        return point2
    elif point2 == xy_neutral:
        return point1
    elif point1 == point2:
        return xy_dbl(point1)
    elif point1 == -point2:
        return xy_neutral
    else:
        x1 = point1.x
        x2 = point2.x
        y1 = point1.y
        y2 = point2.y

        s = int(((y2 - y1) / (x2 - x1)) % gf)

        x3 = ((s ** 2) - x1 - x2) % gf
        y3 = ((s * (x1 - x3)) - y1) % gf

        return PointXY(x3, y3)

def xyz_add(point1: PointXYZ, point2: PointXYZ):
    if point1 == xyz_neutral:
        return point2
    elif point2 == xyz_neutral:
        return point1
    elif point1 == point2:
        return xyz_dbl(point1)
    elif point1 == -point2:
        return xyz_neutral
    else:
        x1 = point1.x
        x2 = point2.x
        y1 = point1.y
        y2 = point2.y
        z1 = point1.z
        z2 = point2.z

        b_a = (y2 * z1 - y1 * z2) % gf
        b_b = (x2 * z1 - x1 * z2) % gf
        b_c = (b_a**2 * z1 * z2 - b_b**3 - 2 * b_b**2 * x1 * z2) % gf

        x3 = (b_b * b_c) % gf
        y3 = (b_a*(b_b**2 * x1 * z2 - b_c) - b_b**3 * y1 * z2) % gf
        z3 = (b_b**3 * z1 * z2) % gf

        return PointXYZ(x3, y3, z3)

def dbl(point):
    if isinstance(point, PointXY):
        return xy_dbl(point)
    elif isinstance(point, PointXYZ):
        return xyz_dbl(point)
    else:
        exception('not implemented')
        return None

def xy_dbl(point: PointXY):
    if point == xy_neutral:
        return xy_neutral
    else:
        x = point.x
        y = point.y

        s = int(((3 * (x ** 2) + a) / (2 * y)) % gf)

        x3 = ((s ** 2) - (2 * x)) % gf
        y3 = ((s * (x - x3)) - y) % gf

        return PointXY(x3, y3)

def xyz_dbl(point: PointXYZ):
    if point == xyz_neutral:
        return xyz_neutral
    else:
        x = point.x
        y = point.y
        z = point.z

        b_a = (a * z**2 + 3 * x**2) % gf
        b_b = (y * z) % gf
        b_c = (x * y * b_b) % gf
        b_d = (b_a**2 - 8 * b_c) % gf

        x3 = (2 * b_b * b_d) % gf
        y3 = (b_a * (4 * b_c - b_d) - 8 * y**2 * b_b**2) % gf
        z3 = (8 * b**3) % gf

        return PointXYZ(x3, y3, z3)
"""