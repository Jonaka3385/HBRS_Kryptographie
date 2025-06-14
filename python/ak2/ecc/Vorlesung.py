from ak2.ecc.Points import PointXY
from ak2.ecc.Weierstrass import WeierstrassCurve


def gen_point(point: PointXY, x):
    new_point = point * x
    return new_point

"""
main() Methode
"""
if __name__ == "__main__":
    # Y^2*Z = X^3 + a*X*Z^2 + b*Z^3
    # y^2 = x^3 + a*X + b

    """
    Kurven-Parameter
    """
    a = 16
    b = 20
    p = 31
    curve = WeierstrassCurve(a, b, p)
    g2 = PointXY(25, 24, curve)
    g_mod = 7
    print(f'Generator: {g2}', f'Modulo: {g_mod}', f'', sep='\n')

    d1 = int(input('d1: '))
    print(f'{d1} mod {g_mod} = {d1 % g_mod}')
    md1 = d1 % g_mod
    p1 = gen_point(g2, md1)
    print(f'Team 1: P{p1}, on_curve: {p1.on_curve()}', f'', sep='\n')

    d2 = int(input('d2: '))
    print(f'{d2} mod {g_mod} = {d2 % g_mod}')
    md2 = d2 % g_mod
    p2 = gen_point(g2, md2)
    print(f'Team 2: P{p2}, on_curve: {p2.on_curve()}', f'', sep='\n')

    secret_p1 = gen_point(p2, md1)
    secret_p2 = gen_point(p1, md2)
    d = d1 * d2
    print(f'd1 * d2 = {d} mod {g_mod} = {d % g_mod}')
    md = d % g_mod
    secret = g2 * md

    print(f'Secret 1: {secret_p1}, {secret_p1.on_curve()}', sep='\n')
    print(f'Secret 2: {secret_p2}, {secret_p2.on_curve()}', sep='\n')
    print(f'Secret d: {secret}, {secret.on_curve()}', sep='\n')
    print(f'Same: {secret_p1 == secret_p2 == secret}')
