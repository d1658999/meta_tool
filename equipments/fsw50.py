from pathlib import Path
import time
from test_scripts.cmw100_items.tx_lmh import TxTestGenre
from equipments.series_basis.spectrum.fsw_series import FSW
from utils.log_init import log_set
from utils.loss_handler_harmonic import get_loss_spectrum
import utils.parameters.external_paramters as ext_pmt


logger = log_set('FSW50')
MARGIN = eval(ext_pmt.cbe_limit_margin)


class FSW50(FSW):
    def __init__(self, equipment='FSW50'):
        super().__init__(equipment)
        self.system_preset()

    def get_level_harmonics(self, tech, band, harmonic_freq, loss):
        # basic environment setting
        # self.set_reference_level(-30 - MARGIN)
        self.set_reference_level_offset(tech, band, loss)
        self.set_input_attenuation(0)
        self.set_freq_center(harmonic_freq)
        self.set_freq_span(500)  # span 500MHz
        self.set_rbw(1000)  # RBW 1MHz
        self.set_vbw_rbw_ratio(1)  # RBW/VBW ratio = 1
        self.set_sweep_count(100)  # count = 100
        self.set_sweep_time_auto('ON')  # auto sweep time dependent on span and RBW
        self.set_diplay_trace_detector()  # default use 'RMS'
        self.set_display_trace_mode(1, 'AVERage')
        self.average_type()
        self.set_sweep_mode('OFF')  # single sweep
        self.fsw.query('*OPC?')
        self.set_reference_level(-30 - MARGIN)
        self.set_measure()  # start to measure

        # mark the peak search
        self.set_peak_mark_auto()  # to activate the peak automatically

        # capture the peak of freq and level
        mark_x = self.get_peak_mark_x_query()
        mark_y = self.get_peak_mark_y_query()
        logger.info(f'Peak level: {mark_y} and response to the Freq: {mark_x}')
        return mark_x, mark_y

    def get_harmonics_order(self, tech, band, order, tx_freq):
        tx_freq_order = int(tx_freq * order)
        loss = get_loss_spectrum(tx_freq_order)
        logger.info(f'This is {order} Harmonic')
        return self.get_level_harmonics(tech, band, tx_freq_order, loss)

    def set_spur_initial(self):
        logger.info('----------select spurious emissions measurement----------')
        self.set_measurement_mode('LIST')
        self.average_type()
        self.set_display_trace_mode()
        self.set_average_count(100)
        self.set_reference_level(40)
        self.set_display_trace_mode()
        self.set_sweep_mode('OFF')
        self.get_spur_list_range_count()

    def set_spur_spec_limit_line(self, band, chan, bw1, bw2=0):  # bw2 is used for ULCA
        logger.info('----------Set Limit Line----------')
        # common parameters
        ghz = 10 ** 9
        mhz = 10 ** 6
        khz = 10 ** 3

        # do something process to tranfer string on ULCA
        if isinstance(band, str):
            band = int(band[:-1])

        else:
            pass

        # the whole body
        if band == 2:
            self.set_sweep_type('SWE')
            self.set_spur_list_range_delete(4)
            if chan == 'L':
                # range
                self.set_spur_list_range_freq_start(1, 1.84 * ghz)
                self.set_spur_list_range_freq_stop(1, 1.849 * ghz)
                self.set_spur_list_range_freq_stop(2, 1.850 * ghz)
                if (bw1 + bw2) == 1.4:
                    self.set_spur_list_range_freq_stop(3, 1.852 * ghz)
                else:
                    self.set_spur_list_range_freq_stop(3, 1.85 * ghz + bw1 * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'CFILter')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 1 * mhz)
                self.set_spur_list_range_band_vbw(1, 3 * mhz)
                if (bw1 + bw2) > 10:
                    self.set_spur_list_range_band_rbw(2, 200 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 200 * khz)
                elif (bw1 + bw2) == 1.4:
                    self.set_spur_list_range_band_rbw(2, 20 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 20 * khz)
                else:
                    self.set_spur_list_range_band_rbw(2, 10 * (bw1 + bw2) * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * (bw1 + bw2) * khz)
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(3, 30)
                self.set_spur_list_range_limit_stop(3, 30)

            elif chan == 'H':
                # range
                if (bw1 + bw2) == 1.4:
                    self.set_spur_list_range_freq_start(1, 1.908 * ghz)
                else:
                    self.set_spur_list_range_freq_start(1, 1.910 * ghz - bw1 * mhz)
                self.set_spur_list_range_freq_stop(1, 1.910 * ghz)
                self.set_spur_list_range_freq_stop(2, 1.911 * ghz)
                self.set_spur_list_range_freq_stop(3, 1.920 * ghz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'CFILter')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(3, 1 * mhz)
                self.set_spur_list_range_band_vbw(3, 3 * mhz)
                if (bw1 + bw2) > 10:
                    self.set_spur_list_range_band_rbw(2, 200 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 200 * khz)

                elif (bw1 + bw2) == 1.4:
                    self.set_spur_list_range_band_rbw(2, 20 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 20 * khz)
                else:
                    self.set_spur_list_range_band_rbw(2, 10 * (bw1 + bw2) * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * (bw1 + bw2) * khz)
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(1, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(3, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(1, 30)
                self.set_spur_list_range_limit_stop(1, 30)

            else:
                logger.info(f'Band{band} does not in FCC request for {chan}chan and BW {bw1}')
                return 1

        elif band == 4:
            self.set_spur_list_range_delete(4)
            self.set_sweep_type('SWE')
            if chan == 'L':
                # range
                self.set_spur_list_range_freq_start(1, 1.7 * ghz)
                self.set_spur_list_range_freq_stop(1, 1.709 * ghz)
                self.set_spur_list_range_freq_stop(2, 1.710 * ghz)
                if bw1 == 1.4:
                    self.set_spur_list_range_freq_stop(3, 1.712 * ghz)
                else:
                    self.set_spur_list_range_freq_stop(3, 1.710 * ghz + bw1 * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'CFILter')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 1 * mhz)
                self.set_spur_list_range_band_vbw(1, 3 * mhz)
                if bw1 > 10:
                    self.set_spur_list_range_band_rbw(2, 200 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 200 * khz)
                elif bw1 == 1.4:
                    self.set_spur_list_range_band_rbw(2, 20 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 20 * khz)
                else:
                    self.set_spur_list_range_band_rbw(2, 10 * bw1 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * bw1 * khz)
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(3, 30)
                self.set_spur_list_range_limit_stop(3, 30)

            elif chan == 'H':
                # range
                if bw1 == 1.4:
                    self.set_spur_list_range_freq_start(1, 1.753 * ghz)
                else:
                    self.set_spur_list_range_freq_start(1, 1.755 * ghz - bw1 * mhz)
                self.set_spur_list_range_freq_stop(1, 1.755 * ghz)
                self.set_spur_list_range_freq_stop(2, 1.756 * ghz)
                self.set_spur_list_range_freq_stop(3, 1.765 * ghz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'CFILter')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(3, 1 * mhz)
                self.set_spur_list_range_band_vbw(3, 3 * mhz)
                if bw1 > 10:
                    self.set_spur_list_range_band_rbw(2, 200 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 200 * khz)
                elif bw1 == 1.4:
                    self.set_spur_list_range_band_rbw(2, 20 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 20 * khz)
                else:
                    self.set_spur_list_range_band_rbw(2, 10 * bw1 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * bw1 * khz)
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(1, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(3, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(1, 30)
                self.set_spur_list_range_limit_stop(1, 30)

            else:
                logger.info(f'Band{band} does not in FCC request for {chan}chan and BW {bw1}')
                return 1

        elif band == 5:
            self.set_spur_list_range_delete(4)
            self.set_sweep_type('SWE')
            if chan == 'L':
                # range
                self.set_spur_list_range_freq_start(1, 815 * mhz)
                self.set_spur_list_range_freq_stop(1, 823 * mhz)
                self.set_spur_list_range_freq_stop(2, 824 * mhz)
                if (bw1 + bw2) == 1.4:
                    self.set_spur_list_range_freq_stop(3, 826 * mhz)
                else:
                    self.set_spur_list_range_freq_stop(3, (824 + bw1 + bw2) * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'CFILter')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)
                if (bw1 + bw2) == 1.4:
                    self.set_spur_list_range_band_rbw(2, 20 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 20 * khz)

                else:
                    self.set_spur_list_range_band_rbw(2, 10 * (bw1 + bw2) * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * (bw1 + bw2) * khz)
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(3, 30)
                self.set_spur_list_range_limit_stop(3, 30)

            elif chan == 'H':
                # range
                if (bw1 + bw2) == 1.4:
                    self.set_spur_list_range_freq_start(1, 847 * mhz)
                else:
                    self.set_spur_list_range_freq_start(1, (849 - (bw1 + bw2)) * mhz)
                self.set_spur_list_range_freq_stop(1, 849 * mhz)
                self.set_spur_list_range_freq_stop(2, 850 * mhz)
                self.set_spur_list_range_freq_stop(3, 860 * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'CFILter')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)
                if (bw1 + bw2) == 1.4:
                    self.set_spur_list_range_band_rbw(2, 20 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 20 * khz)
                else:
                    self.set_spur_list_range_band_rbw(2, 10 * (bw1 + bw2) * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * (bw1 + bw2) * khz)
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(1, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(3, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(1, 30)
                self.set_spur_list_range_limit_stop(1, 30)

            else:
                logger.info(f'Band{band} does not in FCC request for {chan}chan and BW {bw1}')
                return 1

        elif band == 7:
            self.set_sweep_type('SWE')
            if chan == 'L':
                # range
                self.set_spur_list_range_freq_start(1, 2.475 * ghz)
                if (bw1 + bw2) == 5:
                    self.set_spur_list_range_freq_stop(1, 2.494 * ghz)
                else:
                    self.set_spur_list_range_freq_stop(1, 2.49 * ghz)
                self.set_spur_list_range_freq_stop(2, 2.496 * ghz)
                self.set_spur_list_range_freq_stop(3, 2.499 * ghz)
                self.set_spur_list_range_freq_stop(4, 2.500 * ghz)
                self.set_spur_list_range_freq_stop(5, 2.500 * ghz + (bw1 + bw2) * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'NORMal')
                self.set_spur_list_range_filter_type(3, 'CFILter')
                self.set_spur_list_range_filter_type(4, 'CFILter')
                self.set_spur_list_range_filter_type(5, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 1 * mhz)
                self.set_spur_list_range_band_vbw(1, 3 * mhz)
                self.set_spur_list_range_band_rbw(2, 1 * mhz)
                self.set_spur_list_range_band_vbw(2, 3 * mhz)
                self.set_spur_list_range_band_rbw(3, 1 * mhz)
                self.set_spur_list_range_band_vbw(3, 3 * mhz)
                if (bw1 + bw2) == 20:
                    self.set_spur_list_range_band_rbw(4, 500 * khz)
                    self.set_spur_list_range_band_vbw(4, 3 * 500 * khz)
                elif (bw1 + bw2) > 20:
                    self.set_spur_list_range_band_rbw(4, 1 * mhz)
                    self.set_spur_list_range_band_vbw(4, 3 * 1 * mhz)
                else:
                    self.set_spur_list_range_band_rbw(4, 20 * bw1 * khz)
                    self.set_spur_list_range_band_vbw(4, 3 * 20 * bw1 * khz)
                self.set_spur_list_range_band_rbw(5, 100 * khz)
                self.set_spur_list_range_band_vbw(5, 3 * 100 * khz)

                # att
                for r in range(5):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 2001)
                self.set_spur_list_range_sweep_point(2, 2001)
                self.set_spur_list_range_sweep_point(3, 2001)
                self.set_spur_list_range_sweep_point(4, 2001)
                self.set_spur_list_range_sweep_point(5, 2001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -25 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -25 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(3, -10 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -10 - MARGIN)
                self.set_spur_list_range_limit_start(4, -10 - MARGIN)
                self.set_spur_list_range_limit_stop(4, -10 - MARGIN)
                self.set_spur_list_range_limit_start(5, 30)
                self.set_spur_list_range_limit_stop(5, 30)

            elif chan == 'H':
                # range
                self.set_spur_list_range_freq_start(1, 2.57 * ghz - (bw1 + bw2) * mhz)
                self.set_spur_list_range_freq_stop(1, 2.57 * ghz)
                self.set_spur_list_range_freq_stop(2, 2.571 * ghz)
                self.set_spur_list_range_freq_stop(3, 2.575 * ghz)
                if bw1 == 5:
                    self.set_spur_list_range_freq_stop(4, 2.576 * ghz)
                else:
                    self.set_spur_list_range_freq_stop(4, 2.57 * ghz + (bw1 + bw2) * mhz)
                if (bw1 + bw2) > 20:
                    self.set_spur_list_range_freq_stop(5, 2.615 * ghz)
                else:
                    self.set_spur_list_range_freq_stop(5, 2.595 * ghz)

                # filter type
                self.set_spur_list_range_filter_type(5, 'NORMal')
                self.set_spur_list_range_filter_type(4, 'NORMal')
                self.set_spur_list_range_filter_type(3, 'CFILter')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(1, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(5, 1 * mhz)
                self.set_spur_list_range_band_vbw(5, 3 * mhz)
                self.set_spur_list_range_band_rbw(4, 1 * mhz)
                self.set_spur_list_range_band_vbw(4, 3 * mhz)
                self.set_spur_list_range_band_rbw(3, 1 * mhz)
                self.set_spur_list_range_band_vbw(3, 3 * mhz)
                if (bw1 + bw2) == 20:
                    self.set_spur_list_range_band_rbw(2, 500 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 500 * khz)
                elif (bw1 + bw2) > 20:
                    self.set_spur_list_range_band_rbw(2, 1 * mhz)
                    self.set_spur_list_range_band_vbw(2, 3 * 1 * mhz)
                else:
                    self.set_spur_list_range_band_rbw(2, 20 * bw1 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 20 * bw1 * khz)
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)

                # att
                for r in range(5):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(5, 2001)
                self.set_spur_list_range_sweep_point(4, 2001)
                self.set_spur_list_range_sweep_point(3, 2001)
                self.set_spur_list_range_sweep_point(2, 2001)
                self.set_spur_list_range_sweep_point(1, 2001)

                # Abs Limit
                self.set_spur_list_range_limit_start(5, -25 - MARGIN)
                self.set_spur_list_range_limit_stop(5, -25 - MARGIN)
                self.set_spur_list_range_limit_start(4, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(4, -13 - MARGIN)
                self.set_spur_list_range_limit_start(3, -10 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -10 - MARGIN)
                self.set_spur_list_range_limit_start(2, -10 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -10 - MARGIN)
                self.set_spur_list_range_limit_start(1, 30)
                self.set_spur_list_range_limit_stop(1, 30)

            else:
                logger.info(f'Band{band} does not in FCC request for {chan}chan and BW {bw1 + bw2}')
                return 1

        elif band == 12:
            self.set_spur_list_range_delete(4)
            self.set_sweep_type('SWE')
            if chan == 'L':
                # range
                self.set_spur_list_range_freq_start(1, 690 * mhz)
                self.set_spur_list_range_freq_stop(1, 698.9 * mhz)
                self.set_spur_list_range_freq_stop(2, 699 * mhz)
                if bw1 == 1.4:
                    self.set_spur_list_range_freq_stop(3, (699 + 2) * mhz)
                else:
                    self.set_spur_list_range_freq_stop(3, (699 + bw1) * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'CFILter')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(2, 30 * khz)
                self.set_spur_list_range_band_vbw(2, 3 * 30 * khz)
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(3, 30)
                self.set_spur_list_range_limit_stop(3, 30)

            elif chan == 'H':
                # range
                if bw1 == 1.4:
                    self.set_spur_list_range_freq_start(1, (716 - 2) * mhz)
                else:
                    self.set_spur_list_range_freq_start(1, (716 - bw1) * mhz)
                self.set_spur_list_range_freq_stop(1, 716 * mhz)
                self.set_spur_list_range_freq_stop(2, 716.1 * mhz)
                self.set_spur_list_range_freq_stop(3, 725 * mhz)

                # filter type
                self.set_spur_list_range_filter_type(3, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(1, 'CFILter')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(2, 30 * khz)
                self.set_spur_list_range_band_vbw(2, 3 * 30 * khz)
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(1, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(3, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(1, 30)
                self.set_spur_list_range_limit_stop(1, 30)

            else:
                logger.info(f'Band{band} does not in FCC request for {chan}chan and BW {bw1}')
                return 1

        elif band == 13:
            self.set_sweep_type('SWE')
            if chan and bw1:
                # range
                self.set_spur_list_range_freq_start(1, 763 * mhz)
                self.set_spur_list_range_freq_stop(1, 775 * mhz)
                self.set_spur_list_range_freq_stop(2, 775.9 * mhz)
                self.set_spur_list_range_freq_stop(3, 776 * mhz)
                self.set_spur_list_range_freq_start(4, 776 * mhz)
                self.set_spur_list_range_freq_stop(4, 788 * mhz)
                self.set_spur_list_range_freq_stop(5, 788.1 * mhz)
                self.set_spur_list_range_freq_stop(6, 793 * mhz)
                self.set_spur_list_range_freq_stop(7, 806.1 * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'CFILter')
                self.set_spur_list_range_filter_type(4, 'Normal')
                self.set_spur_list_range_filter_type(5, 'CFILter')
                self.set_spur_list_range_filter_type(6, 'CFILter')
                self.set_spur_list_range_filter_type(7, 'Normal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 6.25 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 6.25 * khz)
                self.set_spur_list_range_band_rbw(2, 100 * khz)
                self.set_spur_list_range_band_vbw(2, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(3, 30 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 30 * khz)
                self.set_spur_list_range_band_rbw(4, 100 * khz)
                self.set_spur_list_range_band_vbw(4, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(5, 30 * khz)
                self.set_spur_list_range_band_vbw(5, 3 * 30 * khz)
                self.set_spur_list_range_band_rbw(6, 100 * khz)
                self.set_spur_list_range_band_vbw(6, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(7, 6.25 * khz)
                self.set_spur_list_range_band_vbw(7, 3 * 6.25 * khz)

                # att
                for r in range(7):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(4, 1001)
                self.set_spur_list_range_sweep_point(5, 1001)
                self.set_spur_list_range_sweep_point(6, 1001)
                self.set_spur_list_range_sweep_point(7, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -35)
                self.set_spur_list_range_limit_stop(1, -35)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(3, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -13 - MARGIN)
                self.set_spur_list_range_limit_start(4, 30)
                self.set_spur_list_range_limit_stop(4, 30)
                self.set_spur_list_range_limit_start(5, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(5, -13 - MARGIN)
                self.set_spur_list_range_limit_start(6, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(6, -13 - MARGIN)
                self.set_spur_list_range_limit_start(7, -35)
                self.set_spur_list_range_limit_stop(7, -35)

        elif band == 14:
            self.set_sweep_type('SWE')
            if chan and bw1:
                # range
                self.set_spur_list_range_freq_start(1, 758 * mhz)
                self.set_spur_list_range_freq_stop(1, 769 * mhz)
                self.set_spur_list_range_freq_stop(2, 775 * mhz)
                self.set_spur_list_range_freq_stop(3, 788 * mhz)
                self.set_spur_list_range_freq_start(4, 788 * mhz)
                self.set_spur_list_range_freq_stop(4, 799 * mhz)
                self.set_spur_list_range_freq_stop(5, 805 * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'NORMal')
                self.set_spur_list_range_filter_type(3, 'CFILter')
                self.set_spur_list_range_filter_type(4, 'Normal')
                self.set_spur_list_range_filter_type(5, 'Normal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(2, 6.25 * khz)
                self.set_spur_list_range_band_vbw(2, 3 * 6.25 * khz)
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(4, 100 * khz)
                self.set_spur_list_range_band_vbw(4, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(5, 6.25 * khz)
                self.set_spur_list_range_band_vbw(5, 3 * 6.25 * khz)

                # att
                for r in range(5):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(4, 1001)
                self.set_spur_list_range_sweep_point(5, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -35)
                self.set_spur_list_range_limit_stop(2, -35)
                self.set_spur_list_range_limit_start(3, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -13 - MARGIN)
                self.set_spur_list_range_limit_start(4, 30)
                self.set_spur_list_range_limit_stop(4, 30)
                self.set_spur_list_range_limit_start(5, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(5, -13 - MARGIN)

        elif band == 17:
            self.set_spur_list_range_delete(4)
            self.set_sweep_type('SWE')
            if chan == 'L':
                # range
                self.set_spur_list_range_freq_start(1, 690 * mhz)
                self.set_spur_list_range_freq_stop(1, 703.9 * mhz)
                self.set_spur_list_range_freq_stop(2, 704 * mhz)
                self.set_spur_list_range_freq_stop(3, (704 + bw1) * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'CFILter')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(2, 30 * khz)
                self.set_spur_list_range_band_vbw(2, 3 * 30 * khz)
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(3, 30)
                self.set_spur_list_range_limit_stop(3, 30)

            elif chan == 'H':
                # range
                self.set_spur_list_range_freq_start(1, (716 - bw1) * mhz)
                self.set_spur_list_range_freq_stop(1, 716 * mhz)
                self.set_spur_list_range_freq_stop(2, 716.1 * mhz)
                self.set_spur_list_range_freq_stop(3, 725 * mhz)

                # filter type
                self.set_spur_list_range_filter_type(3, 'CFILter')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(1, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(2, 30 * khz)
                self.set_spur_list_range_band_vbw(2, 3 * 30 * khz)
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(1, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(3, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(1, 30)
                self.set_spur_list_range_limit_stop(1, 30)

            else:
                logger.info(f'Band{band} does not in FCC request for {chan}chan and BW {bw1}')
                return 1

        elif band == 25:
            self.set_spur_list_range_delete(4)
            self.set_sweep_type('SWE')
            if chan == 'L':
                # range
                self.set_spur_list_range_freq_start(1, 1840 * mhz)
                self.set_spur_list_range_freq_stop(1, 1849 * mhz)
                self.set_spur_list_range_freq_stop(2, 1850 * mhz)
                if bw1 == 1.4:
                    self.set_spur_list_range_freq_stop(3, (1850 + 2) * mhz)
                else:
                    self.set_spur_list_range_freq_stop(3, (1850 + bw1) * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'CFILter')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 1 * mhz)
                self.set_spur_list_range_band_vbw(1, 3 * 1 * mhz)
                if bw1 == 1.4:
                    self.set_spur_list_range_band_rbw(2, 10 * 2 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * 2 * khz)
                else:
                    self.set_spur_list_range_band_rbw(2, 10 * bw1 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * bw1 * khz)
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 2001)
                self.set_spur_list_range_sweep_point(2, 2001)
                self.set_spur_list_range_sweep_point(3, 2001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(3, 30)
                self.set_spur_list_range_limit_stop(3, 30)

            elif chan == 'H':
                # range
                if bw1 == 1.4:
                    self.set_spur_list_range_freq_start(1, (1915 - 2) * mhz)
                else:
                    self.set_spur_list_range_freq_start(1, (1915 - bw1) * mhz)
                self.set_spur_list_range_freq_stop(1, 1915 * mhz)
                self.set_spur_list_range_freq_stop(2, 1916 * mhz)
                self.set_spur_list_range_freq_stop(3, 1925 * mhz)

                # filter type
                self.set_spur_list_range_filter_type(3, 'CFILter')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(1, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(3, 1 * mhz)
                self.set_spur_list_range_band_vbw(3, 3 * 1 * mhz)
                if bw1 == 1.4:
                    self.set_spur_list_range_band_rbw(2, 10 * 2 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * 2 * khz)
                else:
                    self.set_spur_list_range_band_rbw(2, 10 * bw1 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * bw1 * khz)
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(3, 2001)
                self.set_spur_list_range_sweep_point(2, 2001)
                self.set_spur_list_range_sweep_point(1, 2001)

                # Abs Limit
                self.set_spur_list_range_limit_start(3, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(1, 30)
                self.set_spur_list_range_limit_stop(1, 30)

            else:
                logger.info(f'Band{band} does not in FCC request for {chan}chan and BW {bw1}')
                return 1

        elif band == 26:
            """
            there are two ceritfication for B26, split it by 824MHz to 26-L/26-H 
            so, Lch use 26-L, Hch use 26-H
            """
            self.set_spur_list_range_delete(4)
            self.set_sweep_type('SWE')
            # if chan == 'L':
            #     # range
            #     self.set_spur_list_range_freq_start(1, 815 * mhz)
            #     self.set_spur_list_range_freq_stop(1, 823 * mhz)
            #     self.set_spur_list_range_freq_stop(2, 824 * mhz)
            #     self.set_spur_list_range_freq_stop(3, (824 + bw1) * mhz)
            #
            #     # filter type
            #     self.set_spur_list_range_filter_type(1, 'NORMal')
            #     self.set_spur_list_range_filter_type(2, 'CFILter')
            #     self.set_spur_list_range_filter_type(3, 'NORMal')
            #
            #     # rbw/vbw
            #     self.set_spur_list_range_band_rbw(1, 1 * mhz)
            #     self.set_spur_list_range_band_vbw(1, 3 * mhz)
            #     if (bw1 + bw2) > 10:
            #         self.set_spur_list_range_band_rbw(2, 200 * khz)
            #         self.set_spur_list_range_band_vbw(2, 3 * 200 * khz)
            #     elif (bw1 + bw2) == 1.4:
            #         self.set_spur_list_range_band_rbw(2, 20 * khz)
            #         self.set_spur_list_range_band_vbw(2, 3 * 20 * khz)
            #
            #     else:
            #         self.set_spur_list_range_band_rbw(2, 10 * bw1 * khz)
            #         self.set_spur_list_range_band_vbw(2, 3 * 10 * bw1 * khz)
            #     self.set_spur_list_range_band_rbw(3, 100 * khz)
            #     self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)
            #
            #     # att
            #     for r in range(3):
            #         r_num = r + 1
            #         self.set_spur_list_range_input_attenuation(r_num, 30)
            #
            #     # sweep points
            #     self.set_spur_list_range_sweep_point(1, 404)
            #     self.set_spur_list_range_sweep_point(2, 2001)
            #     self.set_spur_list_range_sweep_point(3, 2001)
            #
            #     # Abs Limit
            #     self.set_spur_list_range_limit_start(1, -13 - MARGIN)
            #     self.set_spur_list_range_limit_stop(1, -13 - MARGIN)
            #     self.set_spur_list_range_limit_start(2, -13 - MARGIN)
            #     self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
            #     self.set_spur_list_range_limit_start(3, 30)
            #     self.set_spur_list_range_limit_stop(3, 30)
            if chan == 'L' and bw1 == 15:
                # range
                self.set_spur_list_range_freq_start(1, 806.5 * mhz)
                self.set_spur_list_range_freq_stop(1, 813.962 * mhz)
                self.set_spur_list_range_freq_stop(2, 814 * mhz)
                self.set_spur_list_range_freq_stop(3, 829 * mhz)
                self.set_spur_list_range_freq_stop(4, 829.038 * mhz)
                self.set_spur_list_range_freq_stop(5, 836.5 * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'NORMal')
                self.set_spur_list_range_filter_type(3, 'NORMal')
                self.set_spur_list_range_filter_type(4, 'NORMal')
                self.set_spur_list_range_filter_type(5, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(2, 300)
                self.set_spur_list_range_band_vbw(2, 1 * khz)
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(4, 300)
                self.set_spur_list_range_band_vbw(4, 1 * khz)
                self.set_spur_list_range_band_rbw(5, 100 * khz)
                self.set_spur_list_range_band_vbw(5, 3 * 100 * khz)

                # att
                for r in range(5):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(4, 1001)
                self.set_spur_list_range_sweep_point(5, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -20 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -20 - MARGIN)
                self.set_spur_list_range_limit_start(3, 30)
                self.set_spur_list_range_limit_stop(3, 30)
                self.set_spur_list_range_limit_start(4, -20 - MARGIN)
                self.set_spur_list_range_limit_stop(4, -20 - MARGIN)
                self.set_spur_list_range_limit_start(5, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(5, -13 - MARGIN)

            elif chan == 'L' and bw1 == 10:
                # range
                self.set_spur_list_range_freq_start(1, 809 * mhz)
                self.set_spur_list_range_freq_stop(1, 813.962 * mhz)
                self.set_spur_list_range_freq_stop(2, 814 * mhz)
                self.set_spur_list_range_freq_stop(3, 824 * mhz)
                self.set_spur_list_range_freq_stop(4, 824.038 * mhz)
                self.set_spur_list_range_freq_stop(5, 829 * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'NORMal')
                self.set_spur_list_range_filter_type(3, 'NORMal')
                self.set_spur_list_range_filter_type(4, 'NORMal')
                self.set_spur_list_range_filter_type(5, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(2, 300)
                self.set_spur_list_range_band_vbw(2, 1 * khz)
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(4, 300)
                self.set_spur_list_range_band_vbw(4, 1 * khz)
                self.set_spur_list_range_band_rbw(5, 100 * khz)
                self.set_spur_list_range_band_vbw(5, 3 * 100 * khz)

                # att
                for r in range(5):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(4, 1001)
                self.set_spur_list_range_sweep_point(5, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -20 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -20 - MARGIN)
                self.set_spur_list_range_limit_start(3, 30)
                self.set_spur_list_range_limit_stop(3, 30)
                self.set_spur_list_range_limit_start(4, -20 - MARGIN)
                self.set_spur_list_range_limit_stop(4, -20 - MARGIN)
                self.set_spur_list_range_limit_start(5, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(5, -13 - MARGIN)

            elif chan == 'L' and bw1 == 5:
                # range
                self.set_spur_list_range_freq_start(1, 809 * mhz)
                self.set_spur_list_range_freq_stop(1, 813.962 * mhz)
                self.set_spur_list_range_freq_stop(2, 814 * mhz)
                self.set_spur_list_range_freq_stop(3, 819 * mhz)
                self.set_spur_list_range_freq_stop(4, 819.038 * mhz)
                self.set_spur_list_range_freq_stop(5, 824 * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'NORMal')
                self.set_spur_list_range_filter_type(3, 'NORMal')
                self.set_spur_list_range_filter_type(4, 'NORMal')
                self.set_spur_list_range_filter_type(5, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(2, 300)
                self.set_spur_list_range_band_vbw(2, 1 * khz)
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(4, 300)
                self.set_spur_list_range_band_vbw(4, 1 * khz)
                self.set_spur_list_range_band_rbw(5, 100 * khz)
                self.set_spur_list_range_band_vbw(5, 3 * 100 * khz)

                # att
                for r in range(5):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(4, 1001)
                self.set_spur_list_range_sweep_point(5, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -20 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -20 - MARGIN)
                self.set_spur_list_range_limit_start(3, 30)
                self.set_spur_list_range_limit_stop(3, 30)
                self.set_spur_list_range_limit_start(4, -20 - MARGIN)
                self.set_spur_list_range_limit_stop(4, -20 - MARGIN)
                self.set_spur_list_range_limit_start(5, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(5, -13 - MARGIN)

            elif chan == 'L' and bw1 == 3:
                # range
                self.set_spur_list_range_freq_start(1, 810.5 * mhz)
                self.set_spur_list_range_freq_stop(1, 813.962 * mhz)
                self.set_spur_list_range_freq_stop(2, 814 * mhz)
                self.set_spur_list_range_freq_stop(3, 817 * mhz)
                self.set_spur_list_range_freq_stop(4, 817.038 * mhz)
                self.set_spur_list_range_freq_stop(5, 820.5 * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'NORMal')
                self.set_spur_list_range_filter_type(3, 'NORMal')
                self.set_spur_list_range_filter_type(4, 'NORMal')
                self.set_spur_list_range_filter_type(5, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(2, 300)
                self.set_spur_list_range_band_vbw(2, 1 * khz)
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(4, 300)
                self.set_spur_list_range_band_vbw(4, 1 * khz)
                self.set_spur_list_range_band_rbw(5, 100 * khz)
                self.set_spur_list_range_band_vbw(5, 3 * 100 * khz)

                # att
                for r in range(5):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(4, 1001)
                self.set_spur_list_range_sweep_point(5, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -20 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -20 - MARGIN)
                self.set_spur_list_range_limit_start(3, 30)
                self.set_spur_list_range_limit_stop(3, 30)
                self.set_spur_list_range_limit_start(4, -20 - MARGIN)
                self.set_spur_list_range_limit_stop(4, -20 - MARGIN)
                self.set_spur_list_range_limit_start(5, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(5, -13 - MARGIN)

            elif chan == 'L' and bw1 == 1.4:
                # range
                self.set_spur_list_range_freq_start(1, 811.7 * mhz)
                self.set_spur_list_range_freq_stop(1, 813.9625 * mhz)
                self.set_spur_list_range_freq_stop(2, 814 * mhz)
                self.set_spur_list_range_freq_stop(3, 815.4 * mhz)
                self.set_spur_list_range_freq_stop(4, 815.4375 * mhz)
                self.set_spur_list_range_freq_stop(5, 817.7 * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'NORMal')
                self.set_spur_list_range_filter_type(3, 'NORMal')
                self.set_spur_list_range_filter_type(4, 'NORMal')
                self.set_spur_list_range_filter_type(5, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(2, 300)
                self.set_spur_list_range_band_vbw(2, 1 * khz)
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(4, 300)
                self.set_spur_list_range_band_vbw(4, 1 * khz)
                self.set_spur_list_range_band_rbw(5, 100 * khz)
                self.set_spur_list_range_band_vbw(5, 3 * 100 * khz)

                # att
                for r in range(5):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(4, 1001)
                self.set_spur_list_range_sweep_point(5, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -20 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -20 - MARGIN)
                self.set_spur_list_range_limit_start(3, 30)
                self.set_spur_list_range_limit_stop(3, 30)
                self.set_spur_list_range_limit_start(4, -20 - MARGIN)
                self.set_spur_list_range_limit_stop(4, -20 - MARGIN)
                self.set_spur_list_range_limit_start(5, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(5, -13 - MARGIN)

            elif chan == 'H':
                # range
                self.set_spur_list_range_freq_start(1, (849 - bw1) * mhz)
                self.set_spur_list_range_freq_stop(1, 849 * mhz)
                self.set_spur_list_range_freq_stop(2, 850 * mhz)
                self.set_spur_list_range_freq_stop(3, 860 * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'CFILter')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)
                if (bw1 + bw2) > 10:
                    self.set_spur_list_range_band_rbw(2, 200 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 200 * khz)
                elif (bw1 + bw2) == 1.4:
                    self.set_spur_list_range_band_rbw(2, 20 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 20 * khz)
                else:
                    self.set_spur_list_range_band_rbw(2, 10 * bw1 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * bw1 * khz)
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(1, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(3, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(1, 30)
                self.set_spur_list_range_limit_stop(1, 30)

            else:
                logger.info(f'Band{band} does not in FCC request for {chan}chan and BW {bw1}')
                return 1

        elif band == 30:
            self.set_sweep_type('SWE')
            if chan == 'L' and bw1 == 5:
                # range
                self.set_spur_list_range_freq_start(1, 2.288 * ghz)
                self.set_spur_list_range_freq_stop(1, 2.292 * ghz)
                self.set_spur_list_range_freq_stop(2, 2.296 * ghz)
                self.set_spur_list_range_freq_stop(3, 2.3 * ghz)
                self.set_spur_list_range_freq_stop(4, 2.304 * ghz)
                self.set_spur_list_range_freq_stop(5, 2.305 * ghz)
                self.set_spur_list_range_freq_stop(6, 2.310 * ghz)
                self.set_spur_list_range_freq_stop(7, 2.311 * ghz)
                self.set_spur_list_range_freq_stop(8, 2.320 * ghz)
                self.set_spur_list_range_freq_stop(9, 2.324 * ghz)
                self.set_spur_list_range_freq_stop(10, 2.328 * ghz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'NORMal')
                self.set_spur_list_range_filter_type(3, 'NORMal')
                self.set_spur_list_range_filter_type(4, 'CFILter')
                self.set_spur_list_range_filter_type(5, 'CFILter')
                self.set_spur_list_range_filter_type(6, 'NORMmal')
                self.set_spur_list_range_filter_type(7, 'CFILter')
                self.set_spur_list_range_filter_type(8, 'CFILter')
                self.set_spur_list_range_filter_type(9, 'NORMal')
                self.set_spur_list_range_filter_type(10, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 1 * mhz)
                self.set_spur_list_range_band_vbw(1, 3 * mhz)
                self.set_spur_list_range_band_rbw(2, 1 * mhz)
                self.set_spur_list_range_band_vbw(2, 3 * mhz)
                self.set_spur_list_range_band_rbw(3, 1 * mhz)
                self.set_spur_list_range_band_vbw(3, 3 * mhz)
                self.set_spur_list_range_band_rbw(4, 1 * mhz)
                self.set_spur_list_range_band_vbw(4, 3 * mhz)
                self.set_spur_list_range_band_rbw(5, 50 * khz)
                self.set_spur_list_range_band_vbw(5, 3 * 50 * khz)
                self.set_spur_list_range_band_rbw(6, 100 * khz)
                self.set_spur_list_range_band_vbw(6, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(7, 50 * khz)
                self.set_spur_list_range_band_vbw(7, 3 * 50 * khz)
                self.set_spur_list_range_band_rbw(8, 1 * mhz)
                self.set_spur_list_range_band_vbw(8, 3 * mhz)
                self.set_spur_list_range_band_rbw(9, 1 * mhz)
                self.set_spur_list_range_band_vbw(9, 3 * mhz)
                self.set_spur_list_range_band_rbw(10, 1 * mhz)
                self.set_spur_list_range_band_vbw(10, 3 * mhz)

                # att
                for r in range(10):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(4, 1001)
                self.set_spur_list_range_sweep_point(5, 1001)
                self.set_spur_list_range_sweep_point(6, 1001)
                self.set_spur_list_range_sweep_point(7, 1001)
                self.set_spur_list_range_sweep_point(8, 1001)
                self.set_spur_list_range_sweep_point(9, 1001)
                self.set_spur_list_range_sweep_point(10, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -37 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -37 - MARGIN)
                self.set_spur_list_range_limit_start(2, -31 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -31 - MARGIN)
                self.set_spur_list_range_limit_start(3, -25 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -25 - MARGIN)
                self.set_spur_list_range_limit_start(4, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(4, -13 - MARGIN)
                self.set_spur_list_range_limit_start(5, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(5, -13 - MARGIN)
                self.set_spur_list_range_limit_start(6, 30)
                self.set_spur_list_range_limit_stop(6, 30)
                self.set_spur_list_range_limit_start(7, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(7, -13 - MARGIN)
                self.set_spur_list_range_limit_start(8, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(8, -13 - MARGIN)
                self.set_spur_list_range_limit_start(9, -25 - MARGIN)
                self.set_spur_list_range_limit_stop(9, -25 - MARGIN)
                self.set_spur_list_range_limit_start(10, -31 - MARGIN)
                self.set_spur_list_range_limit_stop(10, -31 - MARGIN)

            elif chan == 'H' and bw1 == 5:
                # range
                self.set_spur_list_range_freq_start(1, 2.288 * ghz)
                self.set_spur_list_range_freq_stop(1, 2.292 * ghz)
                self.set_spur_list_range_freq_stop(2, 2.296 * ghz)
                self.set_spur_list_range_freq_stop(3, 2.3 * ghz)
                self.set_spur_list_range_freq_stop(4, 2.309 * ghz)
                self.set_spur_list_range_freq_stop(5, 2.310 * ghz)
                self.set_spur_list_range_freq_stop(6, 2.315 * ghz)
                self.set_spur_list_range_freq_stop(7, 2.316 * ghz)
                self.set_spur_list_range_freq_stop(8, 2.320 * ghz)
                self.set_spur_list_range_freq_stop(9, 2.324 * ghz)
                self.set_spur_list_range_freq_stop(10, 2.328 * ghz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'NORMal')
                self.set_spur_list_range_filter_type(3, 'NORMal')
                self.set_spur_list_range_filter_type(4, 'CFILter')
                self.set_spur_list_range_filter_type(5, 'CFILter')
                self.set_spur_list_range_filter_type(6, 'NORMal')
                self.set_spur_list_range_filter_type(7, 'CFILter')
                self.set_spur_list_range_filter_type(8, 'CFILter')
                self.set_spur_list_range_filter_type(9, 'NORMal')
                self.set_spur_list_range_filter_type(10, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 1 * mhz)
                self.set_spur_list_range_band_vbw(1, 3 * mhz)
                self.set_spur_list_range_band_rbw(2, 1 * mhz)
                self.set_spur_list_range_band_vbw(2, 3 * mhz)
                self.set_spur_list_range_band_rbw(3, 1 * mhz)
                self.set_spur_list_range_band_vbw(3, 3 * mhz)
                self.set_spur_list_range_band_rbw(4, 1 * mhz)
                self.set_spur_list_range_band_vbw(4, 3 * mhz)
                self.set_spur_list_range_band_rbw(5, 50 * khz)
                self.set_spur_list_range_band_vbw(5, 3 * 50 * khz)
                self.set_spur_list_range_band_rbw(6, 100 * khz)
                self.set_spur_list_range_band_vbw(6, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(7, 50 * khz)
                self.set_spur_list_range_band_vbw(7, 3 * 50 * khz)
                self.set_spur_list_range_band_rbw(8, 1 * mhz)
                self.set_spur_list_range_band_vbw(8, 3 * mhz)
                self.set_spur_list_range_band_rbw(9, 1 * mhz)
                self.set_spur_list_range_band_vbw(9, 3 * mhz)
                self.set_spur_list_range_band_rbw(10, 1 * mhz)
                self.set_spur_list_range_band_vbw(10, 3 * mhz)

                # att
                for r in range(10):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(4, 1001)
                self.set_spur_list_range_sweep_point(5, 1001)
                self.set_spur_list_range_sweep_point(6, 1001)
                self.set_spur_list_range_sweep_point(7, 1001)
                self.set_spur_list_range_sweep_point(8, 1001)
                self.set_spur_list_range_sweep_point(9, 1001)
                self.set_spur_list_range_sweep_point(10, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -37 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -37 - MARGIN)
                self.set_spur_list_range_limit_start(2, -31 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -31 - MARGIN)
                self.set_spur_list_range_limit_start(3, -25 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -25 - MARGIN)
                self.set_spur_list_range_limit_start(4, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(4, -13 - MARGIN)
                self.set_spur_list_range_limit_start(5, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(5, -13 - MARGIN)
                self.set_spur_list_range_limit_start(6, 30)
                self.set_spur_list_range_limit_stop(6, 30)
                self.set_spur_list_range_limit_start(7, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(7, -13 - MARGIN)
                self.set_spur_list_range_limit_start(8, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(8, -13 - MARGIN)
                self.set_spur_list_range_limit_start(9, -25 - MARGIN)
                self.set_spur_list_range_limit_stop(9, -25 - MARGIN)
                self.set_spur_list_range_limit_start(10, -31 - MARGIN)
                self.set_spur_list_range_limit_stop(10, -31 - MARGIN)

            elif chan == 'M' and bw1 == 10:
                # range
                self.set_spur_list_range_freq_start(1, 2.288 * ghz)
                self.set_spur_list_range_freq_stop(1, 2.292 * ghz)
                self.set_spur_list_range_freq_stop(2, 2.296 * ghz)
                self.set_spur_list_range_freq_stop(3, 2.3 * ghz)
                self.set_spur_list_range_freq_stop(4, 2.304 * ghz)
                self.set_spur_list_range_freq_stop(5, 2.305 * ghz)
                self.set_spur_list_range_freq_stop(6, 2.315 * ghz)
                self.set_spur_list_range_freq_stop(7, 2.316 * ghz)
                self.set_spur_list_range_freq_stop(8, 2.320 * ghz)
                self.set_spur_list_range_freq_stop(9, 2.324 * ghz)
                self.set_spur_list_range_freq_stop(10, 2.328 * ghz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'NORMal')
                self.set_spur_list_range_filter_type(3, 'Normal')
                self.set_spur_list_range_filter_type(4, 'CFILter')
                self.set_spur_list_range_filter_type(5, 'CFILter')
                self.set_spur_list_range_filter_type(6, 'Normal')
                self.set_spur_list_range_filter_type(7, 'CFILter')
                self.set_spur_list_range_filter_type(8, 'CFILter')
                self.set_spur_list_range_filter_type(9, 'NORMal')
                self.set_spur_list_range_filter_type(10, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 1 * mhz)
                self.set_spur_list_range_band_vbw(1, 3 * mhz)
                self.set_spur_list_range_band_rbw(2, 1 * mhz)
                self.set_spur_list_range_band_vbw(2, 3 * mhz)
                self.set_spur_list_range_band_rbw(3, 1 * mhz)
                self.set_spur_list_range_band_vbw(3, 3 * mhz)
                self.set_spur_list_range_band_rbw(4, 1 * mhz)
                self.set_spur_list_range_band_vbw(4, 3 * mhz)
                self.set_spur_list_range_band_rbw(5, 100 * khz)
                self.set_spur_list_range_band_vbw(5, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(6, 100 * khz)
                self.set_spur_list_range_band_vbw(6, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(7, 100 * khz)
                self.set_spur_list_range_band_vbw(7, 3 * 100 * khz)
                self.set_spur_list_range_band_rbw(8, 1 * mhz)
                self.set_spur_list_range_band_vbw(8, 3 * mhz)
                self.set_spur_list_range_band_rbw(9, 1 * mhz)
                self.set_spur_list_range_band_vbw(9, 3 * mhz)
                self.set_spur_list_range_band_rbw(10, 1 * mhz)
                self.set_spur_list_range_band_vbw(10, 3 * mhz)

                # att
                for r in range(10):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(4, 1001)
                self.set_spur_list_range_sweep_point(5, 1001)
                self.set_spur_list_range_sweep_point(6, 1001)
                self.set_spur_list_range_sweep_point(7, 1001)
                self.set_spur_list_range_sweep_point(8, 1001)
                self.set_spur_list_range_sweep_point(9, 1001)
                self.set_spur_list_range_sweep_point(10, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -37 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -37 - MARGIN)
                self.set_spur_list_range_limit_start(2, -31 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -31 - MARGIN)
                self.set_spur_list_range_limit_start(3, -25 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -25 - MARGIN)
                self.set_spur_list_range_limit_start(4, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(4, -13 - MARGIN)
                self.set_spur_list_range_limit_start(5, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(5, -13 - MARGIN)
                self.set_spur_list_range_limit_start(6, 30)
                self.set_spur_list_range_limit_stop(6, 30)
                self.set_spur_list_range_limit_start(7, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(7, -13 - MARGIN)
                self.set_spur_list_range_limit_start(8, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(8, -13 - MARGIN)
                self.set_spur_list_range_limit_start(9, -25 - MARGIN)
                self.set_spur_list_range_limit_stop(9, -25 - MARGIN)
                self.set_spur_list_range_limit_start(10, -31 - MARGIN)
                self.set_spur_list_range_limit_stop(10, -31 - MARGIN)

            else:
                logger.info(f'Band{band} does not in FCC request for {chan}chan and BW {bw1}')
                return 1

        elif band == 38:
            self.set_sweep_type('SWE')
            if chan == 'L':
                # range
                self.set_spur_list_range_freq_start(1, 2.545 * ghz)
                if (bw1 + bw2) == 5:
                    self.set_spur_list_range_freq_stop(1, 2.545 * ghz + 19 * mhz)
                else:
                    self.set_spur_list_range_freq_stop(1, 2.545 * ghz + (25 - bw1 - bw2) * mhz)
                self.set_spur_list_range_freq_stop(2, 2.565 * ghz)
                self.set_spur_list_range_freq_stop(3, 2.569 * ghz)
                self.set_spur_list_range_freq_stop(4, 2.57 * ghz)
                self.set_spur_list_range_freq_stop(5, 2.57 * ghz + (bw1 + bw2) * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'NORMal')
                self.set_spur_list_range_filter_type(3, 'CFILter')
                self.set_spur_list_range_filter_type(4, 'CFILter')
                self.set_spur_list_range_filter_type(5, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 1 * mhz)
                self.set_spur_list_range_band_vbw(1, 3 * mhz)
                self.set_spur_list_range_band_rbw(2, 1 * mhz)
                self.set_spur_list_range_band_vbw(2, 3 * mhz)
                self.set_spur_list_range_band_rbw(3, 1 * mhz)
                self.set_spur_list_range_band_vbw(3, 3 * mhz)
                if bw1 + bw2 > 15:
                    self.set_spur_list_range_band_rbw(4, 500 * khz)
                    self.set_spur_list_range_band_vbw(4, 1500 * khz)
                else:
                    self.set_spur_list_range_band_rbw(4, 20 * (bw1 + bw2) * khz)
                    self.set_spur_list_range_band_vbw(4, 3 * 20 * (bw1 + bw2) * khz)
                self.set_spur_list_range_band_rbw(5, 100 * khz)
                self.set_spur_list_range_band_vbw(5, 300 * khz)

                # att
                for r in range(5):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 2001)
                self.set_spur_list_range_sweep_point(2, 2001)
                self.set_spur_list_range_sweep_point(3, 2001)
                self.set_spur_list_range_sweep_point(4, 2001)
                self.set_spur_list_range_sweep_point(5, 2001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -25 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -25 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(3, -10 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -10 - MARGIN)
                self.set_spur_list_range_limit_start(4, -10 - MARGIN)
                self.set_spur_list_range_limit_stop(4, -10 - MARGIN)
                self.set_spur_list_range_limit_start(5, 30)
                self.set_spur_list_range_limit_stop(5, 30)

            elif chan == 'H':
                # range
                self.set_spur_list_range_freq_start(1, 2.62 * ghz - (bw1 + bw2) * mhz)
                self.set_spur_list_range_freq_stop(1, 2.62 * ghz)
                self.set_spur_list_range_freq_stop(2, 2.621 * ghz)
                self.set_spur_list_range_freq_stop(3, 2.625 * ghz)
                if (bw1 + bw2) == 5:
                    self.set_spur_list_range_freq_stop(4, 2.626 * ghz)
                else:
                    self.set_spur_list_range_freq_stop(4, 2.62 * ghz + (bw1 + bw2) * mhz)
                self.set_spur_list_range_freq_stop(5, 2.645 * ghz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'CFILter')
                self.set_spur_list_range_filter_type(4, 'NORMal')
                self.set_spur_list_range_filter_type(5, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(5, 1 * mhz)
                self.set_spur_list_range_band_vbw(5, 3 * mhz)
                self.set_spur_list_range_band_rbw(4, 1 * mhz)
                self.set_spur_list_range_band_vbw(4, 3 * mhz)
                self.set_spur_list_range_band_rbw(3, 1 * mhz)
                self.set_spur_list_range_band_vbw(3, 3 * mhz)
                if bw1 + bw2 > 15:
                    self.set_spur_list_range_band_rbw(2, 500 * khz)
                    self.set_spur_list_range_band_vbw(2, 1500 * khz)
                else:
                    self.set_spur_list_range_band_rbw(2, 20 * (bw1 + bw2) * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 20 * (bw1 + bw2) * khz)
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 300 * khz)

                # att
                for r in range(5):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(5, 2001)
                self.set_spur_list_range_sweep_point(4, 2001)
                self.set_spur_list_range_sweep_point(3, 2001)
                self.set_spur_list_range_sweep_point(2, 2001)
                self.set_spur_list_range_sweep_point(1, 2001)

                # Abs Limit
                self.set_spur_list_range_limit_start(5, -25 - MARGIN)
                self.set_spur_list_range_limit_stop(5, -25 - MARGIN)
                self.set_spur_list_range_limit_start(4, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(4, -13 - MARGIN)
                self.set_spur_list_range_limit_start(3, -10 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -10 - MARGIN)
                self.set_spur_list_range_limit_start(2, -10 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -10 - MARGIN)
                self.set_spur_list_range_limit_start(1, 30)
                self.set_spur_list_range_limit_stop(1, 30)

            else:
                logger.info(f'Band{band} does not in FCC request for {chan}chan and BW {bw1 + bw2}')
                return 1

        elif band == 41:
            self.set_sweep_type('SWE')
            if chan == 'L':
                # range
                self.set_spur_list_range_freq_start(1, 2.475 * ghz)
                self.set_spur_list_range_freq_stop(1, 2.4905 * ghz)
                self.set_spur_list_range_freq_stop(2, 2.495 * ghz)
                self.set_spur_list_range_freq_stop(3, 2.496 * ghz)
                self.set_spur_list_range_freq_stop(4, 2.496 * ghz + (bw1 + bw2) * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'CFILter')
                self.set_spur_list_range_filter_type(4, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 1 * mhz)
                self.set_spur_list_range_band_vbw(1, 3 * mhz)
                self.set_spur_list_range_band_rbw(2, 1 * mhz)
                self.set_spur_list_range_band_vbw(2, 3 * mhz)
                if bw1 + bw2 > 30:
                    self.set_spur_list_range_band_rbw(3, 500 * khz)
                    self.set_spur_list_range_band_vbw(3, 1500 * khz)
                else:
                    self.set_spur_list_range_band_rbw(3, 10 * (bw1 + bw2) * khz)
                    self.set_spur_list_range_band_vbw(3, 3 * 10 * (bw1 + bw2) * khz)
                self.set_spur_list_range_band_rbw(4, 100 * khz)
                self.set_spur_list_range_band_vbw(4, 300 * khz)

                # att
                for r in range(4):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 2001)
                self.set_spur_list_range_sweep_point(2, 2001)
                self.set_spur_list_range_sweep_point(3, 2001)
                self.set_spur_list_range_sweep_point(4, 2001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -25 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -25 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(3, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -13 - MARGIN)
                self.set_spur_list_range_limit_start(4, 30)
                self.set_spur_list_range_limit_stop(4, 30)

            elif chan == 'H':
                # range
                self.set_spur_list_range_freq_start(1, 2.69 * ghz - (bw1 + bw2) * mhz)
                self.set_spur_list_range_freq_stop(1, 2.69 * ghz)
                self.set_spur_list_range_freq_stop(2, 2.691 * ghz)
                self.set_spur_list_range_freq_stop(3, 2.695 * ghz)
                if (bw1 + bw2) == 5:
                    self.set_spur_list_range_freq_stop(4, 2.696 * ghz)
                else:
                    self.set_spur_list_range_freq_stop(4, 2.69 * ghz + (bw1 + bw2) * mhz)
                # if (bw1 + bw2) < 50:
                self.set_spur_list_range_freq_stop(5, 2.69 * ghz + (bw1 + bw2 + 5) * mhz)
                # else:
                #     self.set_spur_list_range_freq_stop(5, 2.795 * ghz)  # for 100MHz, so extend lager range

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'CFILter')
                self.set_spur_list_range_filter_type(4, 'NORMal')
                self.set_spur_list_range_filter_type(5, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(5, 1 * mhz)
                self.set_spur_list_range_band_vbw(5, 3 * mhz)
                self.set_spur_list_range_band_rbw(4, 1 * mhz)
                self.set_spur_list_range_band_vbw(4, 3 * mhz)
                self.set_spur_list_range_band_rbw(3, 1 * mhz)
                self.set_spur_list_range_band_vbw(3, 3 * mhz)
                if (bw1 + bw2) > 35:
                    self.set_spur_list_range_band_rbw(2, 1 * mhz)
                    self.set_spur_list_range_band_vbw(2, 3 * 1 * mhz)
                elif (bw1 + bw2) > 15:
                    self.set_spur_list_range_band_rbw(2, 500 * khz)
                    self.set_spur_list_range_band_vbw(2, 1500 * khz)
                else:
                    self.set_spur_list_range_band_rbw(2, 20 * (bw1 + bw2) * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 20 * (bw1 + bw2) * khz)
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 300 * khz)

                # att
                for r in range(5):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(5, 2001)
                self.set_spur_list_range_sweep_point(4, 2001)
                self.set_spur_list_range_sweep_point(3, 2001)
                self.set_spur_list_range_sweep_point(2, 2001)
                self.set_spur_list_range_sweep_point(1, 2001)

                # Abs Limit
                self.set_spur_list_range_limit_start(5, -25 - MARGIN)
                self.set_spur_list_range_limit_stop(5, -25 - MARGIN)
                self.set_spur_list_range_limit_start(4, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(4, -13 - MARGIN)
                self.set_spur_list_range_limit_start(3, -10 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -10 - MARGIN)
                self.set_spur_list_range_limit_start(2, -10 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -10 - MARGIN)
                self.set_spur_list_range_limit_start(1, 30)
                self.set_spur_list_range_limit_stop(1, 30)

            else:
                logger.info(f'Band{band} does not in FCC request for {chan}chan and BW {bw1 + bw2}')
                return 1

        elif band == 66:
            self.set_sweep_type('SWE')
            self.set_spur_list_range_delete(4)
            if chan == 'L':
                # range
                self.set_spur_list_range_freq_start(1, 1.7 * ghz)
                self.set_spur_list_range_freq_stop(1, 1.709 * ghz)
                self.set_spur_list_range_freq_stop(2, 1.71 * ghz)
                if (bw1 + bw2) == 1.4:
                    self.set_spur_list_range_freq_stop(3, 1.712 * ghz)
                else:
                    self.set_spur_list_range_freq_stop(3, 1.71 * ghz + (bw1 + bw2) * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'CFILter')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 1 * mhz)
                self.set_spur_list_range_band_vbw(1, 3 * mhz)
                if (bw1 + bw2) > 10:
                    self.set_spur_list_range_band_rbw(2, 200 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 200 * khz)
                elif (bw1 + bw2) == 1.4:
                    self.set_spur_list_range_band_rbw(2, 20 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 20 * khz)

                else:
                    self.set_spur_list_range_band_rbw(2, 10 * (bw1 + bw2) * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * (bw1 + bw2) * khz)
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(3, 30)
                self.set_spur_list_range_limit_stop(3, 30)

            elif chan == 'H':
                # range
                if (bw1 + bw2) == 1.4:
                    self.set_spur_list_range_freq_start(1, 1.778 * ghz)
                else:
                    self.set_spur_list_range_freq_start(1, 1.78 * ghz - (bw1 + bw2) * mhz)
                self.set_spur_list_range_freq_stop(1, 1.78 * ghz)
                self.set_spur_list_range_freq_stop(2, 1.781 * ghz)
                self.set_spur_list_range_freq_stop(3, 1.79 * ghz + (bw1 + bw2))

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'CFILter')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(3, 1 * mhz)
                self.set_spur_list_range_band_vbw(3, 3 * mhz)
                if (bw1 + bw2) > 10:
                    self.set_spur_list_range_band_rbw(2, 200 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 200 * khz)
                elif (bw1 + bw2) == 1.4:
                    self.set_spur_list_range_band_rbw(2, 20 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 20 * khz)
                else:
                    self.set_spur_list_range_band_rbw(2, 10 * (bw1 + bw2) * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * (bw1 + bw2) * khz)
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(1, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(3, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(1, 30)
                self.set_spur_list_range_limit_stop(1, 30)

            else:
                logger.info(f'Band{band} does not in FCC request for {chan}chan and BW {bw1 + bw2}')
                return 1

        elif band == 71:
            self.set_sweep_type('SWE')
            self.set_spur_list_range_delete(4)
            if chan == 'L':
                # range
                self.set_spur_list_range_freq_start(1, 652 * mhz)
                self.set_spur_list_range_freq_stop(1, 662 * mhz)
                self.set_spur_list_range_freq_stop(2, 663 * mhz)
                self.set_spur_list_range_freq_stop(3, (663 + bw1) * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'CFILter')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)
                if bw1 > 10:
                    self.set_spur_list_range_band_rbw(2, 10 * 20 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * 20 * khz)
                else:
                    self.set_spur_list_range_band_rbw(2, 10 * bw1 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * bw1 * khz)
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(3, 30)
                self.set_spur_list_range_limit_stop(3, 30)

            elif chan == 'H':
                # range
                self.set_spur_list_range_freq_start(1, (698 - bw1) * mhz)
                self.set_spur_list_range_freq_stop(1, 698 * mhz)
                if bw1 == 5:
                    self.set_spur_list_range_freq_stop(2, 698.1 * mhz)
                else:
                    self.set_spur_list_range_freq_stop(2, 699 * mhz)
                self.set_spur_list_range_freq_stop(3, 709 * mhz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'CFILter')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(3, 100 * khz)
                self.set_spur_list_range_band_vbw(3, 3 * 100 * khz)
                if bw1 > 10:
                    self.set_spur_list_range_band_rbw(2, 10 * 20 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * 20 * khz)
                else:
                    self.set_spur_list_range_band_rbw(2, 10 * bw1 * khz)
                    self.set_spur_list_range_band_vbw(2, 3 * 10 * bw1 * khz)
                self.set_spur_list_range_band_rbw(1, 100 * khz)
                self.set_spur_list_range_band_vbw(1, 3 * 100 * khz)

                # att
                for r in range(3):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(2, 1001)
                self.set_spur_list_range_sweep_point(1, 1001)

                # Abs Limit
                self.set_spur_list_range_limit_start(3, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(1, 30)
                self.set_spur_list_range_limit_stop(1, 30)

            else:
                logger.info(f'Band{band} does not in FCC request for {chan}chan and BW {bw1}')
                return 1

        elif band == 48:
            self.set_sweep_type('SWE')
            if chan == 'L':
                # range
                self.set_spur_list_range_freq_start(1, 3.43 * ghz)
                self.set_spur_list_range_freq_stop(1, 3.53 * ghz)
                self.set_spur_list_range_freq_stop(2, 3.54 * ghz)
                self.set_spur_list_range_freq_stop(3, 3.549 * ghz)
                self.set_spur_list_range_freq_stop(4, 3.55 * ghz)
                if (bw1 + bw2) > 10:
                    self.set_spur_list_range_freq_stop(5, 3.55 * ghz + (bw1 + bw2) * mhz)
                    self.set_spur_list_range_freq_stop(6, 3.551 * ghz + (bw1 + bw2) * mhz)
                    self.set_spur_list_range_freq_stop(7, 3.570 * ghz + (bw1 + bw2) * mhz)
                    self.set_spur_list_range_freq_stop(8, 3.60 * ghz + (bw1 + bw2) * mhz)
                else:
                    self.set_spur_list_range_freq_stop(5, 3.56 * ghz)
                    self.set_spur_list_range_freq_stop(6, 3.561 * ghz)
                    self.set_spur_list_range_freq_stop(7, 3.570 * ghz)
                    self.set_spur_list_range_freq_stop(8, 3.61 * ghz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'NORMal')
                self.set_spur_list_range_filter_type(3, 'CFILter')
                self.set_spur_list_range_filter_type(4, 'CFILter')
                self.set_spur_list_range_filter_type(5, 'NORMal')
                self.set_spur_list_range_filter_type(6, 'CFILter')
                self.set_spur_list_range_filter_type(7, 'CFILter')
                self.set_spur_list_range_filter_type(8, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(1, 1 * mhz)
                self.set_spur_list_range_band_vbw(1, 3 * mhz)
                self.set_spur_list_range_band_rbw(2, 1 * mhz)
                self.set_spur_list_range_band_vbw(2, 3 * mhz)
                self.set_spur_list_range_band_rbw(3, 1 * mhz)
                self.set_spur_list_range_band_vbw(3, 3 * mhz)
                if 20 >= (bw1 + bw2) > 10:
                    self.set_spur_list_range_band_rbw(4, 200 * khz)
                    self.set_spur_list_range_band_vbw(4, 3 * 200 * khz)
                elif (bw1 + bw2) > 20:
                    self.set_spur_list_range_band_rbw(4, 500 * khz)
                    self.set_spur_list_range_band_vbw(4, 3 * 500 * khz)
                else:
                    self.set_spur_list_range_band_rbw(4, 10 * (bw1 + bw2) * khz)
                    self.set_spur_list_range_band_vbw(4, 3 * 10 * (bw1 + bw2) * khz)
                self.set_spur_list_range_band_rbw(5, 100 * khz)
                self.set_spur_list_range_band_vbw(5, 3 * 100 * khz)
                if 20 >= (bw1 + bw2) > 10:
                    self.set_spur_list_range_band_rbw(6, 200 * khz)
                    self.set_spur_list_range_band_vbw(6, 3 * 200 * khz)
                elif (bw1 + bw2) > 20:
                    self.set_spur_list_range_band_rbw(6, 500 * khz)
                    self.set_spur_list_range_band_vbw(6, 3 * 500 * khz)
                else:
                    self.set_spur_list_range_band_rbw(6, 10 * (bw1 + bw2) * khz)
                    self.set_spur_list_range_band_vbw(6, 3 * 10 * (bw1 + bw2) * khz)
                self.set_spur_list_range_band_rbw(7, 1 * mhz)
                self.set_spur_list_range_band_vbw(7, 3 * mhz)
                self.set_spur_list_range_band_rbw(8, 1 * mhz)
                self.set_spur_list_range_band_vbw(8, 3 * mhz)

                # att
                for r in range(8):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(1, 401)
                self.set_spur_list_range_sweep_point(2, 401)
                self.set_spur_list_range_sweep_point(3, 401)
                self.set_spur_list_range_sweep_point(4, 1001)
                self.set_spur_list_range_sweep_point(5, 1001)
                self.set_spur_list_range_sweep_point(6, 1001)
                self.set_spur_list_range_sweep_point(7, 401)
                self.set_spur_list_range_sweep_point(8, 401)

                # Abs Limit
                self.set_spur_list_range_limit_start(1, -40 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -40 - MARGIN)
                self.set_spur_list_range_limit_start(2, -25 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -25 - MARGIN)
                self.set_spur_list_range_limit_start(3, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -13 - MARGIN)
                self.set_spur_list_range_limit_start(4, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(4, -13 - MARGIN)
                self.set_spur_list_range_limit_start(5, 30)
                self.set_spur_list_range_limit_stop(5, 30)
                self.set_spur_list_range_limit_start(6, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(6, -13 - MARGIN)
                self.set_spur_list_range_limit_start(7, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(7, -13 - MARGIN)
                self.set_spur_list_range_limit_start(8, -25 - MARGIN)
                self.set_spur_list_range_limit_stop(8, -25 - MARGIN)

            elif chan == 'H':
                # range
                if (bw1 + bw2) > 10:
                    self.set_spur_list_range_freq_start(1, 3.650 * ghz - (bw1 + bw2) * mhz)
                    self.set_spur_list_range_freq_stop(1, 3.680 * ghz - (bw1 + bw2) * mhz)
                    self.set_spur_list_range_freq_stop(2, 3.699 * ghz - (bw1 + bw2) * mhz)
                    self.set_spur_list_range_freq_stop(3, 3.700 * ghz - (bw1 + bw2) * mhz)
                else:
                    self.set_spur_list_range_freq_start(1, 3.64 * ghz)
                    self.set_spur_list_range_freq_stop(1, 3.68 * ghz)
                    self.set_spur_list_range_freq_stop(2, 3.689 * ghz)
                    self.set_spur_list_range_freq_stop(3, 3.69 * ghz)
                self.set_spur_list_range_freq_stop(4, 3.7 * ghz)
                self.set_spur_list_range_freq_stop(5, 3.701 * ghz)
                self.set_spur_list_range_freq_stop(6, 3.71 * ghz)
                self.set_spur_list_range_freq_stop(7, 3.72 * ghz)
                self.set_spur_list_range_freq_stop(8, 3.85 * ghz)

                # filter type
                self.set_spur_list_range_filter_type(1, 'NORMal')
                self.set_spur_list_range_filter_type(2, 'CFILter')
                self.set_spur_list_range_filter_type(3, 'CFILter')
                self.set_spur_list_range_filter_type(4, 'NORMal')
                self.set_spur_list_range_filter_type(5, 'CFILter')
                self.set_spur_list_range_filter_type(6, 'CFILter')
                self.set_spur_list_range_filter_type(7, 'NORMal')
                self.set_spur_list_range_filter_type(8, 'NORMal')

                # rbw/vbw
                self.set_spur_list_range_band_rbw(8, 1 * mhz)
                self.set_spur_list_range_band_vbw(8, 3 * mhz)
                self.set_spur_list_range_band_rbw(7, 1 * mhz)
                self.set_spur_list_range_band_vbw(7, 3 * mhz)
                self.set_spur_list_range_band_rbw(6, 1 * mhz)
                self.set_spur_list_range_band_vbw(6, 3 * mhz)
                if 20 >= (bw1 + bw2) > 10:
                    self.set_spur_list_range_band_rbw(5, 200 * khz)
                    self.set_spur_list_range_band_vbw(5, 3 * 200 * khz)
                elif (bw1 + bw2) > 20:
                    self.set_spur_list_range_band_rbw(5, 500 * khz)
                    self.set_spur_list_range_band_vbw(5, 3 * 500 * khz)
                else:
                    self.set_spur_list_range_band_rbw(5, 10 * (bw1 + bw2) * khz)
                    self.set_spur_list_range_band_vbw(5, 3 * 10 * (bw1 + bw2) * khz)
                self.set_spur_list_range_band_rbw(4, 100 * khz)
                self.set_spur_list_range_band_vbw(4, 3 * 100 * khz)
                if 20 >= (bw1 + bw2) > 10:
                    self.set_spur_list_range_band_rbw(3, 200 * khz)
                    self.set_spur_list_range_band_vbw(3, 3 * 200 * khz)
                elif (bw1 + bw2) > 20:
                    self.set_spur_list_range_band_rbw(3, 500 * khz)
                    self.set_spur_list_range_band_vbw(3, 3 * 500 * khz)
                else:
                    self.set_spur_list_range_band_rbw(3, 10 * (bw1 + bw2) * khz)
                    self.set_spur_list_range_band_vbw(3, 3 * 10 * (bw1 + bw2) * khz)
                self.set_spur_list_range_band_rbw(2, 1 * mhz)
                self.set_spur_list_range_band_vbw(2, 3 * mhz)
                self.set_spur_list_range_band_rbw(1, 1 * mhz)
                self.set_spur_list_range_band_vbw(1, 3 * mhz)

                # att
                for r in range(8):
                    r_num = r + 1
                    self.set_spur_list_range_input_attenuation(r_num, 30)

                # sweep points
                self.set_spur_list_range_sweep_point(8, 401)
                self.set_spur_list_range_sweep_point(7, 401)
                self.set_spur_list_range_sweep_point(6, 401)
                self.set_spur_list_range_sweep_point(5, 1001)
                self.set_spur_list_range_sweep_point(4, 1001)
                self.set_spur_list_range_sweep_point(3, 1001)
                self.set_spur_list_range_sweep_point(2, 401)
                self.set_spur_list_range_sweep_point(1, 401)

                # Abs Limit
                self.set_spur_list_range_limit_start(8, -40 - MARGIN)
                self.set_spur_list_range_limit_stop(8, -40 - MARGIN)
                self.set_spur_list_range_limit_start(7, -25 - MARGIN)
                self.set_spur_list_range_limit_stop(7, -25 - MARGIN)
                self.set_spur_list_range_limit_start(6, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(6, -13 - MARGIN)
                self.set_spur_list_range_limit_start(5, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(5, -13 - MARGIN)
                self.set_spur_list_range_limit_start(4, 30)
                self.set_spur_list_range_limit_stop(4, 30)
                self.set_spur_list_range_limit_start(3, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(3, -13 - MARGIN)
                self.set_spur_list_range_limit_start(2, -13 - MARGIN)
                self.set_spur_list_range_limit_stop(2, -13 - MARGIN)
                self.set_spur_list_range_limit_start(1, -25 - MARGIN)
                self.set_spur_list_range_limit_stop(1, -25 - MARGIN)

            else:
                logger.info(f'Band{band} does not in FCC request for {chan}chan and BW {bw1}')
                return 1

        else:
            logger.info(f'Band{band} does not in FCC request')
            return 1

    def get_spur_screenshot(self, local_file_path):
        self.set_screenshot_format('PNG')
        temp_file_fsw = r"C:\temp\screenshot.png"
        self.set_file_path(temp_file_fsw)
        self.print_screenshot()
        time.sleep(1)
        data = self.get_data_query(r"C:\temp\screenshot.png")
        self.save_file(local_file_path, data)

    @staticmethod
    def save_file(local_file_path, data):
        with open(local_file_path, 'wb') as f:  # open a local file for writing binary data
            f.write(data)  # write the binary data of screenshot to local file


def main():
    test = FSW50()
    test.set_spur_initial()
    # # test.set_freq_center(2501000)
    # # test.set_freq_span(100)
    band = 48
    chan = 'L'
    bw1 = 10
    bw2 = 0
    test.set_spur_spec_limit_line(band, chan, bw1, bw2)
    test.set_suprious_emissions_measure()
    test.fsw_query('*OPC?')
    # time.sleep(10)
    # test.fsw_write('MMEM:NAME "C:\\temp\\screenshot.png"')  # set the file name for saving screenshot on CMW100
    # test.fsw_write('HCOP:DEV:LANG PNG')  # set the file format for saving screenshot on CMW100
    # test.fsw_write('HCOP:IMM')  # trigger a screenshot on CMW100
    test.set_file_path(r"C:\temp\screenshot.png")
    test.set_screenshot_format('PNG')
    test.print_screenshot()
    time.sleep(1)  # wait for 1 second for screenshot to be saved
    # data = test.fsw_query_2('MMEM:DATA? "C:\\temp\\screenshot.png"')  # read the binary data of screenshot from CMW100
    data = test.get_data_query(r"C:\temp\screenshot.png")
    # with open('screenshot.png', 'wb') as f:  # open a local file for writing binary data
    #     f.write(data)  # write the binary data of screenshot to local file
    n = 2
    test.save_file(f'screenshot{n}.png', data)
    test.fsw_close()  # close the connection


if __name__ == '__main__':
    main()
