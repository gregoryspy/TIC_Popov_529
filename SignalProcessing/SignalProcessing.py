import numpy
from scipy import signal
import matplotlib.pyplot as plt


def main():
    n = 500
    Fs = 1000
    F_max = 19
    M_list = [4, 16, 64, 256]
    randomNormal = numpy.random.normal(0, 10, n)
    x = numpy.arange(n) / Fs
    w = F_max / (Fs / 2)
    parametersFilter = signal.butter(3, w, "low", output="sos")
    y = signal.sosfiltfilt(parametersFilter, randomNormal)
    quantizeSignals = []
    dispersions = []
    SNRList = []
    for M in M_list:
        bits = []
        delta = (numpy.max(y) - numpy.min(y)) / (M - 1)
        quantizeSignal = delta * numpy.round(y / delta)
        quantizeLevels = numpy.arange(numpy.min(quantizeSignal), numpy.max(quantizeSignal) + 1, delta)
        quantizeBit = numpy.arange(0, M)
        quantizeBit = [format(bits, '0' + str(int(numpy.log(M) / numpy.log(2))) + 'b') for bits in quantizeBit]
        quantizeSignals.append(quantizeSignal)
        quantizeTable = numpy.c_[quantizeLevels[:M], quantizeBit[:M]]
        fig, ax = plt.subplots(figsize=(14 / 2.54, M / 2.54))
        table = ax.table(cellText=quantizeTable, colLabels=["Значення сигналу", "Кодова послідовність"],
                         loc="center")
        table.set_fontsize(14)
        table.scale(1, 2)
        ax.axis('off')
        fig.savefig(f"figures/Таблиця квантування для {M} рівнів.png", dpi=600)
        plt.show()
        for signal_value in quantizeSignal:
            for index, value in enumerate(quantizeLevels[:M]):
                if numpy.round(numpy.abs(signal_value - value), 0) == 0:
                    bits.append(quantizeBit[index])
                    break
        bits = [int(item) for item in list(''.join(bits))]
        fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
        ax.step(numpy.arange(0, len(bits)), bits, linewidth=0.1)
        ax.set_xlabel("Біти")
        ax.set_ylabel("Амплітуда сигналу")
        plt.title(f"Кодова послідовність сигналу при кількості рівнів квантування {M}", fontsize=14)
        fig.savefig(f"figures/Кодова послідовність сигналу при кількості рівнів квантування {M}.png", dpi=600)
        plt.show()
        E = quantizeSignal - y
        dispersion = numpy.var(E)
        SNR = numpy.var(y) / dispersion
        dispersions.append(dispersion)
        SNRList.append(SNR)
    fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
    s = 0
    for i in range(0, 2):
        for j in range(0, 2):
            ax[i][j].plot(x, quantizeSignals[s], linewidth=1)
            s += 1
    fig.supxlabel("Час (секунди)", fontsize=14)
    fig.supylabel("Амплітуда сигналу", fontsize=14)
    fig.suptitle("Цифрові сигнали з рівнями квантування (4, 16, 64, 256)", fontsize=14)
    fig.savefig(f"figures/Цифрові сигнали з рівнями квантування (4, 16, 64, 256).png", dpi=600)
    plt.show()
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.plot(M_list, dispersions, linewidth=1)
    ax.set_xlabel("Кількість рівнів квантування")
    ax.set_ylabel("Дисперсія")
    plt.title("Залежність дисперсії від кількості рівнів квантування", fontsize=14)
    fig.savefig(f"figures/Залежність дисперсії від кількості рівнів квантування.png", dpi=600)
    plt.show()
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.plot(M_list, SNRList, linewidth=1)
    ax.set_xlabel("Кількість рівнів квантування")
    ax.set_ylabel("ССШ")
    plt.title("Залежність співвідношення сигнал-шум від кількості рівнів квантування", fontsize=14)
    fig.savefig(f"figures/Залежність співвідношення сигнал-шум від кількості рівнів квантування.png", dpi=600)
    plt.show()


if __name__ == '__main__':
    main()
