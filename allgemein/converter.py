def convert():
    return "Hi"


def inttobyte(a):
    if a > 255:
        return '11111111'
    tmp = "{0:b}".format(a)
    while len(tmp) < 8:
        tmp = '0' + tmp
    return tmp


def nexttwosplitted(a, b):
    tmpint = a * 2
    tmptxt = ''
    for i in range(tmpint, tmpint + 2):
        tmptxt = tmptxt + b[i]
    return tmptxt[0], tmptxt[1]


def nextfour(a, b):
    tmpint = a * 4
    tmptxt = ''
    for i in range(tmpint, tmpint + 4):
        tmptxt = tmptxt + b[i]
    return tmptxt


def nexteightsplitted(a, b):
    tmpint = a * 8
    tmptxt1 = ''
    tmptxt2 = ''
    for i in range(tmpint, tmpint + 4):
        tmptxt1 = tmptxt1 + b[i]
    for i in range(tmpint + 4, tmpint + 8):
        tmptxt2 = tmptxt2 + b[i]
    return tmptxt1, tmptxt2


def nextascii(a, b):
    if b[a] == '<':
        x = '<?>'
    else:
        x = b[a]
    return x


def convertbintohex(input):
    output = ''
    for x in range(0, int((len(input) / 4))):
        tmp = nextfour(x, input)
        if tmp == '0000':
            output = output + '0'
        elif tmp == '0001':
            output = output + '1'
        elif tmp == '0010':
            output = output + '2'
        elif tmp == '0011':
            output = output + '3'
        elif tmp == '0100':
            output = output + '4'
        elif tmp == '0101':
            output = output + '5'
        elif tmp == '0110':
            output = output + '6'
        elif tmp == '0111':
            output = output + '7'
        elif tmp == '1000':
            output = output + '8'
        elif tmp == '1001':
            output = output + '9'
        elif tmp == '1010':
            output = output + 'A'
        elif tmp == '1011':
            output = output + 'B'
        elif tmp == '1100':
            output = output + 'C'
        elif tmp == '1101':
            output = output + 'D'
        elif tmp == '1110':
            output = output + 'E'
        elif tmp == '1111':
            output = output + 'F'
        else:
            output = output + 'X'
    return output


