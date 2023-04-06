from random import randrange


def decrypt(encryptedraw):
    encrypted = allcap(encryptedraw)
    ca, cb, cc, cd, ce, cf, cg, ch, ci, cj, ck, cl, cm, cn, co, cp, cq, cr, cs, ct, cu, cv, cw, cx, cy, cz = count(encrypted)
    key = sortvert(encrypted, ca, cb, cc, cd, ce, cf, cg, ch, ci, cj, ck, cl, cm, cn, co, cp, cq, cr, cs, ct, cu, cv, cw, cx, cy, cz)
    decrypted = replacealldecrypt(encrypted, key)
    key = allcap(key)
    print(f'\n\nErgebnis:\n\n{decrypted}\nKey: {key}')
    fertig = input('Richtig?(y/n): ')
    aenderungen = 0
    while fertig == 'n':
        print('Was tauschen?')
        b1 = input('Im Text: ')
        b2 = input('Sollte sein: ')
        key = swapkeyletter(key, b1, b2, encrypted, decrypted)
        decrypted = replacealldecrypt(encrypted, key)
        aenderungen += 1
        print(f'\n\n\nErgebnis:\n\n{decrypted}\nKey: {key}\n')
        fertig = input('Richtig?(y/n): ')
    print(f'\nAenderungen: {aenderungen}\n\n\n')


def decryptwithkey(encryptedraw, key):
    encrypted = allcap(encryptedraw)
    decrypted = replacealldecrypt(encrypted, key)
    print(f'\n\nErgebnis:\n\n{decrypted}\nKey: {key}')


def encrypt(decryptedraw):
    decrypted = allcap(decryptedraw)
    print(decrypted)
    key = 'ENISRATDHULCGMOBWFKZPVJYXQ'
    encrypted = ''
    for i in range(128):
        tmp = ''
        for j in range(len(key)):
            r = randrange(0, 2)
            if r == 0:
                tmp = tmp + key[j]
            else:
                tmp = key[j] + tmp
        key = tmp
    encrypted = replaceallencrypt(decrypted, key)
    print(f'\n\nErgebnis:\n\n{encrypted}\nKey: {key}')


def encryptwithkey(decryptedraw, keyraw):
    decrypted = allcap(decryptedraw)
    print(decrypted)
    key = allcap(keyraw)
    keyreversed = reverse(key)
    encrypted = replaceallencrypt(decrypted, key)
    print(f'\n\nErgebnis:\n\n{encrypted}\nKey: {key}')


def swapkeyletter(key, b1, b2, encr, decr):
    hreihenfolge = 'ENISRATDHULCGMOBWFKZPVJYXQ'

    key = key.replace(b1, 'y')
    key = key.replace(b2, b1)
    key = key.replace('y', b2)
    key = allcap(key)
    return key


def reverse(input):
    output = ''
    l = len(input) - 1
    for i in range(l+1):
        output += input[l-i]
    return output


def swapbb(text, b1, b2):
    b1c = allcap(b1)
    b2c = allcap(b2)
    text = text.replace(b1c, b2)
    text = text.replace(b2c, b1)
    text = allcap(text)
    return text


def allcap(raw):
    raw = raw.replace('a', 'A')
    raw = raw.replace('b', 'B')
    raw = raw.replace('c', 'C')
    raw = raw.replace('d', 'D')
    raw = raw.replace('e', 'E')
    raw = raw.replace('f', 'F')
    raw = raw.replace('g', 'G')
    raw = raw.replace('h', 'H')
    raw = raw.replace('i', 'I')
    raw = raw.replace('j', 'J')
    raw = raw.replace('k', 'K')
    raw = raw.replace('l', 'L')
    raw = raw.replace('m', 'M')
    raw = raw.replace('n', 'N')
    raw = raw.replace('o', 'O')
    raw = raw.replace('p', 'P')
    raw = raw.replace('q', 'Q')
    raw = raw.replace('r', 'R')
    raw = raw.replace('s', 'S')
    raw = raw.replace('t', 'T')
    raw = raw.replace('u', 'U')
    raw = raw.replace('v', 'V')
    raw = raw.replace('w', 'W')
    raw = raw.replace('x', 'X')
    raw = raw.replace('y', 'Y')
    raw = raw.replace('z', 'Z')
    return raw


def allnotcap(raw):
    raw = raw.replace('A', 'a')
    raw = raw.replace('B', 'b')
    raw = raw.replace('C', 'c')
    raw = raw.replace('D', 'd')
    raw = raw.replace('E', 'e')
    raw = raw.replace('F', 'f')
    raw = raw.replace('G', 'g')
    raw = raw.replace('H', 'h')
    raw = raw.replace('I', 'i')
    raw = raw.replace('J', 'j')
    raw = raw.replace('K', 'k')
    raw = raw.replace('L', 'l')
    raw = raw.replace('M', 'm')
    raw = raw.replace('N', 'n')
    raw = raw.replace('O', 'o')
    raw = raw.replace('P', 'p')
    raw = raw.replace('Q', 'q')
    raw = raw.replace('R', 'r')
    raw = raw.replace('S', 's')
    raw = raw.replace('T', 't')
    raw = raw.replace('U', 'u')
    raw = raw.replace('V', 'v')
    raw = raw.replace('W', 'w')
    raw = raw.replace('X', 'x')
    raw = raw.replace('Y', 'y')
    raw = raw.replace('Z', 'z')
    return raw


