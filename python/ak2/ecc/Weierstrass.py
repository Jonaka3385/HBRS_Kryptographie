#from ak2.ecc.Points import PointXY, PointXYZ


class WeierstrassCurve:
    a: int
    b: int
    p: int

    def __init__(self, a: int, b: int, p: int):
        self.a = a
        self.b = b
        self.p = p

    """
    def on(self, point):
        if isinstance(point, PointXY):
            return self.__on_short(point)
        elif isinstance(point, PointXYZ):
            return self.__on_homogenised(point)
        else:
            raise Exception("Point must be of type PointXY or PointXYZ")
    """

    def on_short(self, point):
        x1 = point.x
        y1 = point.y
        a = self.a
        b = self.b
        p = self.p

        left = (y1 ** 2) % p
        right = (x1 ** 3 + a * x1 + b) % p

        return left == right

    def on_homogenised(self, point):
        x1 = point.x
        y1 = point.y
        z1 = point.z
        a = self.a
        b = self.b
        p = self.p

        left = (y1 ** 2 * z1) % p
        right = (x1 ** 3 + a * x1 * z1 ** 2 + b * z1 ** 3) % p

        return left == right

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.p == other.p
