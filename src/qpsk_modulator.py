import random
import math
import numpy as np
import scipy.fft


class QpskModulator:
    def __init__(self, parameters):
        super(QpskModulator, self).__init__()
        self.parameters = parameters
        self.input_bits = []
        self.general_signal = []
        self.i_comp = []
        self.q_comp = []
        self.qpsk = []
        self.qpsk_spectrum = []

        # Синхронизационное время.
        self.sync_time = 0.0
        self.length = round(self.parameters["sr"] * self.parameters["dur"])

        # Несущий сигнал.
        self.generate_general_signal()

    def generate_input_bits(self, n: int):
        """
        Сгенерировать входную последовательность бит заданной длины.

        :param n: Длина последовательности.
        :return: None
        """
        self.input_bits = [random.randint(0, 1) for _ in range(n)]

    def generate_general_signal(self):
        """
        Сгенерировать несущий сигнал с заданными параметрами.

        :return: None
        """
        self.general_signal.clear()
        length = self.length + self.sync_time
        for i in np.arange(self.sync_time, length):
            w = 2. * math.pi * self.parameters['sfreq']
            self.general_signal.append(self.parameters['ampl'] *
                                       math.sin(w * i / self.parameters['sr'] + self.parameters['sph']))

        self.sync_time = length - 1

    def get_qpsk_components(self):
        """
        Выделить синфазную и квадратурную компоненты.

        :return: None
        """
        self.i_comp.clear()
        self.q_comp.clear()
        if self.input_bits:
            for i in range(len(self.input_bits)):
                if i % 2 == 0:
                    self.i_comp.append(self.input_bits[i])
                else:
                    self.q_comp.append(self.input_bits[i])

    def get_qpsk_signal(self):
        """
        Получить модулированный сигнал.

        :return: None
        """
        self.qpsk.clear()
        if self.i_comp and self.q_comp:
            iq_step = self.length / (self.parameters['cobits'] / 2.)
            for i in range(self.length):
                index = int(i / iq_step)
                w = 2. * math.pi * self.parameters['sfreq']
                i_buf = -1 if self.i_comp[index] == 0 else 1
                q_buf = -1 if self.q_comp[index] == 0 else 1
                self.qpsk.append(i_buf * math.cos(w * i / self.parameters['sr'] + self.parameters['sph']) +
                                 q_buf * math.sin(w * i / self.parameters['sr'] + self.parameters['sph']))

    def get_qpsk_spectrum(self):
        """
        Получить спектр модулированного сигнала.

        :return: None
        """
        if self.qpsk:
            self.qpsk_spectrum = list(np.abs(scipy.fft.fft(np.array(self.qpsk))))
