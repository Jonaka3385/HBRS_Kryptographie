from ak2.ecc.Points import PointXY, PointXYZ
from ak2.ecc.Weierstrass import WeierstrassCurve
import random


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
    curve = WeierstrassCurve(a, b, p)
    gx = int(0x8BD2AEB9CB7E57CB2C4B482FFC81B7AFB9DE27E1E3BD23C23A4453BD9ACE3262)
    gy = int(0x547EF835C3DAC4FD97F8461A14611DC9C27745132DED8E545C1D54C72F046997)
    gp = PointXY(gx, gy, curve)
    p1 = PointXYZ(60306380415904663168568911239273826053144841234228559299517684417361346433053,
                  74653857005150983469598545140707432309023702960881435319026826228339031179596, 1, curve)


    """
    Test Punktaddition und Punktverdopplung (A6.1)
    """
    p_val = curve.on_homogenised(p1)
    p2 = p1.dbl()
    p3 = p1 + p2
    p2_val = curve.on_homogenised(p2)
    p3_val = curve.on_homogenised(p3)
    print(f'A6.1', f'p1: {p1}, valid: {p_val}', f'p2: {p2}, valid: {p2_val}', f'p3: {p3}, valid: {p3_val}', f'', sep='\n')


    """
    Test Punktmultiplikation (A6.2)
    """
    x = 45293862615914129592799868910073453280318120139794646860937486992939092186751
    p1_xy = p1.to_xy()
    p4 = p1_xy * x
    p4_val = curve.on_short(p4)
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
    curve = WeierstrassCurve(a, b, p)
    g_xyz = PointXYZ(16,1,1, curve)
    g_xy = g_xyz.to_xy()
    our_x = random.randint(0,100)
    #our_x = 0
    print(f'Geheimes x: {our_x}')

    our_p = gen_point(g_xy, our_x)
    print(f'Unser Punkt: {our_p}')

    #Punkt der anderen Gruppe einsetzen
    their_x = int(input('Their x: '))
    their_y = int(input('Their y: '))
    their_point = PointXY(their_x, their_y, curve) #(9, 26)

    our_secret_point = gen_point(their_point, our_x)
    print(f'Gemeinsames Geheimnis: {our_secret_point}')

    #Generiertes Geheimnis der anderen Gruppe einfÃ¼gen
    their_secret_x = int(input('Their x: '))
    their_secret_y = int(input('Their y: '))
    their_secret_point = PointXY(their_x, their_y, curve)

    print(f'Valid: {test_ecdh(our_secret_point, their_secret_point)}')
