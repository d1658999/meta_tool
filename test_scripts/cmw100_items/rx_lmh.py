from pathlib import Path

from equipments.series_basis.callbox.serial_series import AtCmd
from equipments.cmw100_test import CMW100
from utils.log_init import log_set
import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
import utils.parameters.rb_parameters as scrpt_set
from utils.loss_handler import get_loss
from utils.excel_handler import rxs_relative_plot, rxs_endc_plot, rx_power_endc_test_export_excel
from utils.excel_handler import rx_power_relative_test_export_excel, rx_desense_process, rx_desense_endc_process
from utils.channel_handler import channel_freq_select


logger = log_set('tx_lmh')


class RxTest(AtCmd, CMW100):
    def __init__(self):
        AtCmd.__init__(self)
        CMW100.__init__(self)
        self.script = None
        self.chan = None
        self.resolution = None

    # def query_rx_measure_wcdma(self):
    #     self.query_rsrp_cinr_wcdma()
    #     self.query_agc_wcdma()
    #     self.get_esens_wcdma()

    def query_rx_measure_lte(self):
        self.query_rsrp_cinr_lte()
        self.query_agc_lte()
        self.get_esens_lte()

    def query_rx_measure_fr1(self):
        self.query_rsrp_cinr_fr1()
        self.query_agc_fr1()
        self.get_esens_fr1()

    def query_fer_measure_gsm(self):
        self.sig_gen_gsm()
        self.sync_gsm()
        self.query_fer_measure_gsm()

    def search_process_fr1(self):
        self.query_fer_measure_fr1()
        while self.fer < 500:
            self.rx_level = round(self.rx_level - self.resolution, 1)  # to reduce a unit
            self.set_rx_level_search()
            self.query_fer_measure_fr1()
            # self.command_cmw100_query('*OPC?')

    def search_process_lte(self):
        self.query_fer_measure_lte()
        while self.fer < 500:
            self.rx_level = round(self.rx_level - self.resolution, 1)  # to reduce a unit
            self.set_rx_level_search()
            self.query_fer_measure_lte()
            # self.command_cmw100_query('*OPC?')

    def search_process_wcdma(self):
        self.query_fer_measure_wcdma()
        while self.fer < 100:
            self.rx_level = round(self.rx_level - self.resolution, 1)  # to reduce a unit
            self.set_rx_level_search()
            self.query_fer_measure_wcdma()
            # self.command_cmw100_query('*OPC?')

    def search_process_gsm(self):
        rssi = None
        self.query_fer_measure_gsm()
        while self.fer < 2:
            rssi = self.rssi
            self.rx_level = round(self.rx_level - self.resolution, 1)  # to reduce a unit
            # self.set_rx_level()
            self.query_fer_measure_gsm()
        return rssi
        # self.command_cmw100_query('*OPC?')

    def search_sensitivity_fr1(self):
        reset_rx_level = -80
        self.rx_level = reset_rx_level
        coarse_1 = 2
        coarse_2 = 1
        fine = 0.2
        logger.info('----------Search RX Level----------')
        self.resolution = coarse_1
        self.search_process_fr1()  # first time by coarse_1
        logger.info('Second time to search')
        self.rx_level += coarse_1 * 2
        logger.info(f'==========Back to Search: {self.rx_level} dBm==========')
        self.set_rx_level_search()
        self.resolution = coarse_2
        self.search_process_fr1()  # second time by coarse_2
        logger.info('Third time to search')
        self.rx_level += coarse_2 * 2
        logger.info(f'==========Back to Search: {self.rx_level} dBm==========')
        self.set_rx_level_search()
        self.resolution = fine
        self.search_process_fr1()  # second time by fine
        self.rx_level = round(self.rx_level + fine, 1)
        logger.info(f'Final Rx Level: {self.rx_level}')

    def search_sensitivity_lte(self):
        reset_rx_level = -80
        self.rx_level = reset_rx_level
        coarse_1 = 2
        coarse_2 = 1
        fine = 0.2
        logger.info('----------Search RX Level----------')
        self.resolution = coarse_1
        self.search_process_lte()  # first time by coarse_1
        logger.info('Second time to search')
        self.rx_level += coarse_1 * 2
        logger.info(f'==========Back to Search: {self.rx_level} dBm==========')
        self.set_rx_level_search()
        self.resolution = coarse_2
        self.search_process_lte()  # second time by coarse_2
        logger.info('Third time to search')
        self.rx_level += coarse_2 * 2
        logger.info(f'==========Back to Search: {self.rx_level} dBm==========')
        self.set_rx_level_search()
        self.resolution = fine
        self.search_process_lte()  # second time by fine
        self.rx_level = round(self.rx_level + fine, 1)
        logger.info(f'Final Rx Level: {self.rx_level}')

    def search_sensitivity_wcdma(self):
        reset_rx_level = -106
        self.rx_level = reset_rx_level
        coarse_1 = 2
        coarse_2 = 1
        fine = 0.2
        logger.info('----------Search RX Level----------')
        self.resolution = coarse_1
        self.search_process_wcdma()  # first time by coarse_1
        logger.info('Second time to search')
        self.rx_level += coarse_1 * 2
        logger.info(f'==========Back to Search: {self.rx_level} dBm==========')
        self.set_rx_level_search()
        self.resolution = coarse_2
        self.search_process_wcdma()  # second time by coarse_2
        logger.info('Third time to search')
        self.rx_level += coarse_2 * 2
        logger.info(f'==========Back to Search: {self.rx_level} dBm==========')
        self.set_rx_level_search()
        self.resolution = fine
        self.search_process_wcdma()  # second time by fine
        self.rx_level = round(self.rx_level + fine, 1)
        logger.info(f'Final Rx Level: {self.rx_level}')

    def search_sensitivity_gsm(self):
        reset_rx_level = -104
        self.rx_level = reset_rx_level
        coarse_1 = 2
        coarse_2 = 1
        fine = 0.2
        logger.info('----------Search RX Level----------')
        self.resolution = coarse_1
        self.search_process_gsm()  # first time by coarse_1
        logger.info('Second time to search')
        self.rx_level += coarse_1 * 2
        logger.info(f'==========Back to Search: {self.rx_level} dBm==========')
        # self.set_rx_level()
        self.resolution = coarse_2
        self.search_process_gsm()  # second time by coarse_2
        logger.info('Third time to search')
        self.rx_level += coarse_2 * 2
        logger.info(f'==========Back to Search: {self.rx_level} dBm==========')
        # self.set_rx_level()
        self.resolution = fine
        rssi = self.search_process_gsm()  # second time by fine
        self.rx_level = round(self.rx_level + fine, 1)
        self.rssi = rssi
        logger.info(f'Final Rx Level: {self.rx_level}')
        logger.info(f'Final RSSI: {self.rssi}')
        self.command('AT+TESTRESET')

    def search_sensitivity_pipline_fr1(self):
        self.port_tx = ext_pmt.port_tx
        self.chan = ext_pmt.channel
        self.type_fr1 = 'DFTS'
        self.sa_nsa_mode = ext_pmt.sa_nsa
        self.script = 'GENERAL'
        self.mcs_fr1 = 'QPSK'
        self.file_path = None
        items = [
            (tech, tx_path, bw, ue_power_bool, band)
            for tech in ext_pmt.tech
            for tx_path in ext_pmt.tx_paths
            for bw in ext_pmt.fr1_bandwidths
            for ue_power_bool in ext_pmt.tx_max_pwr_sensitivity
            for band in ext_pmt.fr1_bands
        ]
        for item in items:
            if item[0] == 'FR1' and ext_pmt.fr1_bands != []:
                self.tech = item[0]
                self.tx_path = item[1]
                self.bw_fr1 = item[2]
                self.ue_power_bool = item[3]
                self.tx_level = ext_pmt.tx_level if self.ue_power_bool == 1 else -10
                self.band_fr1 = item[4]
                if self.bw_fr1 in cm_pmt_ftm.bandwidths_selected_fr1(self.band_fr1):
                    self.search_sensitivity_lmh_process_fr1()
                else:
                    logger.info(f'B{self.band_fr1} does not have BW {self.bw_fr1}MHZ')
        for bw in ext_pmt.fr1_bandwidths:
            try:
                parameters = {
                    'script': self.script,
                    'tech': self.tech,
                    'mcs': self.mcs_fr1,
                }
                self.bw_fr1 = bw
                # file_name = f'Sensitivty_{self.bw_fr1}MHZ_{self.tech}_LMH.xlsx'
                # file_path = Path(excel_folder_path()) / Path(file_name)
                rx_desense_process(self.file_path, self.mcs_fr1)
                rxs_relative_plot(self.file_path, parameters)
            except TypeError as err:
                logger.debug(err)
                logger.info(
                    'It might not have the Bw in this Band, so it cannot to be calculated for desens')
            except KeyError as err:
                logger.debug(err)
                logger.info(
                    f"{self.band_fr1} doesn't have this {self.bw_fr1}, so desens progress cannot run")
            except FileNotFoundError as err:
                logger.debug(err)
                logger.info(f"There is not file to plot BW{bw}")

    def search_sensitivity_pipline_lte(self):
        self.port_tx = ext_pmt.port_tx
        self.chan = ext_pmt.channel
        self.mcs_lte = 'QPSK'
        self.script = 'GENERAL'
        self.file_path = None
        items = [
            (tech, tx_path, bw, ue_power_bool, band)
            for tech in ext_pmt.tech
            for tx_path in ext_pmt.tx_paths
            for bw in ext_pmt.lte_bandwidths
            for ue_power_bool in ext_pmt.tx_max_pwr_sensitivity
            for band in ext_pmt.lte_bands
        ]
        for item in items:
            if item[0] == 'LTE' and ext_pmt.lte_bands != []:
                self.tech = item[0]
                self.tx_path = item[1]
                self.bw_lte = item[2]
                self.ue_power_bool = item[3]
                self.tx_level = ext_pmt.tx_level if self.ue_power_bool == 1 else -10
                self.band_lte = item[4]
                if self.bw_lte in cm_pmt_ftm.bandwidths_selected_lte(self.band_lte):
                    self.search_sensitivity_lmh_process_lte()
                else:
                    logger.info(f'B{self.band_lte} does not have BW {self.bw_lte}MHZ')
        for bw in ext_pmt.lte_bandwidths:
            try:
                parameters = {
                    'script': self.script,
                    'tech': self.tech,
                    'mcs': self.mcs_lte,
                }
                self.bw_lte = bw
                # file_name = f'Sensitivty_{self.bw_lte}MHZ_{self.tech}_LMH.xlsx'
                # file_path = Path(excel_folder_path()) / Path(file_name)
                rx_desense_process(self.file_path, self.mcs_lte)
                rxs_relative_plot(self.file_path, parameters)
            except TypeError as err:
                logger.debug(err)
                logger.info(
                    'It might not have the Bw in this Band, so it cannot to be calculated for desens')
            except KeyError as err:
                logger.debug(err)
                logger.info(
                    f"{self.band_lte} doesn't have this {self.bw_lte}, so desens progress cannot run")
            except FileNotFoundError as err:
                logger.debug(err)
                logger.info(f"There is not file to plot BW{bw}")

    def search_sensitivity_pipline_wcdma(self):
        self.port_tx = ext_pmt.port_tx
        self.chan = ext_pmt.channel
        self.mcs_wcdma = 'QPSK'
        self.script = 'GENERAL'
        self.file_path = None
        items = [
            (tech, tx_path, band)
            for tech in ext_pmt.tech
            for tx_path in ext_pmt.tx_paths
            for band in ext_pmt.wcdma_bands
        ]
        for item in items:
            if item[0] == 'WCDMA' and ext_pmt.wcdma_bands != []:
                self.tech = item[0]
                self.tx_path = item[1]
                self.band_wcdma = item[2]
                self.search_sensitivity_lmh_process_wcdma()
        # file_name = f'Sensitivty_5MHZ_{self.tech}_LMH.xlsx'
        # file_path = Path(excel_folder_path()) / Path(file_name)
        parameters = {
            'script': self.script,
            'tech': self.tech,
            'mcs': self.mcs_wcdma,
        }
        rxs_relative_plot(self.file_path, parameters)

    def search_sensitivity_pipline_gsm(self):
        self.port_tx = ext_pmt.port_tx
        self.chan = ext_pmt.channel
        self.mod_gsm = ext_pmt.mod_gsm
        self.script = 'GENERAL'
        self.file_path = None
        items = [
            (tech, band)
            for tech in ext_pmt.tech
            for band in ext_pmt.gsm_bands
        ]
        for item in items:
            if item[0] == 'GSM' and ext_pmt.gsm_bands != []:
                self.tech = item[0]
                self.band_gsm = item[1]
                self.pcl = ext_pmt.tx_pcl_lb if self.band_gsm in [850, 900] else ext_pmt.tx_pcl_mb
                self.search_sensitivity_lmh_process_gsm()
        # file_name = f'Sensitivty_0MHZ_{self.tech}_LMH.xlsx'
        # file_path = Path(excel_folder_path()) / Path(file_name)
        parameters = {
            'script': self.script,
            'tech': self.tech,
            'mcs': 'GMSK',
        }
        rxs_relative_plot(self.file_path, parameters)

    def search_sensitivity_pipline_endc(self):
        self.tx_level_endc_lte = ext_pmt.tx_level_endc_lte
        self.tx_level_endc_fr1 = ext_pmt.tx_level_endc_fr1
        self.port_tx_lte = ext_pmt.port_tx_lte
        self.port_tx_fr1 = ext_pmt.port_tx_fr1
        self.sa_nsa_mode = ext_pmt.sa_nsa
        self.type_fr1 = 'DFTS'
        self.mcs_lte = self.mcs_fr1 = 'QPSK'
        self.tx_path = 'TX1'
        self.rx_path_lte = 15
        self.rx_path_fr1 = 15
        items = [
            (tech, band_combo, bw_lte, bw_fr1, chan_rb, ue_power_bool)
            for tech in ext_pmt.tech
            for band_combo in ext_pmt.endc_bands
            for bw_lte in scrpt_set.ENDC[band_combo]
            for bw_fr1 in scrpt_set.ENDC[band_combo][bw_lte]
            for chan_rb in scrpt_set.ENDC[band_combo][bw_lte][bw_fr1]
            for ue_power_bool in ext_pmt.tx_max_pwr_sensitivity
        ]
        data = []
        for item in items:
            self.tech = item[0]
            self.band_combo = item[1]
            self.bw_lte = item[2]
            self.bw_fr1 = item[3]
            self.chan_rb = item[4]
            self.ue_power_bool = item[5]
            [self.band_lte, self.band_fr1] = self.band_combo.split('_')
            (self.tx_freq_lte, self.tx_freq_fr1) = self.chan_rb[0]
            (self.rb_size_lte, self.rb_start_lte) = self.chan_rb[1]
            (self.rb_size_fr1, self.rb_start_fr1) = self.chan_rb[2]
            self.tx_freq_lte = int(self.tx_freq_lte * 1000)
            self.tx_freq_fr1 = int(self.tx_freq_fr1 * 1000)
            loss_tx_lte = get_loss(self.tx_freq_lte)
            loss_tx_fr1 = get_loss(self.tx_freq_fr1)
            self.rx_freq_fr1 = cm_pmt_ftm.transfer_freq_tx2rx_fr1(self.band_fr1, self.tx_freq_fr1)
            self.rx_freq_lte = cm_pmt_ftm.transfer_freq_tx2rx_lte(self.band_lte, self.tx_freq_lte)
            self.loss_rx = get_loss(self.rx_freq_fr1)
            self.preset_instrument()
            self.set_test_end_lte(delay=0.5)
            self.set_test_end_fr1(delay=0.5)
            self.set_test_mode_lte()
            self.rx_level = -70
            self.sig_gen_lte()
            self.sync_lte()
            self.set_test_mode_fr1()
            self.sig_gen_fr1()
            self.sync_fr1()
            # set LTE power
            self.tx_level = ext_pmt.tx_level_endc_lte if self.ue_power_bool == 1 else -10
            self.loss_tx = loss_tx_lte
            self.port_tx = self.port_tx_lte
            self.tx_set_lte()
            self.rx_path_setting_lte()
            # set FR1 power
            self.tx_level = self.tx_level_endc_fr1
            self.loss_tx = loss_tx_fr1
            self.port_tx = self.port_tx_fr1
            self.tx_set_fr1()
            self.rx_path_setting_fr1()
            aclr_mod_results_fr1 = self.tx_measure_fr1()
            logger.debug(aclr_mod_results_fr1)
            logger.info(f'FR1 Power: {aclr_mod_results_fr1[3]}')
            self.power_endc_fr1 = round(aclr_mod_results_fr1[3], 2)
            self.search_sensitivity_fr1()
            # set LTE power and get ENDC power for LTE
            self.tx_level = ext_pmt.tx_level_endc_lte if self.ue_power_bool == 1 else -10
            self.loss_tx = loss_tx_lte
            self.port_tx = self.port_tx_lte
            self.power_monitor_endc_lte = self.tx_monitor_lte()
            data.append([int(self.band_lte), int(self.band_fr1), self.power_monitor_endc_lte,
                         self.power_endc_fr1, self.rx_level, self.bw_lte, self.bw_fr1,
                         self.tx_freq_lte,
                         self.tx_freq_fr1, self.tx_level, self.tx_level_endc_fr1,
                         self.rb_size_lte,
                         self.rb_start_lte, self.rb_size_fr1, self.rb_start_fr1])
            self.set_test_end_fr1(delay=0.5)
            self.set_test_end_lte(delay=0.5)
        file_path = rx_power_endc_test_export_excel(data)
        # file_name = 'Sensitivty_ENDC.xlsx'
        # file_path = Path(excel_folder_path()) / Path(file_name)
        rx_desense_endc_process(file_path)
        rxs_endc_plot(file_path)

    def search_sensitivity_pipline_fast_lte(self):  # this is not yet used
        """
        This is for that RSRP and CINR without issue because this is calculated method
        """
        self.tx_level = ext_pmt.tx_level
        self.port_tx = ext_pmt.port_tx
        self.chan = ext_pmt.channel
        self.mcs_lte = 'QPSK'
        for tech in ext_pmt.tech:
            if tech == 'LTE' and ext_pmt.lte_bands != []:
                self.tech = 'LTE'
                for tx_path in ext_pmt.tx_paths:
                    self.tx_path = tx_path
                    for bw in ext_pmt.lte_bandwidths:
                        self.bw_lte = bw
                        try:
                            for band in ext_pmt.lte_bands:
                                self.band_lte = band
                                if bw in cm_pmt_ftm.bandwidths_selected_lte(self.band_lte):
                                    self.search_sensitivity_lmh_fast_process_lte()
                                else:
                                    logger.info(f'B{self.band_lte} does not have BW {self.bw_lte}MHZ')
                            # self.txp_aclr_evm_current_plot(self.filename, mode=1)  # mode=1: LMH mode
                        except TypeError as err:
                            logger.debug(err)
                            logger.info(f'there is no data to plot because the band does not have this BW ')

    def search_sensitivity_lmh_process_fr1(self):
        # [L_rx_freq, M_rx_ferq, H_rx_freq]
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('FR1', self.band_fr1, self.bw_fr1)

        rx_freq_select_list = channel_freq_select(self.chan, rx_freq_list)

        for rx_path in ext_pmt.rx_paths:
            data = {}
            for rx_freq in rx_freq_select_list:
                self.rx_level = -70
                self.rx_freq_fr1 = rx_freq
                self.tx_freq_fr1 = cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, self.rx_freq_fr1)
                self.loss_rx = get_loss(self.rx_freq_fr1)
                self.loss_tx = get_loss(self.tx_freq_fr1)
                logger.info('----------Test LMH progress---------')
                self.preset_instrument()
                self.set_test_end_fr1()
                self.set_test_mode_fr1()
                # self.command_cmw100_query('*OPC?')
                self.sig_gen_fr1()
                self.sync_fr1()
                self.rx_path_setting_fr1()
                self.rb_size_fr1, self.rb_start_fr1 = cm_pmt_ftm.special_uplink_config_sensitivity_fr1(
                    self.band_fr1,
                    self.scs,
                    self.bw_fr1)  # for RB set(including special tx setting)
                self.antenna_switch_v2()
                self.tx_set_fr1()
                # aclr_results + mod_results  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET
                aclr_mod_results = self.tx_measure_fr1()
                # self.command_cmw100_query('*OPC?')
                self.search_sensitivity_fr1()
                self.query_rx_measure_fr1()
                logger.info(f'Power: {aclr_mod_results[3]:.1f}, Sensitivity: {self.rx_level}')
                # measured_power, measured_rx_level, rsrp_list, cinr_list, agc_list
                data[self.tx_freq_fr1] = [aclr_mod_results[3], self.rx_level, self.rsrp_list, self.cinr_list,
                                          self.agc_list]
                self.set_test_end_fr1()
            parameters = {
                'script': self.script,
                'tech': self.tech,
                'band': self.band_fr1,
                'bw': self.bw_fr1,
                'tx_level': self.tx_level,
                'mcs': self.mcs_fr1,
                'tx_path': self.tx_path,
                'rx_path': rx_path,
            }
            self.file_path = rx_power_relative_test_export_excel(data, parameters)

    def search_sensitivity_lmh_process_lte(self):
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('LTE', self.band_lte,
                                                   self.bw_lte)  # [L_rx_freq, M_rx_ferq, H_rx_freq]

        rx_freq_select_list = channel_freq_select(self.chan, rx_freq_list)

        for rx_path in ext_pmt.rx_paths:
            data = {}
            for rx_freq in rx_freq_select_list:
                self.rx_level = -70
                self.rx_freq_lte = rx_freq
                self.tx_freq_lte = cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, self.rx_freq_lte)
                self.loss_rx = get_loss(self.rx_freq_lte)
                self.loss_tx = get_loss(self.tx_freq_lte)
                logger.info('----------Test LMH progress---------')
                self.preset_instrument()
                self.set_test_end_lte()
                self.set_test_mode_lte()
                # self.command_cmw100_query('*OPC?')
                self.sig_gen_lte()
                self.sync_lte()
                self.rx_path_setting_lte()
                self.rb_size_lte, self.rb_start_lte = cm_pmt_ftm.special_uplink_config_sensitivity_lte(
                    self.band_lte,
                    self.bw_lte)  # for RB set
                self.antenna_switch_v2()
                self.tx_set_lte()
                aclr_mod_results = self.tx_measure_lte()  # aclr_results + mod_results  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET
                # self.command_cmw100_query('*OPC?')
                self.search_sensitivity_lte()
                self.query_rx_measure_lte()
                logger.info(f'Power: {aclr_mod_results[3]:.1f}, Sensitivity: {self.rx_level}')
                data[self.tx_freq_lte] = [aclr_mod_results[3], self.rx_level, self.rsrp_list, self.cinr_list,
                                          self.agc_list]  # measured_power, measured_rx_level, rsrp_list, cinr_list, agc_list
                self.set_test_end_lte()
            parameters = {
                'script': self.script,
                'tech': self.tech,
                'band': self.band_lte,
                'bw': self.bw_lte,
                'tx_level': self.tx_level,
                'mcs': self.mcs_lte,
                'tx_path': self.tx_path,
                'rx_path': rx_path,
            }
            self.file_path = rx_power_relative_test_export_excel(data, parameters)

    def search_sensitivity_lmh_process_wcdma(self):
        rx_chan_list = cm_pmt_ftm.dl_chan_select_wcdma(self.band_wcdma)
        tx_chan_list = [cm_pmt_ftm.transfer_chan_rx2tx_wcdma(self.band_wcdma, rx_chan) for rx_chan in rx_chan_list]
        tx_rx_chan_list = list(zip(tx_chan_list, rx_chan_list))  # [(tx_chan, rx_chan),...]

        tx_rx_chan_select_list = channel_freq_select(self.chan, tx_rx_chan_list)

        self.preset_instrument()
        for rx_path in ext_pmt.rx_paths:
            self.rx_path_wcdma = rx_path
            if self.rx_path_wcdma in [1, 2, 3, 15]:
                data = {}
                for tx_rx_chan_wcdma in tx_rx_chan_select_list:
                    self.rx_level = -70
                    logger.info('----------Test LMH progress---------')
                    self.rx_chan_wcdma = tx_rx_chan_wcdma[1]
                    self.tx_chan_wcdma = tx_rx_chan_wcdma[0]
                    self.rx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.rx_chan_wcdma,
                                                                             'rx')
                    self.tx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.tx_chan_wcdma,
                                                                             'tx')
                    self.loss_rx = get_loss(self.rx_freq_wcdma)
                    self.loss_tx = get_loss(self.tx_freq_wcdma)
                    self.set_test_end_wcdma()
                    self.set_test_mode_wcdma()
                    self.cmw_query('*OPC?')
                    self.rx_path_setting_wcdma()
                    self.sig_gen_wcdma()
                    self.sync_wcdma()
                    # self.antenna_switch_v2()
                    # self.tx_chan_wcdma = tx_rx_chan_wcdma[0]
                    # self.tx_set_wcdma()
                    # aclr_mod_results = self.tx_measure_wcdma()
                    # logger.debug(aclr_mod_results)
                    # data[self.tx_chan_wcdma] = aclr_mod_results
                    self.search_sensitivity_wcdma()
                    data[self.tx_chan_wcdma] = self.rx_level
                    # self.query_rx_measure_wcdma()
                    # logger.info(f'Power: {aclr_mod_results[3]:.1f}, Sensitivity: {self.rx_level}')
                    # data[self.tx_freq_lte] = [aclr_mod_results[3], self.rx_level, self.rsrp_list, self.cinr_list,
                    #                           self.agc_list]  # measured_power, measured_rx_level, rsrp_list, cinr_list, agc_list
                    self.set_test_end_wcdma()
                parameters = {
                    'script': self.script,
                    'tech': self.tech,
                    'band': self.band_wcdma,
                    'bw': 5,
                    'tx_level': self.tx_level,
                    'mcs': 'QPSK',
                    'tx_path': self.tx_path,
                    'rx_path': rx_path,
                }
                self.file_path = rx_power_relative_test_export_excel(data, parameters)
            else:
                logger.info(f"WCDMA doesn't have this RX path {self.rx_path_wcdma_dict[self.rx_path_wcdma]}")
                continue

    def search_sensitivity_lmh_process_gsm(self):
        rx_chan_list = cm_pmt_ftm.dl_chan_select_gsm(self.band_gsm)

        rx_chan_select_list = channel_freq_select(self.chan, rx_chan_list)

        self.preset_instrument()
        self.set_test_mode_gsm()
        self.set_test_end_gsm()

        for rx_path in ext_pmt.rx_paths:
            self.rx_path_gsm = rx_path
            if self.rx_path_gsm in [1, 2]:
                data = {}
                for rx_chan_gsm in rx_chan_select_list:
                    self.rx_level = -70
                    logger.info('----------Test LMH progress---------')
                    self.rx_chan_gsm = rx_chan_gsm
                    self.rx_freq_gsm = cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, self.rx_chan_gsm, 'rx')
                    self.tx_freq_gsm = cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, self.rx_chan_gsm, 'tx')
                    self.loss_rx = get_loss(self.rx_freq_gsm)
                    self.loss_tx = get_loss(self.tx_freq_gsm)
                    self.set_test_mode_gsm()
                    self.rx_path_setting_gsm()
                    self.sig_gen_gsm()
                    self.sync_gsm()
                    # self.antenna_switch_v2()
                    self.search_sensitivity_gsm()
                    data[self.rx_chan_gsm] = [self.rx_level, self.rssi]
                    # logger.info(f'Power: {aclr_mod_results[3]:.1f}, Sensitivity: {self.rx_level}')
                    # data[self.tx_freq_lte] = [aclr_mod_results[3], self.rx_level, self.rsrp_list, self.cinr_list,
                    #                           self.agc_list]  # measured_power, measured_rx_level, rsrp_list, cinr_list, agc_list
                    self.set_test_end_gsm()
                parameters = {
                    'script': self.script,
                    'tech': self.tech,
                    'band': self.band_gsm,
                    'bw': 0,
                    'tx_level': self.tx_level,
                    'mcs': 'GMSK',
                    'tx_path': self.tx_path,
                    'rx_path': rx_path,
                }
                self.file_path = rx_power_relative_test_export_excel(data, parameters)
            else:
                logger.info(f"GSM doesn't have this RX path {self.rx_path_gsm_dict[self.rx_path_gsm]}")

    def search_sensitivity_lmh_fast_process_lte(self):  # this is not yet used
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('LTE', self.band_lte,
                                                   self.bw_lte)  # [L_rx_freq, M_rx_ferq, H_rx_freq]

        rx_freq_select_list = channel_freq_select(self.chan, rx_freq_list)

        for rx_freq in rx_freq_select_list:
            self.rx_level = -70
            self.rx_freq_lte = rx_freq
            self.tx_freq_lte = cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, self.rx_freq_lte)
            self.loss_rx = get_loss(self.rx_freq_lte)
            self.loss_tx = get_loss(self.tx_freq_lte)
            logger.info('----------Test LMH progress---------')
            self.preset_instrument()
            self.set_test_end_lte()
            self.antenna_switch_v2()
            self.set_test_mode_lte()
            self.cmw_query('*OPC?')
            self.sig_gen_lte()
            self.sync_lte()
            self.rb_size_lte, self.rb_start_lte = cm_pmt_ftm.special_uplink_config_sensitivity_lte(self.band_lte,
                                                                                                   self.bw_lte)  # for RB set
            self.tx_set_lte()
            self.tx_measure_lte()
            aclr_mod_results = self.tx_measure_lte()  # aclr_results + mod_results  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET
            self.rx_path_setting_lte()
            self.query_rx_measure_lte()
            logger.info(f'Power: {aclr_mod_results[3]:.1f}, Sensitivity: {self.esens_list}')
            rsrp_max = max(self.rsrp_list)
            rsrp_max_index = self.rsrp_list.index(rsrp_max)
            rx_level = self.esens_list[rsrp_max_index]
            self.filename = rx_power_relative_test_export_excel(data_freq, self.band_lte, self.bw_lte,
                                                                     rx_level)

    def run(self):
        for tech in ext_pmt.tech:
            if tech == 'LTE':
                self.search_sensitivity_pipline_lte()
            elif tech == 'FR1':
                for script in ext_pmt.scripts:
                    if script == 'GENERAL':
                        self.search_sensitivity_pipline_fr1()
                    elif script == 'ENDC' and ext_pmt.sa_nsa == 1:
                        self.search_sensitivity_pipline_endc()
            elif tech == 'WCDMA':
                self.search_sensitivity_pipline_wcdma()
            elif tech == 'GSM':
                self.search_sensitivity_pipline_gsm()


def main():
    p = Path.cwd()
    print(p)

if __name__ == '__main__':
    main()