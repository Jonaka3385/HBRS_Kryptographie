import string


right_mapping = {'C': 'E', 'Q': 'T', 'P': 'I', 'S': 'A', 'E': 'N', 'B': 'O', 'K': 'S', 'M': 'R', 'G': 'C', 'T': 'L', 'L': 'H', 'O': 'D', 'Y': 'M', 'D': 'P', 'V': 'U', 'Z': 'Y', 'A': 'G', 'I': 'F', 'R': 'W', 'H': 'V', 'X': 'B', 'U': 'K', 'F': 'X', 'J': 'J', 'N': 'Z', 'W': 'Q'}

# Buchstabenhäufigkeiten der englischen Sprache
eng_freq = {"A": 0.0817, "B": 0.0149, "C": 0.0278, "D": 0.0425,
            "E": 0.1270, "F": 0.0223, "G": 0.0202, "H": 0.0609,
            "I": 0.0697, "J": 0.0015, "K": 0.0077, "L": 0.0403,
            "M": 0.0241, "N": 0.0675, "O": 0.0751, "P": 0.0193,
            "Q": 0.0010, "R": 0.0599, "S": 0.0633, "T": 0.0906,
            "U": 0.0276, "V": 0.0098, "W": 0.0236, "X": 0.0015,
            "Y": 0.0197, "Z": 0.0007}


def calculate_freq(text):
    freq = {}
    total = 0
    for char in text:
        if char in string.ascii_uppercase:
            freq[char] = freq.get(char, 0) + 1
            total += 1
    for char in freq:
        freq[char] = freq[char] / total
    return freq


def decrypt(text, freq):
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    sorted_eng_freq = sorted(eng_freq.items(), key=lambda x: x[1], reverse=True)
    mapping = {}
    for i in range(len(sorted_freq)):
        mapping[sorted_freq[i][0]] = sorted_eng_freq[i][0]
    result = ""
    for char in text:
        if char in mapping:
            result += mapping[char]
        else:
            result += char
    return result, mapping


def redecrypt(text, sorted_new_eng_freq, sorted_freq):
    mapping = {}
    for i in range(len(sorted_freq)):
        mapping[sorted_freq[i][0]] = sorted_new_eng_freq[i][0]
    result = ""
    for char in text:
        if char in mapping:
            result += mapping[char]
        else:
            result += char
    return result, mapping


def manual_decryption(klartext, mapping, chiffrat, freq):
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    sorted_new_eng_freq = sorted(eng_freq.items(), key=lambda x: x[1], reverse=True)

    while True:
        print("Welche Buchstaben möchtest du tauschen?")
        char1 = input("Erster Buchstabe: ")
        char2 = input("Zweiter Buchstabe: ")

        if char1 not in mapping or char2 not in mapping:
            print("Mindestens einer der Buchstaben kommt nicht im Schlüssel vor.")
        elif char1 == char2:
            print("Die Buchstaben sind identisch.")
        else:
            i = j = 0
            while sorted_new_eng_freq[i][0] != char1:
                i = i+1
            while sorted_new_eng_freq[j][0] != char2:
                j = j+1
            sorted_new_eng_freq[i], sorted_new_eng_freq[j] = sorted_new_eng_freq[j], sorted_new_eng_freq[i]
            klartext, mapping = redecrypt(chiffrat, sorted_new_eng_freq, sorted_freq)
            print("Neuer Klartext:")
            print(klartext)
            print()
            print("Neuer Schlüssel(Mapping):")
            print(mapping)
            print()

        if input("Jetzt korrekt? (j/n): ") == "j":
            break

    return klartext, mapping


def start():
    path = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak1/prak1Files/chiffrat.txt"
    with open(path, "r") as f:
        chiffrat = f.read()
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


def quickDecrypt(chiffrat, mapping):
    result = ""
    for char in chiffrat:
        if char in mapping:
            result += mapping[char]
        else:
            result += char
    return result


def quickstart():
    path = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak1/prak1Files/chiffrat.txt"
    with open(path, "r") as f:
        chiffrat = f.read()
    print("Chiffrat: ")
    print(quickDecrypt(chiffrat, right_mapping))
    print()
    print("Schlüssel(Mapping): ")
    print(right_mapping)
    print()
