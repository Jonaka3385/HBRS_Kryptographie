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


def kasiskitest(kasiskitest_chiffrat):
    trigrams = find_trigrams(kasiskitest_chiffrat)

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
    haeufigkeitsanalyse_key = ""
    for x in range(gcd):
        x_letters = ""
        for y in range(a-1):  # a-1 falls letztes Pattern unvollstädig
            x_letters += letters[y][x]
        haeufigkeitsanalyse_key += haeufigkeit(x_letters)
    return haeufigkeitsanalyse_key


def keyfinder(keyfinder_chiffrat, gcd):
    split_chiffrat = [keyfinder_chiffrat[i:i + gcd] for i in range(0, len(keyfinder_chiffrat), gcd)]
    a = len(split_chiffrat)
    letters = [[None for _ in range(gcd)] for _ in range(a)]
    i = 0
    for each_split in split_chiffrat:
        j = 0
        for letter in each_split:
            letters[i][j] = letter
            j += 1
        i += 1
    keyfinder_key = haeufigkeitsanalyse(letters, a, gcd)
    return keyfinder_key


def decrypt(decrypt_chiffrat):
    gcd = kasiskitest(decrypt_chiffrat)
    decrypt_key = keyfinder(decrypt_chiffrat, gcd)
    decrypt_klartext, decrypt_key = decryptwithkey(decrypt_chiffrat, decrypt_key)
    return decrypt_klartext, decrypt_key


def decryptwithkey(decryptwithkey_chiffrat, decryptwith_key):
    decrypted = ""
    split_chiffrat = \
        [decryptwithkey_chiffrat[i:i + len(decryptwith_key)] for i in range(0, len(decryptwithkey_chiffrat),
                                                                            len(decryptwith_key))]

    for each_split in split_chiffrat:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] - letter_to_index[decryptwith_key[i]]) % len(alphabet)
            decrypted += index_to_letter[number]
            i += 1

    return decrypted, decryptwith_key


def encryptwithkey(text, encryptwith_key):
    encrypted = ""
    split_chiffrat = [text[i:i + len(encryptwith_key)] for i in range(0, len(text), len(encryptwith_key))]

    for each_split in split_chiffrat:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] + letter_to_index[encryptwith_key[i]]) % len(alphabet)
            encrypted += index_to_letter[number]
            i += 1

    return encrypted, encryptwith_key


if __name__ == "__main__":
    path = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak1/prak1Files/chiffrat2.txt"
    with open(path, "r") as file:
        chiffrat = file.read()
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
    quickstart_path = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak1/prak1Files/chiffrat2.txt"
    with open(quickstart_path, "r") as quickstart_file:
        quickstart_chiffrat = quickstart_file.read()
    quickstart_chiffrat = quickstart_chiffrat.lower()
    quickstart_key = "fwqgczxugp"
    quickstart_klartext, quickstart_key = decryptwithkey(quickstart_chiffrat, quickstart_key)
    quickstart_klartext = quickstart_klartext.upper()
    print("Klartext: ")
    print(quickstart_klartext)
    print()
    print("Schlüssel: ")
    print(quickstart_key)
    print()
