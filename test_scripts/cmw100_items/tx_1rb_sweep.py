from pathlib import Path

from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
from equipments.cmw100 import CMW100
from utils.log_init import log_set
import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
from utils.loss_handler import get_loss
from utils.excel_handler import txp_aclr_evm_current_plot_ftm, tx_power_relative_test_export_excel_ftm
from utils.excel_handler import select_file_name_genre_tx_ftm, excel_folder_path
from utils.channel_handler import channel_freq_select
import utils.parameters.rb_parameters as rb_pmt

logger = log_set('1rb_sweep')


class TxTest1RbSweep(AtCmd, CMW100):
    def __init__(self):
        AtCmd.__init__(self)
        CMW100.__init__(self)
        self.parameters = None
        self.srs_path_enable = ext_pmt.srs_path_enable
        self.file_path = None
        self.tx_1rb_filename_judge = None
        self.script = None
        self.rb_state = None
        self.chan = None
        self.port_table = None

    def port_table_selector(self, band, tx_path='TX1'):
        """
        This is used for multi-ports connection on Tx
        """
        if self.port_table is None:
            self.port_table = self.port_tx_table()

        if ext_pmt.port_table_en:
            self.port_tx = int(self.port_table[tx_path][str(band)])

        else:
            pass

    def select_asw_srs_path(self):
        if self.srs_path_enable:
            self.srs_switch()
        else:
            self.antenna_switch_v2()

    def tx_1rb_sweep_pipeline_fr1(self):
        self.rx_level = ext_pmt.init_rx_sync_level
        self.tx_level = ext_pmt.tx_level
        self.port_tx = ext_pmt.port_tx
        self.chan = ext_pmt.channel
        self.sa_nsa_mode = ext_pmt.sa_nsa
        self.tx_1rb_filename_judge = True
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
                        self.tx_1rb_sweep_process_fr1()
                    else:
                        logger.info(f'B{self.band_fr1} does not have BW {self.bw_fr1}MHZ')

                except KeyError as err:
                    logger.info(f'Band {self.band_fr1} does not have this tx path {self.tx_path}')

        for bw in ext_pmt.fr1_bandwidths:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'FR1', '1rb_sweep')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'GENERAL', 'tech': 'FR1'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundError:
                logger.info(f'there is not file to plot BW{bw} ')
        self.tx_1rb_filename_judge = False

    def tx_1rb_sweep_process_fr1(self):
        logger.info('----------1RB Sweep progress ---------')
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('FR1', self.band_fr1, self.bw_fr1)
        # tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq) for rx_freq in rx_freq_list]
        self.rx_freq_fr1 = rx_freq_list[1]
        self.loss_rx = get_loss(rx_freq_list[1])
        self.preset_instrument()
        self.set_test_end_fr1()
        self.set_test_mode_fr1()
        self.select_asw_srs_path()
        self.sig_gen_fr1()
        self.sync_fr1()

        tx_freq_lmh_list = [cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq) for rx_freq in rx_freq_list]
        tx_freq_select_list = sorted(set(channel_freq_select(self.chan, tx_freq_lmh_list)))

        for mcs in ext_pmt.mcs_fr1:
            self.mcs_fr1 = mcs
            for script in ext_pmt.scripts:
                if script == 'GENERAL':
                    self.script = script
                    for tx_freq_select in tx_freq_select_list:
                        self.tx_freq_fr1 = tx_freq_select
                        self.rb_size_fr1, rb_sweep_fr1 = rb_pmt.GENERAL_FR1[self.bw_fr1][self.scs][self.type_fr1][
                            self.rb_alloc_fr1_dict['EDGE_1RB_RIGHT']]  # capture EDGE_1RB_RIGHT
                        self.rb_state = '1rb_sweep'
                        data = {}
                        for rb_start in range(rb_sweep_fr1 + 1):
                            self.rb_start_fr1 = rb_start
                            self.loss_tx = get_loss(self.tx_freq_fr1)
                            self.tx_set_fr1()
                            aclr_mod_results = self.tx_measure_fr1()
                            logger.debug(aclr_mod_results)
                            data[self.tx_freq_fr1] = aclr_mod_results
                            logger.debug(data)
                            # ready to export to excel
                            self.parameters = {
                                'script': self.script,
                                'tech': self.tech,
                                'band': self.band_fr1,
                                'bw': self.bw_fr1,
                                'tx_freq_level': self.tx_level,
                                'mcs': self.mcs_fr1,
                                'tx_path': self.tx_path,
                                'mod': None,
                                'rb_state': self.rb_state,
                                'rb_size': self.rb_size_fr1,
                                'rb_start': self.rb_start_fr1,
                                'sync_path': self.sync_path,
                                'asw_srs_path': self.asw_srs_path,
                                'scs': self.scs,
                                'type': self.type_fr1,
                                'test_item': '1rb_sweep',
                            }
                            self.file_path = tx_power_relative_test_export_excel_ftm(data, self.parameters)
        self.set_test_end_fr1()

    def run(self):
        for tech in ext_pmt.tech:
            if tech == 'FR1':
                self.tx_1rb_sweep_pipeline_fr1()
            elif tech == 'LTE':
                pass
            else:
                pass
