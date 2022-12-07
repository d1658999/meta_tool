import time
from decimal import Decimal

from equipments.series_basis.callbox.anritsu_series import Anritsu
from utils.log_init import log_set
from utils.loss_handler import read_loss_file
import utils.parameters.common_parameters_anritsu as cm_pmt_anritsu
import utils.parameters.external_paramters as ext_pmt
from utils.fly_mode import FlyMode

logger = log_set('Anritsu8820')


class Anritsu8820(Anritsu):
    def __init__(self, equipment='Anristu8820'):
        super().__init__(equipment)
        self.excel_path = None
        self.band_segment = None
        self.mod = None
        self.evm = None
        self.aclr = None
        self.pwr = None
        self.aclr_ch = None
        self.dl_ch = None
        self.count = None
        self.chcoding = None
        self.std = None

    @staticmethod
    def get_worse_phase_disc(phase_disc):
        [temp1, temp2] = phase_disc
        phase_disc = [Decimal(x) for x in phase_disc]
        phase_disc_worst = max(list(map(abs, phase_disc)))
        if abs(Decimal(temp1)) == phase_disc_worst:
            return Decimal(temp1)
        elif abs(Decimal(temp2)) == phase_disc_worst:
            return Decimal(temp2)

    @staticmethod
    def flymode_circle():
        flymode = FlyMode()
        # flymode.com_open()
        flymode.fly_on()
        time.sleep(3)
        flymode.fly_off()
        flymode.com_close()

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

    def set_switch_to_wcdma(self):
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

    def set_switch_to_gsm(self):
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
        self.set_ulrmc_64QAM('DISABLED')

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
        self.set_ul_rb_position('MIN')
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
        if standard == 'LTE':
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

        elif standard == 'WCDMA':
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

        elif standard == 'GSM':
            pass

    def set_path_loss(self, standard):
        logger.info('Set LOSS')
        self.set_loss_table_delete()  # delete the unknown loss table first

        loss_title = 'LOSSTBLVAL'
        loss_dict = read_loss_file()
        freq = sorted(loss_dict.keys())
        for f in freq:
            self.set_loss_table_8820(loss_title, f, loss_dict[f], loss_dict[f], loss_dict[f])
        logger.debug("Current Format: " + standard)  # WCDMA|GSM|LTE
        self.set_loss_common(standard)

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
                    conn_state = int(self.get_calling_state_query())
                # logger.info('Start calling')
                # conn_state = int(self.get_calling_state_query())
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
        conn_state = int(self.get_calling_state_query())

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
                conn_state = int(self.get_calling_state_query())

            elif conn_state == cm_pmt_anritsu.ANRITSU_IDLE_REGIST:
                logger.info('Status: IDLE_REGIST')
                self.set_connecting()
                time.sleep(1)
                conn_state = int(self.get_calling_state_query())

            elif conn_state == cm_pmt_anritsu.ANRITSU_REGIST:
                logger.info('Status: REGIST')
                time.sleep(1)
                conn_state = int(self.get_calling_state_query())

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
                    conn_state = int(self.get_calling_state_query())
                else:
                    logger.info('Status: LOOP MODE(CLOSE)')
                    time.sleep(2)
                    conn_state = int(self.get_calling_state_query())
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

        conn_state = int(self.get_calling_state_query())

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
                conn_state = int(self.get_calling_state_query())

            elif conn_state == cm_pmt_anritsu.ANRITSU_IDLE_REGIST:
                logger.info('Status: IDLE_REGIST')
                self.set_connecting()
                time.sleep(1)
                conn_state = int(self.get_calling_state_query())

            elif conn_state == cm_pmt_anritsu.ANRITSU_REGIST:
                logger.info('Status: REGIST')
                time.sleep(1)
                conn_state = int(self.get_calling_state_query())

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
                    conn_state = int(self.get_calling_state_query())
                    self.count = 10
                else:
                    logger.info('Status: LOOP MODE(CLOSE)')
                    time.sleep(2)
                    conn_state = int(self.get_calling_state_query())
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
        self.set_throughput_hsupa_on_off('ON')
        self.set_throughput_sample_hsupa(15)
        self.set_ehich_pattern('ACK')

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
        self.set_throughput_hsdpa_on_off('OFF')
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
            # self.set_rx_sample(1000)  # this is should be ber_sample?
            self.ser_ber_sample(10000)
            self.set_throughput_early_on_off('OFF')
            self.set_init_power()
        elif s == 'GSM':
            pass

    def set_rb_location(self, band, bw):
        rb_num, rb_location = cm_pmt_anritsu.special_uplink_config_sensitivity(band, bw)
        self.set_ul_rb_size(rb_num)
        self.set_ul_rb_start(rb_location)

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
        evm_hpm = self.get_evm_hpm_hsdpa()
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
        self.set_throughput_hsupa_on_off('OFF')
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
            mstat = int(self.get_measure_state_query())
            logger.debug(f'mstat: {mstat}')
            if mstat == cm_pmt_anritsu.MESUREMENT_TIMEOUT:
                self.preset_subtest5()
            logger.info('subtest5:')
            power = self.get_uplink_power('WCDMA')
            aclr = self.get_uplink_aclr('WCDMA')

            self.set_throughput_hsupa_on_off('OFF')
            self.set_subtest('SUBTEST1')
            self.set_tpc('ILPC')
            self.set_input_level(5)

            return power, aclr, 5
        elif self.chcoding == 'FIXREFCH':
            logger.info("HSDPA doesn't have subtest5")

    def get_subtest_power_aclr_evm_all(self):
        """
        data = [POPWER, ACLR ,EVM], and ACLR format: [low_-1, up_+1, low_-2, up_+2] for HSDPA
        data = [POPWER, ACLR], and ACLR format: [low_-1, up_+1, low_-2, up_+2] for HSUPA
        :return: data
        """
        data = {}
        subtests = [
            self.get_subtest1_power_aclr(),
            self.get_subtest2_power_aclr(),
            self.get_subtest3_power_aclr(),
            self.get_subtest4_power_aclr(),
            self.get_subtest5_power_aclr(),
        ]

        for subtest in subtests:
            if self.chcoding == 'EDCHTEST':  # this is HSUPA
                power, aclr, subtest_number = subtest
                data[subtest_number] = [power, aclr]

            elif self.chcoding == 'FIXREFCH':  # this is HSDPA
                if subtest is not None:
                    if len(subtest) == 4:  # subtest 3
                        power, aclr, evm, subtest_number = subtest
                        data[subtest_number] = [power, aclr, evm]
                    else:
                        power, aclr, subtest_number = subtest
                        data[subtest_number] = [power, aclr]

        logger.debug(data)
        return data

    def get_uplink_power(self, standard):
        """
        Get UL power
        """
        s = standard  # WCDMA|GSM|LTE
        logger.debug("Current Format: " + s)
        if s == 'LTE':
            # power = Decimal(self.inst.query('POWER? AVG').strip())
            power = round(self.get_power_average_query('LTE'), 1)
            self.anritsu_query('*OPC?')
            logger.info(f'POWER: {power}')
            return power
        elif s == 'WCDMA':
            # power = Decimal(self.inst.query('AVG_POWER?').strip())
            power = round(self.get_power_average_query('WCDMA'), 1)
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
        if s == 'LTE':
            aclr = self.get_aclr_query_lte()
            self.anritsu_query('*OPC?')
            logger.info(f'ACLR: {aclr}')
            return aclr
        elif s == 'WCDMA':
            aclr = self. get_aclr_query_wcdma()
            self.anritsu_query('*OPC?')
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
            evm = round(self.get_evm_query_lte(), 2)
            self.anritsu_query('*OPC?')
            logger.info(f'EVM: {evm}')
            return evm
        elif s == 'WCDMA':
            evm = round(self.get_evm_query_wcdma(), 2)
            self.anritsu_query('*OPC?')
            logger.info(f'EVM: {evm}')
            return evm
        elif s == 'GSM':
            pass

    def sweep_sensitivity(self, start=-70, coarse=1, fine=0.2):
        if self.std == 'LTE':
            touch = 0  # flag if 0: reduce power by coarse, if 1: reduce power by fine
            count = 3
            while True:
                self.set_output_level(start)
                logger.info(f"Search sensitivity: {self.get_output_level_query()}")
                self.set_to_measure()
                time.sleep(0.1)
                status = self.get_throughput_pass_query()
                conn_state = int(self.get_calling_state_query())

                if status == 'PASS' and touch == 0:  # by coarse
                    start -= coarse
                    touch = 0

                elif status == 'PASS' and touch == 1:  # by fine
                    start -= fine
                    status = self.get_throughput_pass_query()
                    while count > 1 and status == 'PASS':
                        status = self.get_throughput_pass_query()
                        count -= 1
                    count = 3

                elif status == 'FAIL' and touch == 0:
                    while count > 0 and status == 'FAIL':  # retest 3 time to judge if it is real sensitivity
                        self.set_to_measure()
                        time.sleep(0.1)
                        status = self.get_throughput_pass_query()
                        logger.info(f'{status}')
                        count -= 1
                    if count != 0:  # if it meets some sudden noise from environment
                        continue
                    else:  # real sensitivity failed
                        logger.info('Back to higher 2dB')
                        start += 2
                        count = 3
                        touch = 1

                elif status == 'FAIL' and touch == 1:  # it might be the real sensitivity
                    while True:
                        if status == 'FAIL':
                            start += fine
                            start = round(start, 1)
                            self.set_output_level(start)
                            self.set_to_measure()
                            status = self.get_throughput_pass_query()
                            output_level = self.get_output_level_query()
                            logger.info(f'level {output_level}, {status}')

                        elif status == '*':
                            logger.info('Connection is dropped')
                            logger.info('Retest again from output level -70dBm')
                            start = -70
                            self.set_output_level(start)
                            self.set_end()
                            time.sleep(2)
                            self.set_connecting()
                            time.sleep(2)
                            self.flymode_circle()
                            logger.info('waiting 10 seconds')
                            time.sleep(10)
                            conn_state = int(self.get_calling_state_query())
                            if conn_state == cm_pmt_anritsu.ANRITSU_CONNECTED:
                                start -= fine
                                self.set_to_measure()
                                status = self.get_throughput_pass_query()
                                while status == 'PASS':
                                    self.set_output_level(start)
                                    self.set_to_measure()
                                    status = self.get_throughput_pass_query()
                                    output_level = self.get_output_level_query('LTE')
                                    logger.info(f'reconnedted level {output_level}: {status}')
                                    start -= fine
                            else:
                                start = -70
                                logger.info('Skip this channel, and set the output level to -70dBm for notice')

                        elif status == 'PASS':
                            while count > 0:
                                self.set_to_measure()
                                output_level = self.get_output_level_query('LTE')
                                status = self.get_throughput_pass_query()
                                if status == 'FAIL':
                                    logger.info(f'{4 - count} times fail')
                                    break
                                logger.info(f"sensitivity: {output_level}, pass {4 - count} times")
                                count -= 1

                            count = 3

                            if status == 'FAIL':
                                continue
                            else:
                                break
                    sensitivity = Decimal(self.get_output_level_query('LTE'))
                    time.sleep(0.1)
                    per = self.get_throughput_per_query()
                    power = round(self.get_power_average_query('LTE'), 1)
                    self.anritsu_query('*OPC?')
                    logger.info(f'Final: POWER: {power}, SENSITIVITY: {sensitivity}, PER:{per}')
                    return [power, sensitivity, per]

                elif conn_state != cm_pmt_anritsu.ANRITSU_CONNECTED:
                    count = 3
                    sub_count = 100
                    while count > 0 and conn_state != cm_pmt_anritsu.ANRITSU_CONNECTED:
                        logger.info('Call drop and fly on and off')
                        self.set_end()
                        time.sleep(2)
                        self.set_connecting()
                        time.sleep(2)
                        self.flymode_circle()
                        while conn_state != cm_pmt_anritsu.ANRITSU_CONNECTED and sub_count > 0:
                            time.sleep(1)
                            logger.info('Wait 1 second to connect')
                            conn_state = int(self.get_calling_state_query())
                            sub_count -= 1
                        logger.info('Reconnected')
                        sub_count = 100
                        count -= 1
                    if count == 0:
                        logger.info('Stop this circle')
                        break
        elif self.std == 'WCDMA':
            touch = 0  # flag if 0: reduce power by coarse, if 1: reduce power by fine
            count = 3
            while True:
                self.set_output_level(start)
                logger.info(f"Search sensitivity: {self.get_output_level_query()}")
                time.sleep(0.1)
                conn_state = int(self.get_calling_state_query())
                self.set_to_measure()
                status = self.get_ber_per_query_wcdma()
                mstate = int(self.get_measure_state_query())
                logger.debug(f'measuring statuse: {mstate}')

                if mstate == cm_pmt_anritsu.MESUREMENT_GOOD and conn_state == cm_pmt_anritsu.ANRITSU_LOOP_MODE_1 \
                        and status == 'PASS' and touch == 0:  # by coarse
                    start -= coarse
                    touch = 0

                elif mstate == cm_pmt_anritsu.MESUREMENT_GOOD and conn_state == cm_pmt_anritsu.ANRITSU_LOOP_MODE_1 \
                        and status == 'PASS' and touch == 1:  # by fine
                    start -= fine
                    status = self.get_ber_per_query_wcdma()
                    while count > 1 and status == 'PASS':
                        status = self.get_ber_per_query_wcdma()
                        count -= 1
                    count = 3

                elif mstate == cm_pmt_anritsu.MESUREMENT_GOOD and conn_state == cm_pmt_anritsu.ANRITSU_LOOP_MODE_1 \
                        and status == 'FAIL' and touch == 0:
                    while count > 0 and status == 'FAIL':  # retest 3 time to judge if it is real sensitivity
                        self.set_to_measure()
                        time.sleep(0.1)
                        status = self.get_ber_per_query_wcdma()
                        logger.info(f'{status}')
                        count -= 1
                    if count != 0:  # if it meets some sudden noise from environment
                        continue
                    else:  # real sensitivity failed
                        logger.info('Back to higher 2dB')
                        start += 2
                        count = 3
                        touch = 1

                elif mstate == cm_pmt_anritsu.MESUREMENT_GOOD and conn_state == cm_pmt_anritsu.ANRITSU_LOOP_MODE_1 \
                        and status == 'FAIL' and touch == 1:  # it might be the real sensitivity
                    while mstate != cm_pmt_anritsu.MESUREMENT_TIMEOUT:
                        if status == 'FAIL':
                            start += fine
                            start = round(start, 1)
                            self.set_output_level(start)
                            self.set_to_measure()
                            status = self.get_ber_per_query_wcdma()
                            output_level = self.get_output_level_query()
                            logger.info(f'level {output_level}, {status}')
                            mstate = int(self.get_measure_state_query())

                        elif conn_state != cm_pmt_anritsu.ANRITSU_LOOP_MODE_1:
                            logger.debug(f'measuring statuse: {mstate}')
                            logger.info('Connection is dropped')
                            logger.info('Retest again from output level -70dBm')
                            start = -70
                            self.set_output_level(start)
                            self.set_input_level()
                            self.set_end()
                            time.sleep(2)
                            self.set_connecting()
                            time.sleep(2)
                            self.flymode_circle()
                            logger.info('waiting 10 seconds')
                            time.sleep(10)
                            conn_state = int(self.get_calling_state_query())
                            if conn_state == cm_pmt_anritsu.ANRITSU_LOOP_MODE_1:
                                self.set_input_level(30)
                                start -= fine
                                self.set_to_measure()
                                status = self.get_ber_per_query_wcdma()
                                while status == 'PASS':
                                    self.set_output_level(start)
                                    self.set_to_measure()
                                    status = self.get_ber_per_query_wcdma()
                                    output_level = self.get_output_level_query()
                                    logger.info(f'reconnedted level {output_level}: {status}')
                                    start -= fine

                            else:
                                start = -70
                                logger.info('Skip this channel, and set the output level to -70dBm for notice')

                        elif status == 'PASS':
                            while count > 0:
                                self.set_to_measure()
                                output_level = self.get_output_level_query()
                                status = self.get_ber_per_query_wcdma()
                                if status == 'FAIL':
                                    logger.info(f'{4 - count} times fail')
                                    break
                                logger.info(f"sensitivity: {output_level}, pass {4 - count} times")
                                count -= 1
                                mstate = int(self.get_measure_state_query())

                            count = 3

                            if status == 'FAIL':
                                continue
                            else:
                                break
                    sensitivity = Decimal(self.get_power_average_query('WCDMA'))
                    time.sleep(0.1)
                    per = self.get_ber_per_query_wcdma()
                    power = Decimal(self.get_avg_power_query())
                    self.anritsu_query('*OPC?')
                    logger.info(f'Final: POWER: {power}, SENSITIVITY: {sensitivity}, PER:{per}')
                    return [power, sensitivity, per]

                elif mstate != cm_pmt_anritsu.MESUREMENT_TIMEOUT and conn_state != cm_pmt_anritsu.ANRITSU_LOOP_MODE_1:
                    logger.debug(f'measuring statuse: {mstate}')
                    logger.info('Call drop and fly on and off')
                    logger.info('Retest again and Reconnected')
                    touch = 0
                    start = -70
                    dl_ch = int(self.get_downlink_channel_query())
                    tpc_status = self.get_tpc_pattern_query()
                    self.set_init_before_calling(self.std, dl_ch)
                    self.set_registration_calling(self.std)
                    self.set_init_rx(self.std)
                    self.set_tpc(tpc_status)
                    if tpc_status == 'ALL1':
                        self.set_input_level(30)
                    elif tpc_status == 'ILPC':
                        self.set_input_level(-10)

                    self.set_ber_measure_on_off('ON')
                    self.set_power_measure_on_off('ON')

                elif mstate == cm_pmt_anritsu.MESUREMENT_TIMEOUT:
                    logger.info('Time out')
                    logger.info('Retest again and Reconnected')
                    touch = 0
                    start = -70
                    dl_ch = int(self.get_downlink_channel_query())
                    tpc_status = self.get_tpc_pattern_query()
                    self.set_init_before_calling(self.std, dl_ch)
                    self.set_registration_calling(self.std)
                    self.set_init_rx(self.std)
                    self.set_tpc(tpc_status)
                    if tpc_status == 'ALL1':
                        self.set_input_level(30)
                    elif tpc_status == 'ILPC':
                        self.set_input_level(-10)

                    self.set_ber_measure_on_off('ON')
                    self.set_power_measure_on_off('ON')

    def get_sensitivity(self, standard, band, dl_ch, bw=None):
        self.std = s = standard
        if s == 'LTE':
            """
                sens_list = [power, sensitivity, per]
            """
            self.set_handover(s, dl_ch, bw)
            time.sleep(0.1)
            self.set_rb_location(band, bw)
            sens_list = self.sweep_sensitivity()
            return sens_list

        elif s == 'WCDMA':
            """
                sens_list = [power, sensitivity, per]
            """
            self.set_ber_measure_on_off('ON')
            self.set_power_measure_on_off('ON')
            self.set_handover(s, dl_ch)
            time.sleep(0.1)
            sens_list = self.sweep_sensitivity()
            return sens_list
        elif s == 'GSM':
            pass

    def get_validation(self, standard):
        s = standard  # WCDMA|GSM|LTE
        logger.debug("Current Format: " + s)
        if s == 'LTE':
            return self.get_power_aclr_evm_lte()
        elif s == 'WCDMA':
            if self.chcoding == 'REFMEASCH':  # this is WCDMA
                return self.get_power_aclr_evm_wcdma()
            elif self.chcoding == 'EDCHTEST':  # this is HSUPA
                return self.get_subtest_power_aclr_evm_all()
            elif self.chcoding == 'FIXREFCH':  # this is HSDPA
                return self.get_subtest_power_aclr_evm_all()
        elif s == 'GSM':
            pass

    def get_power_aclr_evm_lte(self):
        """
            Only measure RB@min
            The format in dictionary is {Q_1: [power, (rb_size, rb_start)],
            Q_P: [power, aclr, evm, (rb_size, rb_start)], ...}
            and ACLR format is [EUTRA-1, EUTRA+1, UTRA-1, URTA+1, UTRA-2, URTA+2,]
        """
        want_mods = [
            'TX_MAXPWR_Q_1',
            'TX_MAXPWR_Q_P',
            'TX_MAXPWR_Q_F',
            'TX_MAXPWR_16_P',
            'TX_MAXPWR_16_F',
            'TX_MAXPWR_64_P',
            'TX_MAXPWR_64_F',
        ]

        validation_dict = {}

        self.set_init_power()
        self.set_init_aclr('LTE')
        self.set_init_mod('LTE')
        self.set_input_level(ext_pmt.tx_level)
        self.set_tpc('ALL3')
        self.anritsu_query('*OPC?')

        for mod in want_mods:
            self.mod = mod[18:]
            conn_state = int(self.get_calling_state_query())
            self.count = 5
            # this is for waiting connection before change modulation if there is connection problems
            while conn_state != cm_pmt_anritsu.ANRITSU_CONNECTED:
                logger.info('Call drops...')
                if self.count == 0:
                    # equipment end call and start call
                    logger.info('End call and then start call')
                    self.flymode_circle()
                    time.sleep(5)
                    self.set_end()
                    self.anritsu_query('*OPC?')
                    time.sleep(1)
                    self.set_connecting()
                    time.sleep(10)
                    self.count = 6
                    conn_state = int(self.get_calling_state_query())

                else:
                    time.sleep(10)
                    self.count -= 1
                    logger.info('wait 10 seconds to connect')
                    logger.info(f'{6 - self.count} times to wait 10 second')
                    conn_state = int(self.get_calling_state_query())

            validation_list = []
            if mod == 'TX_MAXPWR_64_P':
                self.set_test_parameter('TX_MAXPWR_Q_P')
                self.set_ulrmc_64QAM('ENABLED')
                self.set_ulmcs(21)
            elif mod == 'TX_MAXPWR_64_F':
                self.set_test_parameter('TX_MAXPWR_Q_F')
                self.set_ulrmc_64QAM('ENABLED')
                self.set_ulmcs(21)
            else:
                self.set_ulrmc_64QAM('DISABLED')
                self.set_test_parameter(mod)

            self.set_to_measure()
            meas_status = int(self.get_measure_state_query())

            while meas_status == cm_pmt_anritsu.MESUREMENT_BAD:  # this is for the reference signal is not found
                logger.info('measuring status is bad(Reference signal not found)')
                logger.info('Equipment is forced to set End Call')
                self.set_end()
                time.sleep(5)
                logger.info('fly on and off again')
                self.flymode_circle()
                time.sleep(10)
                self.set_connecting()
                logger.info('waiting for 10 second to re-connect')
                logger.info('measure it again')
                self.set_to_measure()
                meas_status = int(self.get_measure_state_query())

            if mod == 'TX_MAXPWR_Q_1':  # mod[10:] -> Q_1
                logger.info(mod)
                validation_list.append(self.get_uplink_power('LTE'))
                validation_list.append((self.get_ul_rb_size_query(), self.get_ul_rb_start_query()))
                validation_dict[mod[10:]] = validation_list
                self.anritsu_query('*OPC?')
            else:  # mod[10:] -> Q_P, Q_F, 16_P, 16_F, 64_F
                logger.info(mod)
                self.pwr = self.get_uplink_power('LTE')
                validation_list.append(self.pwr)
                self.aclr = self.get_uplink_aclr('LTE')
                validation_list.append(self.aclr)
                self.evm = self.get_uplink_evm('LTE')
                validation_list.append(self.evm)
                validation_list.append((self.get_ul_rb_size_query(), self.get_ul_rb_start_query()))
                validation_dict[mod[10:]] = validation_list
                self.anritsu_query('*OPC?')
        logger.debug(validation_dict)
        return validation_dict

    def get_power_aclr_evm_wcdma(self):
        """
            Only measure RB@min
            The format in dictionary is [power, aclr, evm]
            and ACLR format is [UTRA-1, URTA+1, UTRA-2, URTA+2,]
        """

        self.set_init_power()
        self.set_init_aclr('WCDMA')
        self.set_init_mod('WCDMA')
        self.set_input_level(26)
        self.set_output_level(-93)
        self.set_tpc('ALL1')
        self.anritsu_query('*OPC?')

        validation_list = []
        time.sleep(0.1)
        self.set_to_measure()

        self.pwr = self.get_uplink_power('WCDMA')
        validation_list.append(self.pwr)
        self.aclr = self.get_uplink_aclr('WCDMA')
        validation_list.append(self.aclr)
        self.evm = self.get_uplink_evm('WCDMA')
        validation_list.append(self.evm)
        self.anritsu_query('*OPC?')
        logger.debug(validation_list)
        return validation_list
