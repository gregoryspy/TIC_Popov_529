import numpy
from scipy import signal, fft
import matplotlib.pyplot as plt


def main():
    n = 500
    Fs = 1000
    F_max = 3
    Dt_list = [2, 4, 8, 16]
    F_filter = 10
    randomNormal = numpy.random.normal(0, 10, n)
    x = numpy.arange(n) / Fs
    w = F_max / (Fs / 2)
    parametersFilter = signal.butter(3, w, "low", output="sos")
    y = signal.sosfiltfilt(parametersFilter, randomNormal)
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.plot(x, y, linewidth=1)
    ax.set_xlabel("Час (секунди)")
    ax.set_ylabel("Амплітуда сигналу")
    plt.title("Сигнал", fontsize=14)
    fig.savefig(f"figures/Сигнал.png", dpi=600)
    plt.show()

    spectrum = fft.fft(y)
    spectrum_center = numpy.abs(fft.fftshift(spectrum))
    frequencyReadings = fft.fftfreq(n, 1 / n)
    frequency_readings_center = fft.fftshift(frequencyReadings)
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.plot(frequency_readings_center, spectrum_center, linewidth=1)
    ax.set_xlabel("Частота(Гц)")
    ax.set_ylabel("Амплітуда спектру")
    plt.title("Спектр сигналу", fontsize=14)
    fig.savefig(f"figures/Спектр сигналу.png", dpi=600)
    plt.show()

    discrete_signals = []
    discrete_spectrums = []
    vars2 = []
    snr_list = []
    for Dt in Dt_list:
        discreteSignal = numpy.zeros(n)
        for i in range(0, round(n / Dt)):
            discreteSignal[i * Dt] = y[i * Dt]
        discrete_spectrum = fft.fft(discreteSignal)
        discrete_spectrum = numpy.abs(fft.fftshift(discrete_spectrum))
        discrete_signals.append(discreteSignal)
        discrete_spectrums.append(discrete_spectrum)
        E1 = discreteSignal - y
        var1 = numpy.var(y)
        var2 = numpy.var(E1)
        vars2.append(var2)
        snr = var1 / var2
        snr_list.append(snr)
    w = F_filter / (Fs / 2)
    parametersFilter = signal.butter(3, w, 'low', output='sos')
    y = signal.sosfiltfilt(parametersFilter, discrete_signals)
    fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
    s = 0
    for i in range(0, 2):
        for j in range(0, 2):
            ax[i][j].plot(x, discrete_signals[s], linewidth=1)
            s += 1
    fig.supxlabel("Час (секунди)", fontsize=14)
    fig.supylabel("Амплітуда сигналу", fontsize=14)
    fig.suptitle("Сигнал з кроком дисркетизації Dt = (2, 4, 8, 16)", fontsize=14)
    fig.savefig(f"figures/Сигнал з кроком дисркетизації Dt = (2, 4, 8, 16).png", dpi=600)
    plt.show()

    fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
    s = 0
    for i in range(0, 2):
        for j in range(0, 2):
            ax[i][j].plot(frequency_readings_center, discrete_spectrums[s], linewidth=1)
            s += 1
    fig.supxlabel("Частота(Гц)", fontsize=14)
    fig.supylabel("Амплітуда спектру", fontsize=14)
    fig.suptitle("Спектри сигналів з кроком дисркетизації Dt = (2, 4, 8, 16)", fontsize=14)
    fig.savefig(f"figures/Спектри сигналів з кроком дисркетизації Dt = (2, 4, 8, 16).png", dpi=600)
    plt.show()

    fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
    s = 0
    for i in range(0, 2):
        for j in range(0, 2):
            ax[i][j].plot(x, y[s], linewidth=1)
            s += 1
    fig.supxlabel("Час (секунди)", fontsize=14)
    fig.supylabel("Амплітуда сигналу", fontsize=14)
    fig.suptitle("Відновлені аналогові сигнали з кроком дисркетизації Dt = (2, 4, 8, 16)", fontsize=14)
    fig.savefig(f"figures/Відновлені аналогові сигнали з кроком дисркетизації Dt = (2, 4, 8, 16).png", dpi=600)
    plt.show()

    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.plot(Dt_list, vars2, linewidth=1)
    ax.set_xlabel("Крок дискретизації")
    ax.set_ylabel("Дисперсія")
    plt.title("Залежність дисперсії від кроку дискретизації", fontsize=14)
    fig.savefig(f"figures/Залежність дисперсії від кроку дискретизації.png", dpi=600)
    plt.show()

    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.plot(Dt_list, snr_list, linewidth=1)
    ax.set_xlabel("Крок дискретизації")
    ax.set_ylabel("ССШ")
    plt.title("Залежність співвідношення сигнал-шум від кроку дискретизації", fontsize=14)
    fig.savefig(f"figures/Залежність співвідношення сигнал-шум від кроку дискретизації.png", dpi=600)
    plt.show()


if __name__ == '__main__':
    main()
