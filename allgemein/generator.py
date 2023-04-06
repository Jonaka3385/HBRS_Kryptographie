from allgemein import converter
from random import randrange


def generate():
    return 'Baka'


def generatesymbol(x):
    tf = 0
    while tf == 0:
        if x == 34:
            x = randrange(33, 127)
        elif x == 39:
            x = randrange(33, 127)
        elif x == 92:
            x = randrange(33, 127)
        else:
            tf = 1
    return converter.convertbintoascii(converter.inttobyte(x))


def generatepassword(l):
    r = ''
    for i in range(0, l):
        x = randrange(33, 127)
        r += generatesymbol(x)
    return r
