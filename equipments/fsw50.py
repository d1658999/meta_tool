from pathlib import Path
import time
from test_scripts.cmw100_items.tx_lmh import TxTestGenre
from equipments.series_basis.spectrum.fsw_series import FSW
from utils.log_init import log_set
from utils.loss_handler_harmonic import get_loss_spectrum


logger = log_set('FSW50')


class FSW50(FSW):
    def __init__(self, equipment='FSW50'):
        super().__init__(equipment)

    def get_level_harmonics(self, band, harmonic_freq, loss):
        # basic environment setting
        # self.set_reference_level(-30)
        self.set_reference_level_offset(band, loss)
        self.set_input_attenuation(0)
        self.set_freq_center(harmonic_freq)
        self.set_freq_span(500)  # span 500MHz
        self.set_rbw(1000)  # RBW 1MHz
        self.set_vbw_rbw_ratio(1)  # RBW/VBW ratio = 1
        self.set_sweep_count(100)  # count = 100
        self.set_sweep_time_auto('ON')  # auto sweep time dependent on span and RBW
        self.set_diplay_trace_detector()  # default use 'RMS'
        self.set_display_trace_mode(1, 'AVERage')
        self.set_sweep_mode('OFF')  # single sweep
        self.fsw.query('*OPC?')
        self.set_reference_level(-30)
        self.set_measure()  # start to measure

        # mark the peak search
        self.set_peak_mark_auto()  # to activate the peak automatically

        # capture the peak of freq and level
        mark_x = self.get_peak_mark_x_query()
        mark_y = self.get_peak_mark_y_query()
        logger.info(f'Peak level: {mark_y} and response to the Freq: {mark_x}')
        return mark_x, mark_y

    def get_harmonics_order(self, band, order, tx_freq):
        tx_freq_order = int(tx_freq * order)
        loss = get_loss_spectrum(tx_freq_order)
        logger.info(f'This is {order} Harmonic')
        return self.get_level_harmonics(band, tx_freq_order, loss)
