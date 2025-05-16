"""
Uebung 1
"""
from gmpy2 import gcd, is_congruent, invert

if __name__ == "__main__":
    print('Uebung 1.1')
    l1 = gcd(126, 35)
    l2 = gcd(89, 55)
    l3 = gcd(76884956397045344220809746629001649093037950200943055203735601445031516197751,
             59106074526980279816091054855990649698910540574105269979753171365005046919780)
    print(l1, l2, l3, sep='\n')

    print('\nUebung 1.2')
    l1 = is_congruent(133, 45, 60)
    l2 = is_congruent(133, 613, 60)
    l3 = is_congruent(59106074526980279816091054855990649698910540574105269979753171365005046919780,
                      1212380420482660443128237254291015386094479793588251098035787193040477789886045,
                      76884956397045344220809746629001649093037950200943055203735601445031516197751)
    print(l1, l2, l3, sep='\n')

    print('\nUebung 1.3')
    add_inv = -1
    mul_inv = -1
    try:
        add_inv = -35
    except:
        pass
    try:
        mul_inv = invert(35, 126)
    except:
        pass
    l1 = add_inv, mul_inv
    add_inv = -1
    mul_inv = -1
    try:
        add_inv = -55
    except:
        pass
    try:
        mul_inv = invert(55, 89)
    except:
        pass
    l2 = add_inv, mul_inv
    add_inv = -1
    mul_inv = -1
    try:
        add_inv = -59106074526980279816091054855990649698910540574105269979753171365005046919780
    except:
        pass
    try:
        mul_inv = invert(59106074526980279816091054855990649698910540574105269979753171365005046919780,
                         76884956397045344220809746629001649093037950200943055203735601445031516197751)
    except:
        pass
    l3 = add_inv, mul_inv
    print(l1, l2, l3, sep='\n')