def convertbintoascii(input):
    output = ''
    for x in range(0, int((len(input)) / 8)):
        a, b = nexteightsplitted(x, input)
        if a == '0010':
            if b == '0000':
                output = output + ' '
            elif b == '0001':
                output = output + '!'
            elif b == '0010':
                output = output + '\"'
            elif b == '0011':
                output = output + '#'
            elif b == '0100':
                output = output + '$'
            elif b == '0101':
                output = output + '%'
            elif b == '0110':
                output = output + '&'
            elif b == '0111':
                output = output + '\''
            elif b == '1000':
                output = output + '('
            elif b == '1001':
                output = output + ')'
            elif b == '1010':
                output = output + '*'
            elif b == '1011':
                output = output + '+'
            elif b == '1100':
                output = output + ','
            elif b == '1101':
                output = output + '-'
            elif b == '1110':
                output = output + '.'
            elif b == '1111':
                output = output + '/'
            else:
                output = output + '<?>'
        elif a == '0011':
            if b == '0000':
                output = output + '0'
            elif b == '0001':
                output = output + '1'
            elif b == '0010':
                output = output + '2'
            elif b == '0011':
                output = output + '3'
            elif b == '0100':
                output = output + '4'
            elif b == '0101':
                output = output + '5'
            elif b == '0110':
                output = output + '6'
            elif b == '0111':
                output = output + '7'
            elif b == '1000':
                output = output + '8'
            elif b == '1001':
                output = output + '9'
            elif b == '1010':
                output = output + ':'
            elif b == '1011':
                output = output + ';'
            elif b == '1100':
                output = output + '<'
            elif b == '1101':
                output = output + '='
            elif b == '1110':
                output = output + '>'
            elif b == '1111':
                output = output + '?'
            else:
                output = output + '<?>'
        elif a == '0100':
            if b == '0000':
                output = output + '@'
            elif b == '0001':
                output = output + 'A'
            elif b == '0010':
                output = output + 'B'
            elif b == '0011':
                output = output + 'C'
            elif b == '0100':
                output = output + 'D'
            elif b == '0101':
                output = output + 'E'
            elif b == '0110':
                output = output + 'F'
            elif b == '0111':
                output = output + 'G'
            elif b == '1000':
                output = output + 'H'
            elif b == '1001':
                output = output + 'I'
            elif b == '1010':
                output = output + 'J'
            elif b == '1011':
                output = output + 'K'
            elif b == '1100':
                output = output + 'L'
            elif b == '1101':
                output = output + 'M'
            elif b == '1110':
                output = output + 'N'
            elif b == '1111':
                output = output + 'O'
            else:
                output = output + '<?>'
        elif a == '0101':
            if b == '0000':
                output = output + 'P'
            elif b == '0001':
                output = output + 'Q'
            elif b == '0010':
                output = output + 'R'
            elif b == '0011':
                output = output + 'S'
            elif b == '0100':
                output = output + 'T'
            elif b == '0101':
                output = output + 'U'
            elif b == '0110':
                output = output + 'V'
            elif b == '0111':
                output = output + 'W'
            elif b == '1000':
                output = output + 'X'
            elif b == '1001':
                output = output + 'Y'
            elif b == '1010':
                output = output + 'Z'
            elif b == '1011':
                output = output + '['
            elif b == '1100':
                output = output + '\\'
            elif b == '1101':
                output = output + ']'
            elif b == '1110':
                output = output + '^'
            elif b == '1111':
                output = output + '_'
            else:
                output = output + '<?>'
        elif a == '0110':
            if b == '0000':
                output = output + '’'
            elif b == '0001':
                output = output + 'a'
            elif b == '0010':
                output = output + 'b'
            elif b == '0011':
                output = output + 'c'
            elif b == '0100':
                output = output + 'd'
            elif b == '0101':
                output = output + 'e'
            elif b == '0110':
                output = output + 'f'
            elif b == '0111':
                output = output + 'g'
            elif b == '1000':
                output = output + 'h'
            elif b == '1001':
                output = output + 'i'
            elif b == '1010':
                output = output + 'j'
            elif b == '1011':
                output = output + 'k'
            elif b == '1100':
                output = output + 'l'
            elif b == '1101':
                output = output + 'm'
            elif b == '1110':
                output = output + 'n'
            elif b == '1111':
                output = output + 'o'
            else:
                output = output + '<?>'
        elif a == '0111':
            if b == '0000':
                output = output + 'p'
            elif b == '0001':
                output = output + 'q'
            elif b == '0010':
                output = output + 'r'
            elif b == '0011':
                output = output + 's'
            elif b == '0100':
                output = output + 't'
            elif b == '0101':
                output = output + 'u'
            elif b == '0110':
                output = output + 'v'
            elif b == '0111':
                output = output + 'w'
            elif b == '1000':
                output = output + 'x'
            elif b == '1001':
                output = output + 'y'
            elif b == '1010':
                output = output + 'z'
            elif b == '1011':
                output = output + '{'
            elif b == '1100':
                output = output + '|'
            elif b == '1101':
                output = output + '}'
            elif b == '1110':
                output = output + '~'
            else:
                output = output + '<?>'
        elif a == '1000':
            if b == '0001':
                output = output + 'ü'
            elif b == '0100':
                output = output + 'ä'
            elif b == '1110':
                output = output + 'Ä'
            else:
                output = output + '<?>'
        elif a == '1001':
            if b == '0100':
                output = output + 'ö'
            elif b == '1001':
                output = output + 'Ö'
            elif b == '1010':
                output = output + 'Ü'
            elif b == '1011':
                output = output + '€'
            elif b == '1100':
                output = output + '£'
            elif b == '1101':
                output = output + '¥'
            else:
                output = output + '<?>'
        else:
            output = output + '<?>'
    return output


def converthextobin(input):
    output = ''
    for x in range(0, int((len(input)))):
        tmp = input[x]
        if tmp == '0':
            output = output + '0000'
        elif tmp == '1':
            output = output + '0001'
        elif tmp == '2':
            output = output + '0010'
        elif tmp == '3':
            output = output + '0011'
        elif tmp == '4':
            output = output + '0100'
        elif tmp == '5':
            output = output + '0101'
        elif tmp == '6':
            output = output + '0110'
        elif tmp == '7':
            output = output + '0111'
        elif tmp == '8':
            output = output + '1000'
        elif tmp == '9':
            output = output + '1001'
        elif tmp == 'A':
            output = output + '1010'
        elif tmp == 'B':
            output = output + '1011'
        elif tmp == 'C':
            output = output + '1100'
        elif tmp == 'D':
            output = output + '1101'
        elif tmp == 'E':
            output = output + '1110'
        elif tmp == 'F':
            output = output + '1111'
        else:
            output = output + 'XXXX'
    return output


