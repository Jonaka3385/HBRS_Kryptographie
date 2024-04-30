"""
Praktikum 1 Aufgabe 2
p_ = Übergebener Parameter
"""
import math
import string

alphabet = "abcdefghijklmnopqrstuvwxyz"
letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def relhaeufigkeit(p_text):
    """
    :param p_text:
    :return:
    """
    letter_count = {char: 0 for char in alphabet}

    for char in p_text:
        if char.isalpha():
            letter_count[char] += 1

    total_letters = sum(letter_count.values())

    tmp = {}
    for char, count in letter_count.items():
        frequency = count / total_letters
        tmp += char.upper(), ": ", frequency
    return tmp


def find_trigrams(p_text):
    """
    :param p_text:
    :return:
    """
    trigrams = {}
    for i in range(len(p_text) - 2):
        trigram = p_text[i:i + 3]
        if trigram in trigrams:
            trigrams[trigram].append(i)
        else:
            trigrams[trigram] = [i]
    return trigrams


def find_distances(p_trigram_indices):
    """
    :param p_trigram_indices:
    :return:
    """
    distances = []
    for i in range(len(p_trigram_indices) - 1):
        distance = p_trigram_indices[i + 1] - p_trigram_indices[i]
        distances.append(distance)
    return distances


def kasiskitest(p_chiffrat):
    """
    :param p_chiffrat:
    :return:
    """
    trigrams = find_trigrams(p_chiffrat)
    sorted_trigrams = sorted(trigrams.items(), key=lambda x: len(x[1]), reverse=True)
    distances = find_distances(sorted_trigrams[0][1])

    gcd = distances[0]
    for i in range(1, len(distances)):
        gcd = math.gcd(gcd, distances[i])
    return gcd


def calculate_coincidence_index(p_text):
    """
    :param p_text:
    :return:
    """
    letter_frequencies = {}

    for letter in p_text:
        if letter.isalpha():
            if letter in letter_frequencies:
                letter_frequencies[letter] += 1
            else:
                letter_frequencies[letter] = 1
    n = sum(letter_frequencies.values())
    coincidence_index = sum((letter_frequencies[letter] * (letter_frequencies[letter] - 1))
                            for letter in letter_frequencies) / (n * (n - 1))
    return coincidence_index


def calculate_freq(p_text):
    """
    :param p_text:
    :return:
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


def haeufigkeit(p_letters):
    """
    :param p_letters:
    :return:
    """
    p_letters = p_letters.upper()
    freq = calculate_freq(p_letters)
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


def haeufigkeitsanalyse(p_letters, p_a, p_gcd):
    """
    :param p_letters:
    :param p_a:
    :param p_gcd:
    :return:
    """
    haeufigkeitsanalyse_key = ""
    for x in range(p_gcd):
        x_letters = ""
        for y in range(p_a - 1):  # a-1 falls letztes Pattern unvollstädig
            x_letters += p_letters[y][x]
        haeufigkeitsanalyse_key += haeufigkeit(x_letters)
    return haeufigkeitsanalyse_key


def keyfinder(p_chiffrat, p_gcd):
    """
    :param p_chiffrat:
    :param p_gcd:
    :return:
    """
    split_chiffrat = [p_chiffrat[i:i + p_gcd] for i in range(0, len(p_chiffrat), p_gcd)]
    a = len(split_chiffrat)
    letters = [[None for _ in range(p_gcd)] for _ in range(a)]
    i = 0
    for each_split in split_chiffrat:
        j = 0
        for letter in each_split:
            letters[i][j] = letter
            j += 1
        i += 1
    keyfinder_key = haeufigkeitsanalyse(letters, a, p_gcd)
    return keyfinder_key


def decrypt(p_chiffrat):
    """
    :param p_chiffrat:
    :return:
    """
    gcd = kasiskitest(p_chiffrat)
    decrypt_key = keyfinder(p_chiffrat, gcd)
    decrypt_klartext = decryptwithkey(p_chiffrat, decrypt_key)
    return decrypt_klartext, decrypt_key


def decryptwithkey(p_chiffrat, p_key):
    """
    :param p_chiffrat:
    :param p_key:
    :return:
    """
    decrypted = ""
    split_chiffrat = \
        [p_chiffrat[i:i + len(p_key)] for i in range(0, len(p_chiffrat), len(p_key))]

    for each_split in split_chiffrat:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] - letter_to_index[p_key[i]]) % len(alphabet)
            decrypted += index_to_letter[number]
            i += 1
    return decrypted


def encryptwithkey(p_text, p_key):
    """
    :param p_text:
    :param p_key:
    :return:
    """
    encrypted = ""
    split_chiffrat = [p_text[i:i + len(p_key)] for i in range(0, len(p_text), len(p_key))]

    for each_split in split_chiffrat:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] + letter_to_index[p_key[i]]) % len(alphabet)
            encrypted += index_to_letter[number]
            i += 1
    return encrypted, p_key


def quickstart():
    """
    schnell-entschlüsselung mit richtigen Schlüssel
    """
    q_path = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak1/prak1Files/chiffrat2_t.txt"
    with open(q_path) as q_file:
        q_chiffrat = q_file.read()
    q_chiffrat = q_chiffrat.lower()
    # q_key = "fwqgczxugp" //für chiffrat2, folgende für chiffrat2_t
    q_key = "nfxsdljr"
    q_klartext = decryptwithkey(q_chiffrat, q_key)
    q_klartext = q_klartext.upper()
    print(f'Klartext: {q_klartext}', f'Schlüssel: {q_key}', sep='\n')


if __name__ == "__main__":
    # quickstart()
    # quit()
    path = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak1/prak1Files/chiffrat2_t.txt"
    with open(path) as file:
        chiffrat = file.read()
    chiffrat = chiffrat.lower()
    klartext, key = decrypt(chiffrat)
    klartext = klartext.upper()
    print(f'Klartext: {klartext}', f'Schlüssel: {key}', sep='\n')
    keylen_bool = False
    while input("Korrekt(j/n)?: ") == "n":
        print()
        if not keylen_bool:
            if input("Schlüssellänge korrekt?: ") != "n":
                keylen_bool = True
            else:
                new_keylen = int(input("Neue Schlüssellänge: "))
                key = keyfinder(chiffrat, new_keylen)
        if keylen_bool:
            key = input("Neuer Key-Vorschlag: ")
        klartext = decryptwithkey(chiffrat, key)
        klartext = klartext.upper()
        print(f'Klartext: {klartext}', f'Schlüssel: {key}', sep='\n')
