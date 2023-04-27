import time

from utils.log_init import log_set
import utils.parameters.external_paramters as ext_pmt
from connection_interface.connection_serial import ModemComport
from utils.parameters.common_parameters_ftm import TDD_BANDS


logger = log_set('AtCmd')


class AtCmd:
    def __init__(self):
        self.mcs_cc2_lte = None
        self.rb_start_cc2_lte = None
        self.rb_size_cc2_lte = None
        self.mcs_cc1_lte = None
        self.rb_start_cc1_lte = None
        self.rb_size_cc1_lte = None
        self.bw_combo_lte = None
        self.ser = ModemComport()
        self.port_tx = None
        self.tech = None
        self.bw_fr1 = None
        self.bw_lte = None
        self.band_fr1 = None
        self.band_lte = None
        self.band_wcdma = None
        self.band_gsm = None
        self.tx_level = None
        self.rx_level = ext_pmt.init_rx_sync_level
        self.pcl = None
        self.pwr_init_gsm = None
        self.loss_tx = None
        self.loss_rx = None
        self.tx_freq_fr1 = None
        self.tx_freq_lte = None
        self.tx_chan_wcdma = None
        self.tx_freq_gsm = None
        self.rx_freq_fr1 = None
        self.rx_freq_lte = None
        self.rx_freq_wcdma = None
        self.rx_freq_gsm = None
        self.rx_chan_gsm = None
        self.scs = None
        self.type_fr1 = None
        self.mcs_fr1 = None
        self.mcs_lte = None
        self.rb_size_fr1 = None
        self.rb_start_fr1 = None
        self.rb_size_lte = None
        self.rb_start_lte = None
        self.tsc = None
        self.mod_gsm = None
        self.asw_on_off = 0  # 1: AS ON, 0: AS OFF
        self.asw_tech = None
        self.sync_path = ext_pmt.sync_path
        self.asw_srs_path = None
        self.asw_path = ext_pmt.asw_path
        self.srs_path = ext_pmt.srs_path
        self.tx_path = None
        self.rx_path_fr1 = None
        self.rx_path_lte = None
        self.rx_path_wcdma = None
        self.rx_path_gsm = None
        self.sync_mode = 0  # 0: MAIN , 1: 4RX, 2: 6RX
        self.rx_chan_wcdma = None
        self.sa_nsa_mode = ext_pmt.sa_nsa
        self.ul_symbol = None
        self.ul_slot = None
        self.dl_symbol = None
        self.dl_slot = None
        self.uldl_period = None
        self.rssi = None
        self.fer = None
        self.esens_list = None
        self.agc_list = None
        self.cinr_list = None
        self.rsrp_list = None
        self.init_dicts()

    def command(self, command='at', delay=0.2):
        logger.info(f'MTM: <<{command}')
        command = command + '\r'
        self.ser.write(command.encode())
        time.sleep(delay)
        response = self.ser.readlines()
        for res in response:
            r = res.decode().split()
            if len(r) > 1:  # with more than one response
                for rr in r:
                    logger.info(f'MTM: >>{rr}')
            else:
                if not r:  # sometimes there is not \r\n in the middle response
                    continue
                else:  # only one response
                    logger.info(f'MTM: >>{r[0]}')

        while b'OK\r\n' not in response:
            logger.info('OK is not at the end, so repeat again')
            logger.info(f'==========repeat to response again=========')
            response = self.ser.readlines()
            time.sleep(1)
            for res in response:
                r = res.decode().split()
                if len(r) > 1:  # with more than one response
                    for rr in r:
                        logger.info(f'MTM: >>{rr}')
                else:
                    if not r:  # sometimes there is not \r\n in the middle response
                        continue
                    else:  # only one response
                        logger.info(f'MTM: >>{r[0]}')
        return response

    def init_dicts(self):
        self.asw_tech_dict = {
            'GSM': 0,
            'WCDMA': 1,
            'LTE': 2,
            'FR1': 6,
        }
        self.tx_path_dict = {
            'TX1': 0,
            'TX2': 1,
            'MIMO': 20,
        }
        self.bw_lte_dict = {
            1.4: 0,
            3: 1,
            5: 2,
            10: 3,
            15: 4,
            20: 5,
        }
        # self.bw_lte_ca_dict = {
        #     '20+5': 6,
        #     '20+10': 7,
        #     '20+15': 8,
        #     '20+20': 9,
        #     '15+15': 10,
        #     '15+10': 11,
        #     '15+20': 12,
        #     '10+20': 13,
        #     '10+15': 14,
        #     '5+20': 15,
        #     '5+10': 16,
        #     '10+10': 17,
        #     '10+5': 18,
        #     '5+15': 19,
        #     '15+5': 20,
        #     '40': 21,
        # }
        self.bw_fr1_dict = {
            5: 0,
            10: 1,
            15: 2,
            20: 3,
            25: 4,
            30: 5,
            40: 6,
            50: 7,
            60: 8,
            80: 9,
            90: 10,
            100: 11,
            70: 12,
        }
        self.mcs_lte_dict = {
            'QPSK': 0,
            'Q16': 11,
            'Q64': 25,
            'Q256': 27,
        }
        self.mcs_fr1_dict = {
            'BPSK': 1,
            'QPSK': 2,
            'Q16': 4,
            'Q64': 6,
            'Q256': 8,
        }
        self.rb_select_lte_dict = {
            'PRB': 0,
            'FRB': 1,
            '1RB_0': 2,
            '1RB_MAX': 3,
        }
        self.type_dict = {
            'DFTS': 0,
            'CP': 1,
        }
        self.rb_alloc_fr1_dict = {
            'EDGE_FULL_LEFT': 0,
            'EDGE_FULL_RIGHT': 1,
            'EDGE_1RB_LEFT': 2,
            'EDGE_1RB_RIGHT': 3,
            'OUTER_FULL': 4,
            'INNER_FULL': 5,
            'INNER_1RB_LEFT': 6,
            'INNER_1RB_RIGHT': 7,
        }
        self.scs_dict = {
            15: 0,
            30: 1,
            60: 2,
        }
        self.rx_path_gsm_dict = {
            2: 'RX0',
            1: 'RX1',
            4: 'RX2',
            8: 'RX3',
            3: 'RX0+RX1',
            12: 'RX2+RX3',
            15: 'ALL PATH',
        }
        self.rx_path_wcdma_dict = {
            2: 'RX0',
            1: 'RX1',
            4: 'RX2',
            8: 'RX3',
            3: 'RX0+RX1',
            12: 'RX2+RX3',
            15: 'ALL PATH',
        }
        self.rx_path_lte_dict = {
            2: 'RX0',
            1: 'RX1',
            4: 'RX2',
            8: 'RX3',
            3: 'RX0+RX1',
            12: 'RX2+RX3',
            15: 'ALL PATH',
        }
        self.rx_path_fr1_dict = {
            2: 'RX0',
            1: 'RX1',
            4: 'RX2',
            8: 'RX3',
            3: 'RX0+RX1',
            12: 'RX2+RX3',
            15: 'ALL PATH',
        }
        self.duty_cycle_dict = {
            100: (6, 0, 0, 10, 0),
            50: (6, 5, 0, 5, 0),
        }
        self.sync_path_dict = {
            'Main': 0,
            'CA#1': 1,
            'CA#2': 2,
            'CA#3': 3,
        }
        self.band_tx_set_dict_gsm = {
            900: 0,
            1800: 1,
            1900: 2,
            850: 3,
        }

        self.band_tx_meas_dict_gsm = {
            900: 'G09',
            1800: 'G18',
            1900: 'G19',
            850: 'G085',
        }
        self.mod_dict_gsm = {
            'GMSK': 0,
            'EPSK': 1,
        }

    def select_scs_fr1(self, band):
        """
        For now FDD is forced to 15KHz and TDD is to be 30KHz
        """
        if band in TDD_BANDS:
            scs = 1
        else:
            scs = 0
        self.scs = 15 * (2 ** scs)  # for now TDD only use 30KHz, FDD only use 15KHz

    def test_reset_gsm(self):
        print("----------EDGE Test Reset----------")
        self.command(f'AT+TESTRESET')

    def set_test_mode_fr1(self):  # SA: 0, NSA: 1
        """
        SA: 0, NSA: 1
        """
        logger.info('----------Set Test Mode----------')
        self.command(f'AT+NRFFINALSTART={self.band_fr1},{self.sa_nsa_mode}')
        # self.command_cmw100_query('*OPC?')

    def set_test_mode_lte(self):
        logger.info('----------Set Test Mode----------')
        self.command(f'AT+LRFFINALSTART=1,{self.band_lte}')
        self.command(f'AT+LMODETEST')
        # self.command_cmw100_query('*OPC?')

    def set_test_mode_wcdma(self):
        logger.info('----------Set Test Mode----------')
        self.command(f'AT+HSPATMSTART')

    def set_test_mode_gsm(self):
        logger.info('----------Set Test Mode----------')
        self.command(f'AT+HNSSTOP')
        self.command(f'AT+TESTSTR')

    def set_test_end_fr1(self, delay=0.2):
        logger.info('----------Set End----------')
        self.command(f'AT+NRFFINALFINISH', delay)
        # self.command_cmw100_query('*OPC?')

    def set_test_end_lte(self, delay=0.2):
        logger.info('----------Set End----------')
        self.command(f'AT+LRFFINALFINISH', delay)
        # self.command_cmw100_query('*OPC?')

    def set_test_end_wcdma(self, delay=0.2):
        logger.info('----------Set End----------')
        self.command(f'AT+HSPATMEND', delay)
        # self.command_cmw100_query('*OPC?')

    def set_test_end_gsm(self, delay=0.2):
        logger.info('----------Set End----------')
        self.command(f'AT+TESTEND', delay)
        # self.command_cmw100_query('*OPC?')

    def sync_fr1(self):
        logger.info('---------Sync----------')
        scs = 1 if self.band_fr1 in TDD_BANDS else 0
        response = self.command(
            f'AT+NRFSYNC={self.sync_path_dict[self.sync_path]},{self.sync_mode},{scs},'
            f'{self.bw_fr1_dict[self.bw_fr1]},0,{self.rx_freq_fr1}',
            delay=1)
        while b'+NRFSYNC:1\r\n' not in response:
            logger.info('**********Sync repeat**********')
            time.sleep(1)
            response = self.command(
                f'AT+NRFSYNC={self.sync_path_dict[self.sync_path]},{self.sync_mode},{scs},'
                f'{self.bw_fr1_dict[self.bw_fr1]},0,{self.rx_freq_fr1}',
                delay=2)

    def sync_lte(self):
        logger.info('---------Sync----------')
        response = self.command(f'AT+LSYNC={self.sync_path_dict[self.sync_path]},{self.sync_mode},{self.rx_freq_lte}',
                                delay=1.2)
        while b'+LSYNC:1\r\n' not in response:
            logger.info('**********Sync repeat**********')
            time.sleep(1)
            response = self.command(
                f'AT+LSYNC={self.sync_path_dict[self.sync_path]},{self.sync_mode},{self.rx_freq_lte}', delay=2)

    def sync_wcdma(self):
        logger.info('---------Sync----------')
        self.command(f'AT+HDLSYNC={self.rx_chan_wcdma}', delay=0.5)

    def sync_gsm(self):
        logger.info('---------Sync----------')
        self.command(f'AT+TESTRESET', delay=0.2)
        self.command(
            f'AT+TESTSYNC={self.band_tx_set_dict_gsm[self.band_gsm]},0,{self.rx_chan_gsm},'
            f'{-1 * int(round(self.rx_level, 0))}',
            delay=0.5)

    def tx_set_fr1(self):
        logger.info('---------Tx Set----------')
        self.command(
            f'AT+NTXSENDREQ={self.tx_path_dict[self.tx_path]},{self.tx_freq_fr1},{self.bw_fr1_dict[self.bw_fr1]},'
            f'{self.scs_dict[self.scs]},{self.rb_size_fr1},{self.rb_start_fr1},{self.mcs_fr1_dict[self.mcs_fr1]},'
            f'{self.type_dict[self.type_fr1]},{self.tx_level}')
        logger.info(
            f'TX_PATH: {self.tx_path}, BW: {self.bw_fr1}, TX_FREQ: {self.tx_freq_fr1}, RB_SIZE: {self.rb_size_fr1}, '
            f'RB_OFFSET: {self.rb_start_fr1}, MCS: {self.mcs_fr1}, TX_LEVEL: {self.tx_level}')
        # self.command_cmw100_query('*OPC?')

    def tx_set_lte(self):
        """
        tx_path: TX1: 0 (main path)| TX2: 1 (sub path)
        bw_lte: 1.4: 0 | 3: 1 | 5: 2 | 10: 3 | 15: 4 | 20: 5
        tx_freq_lte:
        rb_num:
        rb_start:
        mcs: "QPSK": 0 | "Q16": 11 | "Q64": 25 | "Q256": 27
        pwr:
        """
        logger.info('---------Tx Set----------')
        self.command(
            f'AT+LTXSENDREQ={self.tx_path_dict[self.tx_path]},{self.bw_lte_dict[self.bw_lte]},{self.tx_freq_lte},'
            f'{self.rb_size_lte},{self.rb_start_lte},{self.mcs_lte_dict[self.mcs_lte]},2,1,{self.tx_level}')
        logger.info(f'TX_PATH: {self.tx_path}, BW: {self.bw_lte}, TX_FREQ: {self.tx_freq_lte}, '
                    f'RB_SIZE: {self.rb_size_lte}, RB_OFFSET: {self.rb_start_lte}, MCS: {self.mcs_lte}, '
                    f'TX_LEVEL: {self.tx_level}')
        # self.command_cmw100_query('*OPC?')

    def tx_set_wcdma(self):
        logger.info('---------Tx Set----------')
        self.command(f'AT+HDELULCHAN')
        self.command(f'AT+HTXPERSTART={self.tx_chan_wcdma}')
        self.command(f'AT+HSETMAXPOWER={self.tx_level * 10}')
        logger.info(f'Tx_chan: {self.tx_chan_wcdma}, Tx_level: {self.tx_level}')

    def tx_set_wcdma_level_use(self):
        logger.info('---------Tx Set----------')
        self.command(f'AT+HTXPERSTART={self.tx_chan_wcdma}')
        self.command(f'AT+HSETMAXPOWER={self.tx_level * 10}')
        logger.info(f'Tx_chan: {self.tx_chan_wcdma}, Tx_level: {self.tx_level}')

    def tx_set_gsm(self):
        logger.info('---------Tx Set----------')
        self.command(
            f'AT+TESTTX={self.band_tx_set_dict_gsm[self.band_gsm]},{self.mod_dict_gsm[self.mod_gsm]},'
            f'{self.rx_chan_gsm},1,3')
        self.command(f'AT+TESTPWR=0,{self.pcl},{self.pcl},{self.pcl},{self.pcl}')
        logger.info(f'Band: {self.band_gsm}, Modulation: {self.mod_gsm}, Chan: {self.rx_chan_gsm}, PCL: {self.pcl}')

    def set_duty_cycle(self):
        logger.info(f'----------Set duty cycle: {ext_pmt.duty_cycle}----------')
        if self.band_fr1 in TDD_BANDS:
            self.uldl_period = self.duty_cycle_dict[ext_pmt.duty_cycle][0]
            self.dl_slot = self.duty_cycle_dict[ext_pmt.duty_cycle][1]
            self.dl_symbol = self.duty_cycle_dict[ext_pmt.duty_cycle][2]
            self.ul_slot = self.duty_cycle_dict[ext_pmt.duty_cycle][3]
            self.ul_symbol = self.duty_cycle_dict[ext_pmt.duty_cycle][4]
            logger.info('---TDD, so need to set the duty cycle')
            logger.debug(f'Duty Cycle setting: {self.uldl_period}, {self.dl_slot}, {self.dl_symbol}, {self.ul_slot}, '
                         f'{self.ul_symbol}')
        else:
            self.uldl_period = 0
            self.dl_slot = 0
            self.dl_symbol = 0
            self.ul_slot = 0
            self.ul_symbol = 0
            logger.info("---FDD, so don't need to set the duty cycle")
            logger.debug(f'Duty Cycle setting: {self.uldl_period}, {self.dl_slot}, {self.dl_symbol}, '
                         f'{self.ul_slot}, {self.ul_symbol}')

    def tx_set_no_sync_fr1(self):
        logger.info('---------Tx No Sync----------')
        self.scs = 30 if self.band_fr1 in TDD_BANDS else 15
        self.command(
            f'AT+NRFACTREQ={self.tx_path_dict[self.tx_path]},{self.tx_freq_fr1},{self.bw_fr1_dict[self.bw_fr1]},'
            f'{self.scs_dict[self.scs]},{self.rb_size_fr1},{self.rb_start_fr1},{self.mcs_fr1_dict[self.mcs_fr1]},'
            f'{self.type_dict[self.type_fr1]},{self.tx_level},{self.uldl_period},{self.dl_slot},{self.dl_symbol},'
            f'{self.ul_slot},{self.ul_symbol}')
        logger.info(
            f'TX_PATH: {self.tx_path}, BW: {self.bw_fr1}, TX_FREQ: {self.tx_freq_fr1}, RB_SIZE: {self.rb_size_fr1}, '
            f'RB_OFFSET: {self.rb_start_fr1}, MCS: {self.mcs_fr1}, TX_LEVEL: {self.tx_level}, '
            f'Duty cycle: {ext_pmt.duty_cycle} %')

    def antenna_switch(self):  # 1: AS ON, 0: AS OFF, this is old version, please use v2
        logger.info('---------Antenna Switch----------')
        self.command(f'AT+LTXASTUNESET={self.asw_on_off}')
        if self.asw_on_off == 0:
            logger.info('Antenna Switch OFF')
        elif self.asw_on_off == 1:
            logger.info('Antenna Switch ON')

    def antenna_switch_v2(self):
        """
        this is to place on the first to activate
        AT+ANTSWSEL=P0,P1	//Set Tx DPDT switch
        P0: RAT (0=GSM, 1=WCDMA, 2=LTE, 4=CDMA, 6=NR)
        P1: ANT path (0=default, 1=switched, 4=dynamic mode),
        P1 (P0=NR): ANT Path (0=Tx-Ant1, 1=Tx-Ant2, 2=Tx-Ant3, 3=Tx-Ant4, 4=dynamic switch mode)
        tech:
        ant_path:
        """
        asw_en = ext_pmt.asw_path_enable
        if asw_en:
            self.asw_tech = self.tech
            logger.info('---------Antenna Switch----------')
            self.command(f'AT+ANTSWSEL={self.asw_tech_dict[self.asw_tech]},{self.asw_path}')
            logger.info(f'RAT: {self.asw_tech}, ANT_PATH: {self.asw_path}')
            self.asw_srs_path = self.asw_path
            # self.command_cmw100_query('*OPC?')
        else:
            self.asw_srs_path = self.asw_path = None

    def srs_switch(self):
        logger.info('---------SRS Switch----------')
        self.command(f'AT+NTXSRSSWPATHSET={self.srs_path}')
        logger.info(f'SRS_PATH: {self.srs_path}')
        self.asw_srs_path = self.srs_path

    def rx_path_setting_fr1(self):
        """
        2: PRX, 1: DRX, 4: RX2, 8:RX3, 3: PRX+DRX, 12: RX2+RX3, 15: ALL PATH
        """
        if self.rx_path_fr1 is None:
            self.rx_path_fr1 = 15
        logger.info('----------Rx path setting----------')
        logger.info(f'----------Now is {self.rx_path_fr1_dict[self.rx_path_fr1]}---------')
        self.command(f'AT+NRXMODESET={self.rx_path_fr1}')
        # self.command_cmw100_query('*OPC?')

    def rx_path_setting_lte(self):
        """
        2: PRX, 1: DRX, 4: RX2, 8:RX3, 3: PRX+DRX, 12: RX2+RX3, 15: ALL PATH
        """
        if self.rx_path_lte is None:
            self.rx_path_lte = 15
        logger.info('----------Rx path setting----------')
        logger.info(f'----------Now is {self.rx_path_lte_dict[self.rx_path_lte]}---------')
        self.command(f'AT+LRXMODESET={self.rx_path_lte}')
        # self.command_cmw100_query('*OPC?')

    def rx_path_setting_wcdma(self):
        """
        2: PRX, 1: DRX, 3: PRX+DRX 15: ALL PATH
        """
        logger.info('----------Rx path setting----------')
        logger.info(f'----------Now is {self.rx_path_wcdma_dict[self.rx_path_wcdma]}---------')
        self.command(f'AT+HRXMODESET={self.rx_path_wcdma}')
        # self.command_cmw100_query('*OPC?')

    def rx_path_setting_gsm(self):
        """
        0: PRX, 1: DRX
        """
        logger.info('----------Rx path setting----------')
        logger.info(f'---------Now is {self.rx_path_gsm_dict[self.rx_path_gsm]}---------')
        rx_path_gsm = None
        if self.rx_path_gsm == 2:
            rx_path_gsm = 0
        elif self.rx_path_gsm == 1:
            rx_path_gsm = 1
        self.command(f'AT+ERXSEL={rx_path_gsm}')
        # self.command_cmw100_query('*OPC?')

    def rx_path_setting_sig_lte(self):
        """
        original FTM:
        2: PRX, 1: DRX, 4: RX2, 8:RX3, 3: PRX+DRX, 12: RX2+RX3, 15: ALL PATH
        signaling:
        1: PRX, 2: DRX, 4: RX2, 8:RX3, 3: PRX+DRX, 12: RX2+RX3, 15: ALL PATH
        """
        self.ser.com_open()
        if self.rx_path is None:
            self.rx_path = 0
        logger.info('----------Rx path setting----------')
        rx_path_lte = self.rx_path_lte_dict[self.rx_path]
        logger.info(f'----------Now is {rx_path_lte}---------')
        if self.rx_path == 2:
            rx_path = 1
        elif self.rx_path == 1:
            rx_path = 2
        else:
            rx_path = self.rx_path

        self.command(f'AT+LRXMODESET={rx_path}')
        # self.command_cmw100_query('*OPC?')
        self.ser.com_close()

    def rx_path_setting_sig_wcdma(self):
        """
        original FTM:
        2: PRX, 1: DRX, 3: PRX+DRX 15: ALL PATH
        signaling:
        1: PRX, 2: DRX, 3: PRX+DRX 15: ALL PATH
        """
        self.ser.com_open()
        if self.rx_path is None:
            self.rx_path = 0
        logger.info('----------Rx path setting----------')
        rx_path_wcdma = self.rx_path_wcdma_dict[self.rx_path]
        logger.info(f'----------Now is {rx_path_wcdma}---------')
        if self.rx_path == 2:
            rx_path = 1
        elif self.rx_path == 1:
            rx_path = 2
        else:
            rx_path = self.rx_path
        self.command(f'AT+HRXMODESET={rx_path}')
        # self.command_cmw100_query('*OPC?')
        self.ser.com_close()


    def rx_path_setting_sig_gsm(self):
        """
        0: PRX, 1: DRX
        """
        self.ser.com_open()
        if self.rx_path is None:
            self.rx_path = 0
        logger.info('----------Rx path setting----------')
        rx_path_gsm = self.rx_path_gsm_dict[self.rx_path_gsm]
        logger.info(f'---------Now is {rx_path_gsm}---------')
        if self.rx_path_gsm == 2:
            rx_path = 1
        elif self.rx_path_gsm == 1:
            rx_path = 2
        else:
            rx_path = self.rx_path
        self.command(f'AT+ERXPATHSET={rx_path}')
        # self.command_cmw100_query('*OPC?')
        self.ser.com_close()

    def query_rsrp_cinr_fr1(self):
        res = self.command(f'AT+NRXMEAS={self.rx_path_fr1},20')
        for line in res:
            if '+NRXMEAS:' in line.decode():
                self.rsrp_list = line.decode().split(':')[1].strip().split(',')[:4]
                self.cinr_list = line.decode().split(':')[1].strip().split(',')[4:]
                self.rsrp_list = [eval(rsrp) / 100 for rsrp in self.rsrp_list]
                self.cinr_list = [eval(cinr) / 100 for cinr in self.cinr_list]
                logger.info(f'**** RSRP: {self.rsrp_list} ****')
                logger.info(f'**** CINR: {self.cinr_list} ****')

    def query_rsrp_cinr_lte(self):
        res = self.command(f'AT+LRXMEAS={self.rx_path_lte},20')
        for line in res:
            if '+LRXMEAS:' in line.decode():
                self.rsrp_list = line.decode().split(':')[1].strip().split(',')[:4]
                self.cinr_list = line.decode().split(':')[1].strip().split(',')[4:]
                self.rsrp_list = [eval(rsrp) / 100 for rsrp in self.rsrp_list]
                self.cinr_list = [eval(cinr) / 100 for cinr in self.cinr_list]
                logger.info(f'**** RSRP: {self.rsrp_list} ****')
                logger.info(f'**** CINR: {self.cinr_list} ****')

    # def query_rsrp_cinr_wcdma(self):
    #     res = self.command(f'AT+LRXMEAS={self.rx_path_lte},20')
    #     for line in res:
    #         if '+LRXMEAS:' in line.decode():
    #             self.rsrp_list = line.decode().split(':')[1].strip().split(',')[:4]
    #             self.cinr_list = line.decode().split(':')[1].strip().split(',')[4:]
    #             self.rsrp_list = [eval(rsrp) / 100 for rsrp in self.rsrp_list]
    #             self.cinr_list = [eval(cinr) / 100 for cinr in self.cinr_list]
    #             logger.info(f'**** RSRP: {self.rsrp_list} ****')
    #             logger.info(f'**** CINR: {self.cinr_list} ****')

    def query_agc_fr1(self):
        res = self.command(f'AT+NAGCIDXRD')
        for line in res:
            if '+NRX1RX2AGCIDXRD:' in line.decode():
                self.agc_list = line.decode().split(':')[1].strip().split(',')
                self.agc_list = [eval(agc) for agc in self.agc_list]
                logger.info(f'**** AGC: {self.agc_list} ****')

    def query_agc_lte(self):
        res = self.command(f'AT+LRX1RX2AGCIDXRD')
        for line in res:
            if '+LRX1RX2AGCIDXRD:' in line.decode():
                self.agc_list = line.decode().split(':')[1].strip().split(',')
                self.agc_list = [eval(agc) for agc in self.agc_list]
                logger.info(f'**** AGC: {self.agc_list} ****')

    # def query_agc_wcdma(self):
    #     res = self.command(f'AT+LRX1RX2AGCIDXRD')
    #     for line in res:
    #         if '+LRX1RX2AGCIDXRD:' in line.decode():
    #             self.agc_list = line.decode().split(':')[1].strip().split(',')
    #             self.agc_list = [eval(agc) for agc in self.agc_list]
    #             logger.info(f'**** AGC: {self.agc_list} ****')

    def get_esens_fr1(self):
        self.esens_list = [round(self.rx_level - c - 1, 2) for c in self.cinr_list]
        logger.info(f'**** ESENS: {self.esens_list} ****')

    def get_esens_lte(self):
        self.esens_list = [round(self.rx_level - c - 1, 2) for c in self.cinr_list]
        logger.info(f'**** ESENS: {self.esens_list} ****')

    # def get_esens_wcdma(self):
    #     self.esens_list = [round(self.rx_level - c - 1, 2) for c in self.cinr_list]
    #     logger.info(f'**** ESENS: {self.esens_list} ****')

    def query_fer_measure_fr1(self):
        logger.info('========== FER measure ==========')
        res = self.command('AT+NFERMEASURE=500', delay=0.5)
        for line in res:
            if '+NFERMEASURE:' in line.decode():
                self.fer = eval(line.decode().split(':')[1])
                logger.info(f'****FER: {self.fer / 100} %****')

    def query_fer_measure_lte(self):
        logger.info('========== FER measure ==========')
        res = self.command('AT+LFERMEASURE=500', delay=0.5)
        for line in res:
            if '+LFERMEASURE:' in line.decode():
                self.fer = eval(line.decode().split(':')[1])
                logger.info(f'****FER: {self.fer / 100} %****')

    def query_fer_measure_wcdma(self):
        logger.info('========== FER measure ==========')
        res = self.command('AT+HGETSENSE=100', delay=2)
        for line in res:
            if '+GETSENSE:' in line.decode():
                self.fer = eval(line.decode().split(':')[1])
                logger.info(f'****FER: {self.fer / 1000} %****')

    def query_fer_measure_gsm(self):
        logger.info('========== FER measure ==========')
        res = self.command(f'AT+TESTBER={self.band_tx_set_dict_gsm[self.band_gsm]},{self.mod_dict_gsm[self.mod_gsm]},'
                           f'0,1,{self.rx_chan_gsm},{-1 * int(round(self.rx_level, 0))},7,2', delay=0.5)
        for line in res:
            if '+TESTBER: ' in line.decode():
                results = eval(line.decode().split(': ')[1])
                self.rssi, self.fer = [round(r / 100, 2) for r in results]
                logger.info(f'****RSSI: {self.rssi} ****')
                logger.info(f'****FER: {self.fer} %****')

    def query_thermister0(self):
        return self.command('AT+GOOGTHERMISTOR=0,1')

    def query_thermister1(self):
        return self.command('AT+GOOGTHERMISTOR=1,1')

    def set_level_fr1(self, tx_level):
        self.command(f'AT+NTXPWRLVLSET={tx_level}')

    def set_level_lte(self, tx_level):
        self.command(f'AT+LTXPWRLVLSET={tx_level}')

    def set_chan_request_lte(self):
        self.command(f'AT+LTXCHNSDREQ')

    def set_ulca_combo_lte(self):
        bw_ca_index = {
            '20+5': 6,
            '20+10': 7,
            '20+15': 8,
            '20+20': 9,
            '15+15': 10,
            '15+10': 11,
            '15+20': 12,
            '10+20': 13,
            '10+15': 14,
            '5+20': 15,
            '5+10': 16,
            '10+10': 17,
            '10+5': 18,
            '5+15': 19,
            '15+5': 20,
            '40': 21,
        }
        self.command(f'AT+LTXSENDREQSLOAPT={self.tx_path_dict[self.tx_path]},{bw_ca_index[self.bw_combo_lte]},{self.tx_freq_lte},'
                     f'{self.rb_size_cc1_lte},{self.rb_start_cc1_lte},{self.mcs_lte_dict[self.mcs_cc1_lte]},'
                     f'{self.rb_size_cc2_lte},{self.rb_start_cc2_lte},{self.mcs_lte_dict[self.mcs_cc2_lte]},'
                     f'2,2,{self.tx_level},0')

    @staticmethod
    def set_mipi_voltage_sky51001(tech, band, tx_path):
        mipi_num = None
        usid = None
        addr = None

        if tech in ['LTE', 'FR1']:
            if tx_path == 'TX1':
                if band in [26, 5, 8, 12, 13, 14, 17, 18, 19, 20, 28, 29, 71, 24]:
                    mipi_num, usid, addr = 2, 'b', 0
                elif band in [1, 2, 3, 4, 66, 7, 25, 30, 38, 41, 40, 39, 34, 70, 75, 76, ]:
                    mipi_num, usid, addr = 0, 'b', 0
                elif band in [42, 48, 77, 78, 79, ]:
                    mipi_num, usid, addr = 4, 'b', 0

            elif tx_path == 'TX2':
                if band in [1, 2, 3, 4, 66, 7, 25, 30, 38, 41, 40, 39, 34, 70, 75, 76, ]:
                    mipi_num, usid, addr = 2, 'b', 0
                elif band in [42, 48, 77, 78, 79, ]:
                    mipi_num, usid, addr = 0, 'b', 0

        elif tech in ['WCDMA']:
            if band in [1, 2, 4]:
                mipi_num, usid, addr = 0, 'b', 0
            elif band in [5, 8, 6, 19]:
                mipi_num, usid, addr = 2, 'b', 0

        return mipi_num, usid, addr

    @staticmethod
    def set_mipi_voltage_qm81052(tech, band, tx_path):
        mipi_num = None
        usid = None
        addr = None

        if tech in ['LTE', 'FR1']:
            if tx_path == 'TX1':
                if band in [26, 5, 8, 12, 13, 14, 17, 18, 19, 20, 28, 29, 71, 24]:
                    mipi_num, usid, addr = 0, 4, 0
                elif band in [1, 2, 3, 4, 66, 7, 25, 30, 38, 41, 40, 39, 34, 70, 75, 76, ]:
                    mipi_num, usid, addr = 2, 5, 0
                elif band in [42, 48, 77, 78, 79, ]:
                    mipi_num, usid, addr = 0, 4, 0

            elif tx_path == 'TX2':
                if band in [1, 2, 3, 4, 66, 7, 25, 30, 38, 41, 40, 39, 34, 70, 75, 76, ]:
                    mipi_num, usid, addr = 0, 4, 0
                elif band in [42, 48, 77, 78, 79, ]:
                    mipi_num, usid, addr = 2, 5, 0
                elif band in [26, 5, 8, 12, 13, 14, 17, 18, 19, 20, 28, 29, 71, 24]:
                    mipi_num, usid, addr = 0, 4, 0

        elif tech in ['WCDMA']:
            if band in [1, 2, 4]:
                mipi_num, usid, addr = 2, 5, 0
            elif band in [5, 8, 6, 19]:
                mipi_num, usid, addr = 0, 4, 0

        return mipi_num, usid, addr

    def query_voltage_fr1_sky51001(self, band, tx_path):
        """
        P23:
        MIPI 0 = MHB/ UHB Sub
        MIPI 2 = LB / MHB ENDC
        MIPI 4 = UHB Main
        """
        mipi_num, usid, addr = self.set_mipi_voltage_sky51001('FR1', band, tx_path)

        res = self.command(f'AT+NMIPIREAD={mipi_num},{usid},{addr}', delay=0.2)
        for line in res:
            if '+NMIPIREAD:' in line.decode():
                vol_hex = line.decode().split(':')[1].strip()
                vol_real = (int(vol_hex, 16) * 0.0256) + 0.2
                return [vol_real]

    def query_voltage_lte_sky51001(self, band, tx_path):
        """
        P23:
        MIPI 0 = MHB/ UHB Sub
        MIPI 2 = LB / MHB ENDC
        MIPI 4 = UHB Main
        """
        mipi_num, usid, addr = self.set_mipi_voltage_sky51001('LTE', band, tx_path)

        res = self.command(f'AT+MIPIREAD={mipi_num},{int(usid, 16)},{addr}', delay=0.2)
        for line in res:
            if '+MIPIREAD:' in line.decode():
                vol_hex = line.decode().split(':')[1].strip()
                vol_real = (int(vol_hex, 16) * 0.0256) + 0.2
                return [vol_real]

    def query_voltage_wcdma_sky51001(self, band, tx_path=None):
        """
        P23:
        MIPI 0 = MHB/ UHB Sub
        MIPI 2 = LB / MHB ENDC
        MIPI 4 = UHB Main
        """
        mipi_num, usid, addr = self.set_mipi_voltage_sky51001('WCDMA', band, tx_path)

        res = self.command(f'AT+HREADMIPI={mipi_num},{usid},{addr}', delay=0.2)
        for line in res:
            if 'Data' in line.decode():
                vol_hex = line.decode().split('x')[1].strip()
                vol_real = (int(vol_hex, 16) * 0.0256) + 0.2
                return [vol_real]

    def query_voltage_fr1_qm81052(self, band, tx_path):
        """
        P24:
        APT1: MIPI 0, USID 4 = LB0 / LB1 / MHB1/ UHB0
        APT2: MIPI 2, USID 5 = MHB0 / UHB1

        """
        mipi_num, usid, addr = self.set_mipi_voltage_qm81052('FR1', band, tx_path)

        res = self.command(f'AT+NMIPIREAD={mipi_num},{usid},{addr}', delay=0.2)
        for line in res:
            if '+NMIPIREAD:' in line.decode():
                vol_hex = line.decode().split(':')[1].strip()
                vol_real = (int(vol_hex, 16) * 0.0239) + 0.4
                return [vol_real]

    def query_voltage_lte_qm81052(self, band, tx_path):
        """
        P24:
        APT1: MIPI 0, USID 4 = LB0 / LB1 / MHB1/ UHB0
        APT2: MIPI 2, USID 5 = MHB0 / UHB1
        """
        mipi_num, usid, addr = self.set_mipi_voltage_qm81052('LTE', band, tx_path)

        res = self.command(f'AT+MIPIREAD={mipi_num},{int(usid, 16)},{addr}', delay=0.2)
        for line in res:
            if '+MIPIREAD:' in line.decode():
                vol_hex = line.decode().split(':')[1].strip()
                vol_real = (int(vol_hex, 16) * 0.0239) + 0.4
                return [vol_real]

    def query_voltage_wcdma_qm81052(self, band, tx_path=None):
        """
        P24:
        APT1: MIPI 0, USID 4 = LB0 / LB1 / MHB1/ UHB0
        APT2: MIPI 2, USID 5 = MHB0 / UHB1
        """
        mipi_num, usid, addr = self.set_mipi_voltage_qm81052('WCDMA', band, tx_path)

        res = self.command(f'AT+HREADMIPI={mipi_num},{usid},{addr}', delay=0.2)
        for line in res:
            if 'Data' in line.decode():
                vol_hex = line.decode().split('x')[1].strip()
                vol_real = (int(vol_hex, 16) * 0.0239) + 0.4
                return [vol_real]

    def query_voltage_selector_sky51001(self, tech, band, tx_path):
        if tech == 'FR1':
            return self.query_voltage_fr1_sky51001(band, tx_path)
        elif tech == 'LTE':
            return self.query_voltage_lte_sky51001(band, tx_path)
        elif tech == 'WCDMA':
            return self.query_voltage_wcdma_sky51001(band)

    def query_voltage_selector_qm81052(self, tech, band, tx_path):
        if tech == 'FR1':
            return self.query_voltage_fr1_qm81052(band, tx_path)
        elif tech == 'LTE':
            return self.query_voltage_lte_qm81052(band, tx_path)
        elif tech == 'WCDMA':
            return self.query_voltage_wcdma_qm81052(band)

    def query_voltage_collection(self, module='qm81052'):
        if module == 'sky51001':
            return self.query_voltage_selector_sky51001
        elif module == 'qm81052':
            return self.query_voltage_selector_qm81052