def converthextoascii(input):
    output = ''
    for x in range(0, int((len(input)) / 2)):
        a, b = nexttwosplitted(x, input)
        if a == '2':
            if b == '0':
                output = output + ' '
            elif b == '1':
                output = output + '!'
            elif b == '2':
                output = output + '\"'
            elif b == '3':
                output = output + '#'
            elif b == '4':
                output = output + '$'
            elif b == '5':
                output = output + '%'
            elif b == '6':
                output = output + '&'
            elif b == '7':
                output = output + '\''
            elif b == '8':
                output = output + '('
            elif b == '9':
                output = output + ')'
            elif b == 'A':
                output = output + '*'
            elif b == 'B':
                output = output + '+'
            elif b == 'C':
                output = output + ','
            elif b == 'D':
                output = output + '-'
            elif b == 'E':
                output = output + '.'
            elif b == 'F':
                output = output + '/'
            else:
                output = output + '<?>'
        elif a == '3':
            if b == '0':
                output = output + '0'
            elif b == '1':
                output = output + '1'
            elif b == '2':
                output = output + '2'
            elif b == '3':
                output = output + '3'
            elif b == '4':
                output = output + '4'
            elif b == '5':
                output = output + '5'
            elif b == '6':
                output = output + '6'
            elif b == '7':
                output = output + '7'
            elif b == '8':
                output = output + '8'
            elif b == '9':
                output = output + '9'
            elif b == 'A':
                output = output + ':'
            elif b == 'B':
                output = output + ';'
            elif b == 'C':
                output = output + '<'
            elif b == 'D':
                output = output + '='
            elif b == 'E':
                output = output + '>'
            elif b == 'F':
                output = output + '?'
            else:
                output = output + '<?>'
        elif a == '4':
            if b == '0':
                output = output + '@'
            elif b == '1':
                output = output + 'A'
            elif b == '2':
                output = output + 'B'
            elif b == '3':
                output = output + 'C'
            elif b == '4':
                output = output + 'D'
            elif b == '5':
                output = output + 'E'
            elif b == '6':
                output = output + 'F'
            elif b == '7':
                output = output + 'G'
            elif b == '8':
                output = output + 'H'
            elif b == '9':
                output = output + 'I'
            elif b == 'A':
                output = output + 'J'
            elif b == 'B':
                output = output + 'K'
            elif b == 'C':
                output = output + 'L'
            elif b == 'D':
                output = output + 'M'
            elif b == 'E':
                output = output + 'N'
            elif b == 'F':
                output = output + 'O'
            else:
                output = output + '<?>'
        elif a == '5':
            if b == '0':
                output = output + 'P'
            elif b == '1':
                output = output + 'Q'
            elif b == '2':
                output = output + 'R'
            elif b == '3':
                output = output + 'S'
            elif b == '4':
                output = output + 'T'
            elif b == '5':
                output = output + 'U'
            elif b == '6':
                output = output + 'V'
            elif b == '7':
                output = output + 'W'
            elif b == '8':
                output = output + 'X'
            elif b == '9':
                output = output + 'Y'
            elif b == 'A':
                output = output + 'Z'
            elif b == 'B':
                output = output + '['
            elif b == 'C':
                output = output + '\\'
            elif b == 'D':
                output = output + ']'
            elif b == 'E':
                output = output + '^'
            elif b == 'F':
                output = output + '_'
            else:
                output = output + '<?>'
        elif a == '6':
            if b == '0':
                output = output + '’'
            elif b == '1':
                output = output + 'a'
            elif b == '2':
                output = output + 'b'
            elif b == '3':
                output = output + 'c'
            elif b == '4':
                output = output + 'd'
            elif b == '5':
                output = output + 'e'
            elif b == '6':
                output = output + 'f'
            elif b == '7':
                output = output + 'g'
            elif b == '8':
                output = output + 'h'
            elif b == '9':
                output = output + 'i'
            elif b == 'A':
                output = output + 'j'
            elif b == 'B':
                output = output + 'k'
            elif b == 'C':
                output = output + 'l'
            elif b == 'D':
                output = output + 'm'
            elif b == 'E':
                output = output + 'n'
            elif b == 'F':
                output = output + 'o'
            else:
                output = output + '<?>'
        elif a == '7':
            if b == '0':
                output = output + 'p'
            elif b == '1':
                output = output + 'q'
            elif b == '2':
                output = output + 'r'
            elif b == '3':
                output = output + 's'
            elif b == '4':
                output = output + 't'
            elif b == '5':
                output = output + 'u'
            elif b == '6':
                output = output + 'v'
            elif b == '7':
                output = output + 'w'
            elif b == '8':
                output = output + 'x'
            elif b == '9':
                output = output + 'y'
            elif b == 'A':
                output = output + 'z'
            elif b == 'B':
                output = output + '{'
            elif b == 'C':
                output = output + '|'
            elif b == 'D':
                output = output + '}'
            elif b == 'E':
                output = output + '~'
            else:
                output = output + '<?>'
        elif a == '8':
            if b == '1':
                output = output + 'ü'
            elif b == '4':
                output = output + 'ä'
            elif b == 'E':
                output = output + 'Ä'
            else:
                output = output + '<?>'
        elif a == '9':
            if b == '4':
                output = output + 'ö'
            elif b == '9':
                output = output + 'Ö'
            elif b == 'A':
                output = output + 'Ü'
            elif b == 'B':
                output = output + '€'
            elif b == 'C':
                output = output + '£'
            elif b == 'D':
                output = output + '¥'
            else:
                output = output + '<?>'
        else:
            output = output + '<?>'
    return output


