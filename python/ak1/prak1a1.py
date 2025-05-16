"""
Praktikum 1 Aufgabe 1
p_ = Übergebener Parameter
"""
import string

right_mapping = {'C': 'E', 'Q': 'T', 'P': 'I', 'S': 'A', 'E': 'N', 'B': 'O', 'K': 'S', 'M': 'R', 'G': 'C', 'T': 'L',
                 'L': 'H', 'O': 'D', 'Y': 'M', 'D': 'P', 'V': 'U', 'Z': 'Y', 'A': 'G', 'I': 'F', 'R': 'W', 'H': 'V',
                 'X': 'B', 'U': 'K', 'F': 'X', 'J': 'J', 'N': 'Z', 'W': 'Q'}

# Buchstabenhäufigkeiten der englischen Sprache
eng_freq = {"A": 0.0817, "B": 0.0149, "C": 0.0278, "D": 0.0425,
            "E": 0.1270, "F": 0.0223, "G": 0.0202, "H": 0.0609,
            "I": 0.0697, "J": 0.0015, "K": 0.0077, "L": 0.0403,
            "M": 0.0241, "N": 0.0675, "O": 0.0751, "P": 0.0193,
            "Q": 0.0010, "R": 0.0599, "S": 0.0633, "T": 0.0906,
            "U": 0.0276, "V": 0.0098, "W": 0.0236, "X": 0.0015,
            "Y": 0.0197, "Z": 0.0007}


def calculate_freq(p_text):
    """
    :param p_text:
    :return: Verteilung der Buchstabenhäufigkeit
    """
    freq = {}
    total = 0
    for char in p_text:
        if char in string.ascii_uppercase:
            freq[char] = freq.get(char, 0) + 1
            total += 1
    for char in freq:
        freq[char] /= total
    return freq


def decrypt(p_text, freq):
    """
    :param p_text:
    :param freq:
    :return:
    """
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    sorted_eng_freq = sorted(eng_freq.items(), key=lambda x: x[1], reverse=True)
    decrypt_mapping = {}
    for i in range(len(sorted_freq)):
        decrypt_mapping[sorted_freq[i][0]] = sorted_eng_freq[i][0]
    result = ""
    for char in p_text:
        if char in decrypt_mapping:
            result += decrypt_mapping[char]
        else:
            result += char
    return result, decrypt_mapping


def redecrypt(text, sorted_new_eng_freq, sorted_freq):
    """
    :param text:
    :param sorted_new_eng_freq:
    :param sorted_freq:
    :return:
    """
    redecrypt_mapping = {}
    for i in range(len(sorted_freq)):
        redecrypt_mapping[sorted_freq[i][0]] = sorted_new_eng_freq[i][0]
    result = ""
    for char in text:
        if char in redecrypt_mapping:
            result += redecrypt_mapping[char]
        else:
            result += char
    return result, redecrypt_mapping


def manual_decryption(p_klartext, p_mapping, p_chiffrat, freq):
    """
    :param p_klartext:
    :param p_mapping:
    :param p_chiffrat:
    :param freq:
    :return:
    """
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    sorted_new_eng_freq = sorted(eng_freq.items(), key=lambda x: x[1], reverse=True)

    while True:
        print("Welche Buchstaben möchtest du tauschen?")
        char1 = input("Erster Buchstabe: ")
        char2 = input("Zweiter Buchstabe: ")

        if char1 not in p_mapping or char2 not in p_mapping:
            print("Mindestens einer der Buchstaben kommt nicht im Schlüssel vor.")
        elif char1 == char2:
            print("Die Buchstaben sind identisch.")
        else:
            i = j = 0
            while sorted_new_eng_freq[i][0] != char1:
                i += 1
            while sorted_new_eng_freq[j][0] != char2:
                j += 1
            sorted_new_eng_freq[i], sorted_new_eng_freq[j] = sorted_new_eng_freq[j], sorted_new_eng_freq[i]
            p_klartext, p_mapping = \
                redecrypt(p_chiffrat, sorted_new_eng_freq, sorted_freq)
            print("Neuer Klartext:")
            print(p_klartext)
            print()
            print("Neuer Schlüssel(Mapping):")
            print(p_mapping)
            print()

        if input("Jetzt korrekt? (j/n): ") == "j":
            break

    return p_klartext, p_mapping


if __name__ == "__main__":
    path = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak1/prak1Files/chiffrat1.txt"
    with open(path) as file:
        chiffrat = file.read()
    print("Chiffrat: ")
    print(chiffrat)
    print()

    chiffrat_freq = calculate_freq(chiffrat)
    print("Relative Häufigkeit der Buchstaben im Chiffrat:")
    print(chiffrat_freq)
    print()

    klartext, mapping = decrypt(chiffrat, chiffrat_freq)
    print("Entschlüsselter Text: ")
    print(klartext)
    print()

    print("Schlüssel(Mapping): ")
    print(mapping)
    print()

    if input("Korrrekt? (j/n): ") == "n":
        klartext, mapping = manual_decryption(klartext, mapping, chiffrat, chiffrat_freq)
        print("Endgültiger Klartext: ")
        print(klartext)
        print()
        print("Endgültiger Schlüssel(Mapping): ")
        print(mapping)


def quickdecrypt(p_chiffrat, p_mapping):
    """
    :param p_chiffrat:
    :param p_mapping:
    :return:
    """
    result = ""
    for char in p_chiffrat:
        if char in p_mapping:
            result += p_mapping[char]
        else:
            result += char
    return result


def quickstart():
    """
    manuelles entschlüsseln überspringen (richtiges mapping direkt nutzen)
    """
    quickstart_path = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak1/prak1Files/chiffrat1.txt"
    with open(quickstart_path) as quickstart_file:
        quickstart_chiffrat = quickstart_file.read()
    print("Chiffrat: ")
    print(quickdecrypt(quickstart_chiffrat, right_mapping))
    print()
    print("Schlüssel(Mapping): ")
    print(right_mapping)
    print()
