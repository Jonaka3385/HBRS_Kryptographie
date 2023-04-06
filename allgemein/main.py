from ak1 import prak1a1
from allgemein import haeufigkeitsverteilung


if __name__ == '__main__':
    prak1a1.start()


    path = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak1/prak1Files/chiffrat.txt"
    with open(path, "r") as f:
        chiffrat = f.read()

    haeufigkeitsverteilung.decrypt(chiffrat)