def convertasciitobin(input):
    output = ''
    for x in range(0, int(len(input))):
        a = nextascii(x, input)
        if a == ' ':
            output = output + '00100000'
        elif a == '!':
            output = output + '00100001'
        elif a == '\"':
            output = output + '00100010'
        elif a == '#':
            output = output + '00100011'
        elif a == '$':
            output = output + '00100100'
        elif a == '%':
            output = output + '00100101'
        elif a == '&':
            output = output + '00100110'
        elif a == '\'':
            output = output + '00100111'
        elif a == '(':
            output = output + '00101000'
        elif a == ')':
            output = output + '00101001'
        elif a == '*':
            output = output + '00101010'
        elif a == '+':
            output = output + '00101011'
        elif a == ',':
            output = output + '00101100'
        elif a == '-':
            output = output + '00101101'
        elif a == '.':
            output = output + '00101110'
        elif a == '/':
            output = output + '00101111'
        elif a == '0':
            output = output + '00110000'
        elif a == '1':
            output = output + '00110001'
        elif a == '2':
            output = output + '00110010'
        elif a == '3':
            output = output + '00110011'
        elif a == '4':
            output = output + '00110100'
        elif a == '5':
            output = output + '00110101'
        elif a == '6':
            output = output + '00110110'
        elif a == '7':
            output = output + '00110111'
        elif a == '8':
            output = output + '00111000'
        elif a == '9':
            output = output + '00111001'
        elif a == ':':
            output = output + '00111010'
        elif a == ';':
            output = output + '00111011'
        elif a == '<':
            output = output + '00111100'
        elif a == '=':
            output = output + '00111101'
        elif a == '>':
            output = output + '00111110'
        elif a == '?':
            output = output + '00111111'
        elif a == '@':
            output = output + '01000000'
        elif a == 'A':
            output = output + '01000001'
        elif a == 'B':
            output = output + '01000010'
        elif a == 'C':
            output = output + '01000011'
        elif a == 'D':
            output = output + '01000100'
        elif a == 'E':
            output = output + '01000101'
        elif a == 'F':
            output = output + '01000110'
        elif a == 'G':
            output = output + '01000111'
        elif a == 'H':
            output = output + '01001000'
        elif a == 'I':
            output = output + '01001001'
        elif a == 'J':
            output = output + '01001010'
        elif a == 'K':
            output = output + '01001011'
        elif a == 'L':
            output = output + '01001100'
        elif a == 'M':
            output = output + '01001101'
        elif a == 'N':
            output = output + '01001110'
        elif a == 'O':
            output = output + '01001111'
        elif a == 'P':
            output = output + '01010000'
        elif a == 'Q':
            output = output + '01010001'
        elif a == 'R':
            output = output + '01010010'
        elif a == 'S':
            output = output + '01010011'
        elif a == 'T':
            output = output + '01010100'
        elif a == 'U':
            output = output + '01010101'
        elif a == 'V':
            output = output + '01010110'
        elif a == 'W':
            output = output + '01010111'
        elif a == 'X':
            output = output + '01011000'
        elif a == 'Y':
            output = output + '01011001'
        elif a == 'Z':
            output = output + '01011010'
        elif a == '[':
            output = output + '01011011'
        elif a == '\\':
            output = output + '01011100'
        elif a == ']':
            output = output + '01011101'
        elif a == '^':
            output = output + '01011110'
        elif a == '_':
            output = output + '01011111'
        elif a == '‘':
            output = output + '01100000'
        elif a == 'a':
            output = output + '01100001'
        elif a == 'b':
            output = output + '01100010'
        elif a == 'c':
            output = output + '01100011'
        elif a == 'd':
            output = output + '01100100'
        elif a == 'e':
            output = output + '01100101'
        elif a == 'f':
            output = output + '01100110'
        elif a == 'g':
            output = output + '01100111'
        elif a == 'h':
            output = output + '01101000'
        elif a == 'i':
            output = output + '01101001'
        elif a == 'j':
            output = output + '01101010'
        elif a == 'k':
            output = output + '01101011'
        elif a == 'l':
            output = output + '01101100'
        elif a == 'm':
            output = output + '01101101'
        elif a == 'n':
            output = output + '01101110'
        elif a == 'o':
            output = output + '01101111'
        elif a == 'p':
            output = output + '01110000'
        elif a == 'q':
            output = output + '01110001'
        elif a == 'r':
            output = output + '01110010'
        elif a == 's':
            output = output + '01110011'
        elif a == 't':
            output = output + '01110100'
        elif a == 'u':
            output = output + '01110101'
        elif a == 'v':
            output = output + '01110110'
        elif a == 'w':
            output = output + '01110111'
        elif a == 'x':
            output = output + '01111000'
        elif a == 'y':
            output = output + '01111001'
        elif a == 'z':
            output = output + '01111010'
        elif a == '{':
            output = output + '01111011'
        elif a == '|':
            output = output + '01111100'
        elif a == '}':
            output = output + '01111101'
        elif a == '~':
            output = output + '01111110'
        elif a == 'ü':
            output = output + '10000001'
        elif a == 'ä':
            output = output + '10000100'
        elif a == 'Ä':
            output = output + '10001110'
        elif a == 'ö':
            output = output + '10010100'
        elif a == 'Ö':
            output = output + '10011001'
        elif a == 'Ü':
            output = output + '10011010'
        elif a == '€':
            output = output + '10011011'
        elif a == '£':
            output = output + '10011100'
        elif a == '¥':
            output = output + '10011101'
        else:
            output = output + '11111111'
    return output


