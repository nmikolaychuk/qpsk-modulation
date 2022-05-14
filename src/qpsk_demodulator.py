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
