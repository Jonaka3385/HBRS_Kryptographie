from dataclasses import dataclass

"""
Elliptische Kurve - Brainpool P-256
Korrigierte Version des ursprünglichen Codes
"""

p = int(0xA9FB57DBA1EEA9BC3E660A909D838D726E3BF623D52620282013481D1F6E5377)
a = int(0x7D5A0975FC2C3057EEF67530417AFFE7FB8055C126DC5C6CE94A4B44F330B5D9)
b = int(0x26DC5C6CE94A4B44F330B5D9BBD77CBF958416295CF7E1CE6BCCDC18FF8C07B6)


def mod_inv(k, mod):
    if k == 0:
        raise ZeroDivisionError('Division durch Null')
    return pow(k, -1, mod)


"""
Affiner Punkt - KORRIGIERT
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
        return PointXY(self.x, (-self.y) % p)  # Modulo hinzugefügt

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
            x1, y1 = self.x, self.y
            x2, y2 = other.x, other.y

            s = ((y2 - y1) * mod_inv((x2 - x1) % p, p)) % p

            x3 = ((s ** 2) - x1 - x2) % p
            y3 = ((s * (x1 - x3)) - y1) % p

            return PointXY(x3, y3)

    def __mul__(self, k: int):
        # KORRIGIERTE Skalarmultiplikation
        if k == 0:
            return xy_neutral
        if k < 0:
            return (-self) * (-k)

        result = xy_neutral
        addend = self

        while k:
            if k & 1:
                result = result + addend
            addend = addend.dbl()
            k >>= 1

        return result

    def __str__(self):
        return f'({self.x}, {self.y})'

    def dbl(self):
        if self == xy_neutral or self.y == 0:
            return xy_neutral
        else:
            x1, y1 = self.x, self.y

            s = ((3 * (x1 ** 2) + a) * mod_inv((2 * y1) % p, p)) % p

            x3 = ((s ** 2) - (2 * x1)) % p
            y3 = ((s * (x1 - x3)) - y1) % p

            return PointXY(x3, y3)

    def to_xyz(self):
        if self == xy_neutral:
            return xyz_neutral
        return PointXYZ(self.x, self.y, 1)


"""
Projektiver Punkt - KORRIGIERT
"""
@dataclass
class PointXYZ:
    x: int
    y: int
    z: int

    def __eq__(self, other):
        if self.z == 0 and other.z == 0:
            return True  # Beide sind Punkte im Unendlichen
        if self.z == 0 or other.z == 0:
            return False  # Einer ist im Unendlichen, der andere nicht
        return (self.x * other.z) % p == (other.x * self.z) % p and (self.y * other.z) % p == (other.y * self.z) % p

    def __neg__(self):
        return PointXYZ(self.x, (-self.y) % p, self.z)

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
            x1, y1, z1 = self.x, self.y, self.z
            x2, y2, z2 = other.x, other.y, other.z

            # Berechne u1, u2, s1, s2
            u1 = (x1 * z2) % p
            u2 = (x2 * z1) % p
            s1 = (y1 * z2) % p
            s2 = (y2 * z1) % p

            # Wenn u1 == u2, dann sind die x-Koordinaten gleich
            if u1 == u2:
                if s1 == s2:
                    # Gleiche Punkte - Verdopplung
                    return self.dbl()
                else:
                    # Inverse Punkte - Ergebnis ist neutrales Element
                    return xyz_neutral

            # Berechne h und r
            h = (u2 - u1) % p
            r = (s2 - s1) % p

            # Berechne neue Koordinaten
            h2 = (h * h) % p
            h3 = (h2 * h) % p
            u1h2 = (u1 * h2) % p

            x3 = (r * r - h3 - 2 * u1h2) % p
            y3 = (r * (u1h2 - x3) - s1 * h3) % p
            z3 = (z1 * z2 * h) % p

            return PointXYZ(x3, y3, z3)

    def __mul__(self, k: int):
        # KORRIGIERTE Skalarmultiplikation
        if k == 0:
            return xyz_neutral
        if k < 0:
            return (-self) * (-k)

        result = xyz_neutral
        addend = self

        while k:
            if k & 1:
                result = result + addend
            addend = addend.dbl()
            k >>= 1

        return result

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def dbl(self):
        if self == xyz_neutral:
            return xyz_neutral
        else:
            x1, y1, z1 = self.x, self.y, self.z

            # Spezialfall: y1 = 0 (Punkt hat Ordnung 2)
            if y1 == 0:
                return xyz_neutral

            # KORRIGIERTE projektive Verdopplung (Jacobi-Koordinaten)
            y1_2 = (y1 * y1) % p
            y1_4 = (y1_2 * y1_2) % p
            x1_2 = (x1 * x1) % p
            z1_2 = (z1 * z1) % p

            s = (4 * x1 * y1_2) % p
            m = (3 * x1_2 + a * z1_2) % p

            x3 = (m * m - 2 * s) % p
            y3 = (m * (s - x3) - 8 * y1_4) % p
            z3 = (2 * y1 * z1) % p

            return PointXYZ(x3, y3, z3)

    def to_xy(self):
        if self.z == 0:
            return xy_neutral
        else:
            z_inv = mod_inv(self.z, p)
            new_x = (self.x * z_inv) % p
            new_y = (self.y * z_inv) % p
            return PointXY(new_x, new_y)


# KORRIGIERTE neutrale Elemente
xyz_neutral = PointXYZ(0, 1, 0)
xy_neutral = PointXY(0, 0)  # KORRIGIERT: Verwende (0,0) statt (None, None)


# KORRIGIERTE Validierungsfunktionen
def on_short_weierstrass(point: PointXY):
    # Sonderbehandlung für neutrales Element
    if point == xy_neutral:
        return True

    x1 = point.x
    y1 = point.y

    left = (y1 ** 2) % p
    right = (x1 ** 3 + a * x1 + b) % p

    return left == right


def on_homogenised_weierstrass(point: PointXYZ):
    # Sonderbehandlung für neutrales Element
    if point.z == 0:
        return True

    x1 = point.x
    y1 = point.y
    z1 = point.z

    left = (y1 ** 2 * z1) % p
    right = (x1 ** 3 + a * x1 * z1 ** 2 + b * z1 ** 3) % p

    return left == right


def skalarmul(point: PointXY, k):
    point = point.to_xyz()
    q = xyz_neutral
    j = len(k) - 1
    for i in range(j, -1, -1):
        q = q.dbl()
        if k[i] == '1':
            q = q + point
    return q.to_xy()


"""
main() Methode - KORRIGIERT
"""
if __name__ == "__main__":
    print("=== KORRIGIERTE VERSION ===")

    # Test mit projektiven Punkten
    point_p = PointXYZ(60306380415904663168568911239273826053144841234228559299517684417361346433053,
                       74653857005150983469598545140707432309023702960881435319026826228339031179596, 1)
    p_val = on_homogenised_weierstrass(point_p)
    p2 = point_p.dbl()
    p2_val = on_homogenised_weierstrass(p2)
    p3 = point_p + p2
    p3_val = on_homogenised_weierstrass(p3)
    print(f'point: {point_p}, valid: {p_val}')
    print(f'p2 {p2}, valid: {p2_val}')
    print(f'p3 {p3}, valid: {p3_val}')
    print()

    # Test mit affinen Punkten
    point_p = PointXY(60306380415904663168568911239273826053144841234228559299517684417361346433053,
                      74653857005150983469598545140707432309023702960881435319026826228339031179596)
    p_val = on_short_weierstrass(point_p)
    p2 = point_p.dbl()
    p2_val = on_short_weierstrass(p2)
    pq = point_p + p2
    pq_val = on_short_weierstrass(pq)
    print(f'point: {point_p}, valid: {p_val}')
    print(f'p2 {p2}, valid: {p2_val}')
    print(f'pq {pq}, valid: {pq_val}')
    print()

    # Diffie-Hellman Test
    Gf = PointXY(63243729749562333355292243550312970334778175571054726587095381623627144114786,
                 38218615093753523893122277964030810387585405539772602581557831887485717997975)
    x = 13
    y = 21
    xG = Gf * x
    yG = Gf * y
    y_xG = xG * y
    x_yG = yG * x
    print(f'Gf: {Gf}, {on_short_weierstrass(Gf)}')
    print(f'xG: {xG}, {on_short_weierstrass(xG)}')
    print(f'yG: {yG}, {on_short_weierstrass(yG)}')
    print(f'y_xG: {y_xG}, {on_short_weierstrass(y_xG)}')
    print(f'x_yG: {x_yG}, {on_short_weierstrass(x_yG)}')
    print(f'xyG == yxG: {y_xG == x_yG}')
