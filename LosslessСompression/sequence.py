import random
from string import ascii_lowercase, digits
import math
import collections
from matplotlib import pyplot as plt


def createTable(results, headers, row):
    fig, ax = plt.subplots(figsize=(14 / 1.54, 8 / 1.54))
    ax.axis('off')
    table = ax.table(cellText=results, colLabels=headers, rowLabels=row, loc='center', cellLoc='center')
    table.set_fontsize(14)
    table.scale(0.8, 2)
    fig.savefig("Характеристики сформованих послідовностей")


def main():
    sequence_N = 100
    number = 1
    results = []
    original_sequence1 = list('0' * 99 + '1')
    random.shuffle(original_sequence1)
    original_sequence2 = list("Попов" + '0' * 95)
    original_sequence3 = list("Попов" + '0' * 95)
    random.shuffle(original_sequence3)
    original_sequence4 = ["Попов529"[i % len("Попов529")] for i in range(sequence_N)]
    original_sequence5 = list("По529") * 20
    random.shuffle(original_sequence5)
    original_sequence6 = [random.choice("По") for _ in range(int(0.7 * sequence_N))] + \
                         [random.choice("529") for _ in range(int(0.3 * sequence_N))]
    random.shuffle(original_sequence6)
    original_sequence7 = [random.choice(ascii_lowercase + digits) for _ in range(sequence_N)]
    random.shuffle(original_sequence7)
    original_sequence8 = list('1' * sequence_N)
    for original_sequence in (original_sequence1, original_sequence2, original_sequence3, original_sequence4,
                              original_sequence5, original_sequence6, original_sequence7, original_sequence8):
        original_sequence = ''.join(original_sequence)
        sequence_alphabet_size = len(set(original_sequence))
        original_sequence_size = len(original_sequence)
        counts = collections.Counter(original_sequence)
        probability = {symbol: count / sequence_N for symbol, count in counts.items()}
        probability_str = ', '.join([f"{symbol}={prob:.4f}" for symbol, prob in probability.items()])
        mean_probability = sum(probability.values()) / len(probability)
        equal = all(abs(prob - mean_probability) < 0.05 * mean_probability for prob in
                    probability.values())
        uniformity = "рівна" if equal else "нерівна"
        entropy = -sum(p * math.log2(p) for p in probability.values())
        source_excess = 1 - entropy / math.log2(sequence_alphabet_size) if sequence_alphabet_size > 1 else 1
        results.append([sequence_alphabet_size, round(entropy, 2), round(source_excess, 2), uniformity])
        with open("sequence.txt", 'a', encoding="utf-8") as file:
            file.write(f"originalSequence {number}:\nПослідовність: {original_sequence}\n")
            file.close()
        with open("resultsSequence.txt", 'a', encoding="utf-8") as file:
            file.write(f"originalSequence {number}:\nПослідовність: {original_sequence}\n"
                       f"Розмір послідовності: {original_sequence_size} byte\nРозмір алфавіту: {sequence_alphabet_size}\n"
                       f"Ймовірності появи символів: {probability_str}\nСереднє арифметине ймовірностей: {mean_probability}\n"
                       f"Ймовірність розподілу символів: {uniformity}\nЕнтропія: {entropy}\n"
                       f"Надмірність джерела: {source_excess}\n")
            file.close()
        number += 1
    headers = ['Розмір алфавіту', 'Ентропія', 'Надмірність', 'Ймовірність']
    row = [f"Послідовність {n}" for n in range(1, number)]
    createTable(results=results, headers=headers, row=row)


if __name__ == '__main__':
    main()
