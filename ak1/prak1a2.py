import math

alphabet = "abcdefghijklmnopqrstuvwxyz"
letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def relhaeufigkeit(text):
    letter_count = {char: 0 for char in alphabet}

    for char in text:
        if char.isalpha():
            letter_count[char] += 1

    total_letters = sum(letter_count.values())

    tmp = {}
    for char, count in letter_count.items():
        frequency = count / total_letters
        tmp = tmp + (char.upper(), ": ", frequency)
    return tmp


def find_trigrams(text):
    trigrams = {}
    for i in range(len(text)-2):
        trigram = text[i:i+3]
        if trigram in trigrams:
            trigrams[trigram].append(i)
        else:
            trigrams[trigram] = [i]
    return trigrams


def find_distances(trigram_indices):
    distances = []
    for i in range(len(trigram_indices)-1):
        distance = trigram_indices[i+1] - trigram_indices[i]
        distances.append(distance)
    return distances


def kasiskitest(chiffrat):
    trigrams = find_trigrams(chiffrat)

    sorted_trigrams = sorted(trigrams.items(), key=lambda x: len(x[1]), reverse=True)

    distances = find_distances(sorted_trigrams[0][1])

    gcd = distances[0]
    for i in range(1, len(distances)):
        gcd = math.gcd(gcd, distances[i])

    return gcd


def calculate_coincidence_index(text):
    letter_frequencies = {}

    for letter in text:
        if letter.isalpha():
            if letter in letter_frequencies:
                letter_frequencies[letter] += 1
            else:
                letter_frequencies[letter] = 1

    n = sum(letter_frequencies.values())
    coincidence_index = sum((letter_frequencies[letter] * (letter_frequencies[letter] - 1))
                            for letter in letter_frequencies) / (n * (n - 1))

    return coincidence_index


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


def haeufigkeit(letters):
    letters = letters.upper()
    freq = calculate_freq(letters)
    highest_letter = max(freq, key=freq.get)
    highest_letter = highest_letter.lower()
    i = 0
    while highest_letter != 'e':
        a = letter_to_index[highest_letter] - 1
        i += 1
        if a < 0:
            a = 25
        highest_letter = index_to_letter[a]
    return index_to_letter[i]


def haeufigkeitsanalyse(letters, a, gcd):
    key = ""
    for x in range(gcd):
        x_letters = ""
        for y in range(a-1):  # a-1 falls letztes Pattern unvollstädig
            x_letters += letters[y][x]
        key += haeufigkeit(x_letters)
    return key


def keyfinder(chiffrat, gcd):
    split_chiffrat = [chiffrat[i:i + gcd] for i in range(0, len(chiffrat), gcd)]
    a = len(split_chiffrat)
    letters = [[None for _ in range(gcd)] for _ in range(a)]
    i = 0
    for each_split in split_chiffrat:
        j = 0
        for letter in each_split:
            letters[i][j] = letter
            j += 1
        i += 1
    key = haeufigkeitsanalyse(letters, a, gcd)
    return key


def decrypt(chiffrat):
    gcd = kasiskitest(chiffrat)
    key = keyfinder(chiffrat, gcd)
    klartext, key = decryptwithkey(chiffrat, key)
    return klartext, key


def decryptwithkey(chiffrat, key):
    decrypted = ""
    split_chiffrat = [chiffrat[i:i + len(key)] for i in range(0, len(chiffrat), len(key))]

    for each_split in split_chiffrat:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] - letter_to_index[key[i]]) % len(alphabet)
            decrypted += index_to_letter[number]
            i += 1

    return decrypted, key


def encryptwithkey(text, key):
    encrypted = ""
    split_chiffrat = [text[i:i + len(key)] for i in range(0, len(text), len(key))]

    for each_split in split_chiffrat:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] + letter_to_index[key[i]]) % len(alphabet)
            encrypted += index_to_letter[number]
            i += 1

    return encrypted, key


if __name__ == "__main__":
    path = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak1/prak1Files/chiffrat2.txt"
    with open(path, "r") as f:
        chiffrat = f.read()
    chiffrat = chiffrat.lower()
    klartext, key = decrypt(chiffrat)
    klartext = klartext.upper()
    print("Klartext: ")
    print(klartext)
    print()
    print("Schlüssel: ")
    print(key)
    print()
    while input("Korrekt(j/n)?: ") == "n":
        key = input("Neuer Key-Vorschlag: ")
        klartext, key = decryptwithkey(chiffrat, key)
        klartext = klartext.upper()
        print("Klartext: ")
        print(klartext)
        print()
        print("Schlüssel: ")
        print(key)
        print()


def quickstart():
    path = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak1/prak1Files/chiffrat2.txt"
    with open(path, "r") as f:
        chiffrat = f.read()
    chiffrat = chiffrat.lower()
    key = "fwqgczxugp"
    klartext, key = decryptwithkey(chiffrat, key)
    klartext = klartext.upper()
    print("Klartext: ")
    print(klartext)
    print()
    print("Schlüssel: ")
    print(key)
    print()
