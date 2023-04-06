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


def decrypt(chiffrat):
    gcd = kasiskitest(chiffrat)
    avg_coin_ind = 0
    for i in range(int(len(chiffrat)/gcd)):
        tmp = ""
        for j in range(gcd):
            tmp += chiffrat[i*gcd+j]
        avg_coin_ind += calculate_coincidence_index(tmp)
    avg_coin_ind = avg_coin_ind/(len(chiffrat)/gcd)
    key = "a"*gcd
    # key bestimmen
    klartext = decryptwithkey(chiffrat, key)
    return klartext


def decryptwithkey(chiffrat, key):
    decrypted = ""
    split_chiffrat = [chiffrat[i:i + len(key)] for i in range(0, len(chiffrat), len(key))]

    for each_split in split_chiffrat:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] - letter_to_index[key[i]]) % len(alphabet)
            decrypted += index_to_letter[number]
            i += 1

    return decrypted


def start():
    path = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/Kryptographie/ak1/prak1Files/chiffrat2.txt"
    with open(path, "r") as f:
        chiffrat = f.read()
    chiffrat = chiffrat.lower()
    klartext = decrypt(chiffrat).upper()
    print(klartext)
