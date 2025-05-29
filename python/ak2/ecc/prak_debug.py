from dataclasses import dataclass

# Brainpool P-256 Parameter
p = int(0xA9FB57DBA1EEA9BC3E660A909D838D726E3BF623D52620282013481D1F6E5377)
a = int(0x7D5A0975FC2C3057EEF67530417AFFE7FB8055C126DC5C6CE94A4B44F330B5D9)
b = int(0x26DC5C6CE94A4B44F330B5D9BBD77CBF958416295CF7E1CE6BCCDC18FF8C07B6)


def mod_inv(k, mod):
    if k == 0:
        raise ZeroDivisionError('Division durch Null')
    return pow(k, -1, mod)


@dataclass
class PointXY:
    x: int
    y: int

    def __eq__(self, other):
        if isinstance(other, PointXY):
            return self.x == other.x and self.y == other.y
        return False


@dataclass
class PointXYZ:
    x: int
    y: int
    z: int

    def is_neutral(self):
        return self.z == 0


# Test Funktionen
def on_short_weierstrass(point: PointXY):
    if point.x is None or point.y is None:
        return True  # Neutrales Element

    x1, y1 = point.x, point.y
    left = (y1 * y1) % p
    right = (x1 * x1 * x1 + a * x1 + b) % p
    return left == right


def on_homogenised_weierstrass(point: PointXYZ):
    if point.is_neutral():
        return True

    x1, y1, z1 = point.x, point.y, point.z
    left = (y1 * y1 * z1) % p
    right = (x1 * x1 * x1 + a * x1 * z1 * z1 + b * z1 * z1 * z1) % p
    return left == right


# Debug-Funktion für detaillierte Analyse
def debug_point_validation(point, point_type="XY"):
    print(f"\n=== Debug {point_type} Point ===")

    if point_type == "XY":
        if point.x is None or point.y is None:
            print("Neutrales Element - automatisch gültig")
            return True

        x, y = point.x, point.y
        print(f"Point: ({x}, {y})")

        left = (y * y) % p
        right = (x * x * x + a * x + b) % p

        print(f"Linke Seite (y²): {left}")
        print(f"Rechte Seite (x³ + ax + b): {right}")
        print(f"Modulo p: {p}")
        print(f"Parameter a: {a}")
        print(f"Parameter b: {b}")
        print(f"Gleichheit: {left == right}")

        # Zusätzliche Checks
        print(f"\nZwischenwerte:")
        print(f"x² = {(x * x) % p}")
        print(f"x³ = {(x * x * x) % p}")
        print(f"ax = {(a * x) % p}")
        print(f"x³ + ax = {(x * x * x + a * x) % p}")
        print(f"x³ + ax + b = {right}")

        return left == right

    elif point_type == "XYZ":
        if point.is_neutral():
            print("Neutrales Element (z=0) - automatisch gültig")
            return True

        x, y, z = point.x, point.y, point.z
        print(f"Point: ({x}, {y}, {z})")

        left = (y * y * z) % p
        right = (x * x * x + a * x * z * z + b * z * z * z) % p

        print(f"Linke Seite (y²z): {left}")
        print(f"Rechte Seite (x³ + axz² + bz³): {right}")
        print(f"Gleichheit: {left == right}")

        # Konvertierung zu affinen Koordinaten zum Vergleich
        if z != 0:
            z_inv = mod_inv(z, p)
            x_affin = (x * z_inv) % p
            y_affin = (y * z_inv) % p
            print(f"Affine Koordinaten: ({x_affin}, {y_affin})")

            # Test der affinen Version
            affin_point = PointXY(x_affin, y_affin)
            affin_valid = on_short_weierstrass(affin_point)
            print(f"Affine Version gültig: {affin_valid}")

        return left == right


if __name__ == "__main__":
    print("=== Kurvenparameter ===")
    print(f"p = {hex(p)}")
    print(f"a = {hex(a)}")
    print(f"b = {hex(b)}")

    # Test mit dem ursprünglichen Punkt
    print("\n" + "=" * 50)
    print("TEST 1: Ursprünglicher Punkt")

    # Affiner Punkt
    point_xy = PointXY(60306380415904663168568911239273826053144841234228559299517684417361346433053,
                       74653857005150983469598545140707432309023702960881435319026826228339031179596)

    result_xy = debug_point_validation(point_xy, "XY")

    # Projektiver Punkt
    point_xyz = PointXYZ(60306380415904663168568911239273826053144841234228559299517684417361346433053,
                         74653857005150983469598545140707432309023702960881435319026826228339031179596, 1)

    result_xyz = debug_point_validation(point_xyz, "XYZ")

    print("\n" + "=" * 50)
    print("TEST 2: Bekannter Generator-Punkt (falls verfügbar)")

    # Brainpool P-256 Generator-Punkt (offizieller Generator)
    gx = int(0x8BD2AEB9CB7E57CB2C4B482FFC81B7AFB9DE27E1E3BD23C23A4453BD9ACE3262)
    gy = int(0x547EF835C3DAC4FD97F8461A14611DC9C27745132DED8E545C1D54C72F046997)

    gen_xy = PointXY(gx, gy)
    gen_xyz = PointXYZ(gx, gy, 1)

    print("Generator-Punkt Test:")
    gen_result_xy = debug_point_validation(gen_xy, "XY")
    gen_result_xyz = debug_point_validation(gen_xyz, "XYZ")

    print("\n" + "=" * 50)
    print("ZUSAMMENFASSUNG:")
    print(f"Ursprünglicher Punkt (XY): {'GÜLTIG' if result_xy else 'UNGÜLTIG'}")
    print(f"Ursprünglicher Punkt (XYZ): {'GÜLTIG' if result_xyz else 'UNGÜLTIG'}")
    print(f"Generator-Punkt (XY): {'GÜLTIG' if gen_result_xy else 'UNGÜLTIG'}")
    print(f"Generator-Punkt (XYZ): {'GÜLTIG' if gen_result_xyz else 'UNGÜLTIG'}")