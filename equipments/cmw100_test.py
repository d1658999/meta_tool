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
        self.rx_freq_fr1 = None
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

    def sig_gen_fr1(self):
        """
        scs: FDD is forced to 15KHz and TDD is to be 30KHz
        """
        logger.info('----------Sig Gen----------')
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
        self.set_fr1_uldl_periodicity()
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
        logger.info('----------Sig Gen----------')
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
        self.set_gprf_rx_freq(self.rx_freq_fr1)
        self.set_gprf_rx_level(self.rx_level)
        gprf_gen = self.get_gprf_generator_state_query()
        self.cmw_query('*OPC?')
        if gprf_gen == 'OFF':
            self.set_gprf_generator_state()
            self.cmw_query('*OPC?')


def main():
    cmw100 = CMW100()
    cmw100.cmw_query('*IDN?')


if __name__ == '__main__':
    main()