def convertasciitohex(input):
    output = ''
    for x in range(0, int(len(input))):
        a = nextascii(x, input)
        if a == ' ':
            output = output + '20'
        elif a == '!':
            output = output + '21'
        elif a == '\"':
            output = output + '22'
        elif a == '#':
            output = output + '23'
        elif a == '$':
            output = output + '24'
        elif a == '%':
            output = output + '25'
        elif a == '&':
            output = output + '26'
        elif a == '\'':
            output = output + '27'
        elif a == '(':
            output = output + '28'
        elif a == ')':
            output = output + '29'
        elif a == '*':
            output = output + '2A'
        elif a == '+':
            output = output + '2B'
        elif a == ',':
            output = output + '2C'
        elif a == '-':
            output = output + '2D'
        elif a == '.':
            output = output + '2E'
        elif a == '/':
            output = output + '2F'
        elif a == '0':
            output = output + '30'
        elif a == '1':
            output = output + '31'
        elif a == '2':
            output = output + '32'
        elif a == '3':
            output = output + '33'
        elif a == '4':
            output = output + '34'
        elif a == '5':
            output = output + '35'
        elif a == '6':
            output = output + '36'
        elif a == '7':
            output = output + '37'
        elif a == '8':
            output = output + '38'
        elif a == '9':
            output = output + '39'
        elif a == ':':
            output = output + '3A'
        elif a == ';':
            output = output + '3B'
        elif a == '<':
            output = output + '3C'
        elif a == '=':
            output = output + '3D'
        elif a == '>':
            output = output + '3E'
        elif a == '?':
            output = output + '3F'
        elif a == '@':
            output = output + '40'
        elif a == 'A':
            output = output + '41'
        elif a == 'B':
            output = output + '42'
        elif a == 'C':
            output = output + '43'
        elif a == 'D':
            output = output + '44'
        elif a == 'E':
            output = output + '45'
        elif a == 'F':
            output = output + '46'
        elif a == 'G':
            output = output + '47'
        elif a == 'H':
            output = output + '48'
        elif a == 'I':
            output = output + '49'
        elif a == 'J':
            output = output + '4A'
        elif a == 'K':
            output = output + '4B'
        elif a == 'L':
            output = output + '4C'
        elif a == 'M':
            output = output + '4D'
        elif a == 'N':
            output = output + '4E'
        elif a == 'O':
            output = output + '4F'
        elif a == 'P':
            output = output + '50'
        elif a == 'Q':
            output = output + '51'
        elif a == 'R':
            output = output + '52'
        elif a == 'S':
            output = output + '53'
        elif a == 'T':
            output = output + '54'
        elif a == 'U':
            output = output + '55'
        elif a == 'V':
            output = output + '56'
        elif a == 'W':
            output = output + '57'
        elif a == 'X':
            output = output + '58'
        elif a == 'Y':
            output = output + '59'
        elif a == 'Z':
            output = output + '5A'
        elif a == '[':
            output = output + '5B'
        elif a == '\\':
            output = output + '5C'
        elif a == ']':
            output = output + '5D'
        elif a == '^':
            output = output + '5E'
        elif a == '_':
            output = output + '5F'
        elif a == '‘':
            output = output + '60'
        elif a == 'a':
            output = output + '61'
        elif a == 'b':
            output = output + '62'
        elif a == 'c':
            output = output + '63'
        elif a == 'd':
            output = output + '64'
        elif a == 'e':
            output = output + '65'
        elif a == 'f':
            output = output + '66'
        elif a == 'g':
            output = output + '67'
        elif a == 'h':
            output = output + '68'
        elif a == 'i':
            output = output + '69'
        elif a == 'j':
            output = output + '6A'
        elif a == 'k':
            output = output + '6B'
        elif a == 'l':
            output = output + '6C'
        elif a == 'm':
            output = output + '6D'
        elif a == 'n':
            output = output + '6E'
        elif a == 'o':
            output = output + '6F'
        elif a == 'p':
            output = output + '70'
        elif a == 'q':
            output = output + '71'
        elif a == 'r':
            output = output + '72'
        elif a == 's':
            output = output + '73'
        elif a == 't':
            output = output + '74'
        elif a == 'u':
            output = output + '75'
        elif a == 'v':
            output = output + '76'
        elif a == 'w':
            output = output + '77'
        elif a == 'x':
            output = output + '78'
        elif a == 'y':
            output = output + '79'
        elif a == 'z':
            output = output + '7A'
        elif a == '{':
            output = output + '7B'
        elif a == '|':
            output = output + '7C'
        elif a == '}':
            output = output + '7D'
        elif a == '~':
            output = output + '7E'
        elif a == 'ü':
            output = output + '81'
        elif a == 'ä':
            output = output + '84'
        elif a == 'Ä':
            output = output + '8E'
        elif a == 'ö':
            output = output + '94'
        elif a == 'Ö':
            output = output + '99'
        elif a == 'Ü':
            output = output + '9A'
        elif a == '€':
            output = output + '9B'
        elif a == '£':
            output = output + '9C'
        elif a == '¥':
            output = output + '9D'
        else:
            output = output + 'FF'
    return output


