from equipments.series_basis.cmw_series import CMW
from utils.log_init import log_set

logger = log_set()


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
        elif self.tech== 'GSM':
            self.set_gprf_measurement(self.port_tx, 0.2)

    def set_gprf_measurement(self, port_tx, bw):
        logger.info('----------set GPRF Measurement----------')
        self.set_gprf_if_filter()
        self.set_gprf_bandpass_filter_bw(bw)
        self.set_gprf_rf_input_path(port_tx)
        self.set_gprf_power_count()
        self.set_gprf_power_repetition()
        self.set_gprf_power_list_mode()  # default is off listmode
        self.set_gprf_trigger_source()
        self.set_gprf_trigger_slope()
        self.set_gprf_trigger_step_length(5.0e-3)
        # self.set_gprf_trigger_step_length(8.0e-3)
        self.set_gprf_trigger_measure_length(5.0e-3)
        # self.command_cmw100_write(f'TRIGger:GPRF:MEAS:POWer:OFFSet 2.1E-3')
        # self.command_cmw100_write(f'TRIGger:GPRF:MEAS:POWer:OFFSet 5E-4')
        self.set_gprf_trigger_offset(0)
        self.set_gprf_trigger_mode('ONCE')
        self.set_gprf_expect_power(self.tx_level)
        self.set_gprf_rf_setting_user_margin(10.00)
        self.set_gprf_rf_setting_external_input_attenuation(self.loss_tx)

    def get_gprf_power_avgerage(self):
        self.set_gprf_measure_start_on()
        self.cmw_query('*OPC?')
        f_state = self.get_gprf_power_state_query()
        while f_state != 'RDY':
            f_state = self.get_gprf_power_state_query()
            self.cmw_query('*OPC?')
        power_average = round(eval(self.get_gprf_power_average_query()[1]), 2)
        logger.info(f'Get the GPRF power: {power_average}')
        return power_average

    def set_waveform_fr1(self, bw, scs, mcs):
        if self.band_fr1 in [34, 38, 39, 40, 41, 42, 48, 77, 78, 79]:
            file_path = f"'C:\CMW100_WV\SMU_NodeB_NR_Ant0_NR_{bw}MHz_SCS{scs}_TDD_Sens_MCS{mcs}_rescale.wv'"
        else:
            file_path = f"'C:\CMW100_WV\SMU_NodeB_NR_Ant0_LTE_NR_{bw}MHz_SCS{scs}_FDD_Sens_MCS_{mcs}.wv'"

        self.set_gprf_arb_file(file_path)

    def set_waveform_lte(self, bw):
        if self.band_fr1 in [34, 38, 39, 40, 41, 42, 48]:
            file_path = f'C:\CMW100_WV\SMU_Channel_CC0_RxAnt0_RF_Verification_10M_SIMO_01.wv'
        else:
            file_path = f'C:\CMW100_WV\SMU_NodeB_Ant0_FRC_{bw}MHz.wv'

        self.set_gprf_arb_file(file_path)

    def set_waveform_wcdma(self):
        file_path = r'C:\CMW100_WV\3G_CAL_FINAL.wv'
        self.set_gprf_arb_file(file_path)

    def set_waveform_gsm(self):
        file_path = r'C:\CMW100_WV\2G_FINAL.wv'
        self.set_gprf_arb_file(file_path)

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
        self.set_gprf_rf_output_path(18)
        self.cmw_query('*OPC?')
        self.set_gprf_generator_cmw_port_uasge_all()
        self.cmw_query('*OPC?')
        self.set_gprf_power_list_mode()
        self.cmw_query('*OPC?')
        self.set_gprf_rf_setting_external_output_attenuation(self.loss_rx)
        self.cmw_query('*OPC?')
        self.set_gprf_generator_base_band_mode('ARB')
        self.cmw_query('*OPC?')
        self.set_uldl_periodicity_fr1()
        self.cmw_query('*OPC?')
        self.set_waveform_fr1(self.bw_fr1, scs, mcs=4)
        self.cmw_query('*OPC?')
        self.get_gprf_arb_file_query()
        self.set_gprf_rx_freq(self.rx_freq_fr1)
        self.set_gprf_rx_level(self.rx_level)
        gprf_gen = self.get_gprf_generator_state_query()
        self.cmw_query('*OPC?')
        if gprf_gen == 'OFF':
            self.set_gprf_generator_state()
            self.cmw_query('*OPC?')

    def sig_gen_lte(self):
        logger.info('----------Sig Gen for LTE----------')
        self.system_base_option_version_query('CMW_NRSub6G_Meas')
        self.set_gprf_rf_output_path(18)
        self.cmw_query('*OPC?')
        self.set_gprf_generator_cmw_port_uasge_all()
        self.cmw_query('*OPC?')
        self.set_gprf_power_list_mode()
        self.cmw_query('*OPC?')
        self.set_gprf_rf_setting_external_output_attenuation(self.loss_rx)
        self.cmw_query('*OPC?')
        self.set_gprf_generator_base_band_mode('ARB')
        self.cmw_query('*OPC?')
        self.band_lte = int(self.band_lte)
        self.set_waveform_lte(self.bw_lte)
        self.cmw_query('*OPC?')
        self.get_gprf_arb_file_query()
        self.set_gprf_rx_freq(self.rx_freq_lte)
        self.set_gprf_rx_level(self.rx_level)
        gprf_gen = self.get_gprf_generator_state_query()
        self.cmw_query('*OPC?')
        if gprf_gen == 'OFF':
            self.set_gprf_generator_state()
            self.cmw_query('*OPC?')

    def sig_gen_wcdma(self):
        logger.info('----------Sig Gen for WCDMA----------')
        self.system_base_option_version_query("CMW_NRSub6G_Meas")
        self.set_gprf_rf_output_path(18)
        self.set_gprf_generator_cmw_port_uasge_all()
        self.cmw_query('*OPC?')
        self.set_gprf_power_list_mode()
        self.cmw_query('*OPC?')
        self.set_gprf_rf_setting_external_output_attenuation(self.loss_rx)
        self.cmw_query('*OPC?')
        self.set_gprf_generator_base_band_mode('ARB')
        self.cmw_query('*OPC?')
        self.set_waveform_wcdma()
        self.cmw_query('*OPC?')
        self.get_gprf_arb_file_query()
        self.set_gprf_rx_freq(self.rx_freq_wcdma)
        self.set_gprf_rx_level(self.rx_level)
        gprf_gen = self.get_gprf_generator_state_query()
        self.cmw_query('*OPC?')
        if gprf_gen == 'OFF':
            self.set_gprf_generator_state()
            self.cmw_query('*OPC?')

    def sig_gen_gsm(self):
        logger.info('----------Sig Gen for GSM----------')
        self.system_base_option_version_query("CMW_NRSub6G_Meas")
        self.set_gprf_rf_output_path(18)
        self.set_gprf_generator_cmw_port_uasge_all()
        self.cmw_query('*OPC?')
        self.set_gprf_power_list_mode()
        self.cmw_query('*OPC?')
        self.set_gprf_rf_setting_external_output_attenuation(self.loss_rx)
        self.cmw_query('*OPC?')
        self.set_gprf_generator_base_band_mode('ARB')
        self.cmw_query('*OPC?')
        self.set_waveform_gsm()
        self.cmw_query('*OPC?')
        self.get_gprf_arb_file_query()
        self.set_gprf_rx_freq(self.rx_freq_gsm)
        self.set_gprf_rx_level(self.rx_level)
        gprf_gen = self.get_gprf_generator_state_query()
        self.cmw_query('*OPC?')
        if gprf_gen == 'OFF':
            self.set_gprf_generator_state()
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
        self.set_precoding_fr1()
        self.set_pusch_fr1(self.mcs_fr1, self.rb_size, self.rb_start)
        self.set_phase_compensation()
        self.cmw_query('*OPC?')
        self.set_repetition_fr1()
        self.set_plc_fr1()
        self.set_channel_type_fr1()
        self.set_uldl_periodicity_fr1('M25')
        self.set_uldl_pattern_fr1()
        self.command_cmw100_write(f'CONF:NRS:MEAS:RFS:UMAR 10.000000')
        self.command_cmw100_write(f'CONF:NRS:MEAS:RFS:ENP {self.tx_level + 5}.00')
        self.command_cmw100_write(f'ROUT:NRS:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
        self.command_cmw100_write(f'CONF:NRS:MEAS:RFS:UMAR 10.000000')
        self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:SCO:MOD 5')
        self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:SCO:SPEC:ACLR 5')
        self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:SCO:SPEC:SEM 5')
        self.command_cmw100_write(f"TRIG:NRS:MEAS:MEV:SOUR 'GPRF GEN1: Restart Marker'")
        self.command_cmw100_write(f'TRIG:NRS:MEAS:MEV:THR -20.0')
        self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:REP SING')
        self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:RES:ALL ON, ON, ON, ON, ON, ON, ON, ON, ON, ON')
        self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:NSUB 10')
        self.command_cmw100_write(f'CONFigure:NRSub:MEASurement:MEValuation:MSLot ALL')
        self.command_cmw100_write(f'CONF:NRS:MEAS:SCEN:ACT SAL')
        self.command_cmw100_write(f'CONF:NRS:MEAS:RFS:EATT {self.loss_tx}')
        self.cmw_query(f'*OPC?')
        self.command_cmw100_write(f'ROUT:GPRF:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
        self.cmw_query(f'*OPC?')
        self.command_cmw100_write(f'ROUT:NRS:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
        self.cmw_query(f'*OPC?')
        self.command_cmw100_write(f'INIT:NRS:MEAS:MEV')
        self.cmw_write(f'*OPC?')
        f_state = self.command_cmw100_query(f'FETC:NRS:MEAS:MEV:STAT?')
        while f_state != 'RDY':
            f_state = self.command_cmw100_query(f'FETC:NRS:MEAS:MEV:STAT?')
            self.cmw_query('*OPC?')
        mod_results = self.command_cmw100_query(
            'FETC:NRS:MEAS:MEV:MOD:AVER?')  # P3 is EVM, P15 is Ferr, P14 is IQ Offset
        mod_results = mod_results.split(',')
        mod_results = [mod_results[3], mod_results[15], mod_results[14]]
        mod_results = [eval(m) for m in mod_results]
        logger.info(f'EVM: {mod_results[0]:.2f}, FREQ_ERR: {mod_results[1]:.2f}, IQ_OFFSET: {mod_results[2]:.2f}')
        aclr_results = self.command_cmw100_query('FETC:NRS:MEAS:MEV:ACLR:AVER?')
        aclr_results = aclr_results.split(',')[1:]
        aclr_results = [eval(aclr) * -1 if eval(aclr) > 30 else eval(aclr) for aclr in
                        aclr_results]  # UTRA2(-), UTRA1(-), NR(-), TxP, NR(+), UTRA1(+), UTRA2(+)
        logger.info(
            f'Power: {aclr_results[3]:.2f}, E-UTRA: [{aclr_results[2]:.2f}, {aclr_results[4]:.2f}], UTRA_1: [{aclr_results[1]:.2f}, {aclr_results[5]:.2f}], UTRA_2: [{aclr_results[0]:.2f}, {aclr_results[6]:.2f}]')
        iem_results = self.command_cmw100_query('FETC:NRS:MEAS:MEV:IEM:MARG:AVER?')
        iem_results = iem_results.split(',')
        iem = f'{eval(iem_results[2]):.2f}' if iem_results[2] != 'INV' else 'INV'
        logger.info(f'InBandEmissions Margin: {iem}dB')
        # logger.info(f'IEM_MARG results: {iem_results}')
        esfl_results = self.command_cmw100_query(f'FETC:NRS:MEAS:MEV:ESFL:EXTR?')
        esfl_results = esfl_results.split(',')
        ripple1 = round(eval(esfl_results[2]), 2) if esfl_results[2] != 'NCAP' else esfl_results[2]
        ripple2 = round(eval(esfl_results[3]), 2) if esfl_results[3] != 'NCAP' else esfl_results[3]
        logger.info(f'Equalize Spectrum Flatness: Ripple1:{ripple1} dBpp, Ripple2:{ripple2} dBpp')
        time.sleep(0.2)
        # logger.info(f'ESFL results: {esfl_results}')
        sem_results = self.command_cmw100_query(f'FETC:NRS:MEAS:MEV:SEM:MARG:ALL?')
        logger.info(f'SEM_MARG results: {sem_results}')
        sem_avg_results = self.command_cmw100_query(f'FETC:NRS:MEAS:MEV:SEM:AVERage?')
        sem_avg_results = sem_avg_results.split(',')
        logger.info(
            f'OBW: {eval(sem_avg_results[2]) / 1000000:.3f} MHz, Total TX Power: {eval(sem_avg_results[3]):.2f} dBm')
        # logger.info(f'SEM_AVER results: {sem_avg_results}')
        self.command_cmw100_write(f'STOP:NRS:MEAS:MEV')
        self.cmw_query('*OPC?')

        logger.debug(aclr_results + mod_results)
        return aclr_results + mod_results  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET


def main():
    cmw100 = CMW100()
    cmw100.cmw_query('*IDN?')


if __name__ == '__main__':
    main()
