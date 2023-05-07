import numpy
from scipy import signal, fft
import matplotlib.pyplot as plt


def main():
    n = 500
    Fs = 1000
    FMax = 19
    randomNormal = numpy.random.normal(0, 10, n)
    x = numpy.arange(n) / Fs
    w = FMax / (Fs / 2)
    parametersFilter = signal.butter(3, w, "low", output="sos")
    y = signal.sosfiltfilt(parametersFilter, randomNormal)
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.plot(x, y, linewidth=1)
    ax.set_xlabel("Час (секунди)")
    ax.set_ylabel("Амплітуда сигналу")
    plt.title("Сигнал.png", fontsize=14)
    fig.savefig(f"figures/Сигнал.png", dpi=600)
    plt.show()
    spectrum = fft.fft(y)
    spectrumCenter = numpy.abs(fft.fftshift(spectrum))
    frequencyReadings = fft.fftfreq(n, 1 / n)
    frequencyReadingsCenter = fft.fftshift(frequencyReadings)
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.plot(frequencyReadingsCenter, spectrumCenter, linewidth=1)
    ax.set_xlabel("Частота(Гц)")
    ax.set_ylabel("Амплітуда спектру")
    plt.title("Спектр сигналу", fontsize=14)
    fig.savefig(f"figures/Спектр сигналу.png", dpi=600)
    plt.show()


if __name__ == '__main__':
    main()