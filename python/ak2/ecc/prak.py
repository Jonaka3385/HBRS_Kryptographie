from dataclasses import dataclass
import random


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
        return PointXY(self.x, (-self.y) % p)

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
        q = xy_neutral
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
        if self == xy_neutral:
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

            new_p = PointXYZ(x3, y3, z3)
            if z1 == 1 & z2 == 1:
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

            new_p = PointXYZ(x3, y3, z3)
            if z1 == 1:
                new_p.normalise()
            return new_p

    def to_xy(self):
        if self.z == 0:
            return xy_neutral
        else:
            z_inv = mod_inv(self.z, p)
            new_x = self.x * z_inv
            new_y = self.y * z_inv
            return PointXY(new_x, new_y)

    def normalise(self):
        tmp = self.to_xy()
        self.x = tmp.x
        self.y = tmp.y
        self.z = 1


xyz_neutral = PointXYZ(0, 1, 0)
xy_neutral = PointXY(0, 0)

p = 0
a = 0
b = 0

def on_weierstrass(point):
    if isinstance(point, PointXY):
        return on_short_weierstrass(point)
    elif isinstance(point, PointXYZ):
        return on_homogenised_weierstrass(point)
    else:
        raise Exception("Point must be of type PointXY or PointXYZ")

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
Elliptic Curve Diffie Hellman
"""
def gen_point(point: PointXY, x):
    new_point = point * x
    return new_point

def send_point(point: PointXY):
    return point

def ecdh(point: PointXY):
    alice_x = random.randint(0,100)
    bob_x = random.randint(0,100)

    alice_point = gen_point(point, alice_x)
    bob_point = gen_point(point, bob_x)

    point_bob = send_point(bob_point)
    point_alice = send_point(alice_point)

    alice_secret_point = gen_point(point_bob, alice_x)
    bob_secret_point = gen_point(point_alice, bob_x)

    return alice_secret_point, bob_secret_point

def test_ecdh(key1: PointXY, key2: PointXY):
    return key1 == key2


"""
Man-in-the-Middle ECDH
"""
def ecdh_mitm(point: PointXY):
    alice_x = random.randint(0, 100)
    bob_x = random.randint(0, 100)
    eve_x = random.randint(0,100)

    alice_point = gen_point(point, alice_x)
    bob_point = gen_point(point, bob_x)
    eve_point = gen_point(point, eve_x)

    point_bob = send_point(bob_point)
    point_alice = send_point(alice_point)
    point_eve = send_point(eve_point)

    alice_secret_point = gen_point(point_eve, alice_x)
    bob_secret_point = gen_point(point_eve, bob_x)
    eve_secret_point_alice = gen_point(point_alice, eve_x)
    eve_secret_point_bob = gen_point(point_bob, eve_x)

    return alice_secret_point, eve_secret_point_alice, bob_secret_point, eve_secret_point_bob

"""
main() Methode
"""
if __name__ == "__main__":
    # Y^2*Z = X^3 + a*X*Z^2 + b*Z^3
    # y^2 = x^3 + a*X + b

    """
    Kurven-Parameter
    """
    p = int(0xA9FB57DBA1EEA9BC3E660A909D838D726E3BF623D52620282013481D1F6E5377)
    a = int(0x7D5A0975FC2C3057EEF67530417AFFE7FB8055C126DC5C6CE94A4B44F330B5D9)
    b = int(0x26DC5C6CE94A4B44F330B5D9BBD77CBF958416295CF7E1CE6BCCDC18FF8C07B6)
    gx = int(0x8BD2AEB9CB7E57CB2C4B482FFC81B7AFB9DE27E1E3BD23C23A4453BD9ACE3262)
    gy = int(0x547EF835C3DAC4FD97F8461A14611DC9C27745132DED8E545C1D54C72F046997)
    gp = PointXY(gx,gy)
    p1 = PointXYZ(60306380415904663168568911239273826053144841234228559299517684417361346433053,
                  74653857005150983469598545140707432309023702960881435319026826228339031179596, 1)

    """
    Test Punktaddition und Punktverdopplung (A6.1)
    """
    p_val = on_weierstrass(p1)
    p2 = p1.dbl()
    p3 = p1 + p2
    p2_val = on_weierstrass(p2)
    p3_val = on_weierstrass(p3)
    print(f'A6.1', f'p1: {p1}, valid: {p_val}', f'p2: {p2}, valid: {p2_val}', f'p3: {p3}, valid: {p3_val}', f'', sep='\n')

    """
    Test Punktmultiplikation (A6.2)
    """
    x = 45293862615914129592799868910073453280318120139794646860937486992939092186751
    p1_xy = p1.to_xy()
    p4 = p1_xy * x
    p4_val = on_weierstrass(p4)
    p4_xyz = p4.to_xyz()
    print(f'A6.2', f'p4: {p4_xyz}, valid: {p4_val}', f'', sep='\n')

    """
    Test ECDH (A6.3.1)
    """
    com_key = ecdh(gp)
    ck1, ck2 = com_key
    print(f'A6.3.1', f'Gemeinsames Geheimnis: Alice{ck1}, Bob{ck2}, valid: {test_ecdh(com_key[0], com_key[1])}', f'', sep='\n')

    """
    Test Man-in-the-Middle ECDH (A6.3.3)
    """
    com_keys = ecdh_mitm(gp)
    ck_1,ck_2,ck_3,ck_4 = com_keys
    valid_alice_eve = test_ecdh(com_keys[0], com_keys[1])
    valid_bob_eve = test_ecdh(com_keys[2], com_keys[3])
    print(f'A6.3.3', f'Geheimnis(MitM): Alice{ck_1}, Eve{ck_2}, Valid: {valid_alice_eve}',
          f'Geheimnis(MitM): Bob{ck_3}, Eve{ck_4}, Valid: {valid_bob_eve}', f'', sep='\n')

    """
    Gruppenarbeit (A6.3.4)
    """
    print(f'A6.3.4')
    a = 16
    b = 20
    p = 31
    g_xyz = PointXYZ(16,1,1)
    g_xy = g_xyz.to_xy()
    our_x = random.randint(0,100)
    #our_x = 0
    print(f'Geheimes x: {our_x}')

    our_p = gen_point(g_xy, our_x)
    print(f'Unser Punkt: {our_p}')

    #Punkt der anderen Gruppe einsetzen
    their_x = int(input('Their x: '))
    their_y = int(input('Their y: '))
    their_point = PointXY(their_x, their_y) #(9, 26)

    our_secret_point = gen_point(their_point, our_x)
    print(f'Gemeinsames Geheimnis: {our_secret_point}')

    #Generiertes Geheimnis der anderen Gruppe einfÃ¼gen
    their_secret_x = int(input('Their x: '))
    their_secret_y = int(input('Their y: '))
    their_secret_point = PointXY(their_x, their_y)

    print(f'Valid: {test_ecdh(our_secret_point, their_secret_point)}')
