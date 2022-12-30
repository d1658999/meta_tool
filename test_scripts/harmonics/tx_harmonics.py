from pathlib import Path
from test_scripts.cmw100_items.tx_lmh import TxTestGenre
from equipments.series_basis.spectrum.fsw_series import FSW
from utils.log_init import log_set
from utils.loss_handler_harmonic import get_loss_spectrum


logger = log_set('Tx_Harmonics')


class TxHarmonics(TxTestGenre, FSW):
    def __init__(self):
        TxTestGenre.__init__(self)
        FSW.__init__(self)

    def tx_harmonics_pipline(self):
        # basic environment setting
        self.fsw.set_reference_level(-30)
        self.fsw.set_reference_level_offset(5)
        self.fsw.set_input_attenuation(1)
        self.fsw.set_freq_center(3900000)
        self.fsw.set_freq_span(1000)
        self.fsw.set_rbw(1000)
        self.fsw.set_vbw_rbw_ratio(1)
        self.fsw.set_sweep_count(20)
        self.fsw.set_sweep_time_auto('ON')
        self.fsw.set_sweep_mode('OFF')
        self.fsw.set_measure()

        # mark the peak search
        fsw.set_peak_mark_auto()

        # capture the peak of freq and level
        mark_x = fsw.get_peak_mark_x_query()
        mark_y = fsw.get_peak_mark_y_query()
        print(mark_x, mark_y)
