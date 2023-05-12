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
import time

logger = log_set('level_sweep')


class TxTestLevelSweep(AtCmd, CMW100):
    def __init__(self):
        AtCmd.__init__(self)
        CMW100.__init__(self)
        self.port_mimo_tx2 = None
        self.port_mimo_tx1 = None
        self.tx_path_mimo = None
        self.data = None
        self.aclr_mod_current_results = None
        self.rb_state = None
        self.tx_freq_wcdma = None
        self.script = None
        self.parameters = None
        self.file_path = None
        self.srs_path_enable = ext_pmt.srs_path_enable
        self.chan = None
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

    def results_combination_nlw(self, volt_enable):
        results = None
        if volt_enable:
            volt_mipi_handler = self.query_voltage_collection(ext_pmt.et_tracker)
            if self.tech == 'FR1':
                results = self.aclr_mod_current_results + volt_mipi_handler(
                    self.tech, self.band_fr1, self.tx_path)
            elif self.tech == 'LTE':
                results = self.aclr_mod_current_results + volt_mipi_handler(
                    self.tech, self.band_lte, self.tx_path)
            elif self.tech == 'WCDMA':
                results = self.aclr_mod_current_results + volt_mipi_handler(
                    self.tech, self.band_wcdma, self.tx_path)

            return results

        else:
            results = self.aclr_mod_current_results
            return results

    def select_asw_srs_path(self):
        if self.srs_path_enable:
            self.srs_switch()
        else:
            self.antenna_switch_v2()

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

    def tx_power_relative_test_initial_gsm(self):
        logger.info('----------Relatvie test initial----------')
        self.set_pvt_count_gsm(5)
        self.set_modulation_count_gsm(5)
        self.set_spectrum_modulation_count_gsm(5)
        self.set_spectrum_switching_count_gsm(5)
        self.set_scenario_activate_gsm()
        self.cmw_query(f'*OPC?')
        self.set_rf_tx_port_gsm(self.port_tx)
        self.set_rf_setting_external_tx_port_attenuation_gsm(self.loss_tx)
        self.set_rf_setting_user_margin_gsm(10.00)
        self.set_trigger_source_gsm('Power')
        self.set_trigger_threshold_gsm(-20.0)
        self.set_repetition_gsm('SING')
        self.set_measurements_enable_all_gsm()
        self.cmw_query(f'*OPC?')
        self.set_orfs_modulation_measurement_off_gsm()
        self.set_spectrum_modulation_evaluation_area_gsm()
        self.set_orfs_switching_measurement_off_gsm()
        self.system_err_all_query()

    def tx_power_relative_test_initial_wcdma(self):
        logger.info('----------Relatvie test initial----------')
        self.cmw_write(f'*CLS')
        self.set_modulation_count_wcdma(5)
        self.set_aclr_count_wcdma(5)
        self.set_rf_tx_port_wcdma(self.port_tx)
        self.set_rf_setting_external_tx_port_attenuation_wcdma(self.loss_tx)
        self.set_rf_setting_user_margin_wcdma(10.00)
        self.set_trigger_source_wcdma('Free Run (Fast sync)')
        self.set_trigger_threshold_wcdma(-30)
        self.set_repetition_wcdma('SING')
        self.set_measurements_enable_all_wcdma()
        self.cmw_query(f'*OPC?')
        self.system_err_all_query()
        self.set_band_wcdma(self.band_wcdma)
        self.set_tx_freq_wcdma(self.tx_chan_wcdma)
        self.set_ul_dpdch_wcdma('ON')
        self.set_ul_dpcch_slot_format_wcdma(0)
        self.set_scrambling_code_wcdma(13496235)
        self.set_ul_signal_config_wcdma('WCDM')
        self.system_err_all_query()

    def tx_power_relative_test_initial_lte(self):
        logger.info('----------Relatvie test initial----------')
        self.select_mode_fdd_tdd(self.band_lte)
        self.set_tx_freq_lte(self.tx_freq_lte)
        self.cmw_query(f'*OPC?')
        self.set_bw_lte(self.bw_lte)
        self.set_mcs_lte(self.mcs_lte)
        self.set_rb_size_lte(self.rb_size_lte)
        self.set_rb_start_lte(self.rb_start_lte)
        self.set_type_cyclic_prefix_lte('NORM')
        self.set_plc_lte(0)
        self.set_delta_sequence_shift_lte(0)
        self.set_rb_auto_detect_lte('OFF')
        self.set_meas_on_exception_lte('ON')
        self.set_sem_limit_lte(self.bw_lte)
        self.system_err_all_query()
        self.set_measured_slot_lte('ALL')
        self.set_rf_setting_user_margin_lte(10.00)
        self.set_expect_power_lte(self.tx_level + 5)
        self.set_rf_tx_port_lte(self.port_tx)
        self.cmw_query(f'*OPC?')
        self.set_rf_setting_user_margin_lte(10.00)
        self.set_rb_auto_detect_lte('ON')
        self.set_modulation_count_lte(5)
        self.cmw_query(f'*OPC?')
        self.set_aclr_count_lte(5)
        self.cmw_query(f'*OPC?')
        self.set_sem_count_lte(5)
        self.cmw_query(f'*OPC?')
        self.set_trigger_source_lte('GPRF Gen1: Restart Marker')
        self.set_trigger_threshold_lte(-20.0)
        self.set_repetition_lte('SING')
        self.set_measurements_enable_all_lte()
        self.cmw_query(f'*OPC?')
        self.set_measured_subframe_lte()
        self.set_scenario_activate_lte('SAL')
        self.system_err_all_query()
        self.set_rf_setting_external_tx_port_attenuation_lte(self.loss_tx)
        self.cmw_query(f'*OPC?')
        self.set_rf_tx_port_gprf(self.port_tx)
        self.set_power_count_gprf(2)
        self.set_repetition_gprf('SING')
        self.set_power_list_mode_gprf('OFF')
        self.set_trigger_source_gprf('Free Run')
        self.set_trigger_slope_gprf('REDG')
        self.set_trigger_step_length_gprf(5.0e-3)
        self.set_trigger_measure_length_gprf(8.0e-4)
        self.set_trigger_offset_gprf(2.1E-3)
        self.set_trigger_mode_gprf('ONCE')
        self.set_rf_setting_user_margin_gprf(10.00)
        self.set_expect_power_gprf(self.tx_level + 5)

    def tx_power_relative_test_initial_fr1(self):
        logger.info('----------Relatvie test initial----------')
        self.select_mode_fdd_tdd(self.band_fr1)
        self.set_band_fr1(self.band_fr1)
        self.set_tx_freq_fr1(self.tx_freq_fr1)
        self.cmw_query(f'*OPC?')
        self.set_plc_fr1(0)
        self.set_meas_on_exception_fr1('ON')
        self.set_scs_bw_fr1(self.scs, self.bw_fr1)
        self.set_sem_limit_fr1(self.bw_fr1)
        self.set_pusch_fr1(self.mcs_fr1, self.rb_size_fr1, self.rb_start_fr1)
        self.set_precoding_fr1(self.type_fr1)
        self.set_phase_compensation_fr1()
        self.cmw_query(f'*OPC?')
        self.set_repetition_fr1('SING')
        self.set_plc_fr1(0)
        self.set_channel_type_fr1()
        self.set_uldl_periodicity_fr1('MS25')
        self.set_uldl_pattern_fr1(self.scs)
        self.set_measured_slot_fr1('ALL')
        self.set_rf_tx_port_fr1(self.port_tx)
        self.set_rf_setting_user_margin_fr1(10.00)
        self.set_modulation_count_fr1(5)
        self.set_aclr_count_fr1(5)
        self.set_sem_count_fr1(5)
        self.set_trigger_source_fr1('GPRF GEN1: Restart Marker')
        self.set_trigger_threshold_fr1(-20)
        self.set_repetition_fr1('SING')
        self.set_measurements_enable_all_fr1()
        self.set_measured_subframe_fr1(10)
        self.set_measured_slot_fr1('ALL')
        self.set_scenario_activate_fr1('SAL')
        self.set_rf_setting_external_tx_port_attenuation_fr1(self.loss_tx)
        self.cmw_query(f'*OPC?')

    def tx_level_sweep_process_fr1(self):
        """
        band_fr1:
        bw_fr1:
        tx_freq_fr1:
        rb_num:
        rb_start:
        mcs:
        pwr:
        rf_port:
        loss:
        tx_path:
        data {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('FR1', self.band_fr1, self.bw_fr1)
        tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq) for rx_freq in rx_freq_list]
        self.rx_freq_fr1 = rx_freq_list[1]
        self.tx_freq_fr1 = tx_freq_list[1]
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
                    for rb_ftm in ext_pmt.rb_ftm_fr1:  # INNER, OUTER
                        self.rb_size_fr1, self.rb_start_fr1 = rb_pmt.GENERAL_FR1[self.bw_fr1][self.scs][self.type_fr1][
                            self.rb_alloc_fr1_dict[rb_ftm]]  # INNER: 0, # OUTER: 1
                        self.rb_state = rb_ftm  # INNER, OUTER

                        #  initial all before tx level prgress
                        for tx_freq_select in tx_freq_select_list:
                            self.tx_freq_fr1 = tx_freq_select
                            self.loss_tx = get_loss(self.tx_freq_fr1)
                            self.tx_set_fr1()
                            self.tx_power_relative_test_initial_fr1()

                            #  following is real change tx level prgress
                            self.tx_level_sweep_subprocess_fr1()

                            if self.tx_path in ['TX1', 'TX2']:  # this is for TX1, TX2, not MIMO
                                self.parameters = {
                                    'script': self.script,
                                    'tech': self.tech,
                                    'band': self.band_fr1,
                                    'bw': self.bw_fr1,
                                    'tx_freq_level': self.tx_freq_fr1,
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
                                    'test_item': 'level_sweep',
                                }
                                self.file_path = tx_power_relative_test_export_excel_ftm(self.data, self.parameters)
        self.set_test_end_fr1()

    def tx_level_sweep_process_lte(self):
        """
        band_lte:
        bw_lte:
        tx_freq_lte:
        rb_num:
        rb_start:
        mcs:
        pwr:
        rf_port:
        loss:
        tx_path:
        data {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('LTE', self.band_lte, self.bw_lte)
        tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, rx_freq) for rx_freq in rx_freq_list]
        self.rx_freq_lte = rx_freq_list[1]
        self.tx_freq_lte = tx_freq_list[1]
        self.loss_rx = get_loss(rx_freq_list[1])
        self.preset_instrument()
        self.set_test_end_lte()
        self.set_test_mode_lte()
        self.antenna_switch_v2()
        self.cmw_query('*OPC?')
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

                        #  initial all before tx level prgress
                        for tx_freq_select in tx_freq_select_list:
                            self.tx_freq_lte = tx_freq_select
                            self.loss_tx = get_loss(self.tx_freq_lte)
                            self.tx_set_lte()
                            self.tx_power_relative_test_initial_lte()

                            tx_range_list = ext_pmt.tx_level_range_list  # [tx_level_1, tx_level_2]

                            logger.info('----------TX Level Sweep progress---------')
                            logger.info(f'----------from {tx_range_list[0]} dBm to {tx_range_list[1]} dBm----------')

                            step = -1 if tx_range_list[0] > tx_range_list[1] else 1

                            #  following is real change tx level process
                            data = {}
                            for tx_level in range(tx_range_list[0], tx_range_list[1] + step, step):
                                self.tx_level = tx_level
                                logger.info(f'========Now Tx level = {self.tx_level} dBm========')
                                self.set_level_lte(self.tx_level)
                                self.set_chan_request_lte()
                                self.set_rf_setting_user_margin_lte(10.00)
                                self.set_expect_power_lte(self.tx_level + 5)
                                mod_results = self.get_modulation_avgerage_lte()
                                # logger.info(f'mod_results = {mod_results}')
                                self.set_measure_start_on_lte()
                                self.cmw_query('*OPC?')
                                aclr_results = self.get_aclr_average_lte()
                                aclr_results[3] = mod_results[-1]
                                mod_results.pop()
                                self.get_in_band_emissions_lte()
                                self.get_flatness_extreme_lte()
                                time.sleep(0.2)
                                self.get_sem_average_and_margin_lte()
                                self.set_measure_stop_lte()
                                self.cmw_query('*OPC?')
                                self.aclr_mod_current_results = aclr_mod_results = aclr_results + mod_results
                                logger.debug(aclr_mod_results)
                                self.aclr_mod_current_results.append(self.measure_current(self.band_lte))
                                data[tx_level] = self.results_combination_nlw(ext_pmt.volt_mipi_en)
                            logger.debug(data)
                            self.parameters = {
                                'script': self.script,
                                'tech': self.tech,
                                'band': self.band_lte,
                                'bw': self.bw_lte,
                                'tx_freq_level': self.tx_freq_lte,
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
                                'test_item': 'level_sweep',
                            }
                            self.file_path = tx_power_relative_test_export_excel_ftm(data, self.parameters)
        self.set_test_end_lte()

    def tx_level_sweep_process_wcdma(self):
        """
        band_wcdma:
        bw_wcdma:
        tx_freq_wcdma:
        rb_num:
        rb_start:
        mcs:
        pwr:
        rf_port:
        loss:
        tx_path:
        data {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_chan_list = cm_pmt_ftm.dl_chan_select_wcdma(self.band_wcdma)
        tx_chan_list = [cm_pmt_ftm.transfer_chan_rx2tx_wcdma(self.band_wcdma, rx_chan) for rx_chan in rx_chan_list]
        tx_rx_chan_list = list(zip(tx_chan_list, rx_chan_list))  # [(tx_chan, rx_chan),...]

        tx_rx_chan_select_list = channel_freq_select(self.chan, tx_rx_chan_list)

        self.preset_instrument()

        for script in ext_pmt.scripts:
            if script == 'GENERAL':
                self.script = script
                #  initial all before tx level process
                for tx_rx_chan_wcdma in tx_rx_chan_select_list:
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

                    self.tx_power_relative_test_initial_wcdma()

                    tx_range_list = ext_pmt.tx_level_range_list  # [tx_level_1, tx_level_2]

                    logger.info('----------TX Level Sweep progress---------')
                    logger.info(f'----------from {tx_range_list[0]} dBm to {tx_range_list[1]} dBm----------')

                    step = -1 if tx_range_list[0] > tx_range_list[1] else 1

                    #  following is real change tx level process
                    data = {}
                    for tx_level in range(tx_range_list[0], tx_range_list[1] + step, step):
                        self.tx_level = tx_level
                        logger.info(f'========Now Tx level = {self.tx_level} dBm========')
                        self.tx_set_wcdma_level_use()
                        # self.tx_set_wcdma()
                        self.antenna_switch_v2()

                        # self.command(f'AT+HTXPERSTART={self.tx_chan_wcdma}')
                        # self.command(f'AT+HSETMAXPOWER={self.tx_level * 10}')
                        #
                        self.set_rf_setting_user_margin_wcdma(10.00)
                        self.set_expect_power_wcdma(self.tx_level + 5)
                        mod_results = self.get_modulation_avgerage_wcdma()
                        self.set_measure_start_on_wcdma()
                        self.cmw_query(f'*OPC?')
                        spectrum_results = self.get_aclr_average_wcdma()
                        self.set_measure_stop_wcdma()

                        self.aclr_mod_current_results = spectrum_results + mod_results
                        logger.debug(self.aclr_mod_current_results)
                        self.aclr_mod_current_results.append(self.measure_current(self.band_wcdma))
                        data[tx_level] = self.results_combination_nlw(ext_pmt.volt_mipi_en)
                    logger.debug(data)
                    self.parameters = {
                        'script': self.script,
                        'tech': self.tech,
                        'band': self.band_wcdma,
                        'bw': 5,
                        'tx_freq_level': self.tx_freq_wcdma,
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
                        'test_item': 'level_sweep',
                    }
                    self.file_path = tx_power_relative_test_export_excel_ftm(data, self.parameters)
        self.set_test_end_wcdma()

    def tx_level_sweep_process_gsm(self):
        """
        band_gsm:
        tx_freq_gsm:
        pwr:
        rf_port:
        loss:
        tx_path:
        data {tx_pcl: [power, phase_err_rms, phase_peak, ferr,orfs_mod_-200,orfs_mod_200,...orfs_sw-400,
                                                                                                orfs_sw400,...], ...}
        """
        rx_chan_list = cm_pmt_ftm.dl_chan_select_gsm(self.band_gsm)

        rx_chan_select_list = channel_freq_select(self.chan, rx_chan_list)

        self.preset_instrument()
        self.set_test_mode_gsm()
        self.set_test_end_gsm()

        for script in ext_pmt.scripts:
            if script == 'GENERAL':
                self.script = script
                #  initial all before tx level prgress
                for rx_chan_gsm in rx_chan_select_list:
                    self.rx_chan_gsm = rx_chan_gsm
                    self.rx_freq_gsm = cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, self.rx_chan_gsm, 'rx')
                    self.tx_freq_gsm = cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, self.rx_chan_gsm, 'tx')
                    self.loss_rx = get_loss(self.rx_freq_gsm)
                    self.loss_tx = get_loss(self.tx_freq_gsm)
                    self.set_test_mode_gsm()
                    self.antenna_switch_v2()
                    self.sig_gen_gsm()
                    self.sync_gsm()

                    # self.tx_power_relative_test_initial_gsm()

                    tx_range_list = ext_pmt.tx_pcl_range_list_lb if self.band_gsm in [850, 900] \
                        else ext_pmt.tx_pcl_range_list_mb  # [tx_pcl_1, tx_pcl_2]

                    logger.info('----------TX Level Sweep progress---------')
                    logger.info(f'----------from PCL{tx_range_list[0]} to PCL{tx_range_list[1]}----------')

                    step = -1 if tx_range_list[0] > tx_range_list[1] else 1

                    #  following is real change tx pcl prgress

                    data = {}
                    for tx_pcl in range(tx_range_list[0], tx_range_list[1] + step, step):
                        self.pcl = tx_pcl
                        logger.info(f'========Now Tx PCL = PCL{self.pcl} ========')
                        self.tx_set_gsm()
                        mod_orfs_current_results = mod_orfs_results = self.tx_measure_gsm()
                        logger.debug(mod_orfs_results)
                        mod_orfs_current_results.append(self.measure_current(self.band_gsm))
                        data[tx_pcl] = mod_orfs_current_results
                    logger.debug(data)
                    self.parameters = {
                        'script': self.script,
                        'tech': self.tech,
                        'band': self.band_gsm,
                        'bw': 0,
                        'tx_freq_level': self.rx_freq_gsm,
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
                        'test_item': 'level_sweep',
                    }
                    self.file_path = tx_power_relative_test_export_excel_ftm(data, self.parameters)
        self.set_test_end_gsm()

    def tx_level_sweep_subprocess_fr1(self):
        tx_range_list = ext_pmt.tx_level_range_list  # [tx_level_1, tx_level_2]

        logger.info('----------TX Level Sweep progress---------')
        logger.info(f'----------from {tx_range_list[0]} dBm to {tx_range_list[1]} dBm----------')

        step = -1 if tx_range_list[0] > tx_range_list[1] else 1

        self.data = data = {}
        if self.tx_path in ['TX1', 'TX2']:
            for tx_level in range(tx_range_list[0], tx_range_list[1] + step, step):
                self.tx_level = tx_level
                logger.info(f'========Now Tx level = {self.tx_level} dBm========')
                self.set_level_fr1(self.tx_level)
                self.set_rf_setting_user_margin_fr1(10.00)
                self.set_expect_power_fr1(self.tx_level + 5)
                self.set_measure_start_on_fr1()
                self.cmw_query('*OPC?')
                mod_results = self.get_modulation_avgerage_fr1()
                aclr_results = self.get_aclr_average_fr1()
                aclr_results[3] = mod_results[-1]
                mod_results.pop()
                self.get_in_band_emissions_fr1()
                self.get_flatness_extreme_fr1()
                # time.sleep(0.2)
                self.get_sem_average_and_margin_fr1()
                self.set_measure_stop_fr1()
                self.cmw_query('*OPC?')
                self.aclr_mod_current_results = aclr_mod_results = aclr_results + mod_results
                logger.debug(aclr_mod_results)
                self.aclr_mod_current_results.append(self.measure_current(self.band_fr1))
                self.data[tx_level] = self.results_combination_nlw(ext_pmt.volt_mipi_en)
            logger.debug(self.data)

        elif self.tx_path in ['MIMO']:
            for tx_level in range(tx_range_list[0], tx_range_list[1] + step, step):
                path_count = 1  # this is for mimo path to store tx_path
                for port_tx in [self.port_mimo_tx1, self.port_mimo_tx2]:
                    self.port_tx = port_tx
                    self.tx_path_mimo = self.tx_path + f'_{path_count}'
                    self.tx_level = tx_level
                    logger.info(f'========Now Tx level = {self.tx_level} dBm========')
                    self.set_level_fr1(self.tx_level)
                    self.set_rf_setting_user_margin_fr1(10.00)
                    self.set_expect_power_fr1(self.tx_level + 5)
                    self.set_measure_start_on_fr1()
                    self.cmw_query('*OPC?')
                    mod_results = self.get_modulation_avgerage_fr1()
                    aclr_results = self.get_aclr_average_fr1()
                    aclr_results[3] = mod_results[-1]
                    mod_results.pop()
                    self.get_in_band_emissions_fr1()
                    self.get_flatness_extreme_fr1()
                    # time.sleep(0.2)
                    self.get_sem_average_and_margin_fr1()
                    self.set_measure_stop_fr1()
                    self.cmw_query('*OPC?')
                    self.aclr_mod_current_results = aclr_mod_results = aclr_results + mod_results
                    logger.debug(aclr_mod_results)
                    self.aclr_mod_current_results.append(self.measure_current(self.band_fr1))
                    data[tx_level] = self.results_combination_nlw(ext_pmt.volt_mipi_en)
                    logger.debug(data)
                    self.parameters = {
                        'script': self.script,
                        'tech': self.tech,
                        'band': self.band_fr1,
                        'bw': self.bw_fr1,
                        'tx_freq_level': self.tx_freq_fr1,
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
                        'test_item': 'level_sweep',
                    }
                    self.file_path = tx_power_relative_test_export_excel_ftm(data, self.parameters)

                    path_count += 1
                    data = {}

    def tx_level_sweep_pipeline_fr1(self):
        self.rx_level = ext_pmt.init_rx_sync_level
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
                    self.port_table_selector(self.band_fr1, self.tx_path)
                    if self.bw_fr1 in cm_pmt_ftm.bandwidths_selected_fr1(self.band_fr1):
                        self.tx_level_sweep_process_fr1()
                    else:
                        logger.info(f'NR B{self.band_fr1} does not have BW {self.bw_fr1}MHZ')

                except KeyError:
                    logger.info(f'NR Band {self.band_fr1} does not have this tx path {self.tx_path}')

        for bw in ext_pmt.fr1_bandwidths:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'FR1', 'level_sweep')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'GENERAL', 'tech': 'FR1'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundError:
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_level_sweep_pipeline_lte(self):
        self.rx_level = ext_pmt.init_rx_sync_level
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
                        self.port_table_selector(self.band_lte, self.tx_path)
                        if self.bw_lte in cm_pmt_ftm.bandwidths_selected_lte(self.band_lte):
                            self.tx_level_sweep_process_lte()
                        else:
                            logger.info(f'B{self.band_lte} does not have BW {self.bw_lte}MHZ')

                    else:
                        logger.info(f'LTE Band {self.band_lte} does not have this tx path {self.tx_path}!')

                except KeyError:
                    logger.info(f'LTE Band {self.band_lte} does not have this tx path {self.tx_path}!!')

        for bw in ext_pmt.lte_bandwidths:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'LTE', 'level_sweep')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'GENERAL', 'tech': 'LTE'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundError:
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_level_sweep_pipeline_wcdma(self):
        self.rx_level = ext_pmt.init_rx_sync_level
        self.tx_level = ext_pmt.tx_level
        self.port_tx = ext_pmt.port_tx
        self.chan = ext_pmt.channel
        for tech in ext_pmt.tech:
            if tech == 'WCDMA' and ext_pmt.wcdma_bands != []:
                self.tech = tech
                for tx_path in ext_pmt.tx_paths:
                    self.tx_path = tx_path
                    for band in ext_pmt.wcdma_bands:
                        self.band_wcdma = band
                        self.port_table_selector(self.band_wcdma)
                        self.tx_level_sweep_process_wcdma()
                    txp_aclr_evm_current_plot_ftm(self.file_path, self.parameters)

    def tx_level_sweep_pipeline_gsm(self):
        self.rx_level = ext_pmt.init_rx_sync_level
        self.tx_level = ext_pmt.tx_level
        self.port_tx = ext_pmt.port_tx
        self.chan = ext_pmt.channel
        self.mod_gsm = ext_pmt.mod_gsm
        self.tsc = 0 if self.mod_gsm == 'GMSK' else 5
        for tech in ext_pmt.tech:
            if tech == 'GSM' and ext_pmt.gsm_bands != []:
                self.tech = tech
                for band in ext_pmt.gsm_bands:
                    self.pcl = ext_pmt.tx_pcl_lb if band in [850, 900] else ext_pmt.tx_pcl_mb
                    self.band_gsm = band
                    self.port_table_selector(self.band_gsm)
                    self.tx_level_sweep_process_gsm()
                txp_aclr_evm_current_plot_ftm(self.file_path, self.parameters)

    def run(self):
        for tech in ext_pmt.tech:
            if tech == 'LTE':
                self.tx_level_sweep_pipeline_lte()
            elif tech == 'FR1':
                self.tx_level_sweep_pipeline_fr1()
            elif tech == 'WCDMA':
                self.tx_level_sweep_pipeline_wcdma()
            elif tech == 'GSM':
                self.tx_level_sweep_pipeline_gsm()
        self.cmw_close()