def count(text):
    ca = cb = cc = cd = ce = cf = cg = ch = ci = cj = ck = cl = cm = cn = co = cp = cq = cr = cs = ct = cu = cv = cw = cx = cy = cz = 0
    for i in range(len(text)):
        if text[i] == 'A':
            ca += 1
        elif text[i] == 'B':
            cb += 1
        elif text[i] == 'C':
            cc += 1
        elif text[i] == 'D':
            cd += 1
        elif text[i] == 'E':
            ce += 1
        elif text[i] == 'F':
            cf += 1
        elif text[i] == 'G':
            cg += 1
        elif text[i] == 'H':
            ch += 1
        elif text[i] == 'I':
            ci += 1
        elif text[i] == 'J':
            cj += 1
        elif text[i] == 'K':
            ck += 1
        elif text[i] == 'L':
            cl += 1
        elif text[i] == 'M':
            cm += 1
        elif text[i] == 'N':
            cn += 1
        elif text[i] == 'O':
            co += 1
        elif text[i] == 'P':
            cp += 1
        elif text[i] == 'Q':
            cq += 1
        elif text[i] == 'R':
            cr += 1
        elif text[i] == 'S':
            cs += 1
        elif text[i] == 'T':
            ct += 1
        elif text[i] == 'U':
            cu += 1
        elif text[i] == 'V':
            cv += 1
        elif text[i] == 'W':
            cw += 1
        elif text[i] == 'X':
            cx += 1
        elif text[i] == 'Y':
            cy += 1
        elif text[i] == 'Z':
            cz += 1
    tca = ca, 'A'
    tcb = cb, 'B'
    tcc = cc, 'C'
    tcd = cd, 'D'
    tce = ce, 'E'
    tcf = cf, 'F'
    tcg = cg, 'G'
    tch = ch, 'H'
    tci = ci, 'I'
    tcj = cj, 'J'
    tck = ck, 'K'
    tcl = cl, 'L'
    tcm = cm, 'M'
    tcn = cn, 'N'
    tco = co, 'O'
    tcp = cp, 'P'
    tcq = cq, 'Q'
    tcr = cr, 'R'
    tcs = cs, 'S'
    tct = ct, 'T'
    tcu = cu, 'U'
    tcv = cv, 'V'
    tcw = cw, 'W'
    tcx = cx, 'X'
    tcy = cy, 'Y'
    tcz = cz, 'Z'
    return tca, tcb, tcc, tcd, tce, tcf, tcg, tch, tci, tcj, tck, tcl, tcm, tcn, tco, tcp, tcq, tcr, tcs, tct, tcu, tcv, tcw, tcx, tcy, tcz


def replacealldecrypt(text, hverteilung):
    hreihenfolge = 'enisratdhulcgmobwfkzpvjyxq'
    for j in range(len(hreihenfolge)):
        text = text.replace(hverteilung[j], hreihenfolge[j])
    text = allcap(text)
    return text


def replaceallencrypt(text, key):
    hreihenfolge = 'ENISRATDHULCGMOBWFKZPVJYXQ'
    key = allnotcap(key)
    for j in range(len(hreihenfolge)):
        text = text.replace(hreihenfolge[j], key[j])
    text = allcap(text)
    return text


def sortvert(text, dca, dcb, dcc, dcd, dce, dcf, dcg, dch, dci, dcj, dck, dcl, dcm, dcn, dco, dcp, dcq, dcr, dcs, dct, dcu, dcv, dcw, dcx, dcy, dcz):
    vert = ''
    for i in range(26):
        tmp = 0, ''
        tmp = max(dca, dcb, dcc, dcd, dce, dcf, dcg, dch, dci, dcj, dck, dcl, dcm, dcn, dco, dcp, dcq, dcr, dcs, dct, dcu, dcv, dcw, dcx, dcy, dcz)
        if tmp[1] == 'A':
            dca = -1, ''
            vert += 'A'
        elif tmp[1] == 'B':
            dcb = -1, ''
            vert += 'B'
        elif tmp[1] == 'C':
            dcc = -1, ''
            vert += 'C'
        elif tmp[1] == 'D':
            dcd = -1, ''
            vert += 'D'
        elif tmp[1] == 'E':
            dce = -1, ''
            vert += 'E'
        elif tmp[1] == 'F':
            dcf = -1, ''
            vert += 'F'
        elif tmp[1] == 'G':
            dcg = -1, ''
            vert += 'G'
        elif tmp[1] == 'H':
            dch = -1, ''
            vert += 'H'
        elif tmp[1] == 'I':
            dci = -1, ''
            vert += 'I'
        elif tmp[1] == 'J':
            dcj = -1, ''
            vert += 'J'
        elif tmp[1] == 'K':
            dck = -1, ''
            vert += 'K'
        elif tmp[1] == 'L':
            dcl = -1, ''
            vert += 'L'
        elif tmp[1] == 'M':
            dcm = -1, ''
            vert += 'M'
        elif tmp[1] == 'N':
            dcn = -1, ''
            vert += 'N'
        elif tmp[1] == 'O':
            dco = -1, ''
            vert += 'O'
        elif tmp[1] == 'P':
            dcp = -1, ''
            vert += 'P'
        elif tmp[1] == 'Q':
            dcq = -1, ''
            vert += 'Q'
        elif tmp[1] == 'R':
            dcr = -1, ''
            vert += 'R'
        elif tmp[1] == 'S':
            dcs = -1, ''
            vert += 'S'
        elif tmp[1] == 'T':
            dct = -1, ''
            vert += 'T'
        elif tmp[1] == 'U':
            dcu = -1, ''
            vert += 'U'
        elif tmp[1] == 'V':
            dcv = -1, ''
            vert += 'V'
        elif tmp[1] == 'W':
            dcw = -1, ''
            vert += 'W'
        elif tmp[1] == 'X':
            dcx = -1, ''
            vert += 'X'
        elif tmp[1] == 'Y':
            dcy = -1, ''
            vert += 'Y'
        elif tmp[1] == 'Z':
            dcz = -1, ''
            vert += 'Z'
        else:
            vert += '0'
    return vert
