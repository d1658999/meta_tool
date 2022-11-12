import time
from decimal import Decimal

from equipments.series_basis.callbox.anritsu_series import Anritsu
from utils.log_init import log_set
from utils.loss_handler import read_loss_file
import utils.parameters.common_parameters_anritsu as cm_pmt_anritsu
from utils.fly_mode import FlyMode

logger = log_set('Anritsu8820')


class Anritsu8820(Anritsu):
    def __init__(self, equipments='Anristu8820'):
        super().__init__(equipments)
        self.dl_ch = None
        self.count = None
        self.chcoding = None
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

    @staticmethod
    def flymode_circle():
        flymode = FlyMode()
        flymode.com_open()
        flymode.fly_on()
        time.sleep(3)
        flymode.fly_off()
        flymode.com_close()

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

    def set_authentication_all(self, standard):
        """
        set all authentication
        """
        s = standard
        if s == 'LTE':
            self.set_authentication('ON')
            self.set_authentication_algorithm()
            self.set_authentication_key()
            self.set_opc()
        elif s == 'WCDMA':
            self.set_authentication_algorithm()
            self.set_authentication_key()
            self.set_opc()

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
        self.set_authentication_all('LTE')
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

    def set_registration_calling(self, standard):
        logger.info('Start to calling')
        s = standard
        logger.debug("Current Format: " + s)
        logger.info('Start registration and calling')
        if s == 'LTE':
            self.set_registration_calling_lte()

        elif s == 'WCDMA' and self.chcoding == 'REFMEASCH':  # this is WCDMA
            self.set_registration_calling_wcdma()

        elif s == 'GSM':
            self.set_registration_calling_gsm()

        elif s == 'WCDMA' and self.chcoding == 'EDCHTEST':  # this is HSUPA
            self.set_registration_calling_hspa()
            # self.set_registration_after_calling_hspa()

        elif s == 'WCDMA' and self.chcoding == 'FIXREFCH':  # this is HSDPA
            self.set_registration_calling_hspa()
            # self.set_registration_after_calling_hspa()

    def set_registration_calling_lte(self):
        """
            ANRITSU_IDLE = 1	        #Idle state
            ANRITSU_REGIST = 3			# Under location registration
            ANRITSU_CONNECTED = 6	    # Under communication or connected
        """
        self.set_calling_threshold()
        self.set_lvl_status('ON')
        self.set_test_mode()
        conn_state = int(self.get_calling_state_query())
        while conn_state != cm_pmt_anritsu.ANRITSU_CONNECTED:  # this is for waiting connection
            self.set_calling_clear()
            while conn_state == cm_pmt_anritsu.ANRITSU_IDLE:
                self.set_end()
                logger.info('IDLE')
                logger.info('Start to ON and OFF')
                self.flymode_circle()
                time.sleep(3)
                self.set_connecting()
                while conn_state != cm_pmt_anritsu.ANRITSU_CONNECTED:
                    logger.info('Waiting for connection...')
                    time.sleep(1)
                    conn_state = int(self.get_calling_state_query().strip())
                # logger.info('Start calling')
                # conn_state = int(self.inst.query("CALLSTAT?").strip())
            # logger.info('START CALL')
            # self.inst.write('CALLSA')
            logger.info('Connected')
            time.sleep(1)

    def set_registration_calling_wcdma(self):
        """
            ANRITSU_IDLE = 1	        #Idle state
            ANRITSU_IDLE_REGIST = 2		#Idle( Regist ) Idle state (location registered)
            ANRITSU_LOOP_MODE_1 = 7	    # Under communication or connected
            ANRITSU_LOOP_MODE_1_CLOSED = 9  # it seems like waiting to loop mode between Loopback mode 1 and IDLE
        """
        self.set_lvl_status('ON')
        self.set_test_mode()
        # self.flymode_circle()
        conn_state = int(self.get_calling_state_query().strip())

        self.count = 10
        while conn_state != cm_pmt_anritsu.ANRITSU_LOOP_MODE_1:  # this is for waiting connection
            if conn_state == cm_pmt_anritsu.ANRITSU_IDLE:
                self.set_end()
                logger.info('IDLE')
                time.sleep(10)
                logger.info('START CALL')
                self.flymode_circle()
                time.sleep(10)
                self.set_connecting()
                conn_state = int(self.get_calling_state_query().strip())

            elif conn_state == cm_pmt_anritsu.ANRITSU_IDLE_REGIST:
                logger.info('Status: IDLE_REGIST')
                self.set_connecting()
                time.sleep(1)
                conn_state = int(self.get_calling_state_query().strip())

            elif conn_state == cm_pmt_anritsu.ANRITSU_REGIST:
                logger.info('Status: REGIST')
                time.sleep(1)
                conn_state = int(self.get_calling_state_query().strip())

            elif conn_state == cm_pmt_anritsu.ANRITSU_LOOP_MODE_1_CLOSE:
                if self.count < 0:
                    logger.info('END CALL and FLY ON and OFF for WCDMA')
                    self.set_init_before_calling_wcdma(self.dl_ch)
                    self.set_end()
                    self.set_test_mode()
                    self.set_lvl_status('ON')
                    time.sleep(10)
                    self.flymode_circle()
                    time.sleep(10)
                    self.set_connecting()
                    self.count = 10
                    conn_state = int(self.get_calling_state_query().strip())
                else:
                    logger.info('Status: LOOP MODE(CLOSE)')
                    time.sleep(2)
                    conn_state = int(self.get_calling_state_query().strip())
                    self.count -= 1

        logger.info('Loop mode 1 and connected')

    def set_registration_calling_gsm(self):
        pass

    def set_registration_calling_hspa(self):
        """
            ANRITSU_IDLE = 1	        #Idle state
            ANRITSU_IDLE_REGIST = 2		#Idle( Regist ) Idle state (location registered)
            ANRITSU_LOOP_MODE_1 = 7	    # Under communication or connected
            ANRITSU_LOOP_MODE_1_CLOSED = 9  # it seems like waiting to loop mode between Loopback mode 1 and IDLE
        """
        self.set_lvl_status('ON')
        self.set_test_mode()
        self.set_init_hspa()
        # self.flymode_circle()

        conn_state = int(self.get_calling_state_query().strip())

        self.count = 10
        while conn_state != cm_pmt_anritsu.ANRITSU_LOOP_MODE_1:  # this is for waiting connection
            if conn_state == cm_pmt_anritsu.ANRITSU_IDLE:
                self.set_end()
                logger.info('IDLE')
                time.sleep(10)
                logger.info('START CALL')
                self.flymode_circle()
                time.sleep(10)
                self.set_connecting()
                conn_state = int(self.get_calling_state_query().strip())

            elif conn_state == cm_pmt_anritsu.ANRITSU_IDLE_REGIST:
                logger.info('Status: IDLE_REGIST')
                self.set_connecting()
                time.sleep(1)
                conn_state = int(self.get_calling_state_query().strip())

            elif conn_state == cm_pmt_anritsu.ANRITSU_REGIST:
                logger.info('Status: REGIST')
                time.sleep(1)
                conn_state = int(self.get_calling_state_query().strip())

            elif conn_state == cm_pmt_anritsu.ANRITSU_LOOP_MODE_1_CLOSE:
                if self.count < 0:
                    logger.info('END CALL and FLY ON and OFF for HSUPA')
                    self.set_init_before_calling_wcdma(self.dl_ch)
                    self.set_init_hspa()
                    self.set_end()
                    self.set_test_mode()
                    self.set_lvl_status('ON')
                    time.sleep(10)
                    self.flymode_circle()
                    time.sleep(10)
                    self.set_connecting()
                    conn_state = int(self.get_calling_state_query().strip())
                    self.count = 10
                else:
                    logger.info('Status: LOOP MODE(CLOSE)')
                    time.sleep(2)
                    conn_state = int(self.get_calling_state_query().strip())
                    self.count -= 1

        logger.info('Loop mode 1 and connected')
        time.sleep(2)

        # self.set_registration_after_calling_hspa()

    def set_registration_after_calling_hspa(self):
        if self.chcoding == 'EDCHTEST':  # this is HSUPA
            self.set_registration_after_calling_hsupa()

        elif self.chcoding == 'FIXREFCH':  # this is HSDPA
            self.set_registration_after_calling_hsdpa()

    def set_registration_after_calling_hsdpa(self):
        self.set_screen_select('FMEAS')
        self.set_power_pattern('HSMAXPWR')
        self.set_init_power(1)
        self.set_init_aclr('WCDMA', 1)

    def set_registration_after_calling_hsupa(self):
        self.set_screen_select('FMEAS')
        self.set_power_pattern('HSMAXPWR')
        self.set_output_level(-86)
        self.set_init_power(1)
        self.set_init_aclr('WCDMA', 1)
        self.set_throughput_on_off('ON')
        self.set_throughput_sample_hsupa(15)
        self.set_ehich_pattern('ACK')

    def set_uplink_channel(self, standard, ul_ch):
        """
            Use this function only in FDD test mode.
            For Anritsu8820C, it could be used in link mode
        """
        s = standard
        if s == 'LTE' or s == 'WCDMA':
            return self.set_ulchan(ul_ch)

        elif s == 'GSM':
            pass

    def set_downlink_channel(self, standard, dl_ch):
        """
        Use this function only in FDD test mode
        For Anritsu8820C, it could be used in link mode
        """
        s = standard
        if s == 'LTE' or s == 'WCDMA':
            return self.set_dlchan(dl_ch)
        elif s == 'GSM':
            pass

    def set_init_power(self, count=1):
        self.set_power_measure_on_off('ON')  # Set [Power Measurement] to [On]
        self.set_power_count(count)  # Set [Average Count] to [count] times

    def set_init_aclr(self, standard, count=1):
        s = standard
        if s == 'LTE':
            self.set_aclr_measure_on_off('ON')  # Set [ACLR Measurement] to [On]
            self.set_aclr_count(count)  # Set [ACLR Count] to [count] times
        elif s == 'WCDMA':
            self.set_adj_measure_on_off('ON')  # Set [ACLR Measurement] to [On]
            self.set_adj_count(count)  # Set [ACLR Count] to [count] times
        elif s == 'GSM':
            pass

    def set_init_sem(self, count=1):
        self.set_sem_measure_on_off('ON')  # Set [SEM Measurement] to [On]
        self.set_sem_count(count)  # Set [SEM Count] to [count] times

    def set_init_obw(self, count=20):
        self.set_obw_measure_on_off('ON')  # Set [OBW Measurement] to [On]
        self.set_obw_count(count)  # Set [OBW Count] to [count] times

    def set_init_mod(self, standard, count=1):
        """
        this for EVM usage and some other modulation
        Set the average measurement count to 16 times because the average for 16 timeslots is described in the standards
        for 6.5.2.1A PUSCH-EVM with exclusion period
        """
        s = standard
        if s == 'LTE':
            self.set_mod_measure_on_off('ON')  # Set [MOD Measurement] to [On]
            self.set_mod_count(count)  # Set [MOD Count] to [count] times
        elif s == 'WCDMA':
            self.set_evm_origin_offset_on_off('ON')  # set [EVM include Origin Offset] to [On]
            self.set_mod_measure_on_off('ON')  # Set [MOD Measurement] to [On]
            self.set_mod_count(count)  # Set [MOD Count] to [count] times
        elif s == 'GSM':
            pass

    def set_init_power_template(self, standard, count=1):
        s = standard
        if s == 'LTE':
            self.set_power_template_on_off('ON')  # Set [Power template] to [On]
            self.set_power_template_count(count)  # Set [Power template] to [count] times
        elif s == 'WCDMA':
            self.set_power_wdr_on_off('ON')  # Set [Power template] to [On]
            self.set_power_wdr_count(count)  # Set [Power template] to [count] times
        elif s == 'GSM':
            pass

    def set_init_hspa(self):
        if self.chcoding == 'EDCHTEST':  # this is HSUPA
            self.set_init_hsupa()
        elif self.chcoding == 'FIXREFCH':  # this is HSDPA
            self.set_init_hsdpa()

    def set_init_hsdpa(self):
        self.set_channel_coding('FIXREFCH')
        self.set_dpch_timing_offset(6)
        self.set_power_pattern('HSMAXPWR')
        self.set_register_mode('COMBINED')
        self.set_domain_drmc('CS')
        self.set_authentication_algorithm('XOR')
        self.set_hsupa_setting('HSET1_QPSK')
        self.set_throughput_on_off('OFF')
        self.set_input_level(-10)
        self.anritsu_query('*OPC?')

    def set_init_hsupa(self):
        self.set_channel_coding('EDCHTEST')
        self.set_dpch_timing_offset(6)
        self.set_max_ul_tx_power(21)
        self.set_tpc_algorithm(2)
        self.set_domain_drmc('CS')
        self.set_authentication_algorithm('XOR')
        self.set_hsupa_setting('TTI10_QPSK')
        self.anritsu_query('*OPC?')

    def set_init_rx(self, standard):
        s = standard
        if s == 'LTE':
            self.set_test_parameter('RX_SENS')
            self.set_tpc('AUTO')
            self.set_input_level(5)
            self.set_output_level(-70)
            self.set_rx_sample(1000)
            self.set_throughput_early_on_off('ON')
            self.set_init_power()
            self.set_mod_measure_on_off('OFF')

        elif s == 'WCDMA':
            self.set_input_level(5)
            self.set_output_level(-70)
            self.set_rx_sample(1000)  # this is should be ber_sample?
            self.set_throughput_early_on_off('OFF')
            self.set_init_power()
        elif s == 'GSM':
            pass

    def set_rb_location(self, band, bw):
        rb_num, rb_location = cm_pmt_anritsu.special_uplink_config_sensitivity(band, bw)
        self.set_rb_size(rb_num)
        self.set_rb_start(rb_location)

    def preset_subtest1(self):
        if self.chcoding == 'EDCHTEST':  # this is HSUPA
            self.set_delta_cqi(8)
            self.set_subtest('SUBTEST1')
            self.set_tpc('ILPC')
            self.set_input_level(16)
            time.sleep(0.15)
            self.set_tpc('ALT')
            self.set_input_level(26)
            logger.debug('TPC DOWN')
            time.sleep(0.15)
            self.set_tpc_cmd_down()
            time.sleep(0.1)
            self.set_to_measure()
        elif self.chcoding == 'FIXREFCH':  # this is HSDPA
            self.set_input_level(24)
            self.set_output_level(-86)
            self.set_tpc('ALL1')
            self.set_dtch_data_pattern('PN9')
            self.set_delta_cqi(8)
            self.set_subtest('SUBTEST1')
            time.sleep(0.1)
            self.set_to_measure()

    def get_hsdpa_evm(self):
        """
        evm = [po, p1, p2, p3], phase_disc = [theta0, theta1]
        :return:
        """
        self.set_dpch_timing_offset(6)
        # self.inst.write('CHCODING FIXREFCH')
        self.set_power_pattern('HSPC')
        self.set_delta_cqi(7)
        self.set_subtest('SUBTEST3')
        self.set_output_level(-86.0)
        self.set_dtch_data_pattern('PN9')
        self.set_screen_select('TDMEAS')
        self.set_measurement_object('HSDPCCH_MA')
        self.set_hsma_item('EVMPHASE')
        self.set_rrc_filter('OFF')
        self.set_input_level(35)
        self.set_tpc('ALL1')
        time.sleep(0.3)
        self.set_tpc('ALT')
        time.sleep(0.1)
        self.set_to_measure()
        evm_hpm = self.get_evm_hpm()
        logger.debug(evm_hpm)
        phase_disc_hpm = self.get_phase_disc_query()
        logger.debug(phase_disc_hpm)

        # below is for LPM -18dBm
        # self.set_tpc('ILPC')
        # self.inst.write('HSSCCH OFF')
        # self.inst.write('CQIFEEDBACK 0')
        # self.set_input_level(-18)
        # time.sleep(1)
        # self.set_tpc('ALT')
        # self.inst.write('HSSCCH ON')
        # self.inst.write('CQIFEEDBACK 4')
        # self.set_input_level(-10)
        # self.set_to_measure()
        # evm_lpm = self.inst.query('POINT_EVM? ALL').strip().split(',')  # p0, p1, p2, p3
        # logger.debug(evm_lpm)
        # phase_disc_lpm = self.inst.query('POINT_PHASEDISC? ALL').strip().split(',')  # theta0, theta1
        # logger.debug(phase_disc_lpm)

        return evm_hpm, phase_disc_hpm

    @staticmethod
    def get_worse_phase_disc(phase_disc):
        [temp1, temp2] = phase_disc
        phase_disc = [Decimal(x) for x in phase_disc]
        phase_disc_worst = max(list(map(abs, phase_disc)))
        if abs(Decimal(temp1)) == phase_disc_worst:
            return Decimal(temp1)
        elif abs(Decimal(temp2)) == phase_disc_worst:
            return Decimal(temp2)

    def get_subtest1_power_aclr(self):
        """
        :return: power, ACLR, subtest_number for HSUPA
        :return: power, ACLR, EVM, subtest_number for HSDPA
        """
        logger.info('Start to subtest1')
        if self.chcoding == 'EDCHTEST':  # this is HSUPA
            logger.info('start to measure HSUPA')
            self.preset_subtest1()
            power = self.get_uplink_power('WCDMA')
            result = self.get_etfci_query()
            logger.debug(f'Now ETFCI result is: {result}')
            mstat = int(self.get_measure_state_query())
            logger.debug(f'mstat: {mstat}')
            if mstat == cm_pmt_anritsu.MESUREMENT_TIMEOUT:
                logger.debug('time out and recall')
                self.set_end()
                time.sleep(3)
                self.set_connecting()
                self.preset_subtest1()
            result = cm_pmt_anritsu.HSUPA_ETFCI_SUBTEST1
            logger.debug('force to the subtest1 ETFCI')
            while result == cm_pmt_anritsu.HSUPA_ETFCI_SUBTEST1:
                logger.debug('TPC UP')
                self.set_tpc_cmd_up()
                time.sleep(0.15)
                self.set_to_measure()
                power = self.get_uplink_power('WCDMA')
                result = self.get_etfci_query()
                logger.debug(f'Now ETFCI result is: {result}')

            while result != cm_pmt_anritsu.HSUPA_ETFCI_SUBTEST1:
                logger.debug('TPC DOWN')
                self.set_tpc_cmd_down()
                time.sleep(0.15)
                self.set_to_measure()
                power = self.get_uplink_power('WCDMA')
                result = self.get_etfci_query()
                logger.debug(f'Now ETFCI result is: {result}')

            logger.info(f'Subtest1 to capture the final power is {power}')

            aclr = self.get_uplink_aclr('WCDMA')

            self.set_tpc('ILPC')
            self.set_input_level(5)

            return power, aclr, 1

        elif self.chcoding == 'FIXREFCH':  # this is HSDPA
            logger.info('start to measure HSDPA')
            self.preset_subtest1()
            power = self.get_uplink_power('WCDMA')
            aclr = self.get_uplink_aclr('WCDMA')

            return power, aclr, 1

    def preset_subtest2(self):
        if self.chcoding == 'EDCHTEST':  # this is HSUPA
            self.set_delta_cqi(8)
            self.set_subtest('SUBTEST2')
            self.set_tpc('ILPC')
            self.set_input_level(14)
            time.sleep(0.15)
            self.set_tpc('ALT')
            self.set_input_level(26)
            logger.debug('TPC DOWN')
            self.set_tpc_cmd_down()
            time.sleep(0.15)
            self.set_to_measure()
        elif self.chcoding == 'FIXREFCH':  # this is HSDPA
            self.set_input_level(24)
            self.set_output_level(-86)
            self.set_tpc('ALL1')
            self.set_dtch_data_pattern('PN9')
            self.set_delta_cqi(8)
            self.set_subtest('SUBTEST2')
            time.sleep(0.15)
            self.set_to_measure()

    def get_subtest2_power_aclr(self):
        logger.info('Start to subtest2')
        if self.chcoding == 'EDCHTEST':  # this is HSUPA
            self.preset_subtest2()
            power = self.get_uplink_power('WCDMA')
            result = self.get_etfci_query()
            logger.debug(f'Now ETFCI result is: {result}')
            mstat = int(self.get_measure_state_query())
            logger.debug(f'mstat: {mstat}')
            if mstat == cm_pmt_anritsu.MESUREMENT_TIMEOUT:
                self.preset_subtest2()
            result = cm_pmt_anritsu.HSUPA_ETFCI_SUBTEST2
            logger.debug('force to the subtest2 ETFCI')
            while result == cm_pmt_anritsu.HSUPA_ETFCI_SUBTEST2:
                logger.debug('TPC UP')
                self.set_tpc_cmd_up()
                time.sleep(0.15)
                self.set_to_measure()
                power = self.get_uplink_power('WCDMA')
                result = self.get_etfci_query()
                logger.debug(f'Now ETFCI result is: {result}')

            while result != cm_pmt_anritsu.HSUPA_ETFCI_SUBTEST2:
                logger.debug('TPC DOWN')
                self.set_tpc_cmd_down()
                time.sleep(0.15)
                self.set_to_measure()
                power = self.get_uplink_power('WCDMA')
                result = self.get_etfci_query()
                logger.debug(f'Now ETFCI result is: {result}')

            logger.info(f'Subtest2 to capture the final power is {power}')
            aclr = self.get_uplink_aclr('WCDMA')

            self.set_tpc('ILPC')
            self.set_input_level(5)

            return power, aclr, 2

        elif self.chcoding == 'FIXREFCH':  # this is HSDPA
            logger.info('start to measure HSDPA')
            self.preset_subtest2()
            power = self.get_uplink_power('WCDMA')
            aclr = self.get_uplink_aclr('WCDMA')
            evm = self.get_uplink_evm('WCDMA')

            return power, aclr, 2

    def preset_subtest3(self):
        if self.chcoding == 'EDCHTEST':
            self.set_delta_cqi(8)
            self.set_subtest('SUBTEST3')
            self.set_tpc('ILPC')
            self.set_input_level(15)
            time.sleep(0.15)
            self.set_tpc('ALT')
            self.set_input_level(26)
            logger.debug('TPC DOWN')
            self.set_tpc_cmd_down()
            time.sleep(0.15)
            self.set_to_measure()
        elif self.chcoding == 'FIXREFCH':
            self.set_input_level(24)
            self.set_output_level(-86)
            self.set_tpc('ALL1')
            self.set_dtch_data_pattern('PN9')
            self.set_delta_cqi(8)
            self.set_subtest('SUBTEST3')
            time.sleep(0.15)
            self.set_to_measure()

    def get_subtest3_power_aclr(self):
        logger.info('Start to subtest3')
        if self.chcoding == 'EDCHTEST':  # this is HSUPA
            self.preset_subtest3()
            power = self.get_uplink_power('WCDMA')
            result = self.get_etfci_query()
            logger.debug(f'Now ETFCI result is: {result}')
            mstat = int(self.get_measure_state_query())
            logger.debug(f'mstat: {mstat}')
            if mstat == cm_pmt_anritsu.MESUREMENT_TIMEOUT:
                self.preset_subtest3()
            result = cm_pmt_anritsu.HSUPA_ETFCI_SUBTEST3
            logger.debug('force to the subtest3 ETFCI')
            while result == cm_pmt_anritsu.HSUPA_ETFCI_SUBTEST3:
                logger.debug('TPC UP')
                self.set_tpc_cmd_up()
                time.sleep(0.15)
                self.set_to_measure()
                power = self.get_uplink_power('WCDMA')
                result = self.get_etfci_query()
                logger.debug(f'Now ETFCI result is: {result}')

            while result != cm_pmt_anritsu.HSUPA_ETFCI_SUBTEST3:
                logger.debug('TPC DOWN')
                self.set_tpc_cmd_down()
                time.sleep(0.15)
                self.set_to_measure()
                power = self.get_uplink_power('WCDMA')
                result = self.get_etfci_query()
                logger.debug(f'Now ETFCI result is: {result}')

            logger.info(f'Subtest3 to capture the final power is {power}')
            aclr = self.get_uplink_aclr('WCDMA')

            self.set_tpc('ILPC')
            self.set_input_level(5)

            return power, aclr, 3
        elif self.chcoding == 'FIXREFCH':  # this is HSDPA
            logger.info('start to measure HSDPA')
            self.preset_subtest3()
            power = self.get_uplink_power('WCDMA')
            aclr = self.get_uplink_aclr('WCDMA')
            evm, phase_disc = self.get_hsdpa_evm()
            evm = Decimal(max(evm))
            phase_disc = Decimal(self.get_worse_phase_disc(phase_disc))

            return power, aclr, evm, 3

    def preset_subtest4(self):
        if self.chcoding == 'EDCHTEST':
            self.set_delta_cqi(8)
            self.set_subtest('SUBTEST4')
            self.set_tpc('ILPC')
            self.set_input_level(14)
            time.sleep(0.15)
            self.set_tpc('ALT')
            self.set_input_level(26)
            logger.debug('TPC DOWN')
            self.set_tpc_cmd_down()
            time.sleep(0.15)
            self.set_to_measure()
        elif self.chcoding == 'FIXREFCH':
            self.set_input_level(24)
            self.set_output_level(-86)
            self.set_tpc('ALL1')
            self.set_dtch_data_pattern('PN9')
            self.set_delta_cqi(8)
            self.set_subtest('SUBTEST4')
            time.sleep(0.15)
            self.set_to_measure()

    def get_subtest4_power_aclr(self):
        logger.info('Start to subtest4')
        if self.chcoding == 'EDCHTEST':  # this is HSUPA
            self.preset_subtest4()
            power = self.get_uplink_power('WCDMA')
            result = self.get_etfci_query()
            logger.debug(f'Now ETFCI result is: {result}')
            mstat = int(self.get_measure_state_query())
            logger.debug(f'mstat: {mstat}')
            if mstat == cm_pmt_anritsu.MESUREMENT_TIMEOUT:
                self.preset_subtest4()
            result = cm_pmt_anritsu.HSUPA_ETFCI_SUBTEST4
            logger.debug('force to the subtest4 ETFCI')
            while result == cm_pmt_anritsu.HSUPA_ETFCI_SUBTEST4:
                logger.debug('TPC UP')
                self.set_tpc_cmd_up()
                time.sleep(0.15)
                self.set_to_measure()
                power = self.get_uplink_power('WCDMA')
                result = self.get_etfci_query()
                logger.debug(f'Now ETFCI result is: {result}')

            while result != cm_pmt_anritsu.HSUPA_ETFCI_SUBTEST4:
                logger.debug('TPC DOWN')
                self.set_tpc_cmd_down()
                time.sleep(0.15)
                self.set_to_measure()
                power = self.get_uplink_power('WCDMA')
                result = self.get_etfci_query()
                logger.debug(f'Now ETFCI result is: {result}')

            logger.info(f'Subtest4 to capture the final power is {power}')
            aclr = self.get_uplink_aclr('WCDMA')

            self.set_tpc('ILPC')
            self.set_input_level(5)

            return power, aclr, 4
        elif self.chcoding == 'FIXREFCH':  # this is HSDPA
            logger.info('start to measure HSDPA')
            self.preset_subtest4()
            power = self.get_uplink_power('WCDMA')
            aclr = self.get_uplink_aclr('WCDMA')
            evm = self.get_uplink_evm('WCDMA')

            return power, aclr, 4

    def preset_subtest5(self):
        self.set_throughput_sample_hsupa('OFF')
        self.set_subtest5_versin('NEW')
        self.set_delta_cqi(8)
        self.set_subtest('SUBTEST5')
        self.set_tpc('ILPC')
        self.set_input_level(16)
        time.sleep(0.15)
        self.set_input_level(26)
        self.set_tpc('ALL1')
        time.sleep(1)
        self.set_to_measure()

    def get_subtest5_power_aclr(self):
        logger.info('Start to subtest5')
        if self.chcoding == 'EDCHTEST':  # this is HSUPA
            self.preset_subtest5()
            mstat = int(self.inst.query('mstat?').strip())
            logger.debug(f'mstat: {mstat}')
            if mstat == cm_pmt_anritsu.MESUREMENT_TIMEOUT:
                self.preset_subtest5()
            logger.info('subtest5:')
            power = self.get_uplink_power('WCDMA')
            aclr = self.get_uplink_aclr('WCDMA')

            self.inst.write('TPUTU_MEAS OFF')
            self.inst.write('SET_HSSUBTEST SUBTEST1')
            self.set_tpc('ILPC')
            self.set_input_level(5)

            return power, aclr, 5
        elif self.chcoding == 'FIXREFCH':
            logger.info("HSDPA doesn't have subtest5")

    def get_uplink_power(self, standard):
        """
        Get UL power
        """
        s = standard  # WCDMA|GSM|LTE
        logger.debug("Current Format: " + s)
        if s == 'LTE':
            # power = Decimal(self.inst.query('POWER? AVG').strip())
            power = round(self.get_power_average_query(), 1)
            self.anritsu_query('*OPC?')
            logger.info(f'POWER: {power}')
            return power
        elif s == 'WCDMA':
            # power = Decimal(self.inst.query('AVG_POWER?').strip())
            power = round(self.get_power_average_query(), 2)
            self.anritsu_query('*OPC?')
            logger.info(f'POWER: {power}')
            return power
        elif s == 'GSM':
            pass

    def get_uplink_aclr(self, standard):
        """
            LTE:
                Get LTE ACLR
                return in [EUTRA-1, EUTRA+1, UTRA-1, URTA+1, UTRA-2, URTA+2,]
            WCDMA:
                Get LTE ACLR
                return in [LOW5, UP5, LOW10, UP10,] format

        """
        s = standard  # WCDMA|GSM|LTE
        logger.debug("Current Format: " + s)
        aclr = []
        if s == 'LTE':
            aclr.append(Decimal(self.inst.query('MODPWR? E_LOW1,AVG').strip()))
            aclr.append(Decimal(self.inst.query('MODPWR? E_UP1,AVG').strip()))
            aclr.append(Decimal(self.inst.query('MODPWR? LOW1,AVG').strip()))
            aclr.append(Decimal(self.inst.query('MODPWR? UP1,AVG').strip()))
            aclr.append(Decimal(self.inst.query('MODPWR? LOW2,AVG').strip()))
            aclr.append(Decimal(self.inst.query('MODPWR? UP2,AVG').strip()))
            self.inst.query('*OPC?')
            logger.info(f'ACLR: {aclr}')
            return aclr
        elif s == 'WCDMA':
            aclr.append(Decimal(self.inst.query('AVG_MODPWR? LOW5').strip()))
            aclr.append(Decimal(self.inst.query('AVG_MODPWR? UP5').strip()))
            aclr.append(Decimal(self.inst.query('AVG_MODPWR? LOW10').strip()))
            aclr.append(Decimal(self.inst.query('AVG_MODPWR? UP10').strip()))
            self.inst.query('*OPC?')
            logger.info(f'ACLR: {aclr}')
            return aclr
        elif s == 'GSM':
            pass

    def get_uplink_evm(self, standard):
        """
            Get Error Vector Magnitude (EVM) - PUSCH @ max power
        """
        s = standard  # WCDMA|GSM|LTE
        logger.debug("Current Format: " + s)
        if s == 'LTE':
            evm = Decimal(self.inst.query('EVM? AVG').strip())
            self.inst.query('*OPC?')
            logger.info(f'EVM: {evm}')
            return evm
        elif s == 'WCDMA':
            evm = Decimal(self.inst.query('AVG_EVM?').strip())
            self.inst.query('*OPC?')
            logger.info(f'EVM: {evm}')
            return evm
        elif s == 'GSM':
            pass

    def aclr_ch_judge(self, standard, band, dl_ch, bw=None):
        if standard == 'LTE':
            if dl_ch < cm_pmt_anritsu.dl_ch_selected(self.std, band, bw)[1]:
                self.aclr_ch = 'ch01'
            elif dl_ch == cm_pmt_anritsu.dl_ch_selected(self.std, band, bw)[1]:
                self.aclr_ch = 'ch02'
            elif dl_ch > cm_pmt_anritsu.dl_ch_selected(self.std, band, bw)[1]:
                self.aclr_ch = 'ch03'
        elif standard == 'WCDMA':
            if dl_ch < cm_pmt_anritsu.dl_ch_selected(self.std, band)[1]:
                self.aclr_ch = 'ch01'
            elif dl_ch == cm_pmt_anritsu.dl_ch_selected(self.std, band)[1]:
                self.aclr_ch = 'ch02'
            elif dl_ch > cm_pmt_anritsu.dl_ch_selected(self.std, band)[1]:
                self.aclr_ch = 'ch03'
        elif standard == 'GSM':
            pass


