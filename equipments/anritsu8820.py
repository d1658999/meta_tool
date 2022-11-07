import time

from equipments.series_basis.callbox.anritsu_series import Anritsu
from utils.log_init import log_set
from utils.loss_handler import read_loss_file

logger = log_set('Anritsu8820')


class Anritsu8820(Anritsu):
    def __init__(self, equipments='Anristu8820'):
        super().__init__(equipments)
        self.std = None

    def preset(self):
        """
        Preset Anritsu 8820C
        """
        logger.info("Preset Anritsu 8820/8821")
        self.anritsu_query('*ESR?')
        self.set_end()
        s = self.get_standard_query()  # WCDMA|GSM|LTE|CDMA2K
        if s == 'WCDMA':
            self.set_end()
            time.sleep(2)
            self.preset_3gpp()
            self.set_lvl_status('OFF')
        else:
            self.anritsu_write("*RST")  # this command changes measurement count to "single"
        self.anritsu_write("*CLS")
        self.set_all_measurement_items_off()  # Set all measurements to off

    def set_switch_to_lte(self):
        """
        switch to LTE mode
        switch ok => return 0
        switch fail => return 1
        """
        self.set_end()
        time.sleep(2)
        self.std = self.get_standard_query()  # WCDMA|GSM|LTE
        logger.info("Current Format: " + self.std)
        if self.std == 'LTE':
            logger.info("Already LTE mode")
            return self.std
        else:
            self.set_standard('LTE')  # switch to LTE
            time.sleep(1)
            self.std = self.get_standard_query()
            if self.std == 'LTE':
                logger.info("Switch to LTE mode OK")
                return self.std
            else:
                logger.info("Switch to LTE mode fail")
                return 1

    def switch_to_wcdma(self):
        """
        switch to WCDMA mode
        switch ok => return 0
        switch fail => return 1
        """
        self.set_end()
        time.sleep(1)
        self.std = self.get_standard_query()  # WCDMA|GSM|LTE
        logger.debug("Current Function: " + self.std)
        if self.std == 'WCDMA':
            logger.info("Already WCDMA mode")
            return self.std
        else:
            self.set_standard('WCDMA')  # switch to WCDMA
            time.sleep(1)
            self.std = self.get_standard_query()
            if self.std == 'WCDMA':
                logger.info("Switch to WCDMA mode OK")
                return self.std
            else:
                logger.info("Switch to WCDMA mode fail")
                return 1

    def switch_to_gsm(self):
        """
            switch to GSM mode
            switch ok => return 0
            switch fail => return 1
        """
        self.set_end()
        time.sleep(1)
        self.std = self.get_standard_query()  # WCDMA|GSM|LTE
        logger.debug("Current Format: " + self.std)
        if self.std == 'GSM':
            logger.info("Already GSM mode")
            return self.std
        else:
            self.set_standard('GSM')  # switch to GSM
            time.sleep(1)
            self.std = self.get_standard_query()
            if self.std == "GSM":
                logger.info("Switch to GSM mode OK")
                return self.std
            else:
                logger.info("Switch to GSM mode fail")
                return 1

    def set_test_parameter_normal(self):
        self.set_test_parameter('NORMAL')
        self.set_ulrmc_64QAM('DISABLE')

    def set_init_before_calling(self, standard, dl_ch, bw=5):
        logger.info('init equipment before calling')
        s = standard
        if s == 'LTE':
            self.set_init_before_calling_lte(dl_ch, bw)
        elif s == 'WCDMA':
            self.set_init_before_calling_wcdma(dl_ch)
        elif s == 'GSM':
            pass

    def set_init_before_calling_wcdma(self, dl_ch):
        """
            preset before start to calling for WCDMA
        """
        self.set_band_cal()
        self.preset()
        self.set_integrity('WCDMA', 'ON')
        self.set_screen('OFF')
        self.set_display_remain()
        self.set_init_miscs('WCDMA')
        self.set_test_mode('OFF')
        self.set_imsi()
        self.set_authentication_all('WCDMA')
        self.set_all_measurement_items_off()
        self.set_path_loss('WCDMA')
        self.set_init_level('WCDMA')
        self.set_handover('WCDMA', dl_ch)
        self.anritsu_query('*OPC?')

    def set_init_before_calling_lte(self, dl_ch, bw):
        """
            preset before start to calling for LTE
        """
        self.preset()
        self.set_band_cal()
        self.set_screen('OFF')
        self.set_display_remain()
        self.preset_extarb()
        self.set_lvl_status('OFF')
        # if 53 >= band >= 33:
        #     self.set_fdd_tdd_mode('FDD')
        # else:
        #     self.set_fdd_tdd_mode('TDD')
        self.set_test_mode('OFF')
        self.set_integrity('LTE', 'SNOW3G')
        self.set_scenario()
        self.set_pdn_type()
        self.set_mcc_mnc()
        self.set_ant_config()
        self.set_imsi()
        self.set_authentication_all()
        self.set_all_measurement_items_off()
        self.set_init_miscs('LTE')
        self.set_path_loss('LTE')
        self.set_init_level('LTE')
        self.set_handover('LTE', dl_ch, bw)
        self.set_ul_rb_start('MIN')
        self.anritsu_query('*OPC?')

    def set_init_level(self, standard):
        """
            LTE:
                initial input_level=5 and output_level=-60
            WCDMA:
                initial input_level=5 and output_level=-75
        """
        s = standard
        if s == 'LTE':
            self.set_input_level()
            self.set_output_level()
            self.anritsu_query('*OPC?')
        elif s == 'WCDMA':
            self.set_input_level()
            self.set_output_level(-50)
            self.anritsu_query('*OPC?')
        elif s == 'GSM':
            pass

    def set_init_miscs(self, standard):
        """
        the rest part of that tricky setting
        """
        s = standard
        if s == 'LTE':
            self.set_rf_out_port('MAIN')
            self.set_rrc_update('PAGING')
            self.set_power_trigger_source('FRAME')
            self.set_modified_period('N2')
            self.set_paging_cycle(32)
            self.set_rrc_release('OFF')
            self.set_freq_err_range('NARROW')  # NORMAL | NARROW
            self.set_robust_connection('OFF')  # ON | OFF
            self.set_test_mode('OFF')
            self.set_ue_category(3)
            self.set_additional_spectrum_emission_ns('01')

        elif s == 'WCDMA':
            self.set_rf_out_port('MAIN')
            self.set_band_indicator('AUTO')
            # self.inst.write('ATTFLAG OFF')
            # self.inst.write('MEASREP OFF')
            self.set_drx_cycling(64)
            self.set_ber_sample(10000)
            self.set_config_measurement('ON')
            self.set_rx_timeout(5)
            self.set_domain_drmc('CS')
            self.set_register_mode('AUTO')

        elif s == 'GSM':
            pass

    def set_path_loss(self, standard):
        logger.info('Set LOSS')
        self.set_loss_table_delete()  # delete the unknown loss table first

        loss_title = 'LOSSTBLVAL'
        loss_dict = read_loss_file()
        freq = sorted(loss_dict.keys())
        for f in freq:
            self.set_loss_table(loss_title, f, loss_dict[f], loss_dict[f], loss_dict[f])
        s = standard  # WCDMA|GSM|LTE
        logger.debug("Current Format: " + s)
        self.set_loss_common(s)

    def set_handover(self, standard, dl_ch, bw=5):
        s = standard  # WCDMA|GSM|LTE
        logger.debug("Current Format: " + s)
        if s == 'LTE':
            self.set_bandwidth(bw)
            self.set_downlink_channel(s, dl_ch)
            # ul_ch = self.inst.query('ULCHAN?')
            self.anritsu_query('*OPC?')
            # if ul_ch != dl_ch:
            #     self.set_fdd_tdd_mode('FDD')
            # elif ul_ch == dl_ch:
            #     self.set_fdd_tdd_mode('TDD')
            # else:
            #     print('comparison between ul_ch and dl_ch seems like error!')
        elif s == 'WCDMA' or s == 'GSM':
            self.set_downlink_channel(s, dl_ch)
            self.anritsu_query('*OPC?')
        else:
            logger.info('Standard switch @handover function seems like error!')