from pathlib import Path
from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
from equipments.cmw100 import CMW100
from utils.log_init import log_set
import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
from utils.loss_handler import get_loss
from utils.adb_handler import get_odpm_current, RecordCurrent
from equipments.power_supply import Psu
from utils.excel_handler import txp_aclr_evm_current_plot_ftm, tx_power_relative_test_export_excel_ftm
from utils.excel_handler import select_file_name_genre_tx_ftm, excel_folder_path
from utils.channel_handler import channel_freq_select
import utils.parameters.rb_parameters as rb_pmt

logger = log_set('tx_lmh')


class TxTestGenre(AtCmd, CMW100):
    def __init__(self):
        AtCmd.__init__(self)
        CMW100.__init__(self)
        self.tx_path_mimo = None
        self.data_freq = None
        self.aclr_mod_current_results = None
        self.port_mimo_tx2 = None
        self.port_mimo_tx1 = None
        self.psu = None
        self.tx_freq_wcdma = None
        self.file_path = None
        self.parameters = None
        self.rb_state = None
        self.script = None
        self.chan = None
        self.srs_path_enable = ext_pmt.srs_path_enable
        self.odpm2 = None
        self.psu = None
        self.port_table = None

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

    def get_temperature(self, state=False):
        """
        for P22, AT+GOOGTHERMISTOR=1,1 for MHB LPAMid/ MHB Rx1 LFEM, AT+GOOGTHERMISTOR=0,1
        for LB LPAMid, MHB ENDC LPAMid, UHB(n77/n79 LPAF)
        :return:
        """
        if state is True:
            res0 = self.query_thermister0()
            res1 = self.query_thermister1()
            res_list = [res0, res1]
            therm_list = []
            for res in res_list:
                for r in res:
                    if 'TEMPERATURE' in r.decode().strip():
                        try:
                            temp = eval(r.decode().strip().split(':')[1]) / 1000
                            therm_list.append(temp)
                        except Exception as err:
                            logger.debug(err)
                            therm_list.append(None)
            logger.info(f'thermistor0 get temp: {therm_list[0]}')
            logger.info(f'thermistor1 get temp: {therm_list[1]}')

        else:
            therm_list = [None, None]

        return therm_list

    def results_combination_nlw(self, volt_enable):
        results = None
        if volt_enable:
            volt_mipi_handler = self.query_voltage_collection(ext_pmt.et_tracker)
            if self.tech == 'FR1':
                results = self.aclr_mod_current_results + self.get_temperature() + volt_mipi_handler(
                    self.tech, self.band_fr1, self.tx_path)
            elif self.tech == 'LTE':
                results = self.aclr_mod_current_results + self.get_temperature() + volt_mipi_handler(
                    self.tech, self.band_lte, self.tx_path)
            elif self.tech == 'WCDMA':
                results = self.aclr_mod_current_results + self.get_temperature() + volt_mipi_handler(
                    self.tech, self.band_wcdma, self.tx_path)

            return results

        else:
            results = self.aclr_mod_current_results + self.get_temperature()
            return results

    def measure_current_select(self, n=1):
        if ext_pmt.record_current_enable:
            if self.odpm2 is None:
                self.odpm2 = RecordCurrent()
                self.odpm2.record_current_index_search()
                return self.odpm2.record_current(n)
            else:
                return self.odpm2.record_current(n)
        elif ext_pmt.odpm_enable:
            return get_odpm_current(n)

        elif ext_pmt.psu_enable:
            if self.psu is None:
                self.psu = Psu()
                return self.psu.psu_current_average(n)
            else:
                return self.psu.psu_current_average(n)

    def measure_current(self, band):
        count = ext_pmt.current_count
        if not ext_pmt.odpm_enable and not ext_pmt.psu_enable and not ext_pmt.record_current_enable:
            return None

        elif self.tech == 'GSM':
            current_list = []
            for _ in range(5):  # addtional average again
                current_list.append(self.measure_current_select(count))
            avg_sample = sum(current_list) / len(current_list)
            logger.info(f'Average of above current for GSM: {avg_sample}')
            return avg_sample
        else:
            # if band in [34, 38, 39, 40, 41, 42, 48, 77, 78, 79]:
            #     n = count
            # else:
            #     n = 2
            # return self.measure_current_select(n)
            return self.measure_current_select(count)

    def select_asw_srs_path(self):
        if self.srs_path_enable:
            self.srs_switch()
        else:
            self.antenna_switch_v2()

    def tx_power_aclr_evm_lmh_process_fr1(self):
        """
        order: tx_path > bw > band > mcs > rb > chan
        band_fr1:
        bw_fr1:
        tx_level:
        rf_port:
        freq_select: 'LMH'
        tx_path:
        data: {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('FR1', self.band_fr1,
                                                   self.bw_fr1)  # [L_rx_freq, M_rx_ferq, H_rx_freq]
        self.rx_freq_fr1 = rx_freq_list[1]
        self.loss_rx = get_loss(rx_freq_list[1])
        logger.info('----------Test LMH progress---------')
        self.preset_instrument()
        self.set_test_end_fr1()
        self.set_test_mode_fr1()
        self.select_asw_srs_path()
        self.sig_gen_fr1()
        self.sync_fr1()

        # scs = 1 if self.band_fr1 in [34, 38, 39, 40, 41, 42, 48, 77, 78,  # temp
        #                              79] else 0  # for now FDD is forced to 15KHz and TDD is to be 30KHz  # temp
        # scs = 15 * (2 ** scs)  # temp
        # self.scs = scs  # temp

        tx_freq_lmh_list = [cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq) for rx_freq in rx_freq_list]
        tx_freq_select_list = sorted(set(channel_freq_select(self.chan, tx_freq_lmh_list)))

        for mcs in ext_pmt.mcs_fr1:
            self.mcs_fr1 = mcs
            for script in ext_pmt.scripts:
                if script == 'GENERAL':
                    self.script = script
                    for rb_ftm in ext_pmt.rb_ftm_fr1:  # INNER_FULL, OUTER_FULL
                        self.rb_size_fr1, self.rb_start_fr1 = \
                            rb_pmt.GENERAL_FR1[self.bw_fr1][self.scs][self.type_fr1][self.rb_alloc_fr1_dict[rb_ftm]]
                        self.rb_state = rb_ftm  # INNER_FULL, OUTER_FULL
                        for tx_freq_fr1 in tx_freq_select_list:
                            self.tx_freq_fr1 = tx_freq_fr1
                            self.tx_power_aclr_evm_lmh_subprocess_fr1()

                            if self.tx_path in ['TX1', 'TX2']:  # this is for TX1, TX2, not MIMO
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
                                    'test_item': 'lmh',
                                }
                                self.file_path = tx_power_relative_test_export_excel_ftm(self.data_freq,
                                                                                         self.parameters)

        self.set_test_end_fr1()

    def tx_power_aclr_evm_lmh_process_lte(self):
        """
        order: tx_path > bw > band > mcs > rb > chan
        band_lte:
        bw_lte:
        tx_level:
        rf_port:
        freq_select: 'LMH'
        tx_path:
        data: {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('LTE', self.band_lte,
                                                   self.bw_lte)  # [L_rx_freq, M_rx_ferq, H_rx_freq]
        self.rx_freq_lte = rx_freq_list[1]
        self.loss_rx = get_loss(rx_freq_list[1])
        logger.info('----------Test LMH progress---------')
        self.preset_instrument()
        self.set_test_end_lte()
        self.set_test_mode_lte()
        self.antenna_switch_v2()
        self.sig_gen_lte()
        self.sync_lte()

        tx_freq_lmh_list = [cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, rx_freq) for rx_freq in rx_freq_list]
        tx_freq_select_list = sorted(set(channel_freq_select(self.chan, tx_freq_lmh_list)))

        for mcs in ext_pmt.mcs_lte:
            self.mcs_lte = mcs
            for script in ext_pmt.scripts:
                if script == 'GENERAL':
                    self.script = script
                    for rb_ftm in ext_pmt.rb_ftm_lte:  # PRB, FRB
                        self.rb_size_lte, self.rb_start_lte = rb_pmt.GENERAL_LTE[self.bw_lte][
                            self.rb_select_lte_dict[rb_ftm]]  # PRB: 0, # FRB: 1
                        self.rb_state = rb_ftm  # PRB, FRB
                        data_freq = {}
                        for tx_freq_lte in tx_freq_select_list:
                            self.tx_freq_lte = tx_freq_lte
                            self.loss_tx = get_loss(self.tx_freq_lte)
                            self.tx_set_lte()
                            self.aclr_mod_current_results = aclr_mod_results = self.tx_measure_lte()
                            logger.debug(aclr_mod_results)
                            self.aclr_mod_current_results.append(self.measure_current(self.band_lte))
                            data_freq[self.tx_freq_lte] = self.results_combination_nlw(ext_pmt.volt_mipi_en)
                        logger.debug(data_freq)

                        # ready to export to excel
                        self.parameters = {
                            'script': self.script,
                            'tech': self.tech,
                            'band': self.band_lte,
                            'bw': self.bw_lte,
                            'tx_freq_level': self.tx_level,
                            'mcs': self.mcs_lte,
                            'tx_path': self.tx_path,
                            'mod': None,
                            'rb_state': self.rb_state,
                            'rb_size': self.rb_size_lte,
                            'rb_start': self.rb_start_lte,
                            'sync_path': self.sync_path,
                            'asw_srs_path': self.asw_srs_path,
                            'scs': None,
                            'type': None,
                            'test_item': 'lmh',
                        }
                        self.file_path = tx_power_relative_test_export_excel_ftm(data_freq, self.parameters)
        self.set_test_end_lte()

    def tx_power_aclr_evm_lmh_process_wcdma(self):
        """
                order: tx_path > bw > band > mcs > rb > chan
                band_wcdma:
                tx_level:
                rf_port:
                freq_select: 'LMH'
                tx_path:
                data: {tx_level: [Pwr, U_-1, U_+1, U_-2, U_+2, OBW, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_chan_list = cm_pmt_ftm.dl_chan_select_wcdma(self.band_wcdma)
        tx_chan_list = [cm_pmt_ftm.transfer_chan_rx2tx_wcdma(self.band_wcdma, rx_chan) for rx_chan in rx_chan_list]
        tx_rx_chan_list = list(zip(tx_chan_list, rx_chan_list))  # [(tx_chan, rx_chan),...]

        tx_rx_chan_select_list = channel_freq_select(self.chan, tx_rx_chan_list)

        self.preset_instrument()

        for script in ext_pmt.scripts:
            if script == 'GENERAL':
                self.script = script
                data_chan = {}
                for tx_rx_chan_wcdma in tx_rx_chan_select_list:
                    logger.info('----------Test LMH progress---------')
                    self.rx_chan_wcdma = tx_rx_chan_wcdma[1]
                    self.tx_chan_wcdma = tx_rx_chan_wcdma[0]
                    self.rx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.rx_chan_wcdma, 'rx')
                    self.tx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.tx_chan_wcdma, 'tx')
                    self.loss_rx = get_loss(self.rx_freq_wcdma)
                    self.loss_tx = get_loss(self.tx_freq_wcdma)
                    self.set_test_end_wcdma()
                    self.set_test_mode_wcdma()
                    self.cmw_query('*OPC?')
                    self.sig_gen_wcdma()
                    self.sync_wcdma()
                    self.tx_set_wcdma()
                    self.antenna_switch_v2()
                    self.aclr_mod_current_results = aclr_mod_results = self.tx_measure_wcdma()
                    logger.debug(aclr_mod_results)
                    self.aclr_mod_current_results.append(self.measure_current(self.band_wcdma))
                    tx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.tx_chan_wcdma)
                    data_chan[tx_freq_wcdma] = self.results_combination_nlw(ext_pmt.volt_mipi_en)
                logger.debug(data_chan)

                # ready to export to excel
                self.parameters = {
                    'script': self.script,
                    'tech': self.tech,
                    'band': self.band_wcdma,
                    'bw': 5,
                    'tx_freq_level': self.tx_level,
                    'mcs': 'QPSK',
                    'tx_path': None,
                    'mod': None,
                    'rb_state': None,
                    'rb_size': None,
                    'rb_start': None,
                    'sync_path': None,
                    'asw_srs_path': self.asw_srs_path,
                    'scs': None,
                    'type': None,
                    'test_item': 'lmh',
                }
                self.file_path = tx_power_relative_test_export_excel_ftm(data_chan, self.parameters)  # mode=1: LMH mode
        self.set_test_end_wcdma()

    def tx_power_aclr_evm_lmh_process_gsm(self):
        """
                order: tx_path > band > chan
                band_gsm:
                tx_pcl:
                rf_port:
                freq_select: 'LMH'
                tx_path:
                data: {rx_freq: [power, phase_err_rms, phase_peak, ferr,orfs_mod_-200,orfs_mod_200,...
                orfs_sw-400,orfs_sw400,...], ...}
        """
        rx_chan_list = cm_pmt_ftm.dl_chan_select_gsm(self.band_gsm)

        rx_chan_select_list = channel_freq_select(self.chan, rx_chan_list)

        self.preset_instrument()
        self.set_test_mode_gsm()
        self.set_test_end_gsm()

        for script in ext_pmt.scripts:
            if script == 'GENERAL':
                self.script = script
                data_chan = {}
                for rx_chan_gsm in rx_chan_select_list:
                    logger.info('----------Test LMH progress---------')
                    self.rx_chan_gsm = rx_chan_gsm
                    self.rx_freq_gsm = cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, self.rx_chan_gsm, 'rx')
                    self.tx_freq_gsm = cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, self.rx_chan_gsm, 'tx')
                    self.loss_rx = get_loss(self.rx_freq_gsm)
                    self.loss_tx = get_loss(self.tx_freq_gsm)
                    self.set_test_mode_gsm()
                    self.antenna_switch_v2()
                    self.sig_gen_gsm()
                    self.sync_gsm()
                    self.tx_set_gsm()
                    aclr_mod_current_results = aclr_mod_results = self.tx_measure_gsm()
                    logger.debug(aclr_mod_results)
                    aclr_mod_current_results.append(self.measure_current(self.band_gsm))
                    data_chan[self.rx_freq_gsm] = aclr_mod_current_results + self.get_temperature()
                logger.debug(data_chan)

                # ready to export to excel
                self.parameters = {
                    'script': self.script,
                    'tech': self.tech,
                    'band': self.band_gsm,
                    'bw': 0,
                    'tx_freq_level': self.pcl,
                    'mcs': None,
                    'tx_path': None,
                    'mod': self.mod_gsm,
                    'rb_state': None,
                    'rb_size': None,
                    'rb_start': None,
                    'sync_path': None,
                    'asw_srs_path': self.asw_srs_path,
                    'scs': None,
                    'type': None,
                    'test_item': 'lmh',
                }
                self.file_path = tx_power_relative_test_export_excel_ftm(data_chan, self.parameters)  # mode=1: LMH mode
        self.set_test_end_gsm()

    def tx_power_aclr_evm_lmh_subprocess_fr1(self):
        self.data_freq = data_freq = {}
        self.rx_freq_fr1 = cm_pmt_ftm.transfer_freq_tx2rx_fr1(self.band_fr1, self.tx_freq_fr1)  # temp
        self.loss_tx = get_loss(self.tx_freq_fr1)
        # self.loss_rx = get_loss(rx_freq_list[1])  # temp
        # self.set_test_end_fr1()  # temp
        # self.set_test_mode_fr1()  # temp
        # self.select_asw_srs_path() # temp
        # self.sig_gen_fr1()  # temp
        # self.sync_fr1()  # temp
        if self.tx_path in ['TX1', 'TX2']:
            self.tx_set_fr1()
            self.aclr_mod_current_results = aclr_mod_results = self.tx_measure_fr1()
            logger.debug(aclr_mod_results)
            self.aclr_mod_current_results.append(self.measure_current(self.band_fr1))
            self.data_freq[self.tx_freq_fr1] = self.results_combination_nlw(ext_pmt.volt_mipi_en)
            logger.debug(self.data_freq)

        elif self.tx_path in ['MIMO']:  # measure two port
            path_count = 1  # this is for mimo path to store tx_path
            for port_tx in [self.port_mimo_tx1, self.port_mimo_tx2]:
                self.port_tx = port_tx
                self.tx_path_mimo = self.tx_path + f'_{path_count}'
                self.tx_set_fr1()
                self.aclr_mod_current_results = aclr_mod_results = self.tx_measure_fr1()
                logger.debug(aclr_mod_results)
                self.aclr_mod_current_results.append(self.measure_current(self.band_fr1))
                data_freq[self.tx_freq_fr1] = self.results_combination_nlw(ext_pmt.volt_mipi_en)
                logger.debug(data_freq)

                # ready to export to excel
                self.parameters = {
                    'script': self.script,
                    'tech': self.tech,
                    'band': self.band_fr1,
                    'bw': self.bw_fr1,
                    'tx_freq_level': self.tx_level,
                    'mcs': self.mcs_fr1,
                    'tx_path': self.tx_path_mimo,
                    'mod': None,
                    'rb_state': self.rb_state,
                    'rb_size': self.rb_size_fr1,
                    'rb_start': self.rb_start_fr1,
                    'sync_path': self.sync_path,
                    'asw_srs_path': self.asw_srs_path,
                    'scs': self.scs,
                    'type': self.type_fr1,
                    'test_item': 'lmh',
                }
                self.file_path = tx_power_relative_test_export_excel_ftm(data_freq, self.parameters)

                path_count += 1

    def tx_power_aclr_evm_lmh_pipeline_fr1(self):
        self.tx_level = ext_pmt.tx_level
        self.port_tx = ext_pmt.port_tx
        self.chan = ext_pmt.channel
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
                    self.port_table_selector(self.band_fr1, self.tx_path)  # this is determined if using port table
                    if self.bw_fr1 in cm_pmt_ftm.bandwidths_selected_fr1(self.band_fr1):
                        self.tx_power_aclr_evm_lmh_process_fr1()
                    else:
                        logger.info(f'NR B{self.band_fr1} does not have BW {self.bw_fr1}MHZ')

                except KeyError:
                    logger.info(f'NR Band {self.band_fr1} does not have this tx path {self.tx_path}')

        for bw in ext_pmt.fr1_bandwidths:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'FR1', 'lmh')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'GENERAL', 'tech': 'FR1'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundError:
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_power_aclr_evm_lmh_pipeline_lte(self):
        self.tx_level = ext_pmt.tx_level
        self.port_tx = ext_pmt.port_tx
        self.chan = ext_pmt.channel
        items = [
            (tech, tx_path, bw, band)
            for tech in ext_pmt.tech
            for tx_path in ext_pmt.tx_paths
            for bw in ext_pmt.lte_bandwidths
            for band in ext_pmt.lte_bands
        ]
        for item in items:
            if item[0] == 'LTE' and ext_pmt.lte_bands != []:
                self.tech = item[0]
                self.tx_path = item[1]
                self.bw_lte = item[2]
                self.band_lte = item[3]
                try:
                    if self.tx_path in ['TX1', 'TX2']:
                        self.port_table_selector(self.band_lte, self.tx_path)  # this is determined if using port table
                        if self.bw_lte in cm_pmt_ftm.bandwidths_selected_lte(self.band_lte):
                            self.tx_power_aclr_evm_lmh_process_lte()
                        else:
                            logger.info(f'B{self.band_lte} does not have BW {self.bw_lte}MHZ')
                    else:
                        logger.info(f'LTE Band {self.band_lte} does not have this tx path {self.tx_path}!')

                except KeyError:
                    logger.info(f'LTE Band {self.band_lte} does not have this tx path {self.tx_path}!!')

        for bw in ext_pmt.lte_bandwidths:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'LTE', 'lmh')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'GENERAL', 'tech': 'LTE'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundError:
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_power_aclr_evm_lmh_pipeline_wcdma(self):
        self.tx_level = ext_pmt.tx_level
        self.port_tx = ext_pmt.port_tx
        self.chan = ext_pmt.channel
        for tech in ext_pmt.tech:
            if tech == 'WCDMA' and ext_pmt.wcdma_bands != []:
                self.tech = 'WCDMA'
                for band in ext_pmt.wcdma_bands:
                    self.band_wcdma = band
                    self.port_table_selector(self.band_wcdma)  # this is determined if using port table
                    self.tx_power_aclr_evm_lmh_process_wcdma()
                txp_aclr_evm_current_plot_ftm(self.file_path, self.parameters)

    def tx_power_aclr_evm_lmh_pipeline_gsm(self):
        self.tx_level = ext_pmt.tx_level
        self.port_tx = ext_pmt.port_tx
        self.chan = ext_pmt.channel
        self.mod_gsm = ext_pmt.mod_gsm
        self.tsc = 0 if self.mod_gsm == 'GMSK' else 5
        for tech in ext_pmt.tech:
            if tech == 'GSM' and ext_pmt.gsm_bands != []:
                self.tech = 'GSM'
                for band in ext_pmt.gsm_bands:
                    self.pcl = ext_pmt.tx_pcl_lb if band in [850, 900] else ext_pmt.tx_pcl_mb
                    self.band_gsm = band
                    self.port_table_selector(self.band_gsm)  # this is determined if using port table
                    self.tx_power_aclr_evm_lmh_process_gsm()
                txp_aclr_evm_current_plot_ftm(self.file_path, self.parameters)

    def run(self):
        for tech in ext_pmt.tech:
            if tech == 'LTE':
                self.tx_power_aclr_evm_lmh_pipeline_lte()
            elif tech == 'FR1':
                self.tx_power_aclr_evm_lmh_pipeline_fr1()
            elif tech == 'WCDMA':
                self.tx_power_aclr_evm_lmh_pipeline_wcdma()
            elif tech == 'GSM':
                self.tx_power_aclr_evm_lmh_pipeline_gsm()
        self.cmw_close()


def main():
    pass


if __name__ == '__main__':
    main()