def converthextoallascii(input):
    output = ''
    for x in range(0, int((len(input)) / 2)):
        a, b = nexttwosplitted(x, input)
        if a == '0':
            if b == '0':
                output = output + '[NUL]'
            elif b == '1':
                output = output + '[SOH]'
            elif b == '2':
                output = output + '[STX]'
            elif b == '3':
                output = output + '[ETX]'
            elif b == '4':
                output = output + '[EOT]'
            elif b == '5':
                output = output + '[ENQ]'
            elif b == '6':
                output = output + '[ACK]'
            elif b == '7':
                output = output + '[BEL]'
            elif b == '8':
                output = output + '[BS]'
            elif b == '9':
                output = output + '[TAB]'
            elif b == 'A':
                output = output + '[LF]'
            elif b == 'B':
                output = output + '[VT]'
            elif b == 'C':
                output = output + '[FF]'
            elif b == 'D':
                output = output + '[CR]'
            elif b == 'E':
                output = output + '[SO]'
            elif b == 'F':
                output = output + '[SI]'
            else:
                output = output + '<?>'
        elif a == '1':
            if b == '0':
                output = output + '[DLE]'
            elif b == '1':
                output = output + '[DC1]'
            elif b == '2':
                output = output + '[DC2]'
            elif b == '3':
                output = output + '[DC3]'
            elif b == '4':
                output = output + '[DC4]'
            elif b == '5':
                output = output + '[NAK]'
            elif b == '6':
                output = output + '[SYN]'
            elif b == '7':
                output = output + '[ETB]'
            elif b == '8':
                output = output + '[CAN]'
            elif b == '9':
                output = output + '[EM]'
            elif b == 'A':
                output = output + '[SUB]'
            elif b == 'B':
                output = output + '[ESC]'
            elif b == 'C':
                output = output + '[FS]'
            elif b == 'D':
                output = output + '[GS]'
            elif b == 'E':
                output = output + '[RS]'
            elif b == 'F':
                output = output + '[US]'
            else:
                output = output + '<?>'
        elif a == '2':
            if b == '0':
                output = output + ' '
            elif b == '1':
                output = output + '!'
            elif b == '2':
                output = output + '"'
            elif b == '3':
                output = output + '#'
            elif b == '4':
                output = output + '$'
            elif b == '5':
                output = output + '%'
            elif b == '6':
                output = output + '&'
            elif b == '7':
                output = output + '\''
            elif b == '8':
                output = output + '('
            elif b == '9':
                output = output + ')'
            elif b == 'A':
                output = output + '*'
            elif b == 'B':
                output = output + '+'
            elif b == 'C':
                output = output + ','
            elif b == 'D':
                output = output + '-'
            elif b == 'E':
                output = output + '.'
            elif b == 'F':
                output = output + '/'
            else:
                output = output + '<?>'
        elif a == '3':
            if b == '0':
                output = output + '0'
            elif b == '1':
                output = output + '1'
            elif b == '2':
                output = output + '2'
            elif b == '3':
                output = output + '3'
            elif b == '4':
                output = output + '4'
            elif b == '5':
                output = output + '5'
            elif b == '6':
                output = output + '6'
            elif b == '7':
                output = output + '7'
            elif b == '8':
                output = output + '8'
            elif b == '9':
                output = output + '9'
            elif b == 'A':
                output = output + ':'
            elif b == 'B':
                output = output + ';'
            elif b == 'C':
                output = output + '<'
            elif b == 'D':
                output = output + '='
            elif b == 'E':
                output = output + '>'
            elif b == 'F':
                output = output + '?'
            else:
                output = output + '<?>'
        elif a == '4':
            if b == '0':
                output = output + '@'
            elif b == '1':
                output = output + 'A'
            elif b == '2':
                output = output + 'B'
            elif b == '3':
                output = output + 'C'
            elif b == '4':
                output = output + 'D'
            elif b == '5':
                output = output + 'E'
            elif b == '6':
                output = output + 'F'
            elif b == '7':
                output = output + 'G'
            elif b == '8':
                output = output + 'H'
            elif b == '9':
                output = output + 'I'
            elif b == 'A':
                output = output + 'J'
            elif b == 'B':
                output = output + 'K'
            elif b == 'C':
                output = output + 'L'
            elif b == 'D':
                output = output + 'M'
            elif b == 'E':
                output = output + 'N'
            elif b == 'F':
                output = output + 'O'
            else:
                output = output + '<?>'
        elif a == '5':
            if b == '0':
                output = output + 'P'
            elif b == '1':
                output = output + 'Q'
            elif b == '2':
                output = output + 'R'
            elif b == '3':
                output = output + 'S'
            elif b == '4':
                output = output + 'T'
            elif b == '5':
                output = output + 'U'
            elif b == '6':
                output = output + 'V'
            elif b == '7':
                output = output + 'W'
            elif b == '8':
                output = output + 'X'
            elif b == '9':
                output = output + 'Y'
            elif b == 'A':
                output = output + 'Z'
            elif b == 'B':
                output = output + '['
            elif b == 'C':
                output = output + '\\'
            elif b == 'D':
                output = output + ']'
            elif b == 'E':
                output = output + '^'
            elif b == 'F':
                output = output + '_'
            else:
                output = output + '<?>'
        elif a == '6':
            if b == '0':
                output = output + '’'
            elif b == '1':
                output = output + 'a'
            elif b == '2':
                output = output + 'b'
            elif b == '3':
                output = output + 'c'
            elif b == '4':
                output = output + 'd'
            elif b == '5':
                output = output + 'e'
            elif b == '6':
                output = output + 'f'
            elif b == '7':
                output = output + 'g'
            elif b == '8':
                output = output + 'h'
            elif b == '9':
                output = output + 'i'
            elif b == 'A':
                output = output + 'j'
            elif b == 'B':
                output = output + 'k'
            elif b == 'C':
                output = output + 'l'
            elif b == 'D':
                output = output + 'm'
            elif b == 'E':
                output = output + 'n'
            elif b == 'F':
                output = output + 'o'
            else:
                output = output + '<?>'
        elif a == '7':
            if b == '0':
                output = output + 'p'
            elif b == '1':
                output = output + 'q'
            elif b == '2':
                output = output + 'r'
            elif b == '3':
                output = output + 's'
            elif b == '4':
                output = output + 't'
            elif b == '5':
                output = output + 'u'
            elif b == '6':
                output = output + 'v'
            elif b == '7':
                output = output + 'w'
            elif b == '8':
                output = output + 'x'
            elif b == '9':
                output = output + 'y'
            elif b == 'A':
                output = output + 'z'
            elif b == 'B':
                output = output + '{'
            elif b == 'C':
                output = output + '|'
            elif b == 'D':
                output = output + '}'
            elif b == 'E':
                output = output + '~'
            elif b == 'F':
                output = output + '[DEL]'
            else:
                output = output + '<?>'
        elif a == '8':
            if b == '0':
                output = output + '<[big]ç>'
            elif b == '1':
                output = output + 'ü'
            elif b == '2':
                output = output + 'é'
            elif b == '3':
                output = output + 'â'
            elif b == '4':
                output = output + 'ä'
            elif b == '5':
                output = output + 'à'
            elif b == '6':
                output = output + 'å'
            elif b == '7':
                output = output + 'ç'
            elif b == '8':
                output = output + 'ê'
            elif b == '9':
                output = output + '<:e>'
            elif b == 'A':
                output = output + 'è'
            elif b == 'B':
                output = output + '<:i>'
            elif b == 'C':
                output = output + 'î'
            elif b == 'D':
                output = output + 'ì'
            elif b == 'E':
                output = output + 'Ä'
            elif b == 'F':
                output = output + 'Å'
            else:
                output = output + '<?>'
        elif a == '9':
            if b == '0':
                output = output + 'É'
            elif b == '1':
                output = output + 'æ'
            elif b == '2':
                output = output + 'Æ'
            elif b == '3':
                output = output + 'ô'
            elif b == '4':
                output = output + 'ö'
            elif b == '5':
                output = output + 'ò'
            elif b == '6':
                output = output + 'û'
            elif b == '7':
                output = output + 'ù'
            elif b == '8':
                output = output + '<:y>'
            elif b == '9':
                output = output + 'Ö'
            elif b == 'A':
                output = output + 'Ü'
            elif b == 'B':
                output = output + '€'
            elif b == 'C':
                output = output + '£'
            elif b == 'D':
                output = output + '¥'
            elif b == 'E':
                output = output + '<?>'
            elif b == 'F':
                output = output + '<?>'
            else:
                output = output + '<?>'
        elif a == 'A':
            if b == '0':
                output = output + 'á'
            elif b == '1':
                output = output + 'í'
            elif b == '2':
                output = output + 'ó'
            elif b == '3':
                output = output + 'ú'
            elif b == '4':
                output = output + 'ñ'
            elif b == '5':
                output = output + 'Ñ'
            elif b == '6':
                output = output + '<?>'
            elif b == '7':
                output = output + '<?>'
            elif b == '8':
                output = output + '¿'
            elif b == '9':
                output = output + '<?>'
            elif b == 'A':
                output = output + '<?>'
            elif b == 'B':
                output = output + '<?>'
            elif b == 'C':
                output = output + '<?>'
            elif b == 'D':
                output = output + '<?>'
            elif b == 'E':
                output = output + '<?>'
            elif b == 'F':
                output = output + '<?>'
            else:
                output = output + '<?>'
        elif a == 'B':
            if b == '0':
                output = output + '<?>'
            elif b == '1':
                output = output + '<?>'
            elif b == '2':
                output = output + '<?>'
            elif b == '3':
                output = output + '<?>'
            elif b == '4':
                output = output + '<?>'
            elif b == '5':
                output = output + '<?>'
            elif b == '6':
                output = output + '<?>'
            elif b == '7':
                output = output + '<?>'
            elif b == '8':
                output = output + '<?>'
            elif b == '9':
                output = output + '<?>'
            elif b == 'A':
                output = output + '<?>'
            elif b == 'B':
                output = output + '<?>'
            elif b == 'C':
                output = output + '<?>'
            elif b == 'D':
                output = output + '<?>'
            elif b == 'E':
                output = output + '<?>'
            elif b == 'F':
                output = output + '<?>'
            else:
                output = output + '<?>'
        elif a == 'C':
            if b == '0':
                output = output + '<?>'
            elif b == '1':
                output = output + '<?>'
            elif b == '2':
                output = output + '<?>'
            elif b == '3':
                output = output + '<?>'
            elif b == '4':
                output = output + '<?>'
            elif b == '5':
                output = output + '<?>'
            elif b == '6':
                output = output + '<?>'
            elif b == '7':
                output = output + '<?>'
            elif b == '8':
                output = output + '<?>'
            elif b == '9':
                output = output + '<?>'
            elif b == 'A':
                output = output + '<?>'
            elif b == 'B':
                output = output + '<?>'
            elif b == 'C':
                output = output + '<?>'
            elif b == 'D':
                output = output + '<?>'
            elif b == 'E':
                output = output + '<?>'
            elif b == 'F':
                output = output + '<?>'
            else:
                output = output + '<?>'
        elif a == 'D':
            if b == '0':
                output = output + '<?>'
            elif b == '1':
                output = output + '<?>'
            elif b == '2':
                output = output + '<?>'
            elif b == '3':
                output = output + '<?>'
            elif b == '4':
                output = output + '<?>'
            elif b == '5':
                output = output + '<?>'
            elif b == '6':
                output = output + '<?>'
            elif b == '7':
                output = output + '<?>'
            elif b == '8':
                output = output + '<?>'
            elif b == '9':
                output = output + '<?>'
            elif b == 'A':
                output = output + '<?>'
            elif b == 'B':
                output = output + '<?>'
            elif b == 'C':
                output = output + '<?>'
            elif b == 'D':
                output = output + '<?>'
            elif b == 'E':
                output = output + '<?>'
            elif b == 'F':
                output = output + '<?>'
            else:
                output = output + '<?>'
        elif a == 'E':
            if b == '0':
                output = output + '<?>'
            elif b == '1':
                output = output + '<?>'
            elif b == '2':
                output = output + '<?>'
            elif b == '3':
                output = output + '<?>'
            elif b == '4':
                output = output + '<?>'
            elif b == '5':
                output = output + '<?>'
            elif b == '6':
                output = output + '<?>'
            elif b == '7':
                output = output + '<?>'
            elif b == '8':
                output = output + '<?>'
            elif b == '9':
                output = output + '<?>'
            elif b == 'A':
                output = output + '<?>'
            elif b == 'B':
                output = output + '<?>'
            elif b == 'C':
                output = output + '<?>'
            elif b == 'D':
                output = output + '<?>'
            elif b == 'E':
                output = output + '<?>'
            elif b == 'F':
                output = output + '<?>'
            else:
                output = output + '<?>'
        elif a == 'F':
            if b == '0':
                output = output + '<?>'
            elif b == '1':
                output = output + '<?>'
            elif b == '2':
                output = output + '<?>'
            elif b == '3':
                output = output + '<?>'
            elif b == '4':
                output = output + '<?>'
            elif b == '5':
                output = output + '<?>'
            elif b == '6':
                output = output + '<?>'
            elif b == '7':
                output = output + '<?>'
            elif b == '8':
                output = output + '<?>'
            elif b == '9':
                output = output + '<?>'
            elif b == 'A':
                output = output + '<?>'
            elif b == 'B':
                output = output + '<?>'
            elif b == 'C':
                output = output + '<?>'
            elif b == 'D':
                output = output + '<?>'
            elif b == 'E':
                output = output + '<?>'
            elif b == 'F':
                output = output + '<?>'
            else:
                output = output + '<?>'
        else:
            output = output + '<?>'
    return output
