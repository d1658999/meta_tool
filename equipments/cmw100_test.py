import math
import time

from equipments.series_basis.cmw_series import CMW
from utils.log_init import log_set

logger = log_set('CMW100')


class CMW100(CMW):
    def __init__(self, equipment='cmw100'):
        super().__init__(equipment)
        self.port_tx = None
        self.tech = None
        self.bw_fr1 = None
        self.bw_lte = None
        self.band_fr1 = None
        self.band_lte = None
        self.band_wcdma = None
        self.band_gsm = None
        self.tx_level = None
        self.rx_level = None
        self.loss_tx = None
        self.loss_rx = None
        self.tx_freq_fr1 = None
        self.tx_freq_lte = None
        self.tx_freq_wcdma = None
        self.tx_freq_gsm = None
        self.rx_freq_fr1 = None
        self.rx_freq_lte = None
        self.rx_freq_wcdma = None
        self.rx_freq_gsm = None
        self.scs = None
        self.type_fr1 = None
        self.mcs_fr1 = None
        self.mcs_lte = None
        self.rb_size_fr1 = None
        self.rb_start_fr1 = None
        self.rb_size_lte = None
        self.rb_start_lte = None

    def preset_instrument(self):
        logger.info('----------Preset CMW----------')
        self.system_preset_all()
        self.system_base_option_version_query('CMW_NRSub6G_Meas')
        self.set_fd_correction_deactivate_all()
        self.set_fd_correction_ctable_delete()
        self.cmw_query('*OPC?')
        self.system_err_all_query()
        self.cmw_write('*RST')
        self.cmw_query('*OPC?')

    def set_gprf_measurement_group(self):
        if self.tech == 'FR1':
            self.set_gprf_measurement(self.port_tx, self.bw_fr1)
        elif self.tech == 'LTE':
            self.set_gprf_measurement(self.port_tx, self.bw_lte)
        elif self.tech == 'WCDMA':
            self.set_gprf_measurement(self.port_tx, 5)
        elif self.tech == 'GSM':
            self.set_gprf_measurement(self.port_tx, 0.2)

    def set_gprf_measurement(self, port_tx, bw):
        logger.info('----------set GPRF Measurement----------')
        self.set_if_filter_gprf()
        self.set_bandpass_filter_bw_gprf(bw)
        self.set_rf_tx_port_gprf(port_tx)
        self.set_power_count_gprf()
        self.set_power_repetition_gprf()
        self.set_power_list_mode_gprf()  # default is off listmode
        self.set_trigger_source_gprf()
        self.set_trigger_slope_gprf()
        self.set_trigger_step_length_gprf(5.0e-3)
        # self.set_trigger_step_length_gprf(8.0e-3)
        self.set_trigger_measure_length_gprf(5.0e-3)
        # self.command_cmw100_write(f'TRIGger:GPRF:MEAS:POWer:OFFSet 2.1E-3')
        # self.command_cmw100_write(f'TRIGger:GPRF:MEAS:POWer:OFFSet 5E-4')
        self.set_trigger_offset_gprf(0)
        self.set_trigger_mode_gprf('ONCE')
        self.set_expect_power_gprf(self.tx_level)
        self.set_rf_setting_user_margin_gprf(10.00)
        self.set_rf_setting_external_tx_port_attenuation_gprf(self.loss_tx)

    def get_power_avgerage_gprf(self):
        self.set_measure_start_on_gprf()
        self.cmw_query('*OPC?')
        f_state = self.get_power_state_query_gprf()
        while f_state != 'RDY':
            f_state = self.get_power_state_query_gprf()
            self.cmw_query('*OPC?')
        power_average = round(eval(self.get_power_average_query_gprf()[1]), 2)
        logger.info(f'Get the GPRF power: {power_average}')
        return power_average

    def get_modulation_avgerage_fr1(self):
        f_state = self.get_power_state_query_fr1()
        while f_state != 'RDY':
            f_state = self.get_power_state_query_fr1()
            self.cmw_query('*OPC?')
        mod_results = self.get_modulation_average_query_fr1()  # P[3] is EVM, P[15] is Ferr, P[14] is IQ Offset
        mod_results = mod_results.split(',')
        mod_results = [mod_results[3], mod_results[15], mod_results[14]]
        mod_results = [eval(m) for m in mod_results]
        logger.info(f'EVM: {mod_results[0]:.2f}, FREQ_ERR: {mod_results[1]:.2f}, IQ_OFFSET: {mod_results[2]:.2f}')
        return mod_results

    def get_aclr_average_fr1(self):
        aclr_results = self.get_aclr_average_query_fr1()
        aclr_results = aclr_results.split(',')[1:]
        aclr_results = [eval(aclr) * -1 if eval(aclr) > 30 else eval(aclr) for aclr in
                        aclr_results]  # UTRA2(-), UTRA1(-), NR(-), TxP, NR(+), UTRA1(+), UTRA2(+)
        logger.info(f'Power: {aclr_results[3]:.2f}, '
                    f'E-UTRA: [{aclr_results[2]:.2f}, {aclr_results[4]:.2f}], '
                    f'UTRA_1: [{aclr_results[1]:.2f}, {aclr_results[5]:.2f}], '
                    f'UTRA_2: [{aclr_results[0]:.2f}, {aclr_results[6]:.2f}]')
        return aclr_results

    def get_in_band_emissions_fr1(self):
        iem_results = self.get_in_band_emission_query_fr1()
        iem_results = iem_results.split(',')
        iem = f'{eval(iem_results[2]):.2f}' if iem_results[2] != 'INV' else 'INV'
        logger.info(f'InBandEmissions Margin: {iem}dB')
        # logger.info(f'IEM_MARG results: {iem_results}')
        return iem_results

    def get_flatness_extreme_fr1(self):
        esfl_results = self.get_flatness_extreme_query_fr1()
        esfl_results = esfl_results.split(',')
        ripple1 = round(eval(esfl_results[2]), 2) if esfl_results[2] != 'NCAP' else esfl_results[2]
        ripple2 = round(eval(esfl_results[3]), 2) if esfl_results[3] != 'NCAP' else esfl_results[3]
        logger.info(f'Equalize Spectrum Flatness: Ripple1:{ripple1} dBpp, Ripple2:{ripple2} dBpp')
        # logger.info(f'ESFL results: {esfl_results}')
        return ripple1, ripple2

    def get_sem_average_and_margin_fr1(self):
        sem_results = self.get_sem_margin_all_query_fr1()
        logger.info(f'SEM_MARG results: {sem_results}')
        sem_avg_results = self.get_sem_average_query_fr1()
        sem_avg_results = sem_avg_results.split(',')
        logger.info(f'OBW: {eval(sem_avg_results[2]) / 1000000:.3f} MHz, '
                    f'Total TX Power: {eval(sem_avg_results[3]):.2f} dBm')
        # logger.info(f'SEM_AVER results: {sem_avg_results}')
        return sem_results, sem_avg_results

    def set_waveform_fr1(self, bw, scs, mcs):
        if self.band_fr1 in [34, 38, 39, 40, 41, 42, 48, 77, 78, 79]:
            file_path = f'C:\\CMW100_WV\\SMU_NodeB_NR_Ant0_NR_{bw}MHz_SCS{scs}_TDD_Sens_MCS{mcs}_rescale.wv'
        else:
            file_path = f'C:\\CMW100_WV\\SMU_NodeB_NR_Ant0_LTE_NR_{bw}MHz_SCS{scs}_FDD_Sens_MCS_{mcs}.wv'

        self.set_arb_file_gprf(file_path)

    def set_waveform_lte(self, bw):
        if self.band_fr1 in [34, 38, 39, 40, 41, 42, 48]:
            file_path = f'C:\\CMW100_WV\\SMU_Channel_CC0_RxAnt0_RF_Verification_10M_SIMO_01.wv'
        else:
            file_path = f'C:\\CMW100_WV\\SMU_NodeB_Ant0_FRC_{bw}MHz.wv'

        self.set_arb_file_gprf(file_path)

    def set_waveform_wcdma(self):
        file_path = r'C:\CMW100_WV\3G_CAL_FINAL.wv'
        self.set_arb_file_gprf(file_path)

    def set_waveform_gsm(self):
        file_path = r'C:\CMW100_WV\2G_FINAL.wv'
        self.set_arb_file_gprf(file_path)

    def sig_gen_fr1(self):
        """
        scs: FDD is forced to 15KHz and TDD is to be 30KHz
        """
        logger.info('----------Sig Gen for FR1----------')
        self.band_fr1 = int(self.band_fr1)
        scs = 1 if self.band_fr1 in [34, 38, 39, 40, 41, 42, 48, 77, 78,
                                     79] else 0  # for now FDD is forced to 15KHz and TDD is to be 30KHz
        scs = 15 * (2 ** scs)
        self.scs = scs
        self.system_base_option_version_query('CMW_NRSub6G_Meas')
        self.set_rf_rx_port_gprf(18)
        self.cmw_query('*OPC?')
        self.set_generator_cmw_port_uasge_all_gprf()
        self.cmw_query('*OPC?')
        self.set_power_list_mode_gprf()
        self.cmw_query('*OPC?')
        self.set_rf_setting_external_rx_port_attenuation_gprf(self.loss_rx)
        self.cmw_query('*OPC?')
        self.set_generator_base_band_mode_gprf('ARB')
        self.cmw_query('*OPC?')
        self.set_uldl_periodicity_fr1()
        self.cmw_query('*OPC?')
        self.set_waveform_fr1(self.bw_fr1, scs, mcs=4)
        self.cmw_query('*OPC?')
        self.get_arb_file_query_gprf()
        self.set_rx_freq_gprf(self.rx_freq_fr1)
        self.set_rx_level_gprf(self.rx_level)
        gprf_gen = self.get_generator_state_query_gprf()
        self.cmw_query('*OPC?')
        if gprf_gen == 'OFF':
            self.set_generator_state_gprf()
            self.cmw_query('*OPC?')

    def sig_gen_lte(self):
        logger.info('----------Sig Gen for LTE----------')
        self.system_base_option_version_query('CMW_NRSub6G_Meas')
        self.set_rf_rx_port_gprf(18)
        self.cmw_query('*OPC?')
        self.set_generator_cmw_port_uasge_all_gprf()
        self.cmw_query('*OPC?')
        self.set_power_list_mode_gprf()
        self.cmw_query('*OPC?')
        self.set_rf_setting_external_rx_port_attenuation_gprf(self.loss_rx)
        self.cmw_query('*OPC?')
        self.set_generator_base_band_mode_gprf('ARB')
        self.cmw_query('*OPC?')
        self.band_lte = int(self.band_lte)
        self.set_waveform_lte(self.bw_lte)
        self.cmw_query('*OPC?')
        self.get_arb_file_query_gprf()
        self.set_rx_freq_gprf(self.rx_freq_lte)
        self.set_rx_level_gprf(self.rx_level)
        gprf_gen = self.get_generator_state_query_gprf()
        self.cmw_query('*OPC?')
        if gprf_gen == 'OFF':
            self.set_generator_state_gprf()
            self.cmw_query('*OPC?')

    def sig_gen_wcdma(self):
        logger.info('----------Sig Gen for WCDMA----------')
        self.system_base_option_version_query("CMW_NRSub6G_Meas")
        self.set_rf_rx_port_gprf(18)
        self.set_generator_cmw_port_uasge_all_gprf()
        self.cmw_query('*OPC?')
        self.set_power_list_mode_gprf()
        self.cmw_query('*OPC?')
        self.set_rf_setting_external_rx_port_attenuation_gprf(self.loss_rx)
        self.cmw_query('*OPC?')
        self.set_generator_base_band_mode_gprf('ARB')
        self.cmw_query('*OPC?')
        self.set_waveform_wcdma()
        self.cmw_query('*OPC?')
        self.get_arb_file_query_gprf()
        self.set_rx_freq_gprf(self.rx_freq_wcdma)
        self.set_rx_level_gprf(self.rx_level)
        gprf_gen = self.get_generator_state_query_gprf()
        self.cmw_query('*OPC?')
        if gprf_gen == 'OFF':
            self.set_generator_state_gprf()
            self.cmw_query('*OPC?')

    def sig_gen_gsm(self):
        logger.info('----------Sig Gen for GSM----------')
        self.system_base_option_version_query("CMW_NRSub6G_Meas")
        self.set_rf_rx_port_gprf(18)
        self.set_generator_cmw_port_uasge_all_gprf()
        self.cmw_query('*OPC?')
        self.set_power_list_mode_gprf()
        self.cmw_query('*OPC?')
        self.set_rf_setting_external_rx_port_attenuation_gprf(self.loss_rx)
        self.cmw_query('*OPC?')
        self.set_generator_base_band_mode_gprf('ARB')
        self.cmw_query('*OPC?')
        self.set_waveform_gsm()
        self.cmw_query('*OPC?')
        self.get_arb_file_query_gprf()
        self.set_rx_freq_gprf(self.rx_freq_gsm)
        self.set_rx_level_gprf(self.rx_level)
        gprf_gen = self.get_generator_state_query_gprf()
        self.cmw_query('*OPC?')
        if gprf_gen == 'OFF':
            self.set_generator_state_gprf()
            self.cmw_query('*OPC?')

    def set_sem_limit_fr1(self, bw):
        self.set_spectrum_limit_fr1(1, bw, 0.015, 0.0985, round(-13.5 - 10 * math.log10(bw / 5), 1), 'K030')
        self.set_spectrum_limit_fr1(2, bw, 1.5, 4.5, -8.5, 'M1')
        self.set_spectrum_limit_fr1(3, bw, 5.5, round(-0.5 + bw, 1), -11.5, 'M1')
        self.set_spectrum_limit_fr1(4, bw, round(0.5 + bw, 1), round(4.5 + bw, 1), -23.5, 'M1')

    def tx_measure_fr1(self):
        scs = 1 if self.band_fr1 in [34, 38, 39, 40, 41, 42, 48, 75, 76, 77, 78,
                                     79] else 0  # for now FDD is forced to 15KHz and TDD is to be 30KHz
        self.scs = 15 * (2 ** scs)  # for now TDD only use 30KHz, FDD only use 15KHz
        logger.info('---------Tx Measure----------')
        mode = "TDD" if self.band_fr1 in [34, 38, 39, 40, 41, 42, 48, 75, 76, 77, 78, 79] else "FDD"
        self.system_base_option_version_query("CMW_NRSub6G_Meas")
        self.set_duplexer_mode_fr1(mode)
        self.set_band_fr1(self.band_fr1)
        self.set_tx_freq_fr1(self.tx_freq_fr1)
        self.cmw_write('*OPC?')
        self.set_plc_fr1()
        self.set_meas_on_exception_fr1('ON')
        self.set_scs_bw_fr1(self.scs, self.bw_fr1)
        self.set_sem_limit_fr1(self.bw_fr1)
        self.set_precoding_fr1(self.type_fr1)
        self.set_pusch_fr1(self.mcs_fr1, self.rb_size_fr1, self.rb_start_fr1)
        self.set_phase_compensation_fr1()
        self.cmw_query('*OPC?')
        self.set_repetition_fr1()
        self.set_plc_fr1()
        self.set_channel_type_fr1()
        self.set_uldl_periodicity_fr1('M25')
        self.set_uldl_pattern_fr1(self.scs)
        self.set_rf_setting_user_margin_fr1(10.00)
        self.set_expect_power_fr1(self.tx_level + 5)
        self.set_rf_tx_port_fr1(self.port_tx)
        self.set_rf_setting_user_margin_fr1(10.00)
        self.set_statistic_count_fr1(5)
        self.set_aclr_count_fr1(5)
        self.set_sem_count_fr1(5)
        self.set_trigger_source_fr1('GPRF GEN1: Restart Marker')
        self.set_trigger_threshold_fr1(-20)
        self.set_repetition_fr1()
        self.set_measurements_enable_all_fr1()
        self.set_subframe_fr1(10)
        self.set_measured_slot('ALL')
        self.set_scenario_activate_fr1('SAL')
        self.set_rf_setting_external_tx_port_attenuation_fr1(self.loss_tx)
        self.cmw_query(f'*OPC?')
        self.set_rf_tx_port_gprf(self.port_tx)
        self.cmw_query(f'*OPC?')
        self.set_rf_tx_port_fr1(self.port_tx)
        self.cmw_query(f'*OPC?')
        self.set_measure_start_on_fr1()
        self.cmw_write(f'*OPC?')
        mod_results = self.get_modulation_avgerage_fr1()
        aclr_results = self.get_aclr_average_fr1()
        self.get_in_band_emissions_fr1()
        self.get_flatness_extreme_fr1()
        # time.sleep(0.2)
        self.get_sem_average_and_margin_fr1()
        self.set_measure_stop_fr1()
        self.cmw_query('*OPC?')
        logger.debug(aclr_results + mod_results)
        return aclr_results + mod_results  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET

    def tx_measure_lte(self):
        logger.info('---------Tx Measure----------')
        mode = 'TDD' if self.band_lte in [38, 39, 40, 41, 42, 48] else 'FDD'
        self.set_duplexer_mode_lte(mode)
        self.set_band_lte(self.band_lte)
        self.set_tx_freq_lte(self.tx_freq_lte)
        self.cmw_query('*OPC?')
        self.set_bw_lte(self.bw_lte)
        self.set_mcs_lte(self.mcs_lte)
        self.set_rb_size_lte(self.rb_size_lte)
        self.set_rb_start_lte(self.rb_start_lte)
        self.set_type_cyclic_prefix_lte('NORM')
        self.set_plc_lte(0)
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:DSSP 0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:AUTO OFF')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MOEX ON')
        lim1 = -10 if self.bw_lte == 1.4 else -13 if self.bw_lte == 3 else -15 if self.bw_lte == 5 else -18 if self.bw_lte == 10 else -20 if self.bw_lte == 15 else -21
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM1:CBAN{self.bw_lte * 10} ON,0MHz,1MHz,{lim1},K030')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM2:CBAN{self.bw_lte * 10} ON,1MHz,2.5MHz,-10,M1')
        self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM3:CBAN{self.bw_lte * 10} ON,2.5MHz,2.8MHz,-25,M1') if self.bw_lte < 3 else self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM3:CBAN{self.bw_lte * 10} ON,2.5MHz,2.8MHz,-10,M1')
        self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM4:CBAN{self.bw_lte * 10} ON,2.8MHz,5MHz,-10,M1') if self.bw_lte >= 3 else self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM4:CBAN{self.bw_lte * 10} OFF,2.8MHz,5MHz,-25,M1')
        self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM5:CBAN{self.bw_lte * 10} ON,5MHz,6MHz,-13,M1') if self.bw_lte > 3 else self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM5:CBAN{self.bw_lte * 10} OFF,5MHz,6MHz,-25,M1') if self.bw_lte < 3 else self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM5:CBAN{self.bw_lte * 10} ON,5MHz,6MHz,-25,M1')
        self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM6:CBAN{self.bw_lte * 10} ON,6MHz,10MHz,-13,M1') if self.bw_lte > 5 else self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM6:CBAN{self.bw_lte * 10} OFF,6MHz,10MHz,-25,M1') if self.bw_lte < 5 else self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM6:CBAN{self.bw_lte * 10} ON,6MHz,10MHz,-25,M1')
        self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM7:CBAN{self.bw_lte * 10} ON,10MHz,15MHz,-13,M1') if self.bw_lte > 10 else self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM7:CBAN{self.bw_lte * 10} OFF,10MHz,15MHz,-25,M1') if self.bw_lte < 10 else self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM7:CBAN{self.bw_lte * 10} ON,10MHz,15MHz,-25,M1')
        self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM8:CBAN{self.bw_lte * 10} ON,15MHz,20MHz,-13,M1') if self.bw_lte > 15 else self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM8:CBAN{self.bw_lte * 10} OFF,15MHz,20MHz,-25,M1') if self.bw_lte < 15 else self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM8:CBAN{self.bw_lte * 10} ON,15MHz,20MHz,-25,M1')
        self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM9:CBAN{self.bw_lte * 10} ON,20MHz,25MHz,-25,M1') if self.bw_lte == 20 else self.command_cmw100_write(
            f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM9:CBAN{self.bw_lte * 10} OFF,20MHz,25MHz,-25,M1')
        self.command_cmw100_query('SYST:ERR:ALL?')
        self.command_cmw100_write(f'CONFigure:LTE:MEAS:MEValuation:MSLot ALL')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:UMAR 10.000000')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:ENP {self.tx_level + 5}.00')
        self.command_cmw100_write(f'ROUT:LTE:MEAS:SCEN:SAL R11, RX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:UMAR 10.000000')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:AUTO ON')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:SCO:MOD 5')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:SCO:SPEC:ACLR 5')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:SCO:SPEC:SEM 5')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f"TRIG:LTE:MEAS:MEV:SOUR 'GPRF Gen1: Restart Marker'")
        self.command_cmw100_write(f'TRIG:LTE:MEAS:MEV:THR -20.0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:REP SING')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RES:ALL ON, ON, ON, ON, ON, ON, ON, ON, ON, ON')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MSUB 2, 10, 0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:SCEN:ACT SAL')
        self.command_cmw100_query('SYST:ERR:ALL?')
        self.command_cmw100_write(f'ROUT:GPRF:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'ROUT:LTE:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:EATT {self.loss_tx}')
        self.command_cmw100_query('*OPC?')
        time.sleep(0.2)
        mod_results = self.command_cmw100_query(
            'READ:LTE:MEAS:MEV:MOD:AVER?')  # P3 is EVM, P15 is Ferr, P14 is IQ Offset
        mod_results = mod_results.split(',')
        mod_results = [mod_results[3], mod_results[15], mod_results[14]]
        mod_results = [eval(m) for m in mod_results]
        logger.info(f'EVM: {mod_results[0]:.2f}, FREQ_ERR: {mod_results[1]:.2f}, IQ_OFFSET: {mod_results[2]:.2f}')
        self.command_cmw100_write(f'INIT:LTE:MEAS:MEV')
        self.command_cmw100_query('*OPC?')
        f_state = self.command_cmw100_query('FETC:LTE:MEAS:MEV:STAT?')
        while f_state != 'RDY':
            f_state = self.command_cmw100_query('FETC:LTE:MEAS:MEV:STAT?')
            self.command_cmw100_query('*OPC?')
        aclr_results = self.command_cmw100_query('FETC:LTE:MEAS:MEV:ACLR:AVER?')
        aclr_results = aclr_results.split(',')[1:]
        aclr_results = [eval(aclr) * -1 if eval(aclr) > 30 else eval(aclr) for aclr in
                        aclr_results]  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2
        logger.info(
            f'Power: {aclr_results[3]:.2f}, E-UTRA: [{aclr_results[2]:.2f}, {aclr_results[4]:.2f}], UTRA_1: [{aclr_results[1]:.2f}, {aclr_results[5]:.2f}], UTRA_2: [{aclr_results[0]:.2f}, {aclr_results[6]:.2f}]')
        iem_results = self.command_cmw100_query('FETC:LTE:MEAS:MEV:IEM:MARG?')
        iem_results = iem_results.split(',')
        logger.info(f'InBandEmissions Margin: {eval(iem_results[2]):.2f}dB')
        # logger.info(f'IEM_MARG results: {iem_results}')
        esfl_results = self.command_cmw100_query(f'FETC:LTE:MEAS:MEV:ESFL:EXTR?')
        esfl_results = esfl_results.split(',')
        ripple1 = round(eval(esfl_results[2]), 2) if esfl_results[2] != 'NCAP' else esfl_results[2]
        ripple2 = round(eval(esfl_results[3]), 2) if esfl_results[3] != 'NCAP' else esfl_results[3]
        logger.info(f'Equalize Spectrum Flatness: Ripple1:{ripple1} dBpp, Ripple2:{ripple2} dBpp')
        time.sleep(0.2)
        # logger.info(f'ESFL results: {esfl_results}')
        sem_results = self.command_cmw100_query(f'FETC:LTE:MEAS:MEV:SEM:MARG?')
        logger.info(f'SEM_MARG results: {sem_results}')
        sem_avg_results = self.command_cmw100_query(f'FETC:LTE:MEAS:MEV:SEM:AVER?')
        sem_avg_results = sem_avg_results.split(',')
        logger.info(
            f'OBW: {eval(sem_avg_results[2]) / 1000000:.3f} MHz, Total TX Power: {eval(sem_avg_results[3]):.2f} dBm')
        # logger.info(f'SEM_AVER results: {sem_avg_results}')
        self.command_cmw100_write(f'STOP:LTE:MEAS:MEV')
        self.command_cmw100_query('*OPC?')

        logger.debug(aclr_results + mod_results)
        return aclr_results + mod_results  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET

    def tx_measure_wcdma(self):
        logger.info('---------Tx Measure----------')
        self.command_cmw100_write(f'*CLS')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:MEV:SCO:MOD 5')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:MEV:SCO:SPEC 5')
        self.command_cmw100_write(f'ROUT:WCDMA:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
        self.command_cmw100_write(f'CONF:WCDMA:MEAS:RFS:EATT {self.loss_tx}')
        self.command_cmw100_write(f'CONF:WCDMA:MEAS:RFS:UMAR 10.00')
        self.command_cmw100_write(f"TRIG:WCDM:MEAS:MEV:SOUR 'Free Run (Fast sync)'")
        self.command_cmw100_write(f'TRIG:WCDM:MEAS:MEV:THR -30')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:MEV:REP SING')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:MEV:RES:ALL ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_query('SYST:ERR:ALL?')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:BAND OB{self.band_wcdma}')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:RFS:FREQ {self.tx_chan_wcdma} CH')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:UES:DPDC ON')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:UES:SFOR 0')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:UES:SCOD 13496235')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:UES:ULC WCDM')
        self.command_cmw100_query('SYST:ERR:ALL?')
        self.command_cmw100_write(f'CONF:WCDMA:MEAS:RFS:UMAR 10.00')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:RFS:ENP {self.tx_level + 5}')
        mod_results = self.command_cmw100_query(
            f'READ:WCDM:MEAS:MEV:MOD:AVER?')  # P1 is EVM, P4 is Ferr, P8 is IQ Offset
        mod_results = mod_results.split(',')
        mod_results = [mod_results[1], mod_results[4], mod_results[8]]
        mod_results = [eval(m) for m in mod_results]
        logger.info(f'EVM: {mod_results[0]:.2f}, FREQ_ERR: {mod_results[1]:.2f}, IQ_OFFSET: {mod_results[2]:.2f}')
        self.command_cmw100_write(f'INIT:WCDM:MEAS:MEV')
        self.command_cmw100_write(f'*OPC?')
        f_state = self.command_cmw100_query(f'FETC:WCDM:MEAS:MEV:STAT?')
        while f_state != 'RDY':
            time.sleep(0.2)
            f_state = self.command_cmw100_query('FETC:WCDM:MEAS:MEV:STAT?')
            self.command_cmw100_query('*OPC?')
        spectrum_results = self.command_cmw100_query(
            f'FETC:WCDM:MEAS:MEV:SPEC:AVER?')  # P1: Power, P2: ACLR_-2, P3: ACLR_-1, P4:ACLR_+1, P5:ACLR_+2, P6:OBW
        spectrum_results = spectrum_results.split(',')
        spectrum_results = [
            round(eval(spectrum_results[1]), 2),
            round(eval(spectrum_results[3]) - eval(spectrum_results[1]), 2),
            round(eval(spectrum_results[4]) - eval(spectrum_results[1]), 2),
            round(eval(spectrum_results[2]) - eval(spectrum_results[1]), 2),
            round(eval(spectrum_results[5]) - eval(spectrum_results[1]), 2),
            round(eval(spectrum_results[6]) / 1000000, 2)
        ]
        logger.info(
            f'Power: {spectrum_results[0]:.2f}, ACLR_-1: {spectrum_results[2]:.2f}, ACLR_1: {spectrum_results[3]:.2f}, ACLR_-2: {spectrum_results[1]:.2f}, ACLR_+2: {spectrum_results[4]:.2f}, OBW: {spectrum_results[5]:.2f}MHz')
        self.command_cmw100_write(f'STOP:WCDM:MEAS:MEV')
        self.command_cmw100_query('*OPC?')

        return spectrum_results + mod_results

    def tx_measure_gsm(self):
        logger.info('---------Tx Measure----------')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:SCO:PVT 5')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:SCO:MOD 5')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:SCO:SMOD 5')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:SCO:SSW 5')
        self.command_cmw100_write(f'CONF:GSM:MEAS:SCEN:ACT STAN')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'ROUT:GSM:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
        self.command_cmw100_write(f'CONF:GSM:MEAS:RFS:EATT {self.loss_tx}')
        self.command_cmw100_write(f'CONF:GSM:MEAS:RFS:UMAR 10.00')
        self.command_cmw100_write(f"TRIG:GSM:MEAS:MEV:SOUR 'Power'")
        self.command_cmw100_write(f'TRIG:GSM:MEAS:MEV:THR -20.0')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:REP SING')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:RES:ALL ON, ON, ON, ON, ON, ON, ON, ON, ON, ON, OFF, ON')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(
            f'CONF:GSM:MEAS:MEV:SMOD:OFR 100KHZ,200KHZ,250KHZ,400KHZ,600KHZ,800KHZ,1600KHZ,1800KHZ,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:SMOD:EAR ON,6,45,ON,90,129')
        self.command_cmw100_write(
            f'CONF:GSM:MEAS:MEV:SSW:OFR 400KHZ,600KHZ,1200KHZ,1800KHZ,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
        self.command_cmw100_query('SYST:ERR:ALL?')
        self.command_cmw100_write(f'CONF:GSM:MEAS:BAND {self.band_tx_meas_dict_gsm[self.band_gsm]}')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:GSM:MEAS:CHAN {self.rx_chan_gsm}')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:MOEX ON')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:TSEQ TSC{self.tsc}')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:MVI {",".join([self.mod_gsm] * 8)}')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:MSL 0,1,0')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_query('SYST:ERR:ALL?')
        self.power_init_gsm()
        self.command_cmw100_write(f'CONF:GSM:MEAS:RFS:ENP {self.pwr_init_gsm}')
        mod_results = self.command_cmw100_query(
            f'READ:GSM:MEAS:MEV:MOD:AVER?')  # P12 is Power, P6 is phase_err_rms, P2 is EVM_rms, P10 is ferr
        mod_results = mod_results.split(',')
        mod_results = [mod_results[12], mod_results[6], mod_results[7],
                       mod_results[10]]  # power, phase_err_rms, phase_peak, ferr
        mod_results = [round(eval(m), 2) for m in mod_results]
        logger.info(
            f'Power: {mod_results[0]:.2f}, Phase_err_rms: {mod_results[1]:.2f}, Phase_peak: {mod_results[2]:.2f}, Ferr: {mod_results[3]:.2f}')
        self.command_cmw100_write(f'INIT:GSM:MEAS:MEV')
        self.command_cmw100_write(f'*OPC?')
        self.command_cmw100_write(f'CONF:GSM:MEAS:RFS:ENP {mod_results[0]:.2f}')
        f_state = self.command_cmw100_query(f'FETC:GSM:MEAS:MEV:STAT?')
        while f_state != 'RDY':
            time.sleep(0.2)
            f_state = self.command_cmw100_query('FETC:GSM:MEAS:MEV:STAT?')
            self.command_cmw100_query('*OPC?')
        pvt = self.command_cmw100_query(f'FETC:GSM:MEAS:MEV:PVT:AVER:SVEC?')  # PVT, but it is of no use
        orfs_mod = self.command_cmw100_query(f'FETC:GSM:MEAS:MEV:SMOD:FREQ?')  # MOD_ORFS
        orfs_mod = [round(eval(orfs_mod), 2) for orfs_mod in orfs_mod.split(',')[13:29]]
        orfs_mod = [
            orfs_mod[6],  # -200 KHz
            orfs_mod[10],  # 200 KHz
            orfs_mod[4],  # -400 KHz
            orfs_mod[12],  # 400 KHz
            orfs_mod[3],  # -600 KHz
            orfs_mod[13],  # 600 KHz
        ]
        logger.info(f'ORFS_MOD_-200KHz: {orfs_mod[0]}, ORFS_MOD_200KHz: {orfs_mod[1]}')
        logger.info(f'ORFS_MOD_-400KHz: {orfs_mod[2]}, ORFS_MOD_400KHz: {orfs_mod[3]}')
        logger.info(f'ORFS_MOD_-600KHz: {orfs_mod[4]}, ORFS_MOD_600KHz: {orfs_mod[5]}')
        orfs_sw = self.command_cmw100_query(f'FETC:GSM:MEAS:MEV:SSW:FREQ?')  # SW_ORFS
        orfs_sw = [round(eval(orfs_sw), 2) for orfs_sw in orfs_sw.split(',')[17:25]]
        orfs_sw = [
            orfs_sw[3],  # -400 KHz
            orfs_sw[5],  # 400 KHz
            orfs_sw[2],  # -600 KHz
            orfs_sw[6],  # 600 KHz
            orfs_sw[1],  # -1200 KHz
            orfs_sw[7],  # 1200 KHz
        ]
        logger.info(f'ORFS_SW_-400KHz: {orfs_sw[0]}, ORFS_SW_400KHz: {orfs_sw[1]}')
        logger.info(f'ORFS_SW_-600KHz: {orfs_sw[2]}, ORFS_SW_600KHz: {orfs_sw[3]}')
        logger.info(f'ORFS_SW_-1200KHz: {orfs_sw[4]}, ORFS_SW_1200KHz: {orfs_sw[5]}')
        self.command_cmw100_write(f'STOP:WCDM:MEAS:MEV')
        self.command_cmw100_query('*OPC?')

        return mod_results + orfs_mod + orfs_sw  # [0~3] + [4~10] + [11~17]

    def tx_monitor_lte(self):
        logger.info('---------Tx Monitor----------')
        # self.sig_gen_lte()
        self.command_cmw100_write(f'CONFigure:LTE:MEAS:MEV:RES:PMONitor ON')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f"TRIG:LTE:MEAS:MEV:SOUR 'GPRF Gen1: Restart Marker'")
        self.command_cmw100_write(f'CONFigure:LTE:MEAS:MEValuation:MSLot ALL')
        self.command_cmw100_write(f'TRIG:LTE:MEAS:MEV:THR -20.0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:REP SING')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MOEX ON')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:CPR NORM')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MSUB 2, 10, 0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:AUTO ON')
        mode = 'TDD' if self.band_lte in [38, 39, 40, 41, 42, 48] else 'FDD'
        self.command_cmw100_write(f'CONF:LTE:MEAS:DMODe {mode}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:BAND OB{self.band_lte}')
        rb = f'0{self.bw_lte * 10}' if self.bw_lte < 10 else f'{self.bw_lte * 10}'
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:CBAN B{rb}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MOD:MSCH {self.mcs_lte}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:FREQ {self.tx_freq_lte}KHz')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:EATT {self.loss_tx}')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'ROUT:GPRF:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'ROUT:LTE:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:UMAR 10.000000')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:ENP {self.tx_level}.00')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'INIT:LTE:MEAS:MEV')
        f_state = self.command_cmw100_query('FETC:LTE:MEAS:MEV:STAT?')
        while f_state != 'RDY':
            f_state = self.command_cmw100_query('FETC:LTE:MEAS:MEV:STAT?')
            self.command_cmw100_query('*OPC?')
        self.command_cmw100_query('*OPC?')
        power_results = self.command_cmw100_query(f'FETCh:LTE:MEAS:MEV:PMON:AVER?')
        power = power_results.strip().split(',')[2]
        logger.info(f'LTE power by Tx monitor: {round(eval(power), 2)}')
        return round(eval(power), 2)


def main():
    cmw100 = CMW100()
    cmw100.cmw_query('*IDN?')


if __name__ == '__main__':
    main()
