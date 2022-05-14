from PyQt5 import QtWidgets, QtCore, uic
import pyqtgraph as pg

from qpsk_modulator import QpskModulator
from defaults import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Загрузка интерфейса.
        uic.loadUi("../ui/main.ui", self)

        # Инициализация графиков.
        self.curve_width = 2
        self.rpen = pg.mkPen('r', width=self.curve_width)
        self.plot(self.inputModSignal, [], [], pen=self.rpen)
        self.plot(self.outputModSignal, [], [], pen=self.rpen)
        self.plot(self.inputDemodSignal, [], [], pen=self.rpen)
        self.plot(self.outputDemodSignal, [], [], pen=self.rpen)

        # Обработчики кнопок.
        self.getInputBitsButton.clicked.connect(self.get_input_bits)
        self.doModulationButton.clicked.connect(self.do_modulation)
        self.showComponentsButton.clicked.connect(self.show_qpsk_components)
        self.showSpectrumButton.clicked.connect(self.show_spectrum)
        self.showGeneralSignal.clicked.connect(self.show_general)

        # Параметры.
        self.parameters = dict(ampl=A, sph=SP, sr=SR, sfreq=SF, dur=DUR, cobits=BITS)
        self.modulator = QpskModulator(self.parameters)
        self.demodulator = None

    def get_input_bits(self):
        """
        Получить входную последовательность бит.

        :return: None
        """
        self.modulator.generate_input_bits(self.parameters['cobits'])
        x, y = self.bits_to_plot(self.modulator.input_bits)
        self.plot(self.inputModSignal, x, y, pen=pg.mkPen('r', width=self.curve_width))

    def do_modulation(self):
        """
        Провести квадратурную модуляцию входной последовательности.

        :return: None
        """
        self.modulator.get_qpsk_components()
        self.modulator.get_qpsk_signal()
        x, y = self.graph_to_plot(self.modulator.qpsk)
        self.plot(self.outputModSignal, x, y, pen=pg.mkPen('b', width=self.curve_width))

    def show_qpsk_components(self):
        """
        Отобразить I и Q компоненты в новом окне.

        :return: None
        """
        if self.modulator.i_comp and self.modulator.q_comp:
            i_x, i_y = self.bits_to_plot(self.modulator.i_comp)
            q_x, q_y = self.bits_to_plot(self.modulator.q_comp)

            self.draw_graph("I-компонента", i_x, i_y, pg.mkPen('r', width=self.curve_width))
            self.draw_graph("Q-компонента", q_x, q_y, pg.mkPen('g', width=self.curve_width))

    def show_spectrum(self):
        """
        Отобразить спектр модулированного сигнала в новом окне.

        :return: None
        """
        if self.modulator.qpsk:
            self.modulator.get_qpsk_spectrum()
            x, y = self.graph_to_plot(self.modulator.qpsk_spectrum)
            self.draw_graph("Спектр QPSK сигнала", x, y, pg.mkPen('b', width=self.curve_width))

    def show_general(self):
        """
        Отобразить несущий сигнал в новом окне.

        :return: None
        """
        self.modulator.generate_general_signal()
        x, y = self.graph_to_plot(self.modulator.general_signal)
        self.draw_graph("Несущий сигнал", x, y, pg.mkPen('r', width=self.curve_width))

    @staticmethod
    def draw_graph(title: str, x: list, y: list, pen):
        """
        Создать график посредством pyqtgraph.

        :param title: Название графика.
        :param x: Данные по оси x.
        :param y: Данные по оси y.
        :param pen: Цвет.
        :return: None
        """
        plt = pg.plot()
        plt.setBackground((235, 235, 235))
        plt.showGrid(x=True, y=True)
        plt.setWindowTitle(title)
        plt.plot(x, y, pen=pen)

    @staticmethod
    def graph_to_plot(graphic: list):
        """
        Получить списки x, y для значений графика.

        :param graphic: Последовательность значений графика.
        :return: x, y
        """
        x = [i for i, _ in enumerate(graphic)]
        return x, graphic

    @staticmethod
    def bits_to_plot(input_bits: list):
        """
        Получить списки x, y для входной последовательности бит.

        :param input_bits: Входная последовательность бит.
        :return: x, y
        """
        x = []
        y = []
        for i in range(len(input_bits)):
            x.append(i)
            y.append(input_bits[i])
            if i < len(input_bits) - 1:
                if input_bits[i] != input_bits[i+1]:
                    x.append(i+1)
                    y.append(input_bits[i])
            else:
                x.append(i+1)
                y.append(input_bits[i])
        return x, y

    @staticmethod
    def plot(widget, x, y, pen):
        # Очистка графика.
        widget.clear()
        # Прозрачный фон.
        widget.setBackground((235, 235, 235))
        # Сетка.
        widget.showGrid(x=True, y=True, alpha=0.2)
        # Отрисовка данных.
        widget.plot(x=x, y=y, pen=pen)

    def keyPressEvent(self, event):
        """
        Обработка нажатия на кнопки.

        :param event: Событие
        :return: None
        """
        if event.key() == QtCore.Qt.Key.Key_F11:
            if not self.isMaximized():
                self.showMaximized()
            else:
                self.showNormal()

        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
