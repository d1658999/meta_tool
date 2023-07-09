from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
from equipments.cmw100 import CMW100
from utils.log_init import log_set
import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
from utils.loss_handler import get_loss
from utils.excel_handler import tx_power_fcc_ce_export_excel_ftm
import utils.parameters.rb_parameters as rb_pmt
import utils.parameters.fcc as fcc
import utils.parameters.ce as ce

logger = log_set('tx_fcc_ce')


class TxTestFccCe(AtCmd, CMW100):
    def __init__(self):
        AtCmd.__init__(self)
        CMW100.__init__(self)
        self.chan_mark = None
        self.rb_state = None
        self.script = None
        self.file_path = None
        self.srs_path_enable = ext_pmt.srs_path_enable
        self.port_table = None
        self.port_mimo_tx1 = None
        self.port_mimo_tx2 = None

    def port_table_selector(self, band, tx_path='TX1'):
        """
        This is used for multi-ports connection on Tx
        """
        if self.port_table is None:  # to initial port table at first time
            if ext_pmt.asw_path_enable is False:
                txas_select = 0
                self.port_table = self.port_tx_table(txas_select)
            else:
                self.port_table = self.port_tx_table(self.asw_path)

        if ext_pmt.port_table_en and tx_path in ['TX1', 'TX2']:
            self.port_tx = int(self.port_table[tx_path][str(band)])

        elif ext_pmt.port_table_en and tx_path in ['MIMO']:
            self.port_mimo_tx1 = int(self.port_table['MIMO_TX1'][str(band)])
            self.port_mimo_tx2 = int(self.port_table['MIMO_TX2'][str(band)])

        else:
            pass

    def select_asw_srs_path(self):
        if self.srs_path_enable:
            self.srs_switch()
        else:
            self.antenna_switch_v2()

    def tx_power_pipline_fcc_fr1(self):  # band > bw > mcs > rb
        self.tx_level = ext_pmt.tx_level
        self.port_tx = ext_pmt.port_tx
        self.sa_nsa_mode = ext_pmt.sa_nsa
        items = [
            (tech, tx_path, bw, band, type_)
            for tech in ext_pmt.tech
            for tx_path in ext_pmt.tx_paths
            for bw in ext_pmt.fr1_bandwidths
            for band in ext_pmt.fr1_bands
            for type_ in ext_pmt.type_fr1
        ]

        for item in items:
            if item[0] == 'FR1' and ext_pmt.fr1_bands != []:
                self.tech = item[0]
                self.tx_path = item[1]
                self.bw_fr1 = item[2]
                self.band_fr1 = item[3]
                self.type_fr1 = item[4]
                try:
                    self.port_table_selector(self.band_fr1, self.tx_path)
                    if self.bw_fr1 in cm_pmt_ftm.bandwidths_selected_fr1(self.band_fr1):
                        self.tx_power_fcc_fr1()
                    else:
                        logger.info(f'B{self.band_fr1} does not have BW {self.bw_fr1}MHZ')

                except KeyError:
                    logger.info(f'NR Band {self.band_fr1} does not have this tx path {self.tx_path}')

    def tx_power_fcc_fr1(self):
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('FR1', self.band_fr1,
                                                   self.bw_fr1)  # [L_rx_freq, M_rx_ferq, H_rx_freq]
        self.rx_freq_fr1 = rx_freq_list[1]
        self.loss_rx = self.loss_selector(rx_freq_list[1], ext_pmt.fdc_en)
        self.loss_tx = self.loss_selector(cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, self.rx_freq_fr1), ext_pmt.fdc_en)
        logger.info('----------Test FCC LMH progress---------')
        self.preset_instrument()
        self.set_measurement_group_gprf()
        self.set_test_end_fr1()
        self.set_test_mode_fr1()
        self.select_asw_srs_path()
        self.cmw_query('*OPC?')

        tx_freq_select_list = []
        try:
            tx_freq_select_list = [int(freq * 1000) for freq in
                                   fcc.tx_freq_list_fr1[self.band_fr1][self.bw_fr1]]  # band > bw > tx_fre1_list
        except KeyError as err:
            logger.info(f"this Band: {err} don't have to  test this BW: {self.bw_fr1} for FCC")

        for mcs in ext_pmt.mcs_fr1:
            self.mcs_fr1 = mcs
            for script in ext_pmt.scripts:
                if script == 'FCC':
                    self.script = script
                    self.rb_state = 'FCC'
                    try:
                        for self.rb_size_fr1, self.rb_start_fr1 in \
                                rb_pmt.FCC_FR1[self.band_fr1][self.bw_fr1][self.mcs_fr1]:

                            for num, tx_freq_fr1 in enumerate(tx_freq_select_list):
                                self.chan_mark = f'chan{num}'
                                self.tx_freq_fr1 = tx_freq_fr1
                                self.tx_power_fcc_subprocess_fr1()

                                if self.tx_path in ['TX1', 'TX2']:  # this is for TX1, TX2, not MIMO
                                    # ready to export to excel
                                    self.parameters = {
                                        'script': self.script,
                                        'tech': self.tech,
                                        'band': self.band_fr1,
                                        'bw': self.bw_fr1,
                                        'rb_size': self.rb_size_fr1,
                                        'rb_start': self.rb_start_fr1,
                                        'tx_level': self.tx_level,
                                        'mcs': self.mcs_fr1,
                                        'tx_path': self.tx_path,
                                    }
                                    self.file_path = tx_power_fcc_ce_export_excel_ftm(self.data, self.parameters)

                    except KeyError as err:
                        logger.debug(f'show error: {err}')
                        logger.info(
                            f"Band {self.band_fr1}, BW: {self.bw_fr1} don't need to test this MCS: {self.mcs_fr1} "
                            f"for FCC")
        self.set_test_end_fr1()

    def tx_power_pipline_ce_fr1(self):  # band > bw > mcs > rb
        self.tx_level = ext_pmt.tx_level
        self.port_tx = ext_pmt.port_tx
        self.sa_nsa_mode = ext_pmt.sa_nsa
        items = [
            (tech, tx_path, bw, band, type_)
            for tech in ext_pmt.tech
            for tx_path in ext_pmt.tx_paths
            for bw in ext_pmt.fr1_bandwidths
            for band in ext_pmt.fr1_bands
            for type_ in ext_pmt.type_fr1
        ]

        for item in items:
            if item[0] == 'FR1' and ext_pmt.fr1_bands != []:
                self.tech = item[0]
                self.tx_path = item[1]
                self.bw_fr1 = item[2]
                self.band_fr1 = item[3]
                self.type_fr1 = item[4]
                try:
                    self.port_table_selector(self.band_fr1, self.tx_path)
                    if self.bw_fr1 in cm_pmt_ftm.bandwidths_selected_fr1(self.band_fr1):
                        self.tx_power_ce_fr1()
                    else:
                        logger.info(f'B{self.band_fr1} does not have BW {self.bw_fr1}MHZ')
                except KeyError:
                    logger.info(f'NR Band {self.band_fr1} does not have this tx path {self.tx_path}')

    def tx_power_ce_fr1(self):
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('FR1', self.band_fr1,
                                                   self.bw_fr1)  # [L_rx_freq, M_rx_ferq, H_rx_freq]
        self.rx_freq_fr1 = rx_freq_list[1]
        self.loss_rx = self.loss_selector(rx_freq_list[1], ext_pmt.fdc_en)
        self.loss_tx = self.loss_selector(cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, self.rx_freq_fr1), ext_pmt.fdc_en)
        logger.info('----------Test CE LMH progress---------')
        self.preset_instrument()
        self.set_measurement_group_gprf()
        self.set_test_end_fr1()
        self.set_test_mode_fr1()
        self.select_asw_srs_path()

        tx_freq_select_list = []
        try:
            tx_freq_select_list = [int(freq * 1000) for freq in
                                   ce.tx_freq_list_fr1[self.band_fr1][self.bw_fr1]]  # band > bw > tx_fre1_list
        except KeyError as err:
            logger.info(f"this Band: {err} don't have to  test this BW: {self.bw_fr1} for CE")

        for mcs in ext_pmt.mcs_fr1:
            self.mcs_fr1 = mcs
            for script in ext_pmt.scripts:
                if script == 'CE':
                    self.script = script
                    self.rb_state = 'CE'
                    try:
                        for self.rb_size_fr1, self.rb_start_fr1 in \
                                rb_pmt.CE_FR1[self.band_fr1][self.bw_fr1][self.mcs_fr1]:

                            for num, tx_freq_fr1 in enumerate(tx_freq_select_list):
                                self.chan_mark = f'chan{num}'
                                self.tx_freq_fr1 = tx_freq_fr1
                                self.tx_power_ce_subprocess_fr1()

                                if self.tx_path in ['TX1', 'TX2']:  # this is for TX1, TX2, not MIMO
                                    # ready to export to excel
                                    self.parameters = {
                                        'script': self.script,
                                        'tech': self.tech,
                                        'band': self.band_fr1,
                                        'bw': self.bw_fr1,
                                        'rb_size': self.rb_size_fr1,
                                        'rb_start': self.rb_start_fr1,
                                        'tx_level': self.tx_level,
                                        'mcs': self.mcs_fr1,
                                        'tx_path': self.tx_path,
                                    }
                                    self.file_path = tx_power_fcc_ce_export_excel_ftm(self.data, self.parameters)
                    except KeyError as err:
                        logger.debug(f'show error: {err}')
                        logger.info(
                            f"Band {self.band_fr1}, BW: {self.bw_fr1} don't need to test this MCS: "
                            f"{self.mcs_fr1} for CE")
        self.set_test_end_fr1()

    def tx_power_fcc_subprocess_fr1(self):
        self.data = data = {}
        self.loss_tx = self.loss_selector(self.tx_freq_fr1, ext_pmt.fdc_en)
        self.set_tx_freq_gprf(self.tx_freq_fr1)
        self.set_duty_cycle()
        if self.tx_path in ['TX1', 'TX2']:
            self.tx_set_no_sync_fr1()
            power_results = self.get_power_avgerage_gprf()
            self.data[self.tx_freq_fr1] = (self.chan_mark, power_results)  # data = {tx_freq:(chan_mark, power)}
            logger.debug(self.data)

        elif self.tx_path in ['MIMO']:  # measure two port
            path_count = 1  # this is for mimo path to store tx_path
            for port_tx in [self.port_mimo_tx1, self.port_mimo_tx2]:
                self.port_tx = port_tx
                self.set_rf_tx_port_gprf(self.port_tx)
                self.tx_path_mimo = self.tx_path + f'_{path_count}'
                self.tx_set_no_sync_fr1()
                power_results = self.get_power_avgerage_gprf()
                data[self.tx_freq_fr1] = (self.chan_mark, power_results)  # data = {tx_freq:(chan_mark, power)}
                logger.debug(data)

                # ready to export to excel
                self.parameters = {
                    'script': self.script,
                    'tech': self.tech,
                    'band': self.band_fr1,
                    'bw': self.bw_fr1,
                    'rb_size': self.rb_size_fr1,
                    'rb_start': self.rb_start_fr1,
                    'tx_level': self.tx_level,
                    'mcs': self.mcs_fr1,
                    'tx_path': self.tx_path_mimo,
                }
                self.file_path = tx_power_fcc_ce_export_excel_ftm(self.data, self.parameters)

                path_count += 1

    def tx_power_ce_subprocess_fr1(self):
        self.data = data = {}
        self.loss_tx = self.loss_selector(self.tx_freq_fr1, ext_pmt.fdc_en)
        self.set_tx_freq_gprf(self.tx_freq_fr1)
        self.set_duty_cycle()
        if self.tx_path in ['TX1', 'TX2']:
            self.tx_set_no_sync_fr1()
            power_results = self.get_power_avgerage_gprf()
            self.data[self.tx_freq_fr1] = (self.chan_mark, power_results)  # data = {tx_freq:(chan_mark, power)}
            logger.debug(self.data)

        elif self.tx_path in ['MIMO']:  # measure two port
            path_count = 1  # this is for mimo path to store tx_path
            for port_tx in [self.port_mimo_tx1, self.port_mimo_tx2]:
                self.port_tx = port_tx
                self.set_rf_tx_port_gprf(self.port_tx)
                self.tx_path_mimo = self.tx_path + f'_{path_count}'
                self.tx_set_no_sync_fr1()
                power_results = self.get_power_avgerage_gprf()
                data[self.tx_freq_fr1] = (self.chan_mark, power_results)  # data = {tx_freq:(chan_mark, power)}
                logger.debug(data)

                # ready to export to excel
                self.parameters = {
                    'script': self.script,
                    'tech': self.tech,
                    'band': self.band_fr1,
                    'bw': self.bw_fr1,
                    'rb_size': self.rb_size_fr1,
                    'rb_start': self.rb_start_fr1,
                    'tx_level': self.tx_level,
                    'mcs': self.mcs_fr1,
                    'tx_path': self.tx_path_mimo,
                }
                self.file_path = tx_power_fcc_ce_export_excel_ftm(self.data, self.parameters)

                path_count += 1

    def run(self, script):
        for tech in ext_pmt.tech:
            if tech == 'FR1':
                if script == 'FCC':
                    self.tx_power_pipline_fcc_fr1()
                elif script == 'CE':
                    self.tx_power_pipline_ce_fr1()
        self.cmw_close()
