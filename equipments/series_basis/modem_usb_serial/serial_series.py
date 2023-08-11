import time

from utils.log_init import log_set
import utils.parameters.external_paramters as ext_pmt
from connection_interface.connection_serial import ModemComport
from utils.parameters.common_parameters_ftm import TDD_BANDS
import utils.parameters.rssi_parameters as rssi
from utils.regy_handler import regy_parser, regy_parser_v2

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

    def command_nv(self, cmd='at', delay=0.2, mode='N'):
        logger.info(f'MTM: <<{cmd}')
        cmd = cmd + '\r'

        if mode == 'Q':
            self.ser.write(cmd.encode())
            time.sleep(delay)

        elif mode == 'N':
            self.ser.write(cmd.encode())
            time.sleep(delay)
            response = self.ser.readlines()
            for res in response:
                r = res.decode().strip()
                if len(r) > 1:  # with more than one response
                    logger.info(f'MTM: >>{r}')
                # else:
                #     if not r:  # sometimes there is not \r\n in the middle response
                #         continue
                #     else:  # only one response
                #         logger.info(f'MTM: >>{r[0]}')

            while b'OK\r\n' not in response:
                logger.info('OK is not at the end, so repeat again')
                logger.info(f'==========repeat to response again=========')
                response = self.ser.readlines()
                time.sleep(1)
                for res in response:
                    r = res.decode()
                    if len(r) > 1:  # with more than one response
                        for rr in r:
                            logger.info(f'MTM: >>{rr}')
                    else:
                        if not r:  # sometimes there is not \r\n in the middle response
                            continue
                        else:  # only one response
                            logger.info(f'MTM: >>{r[0]}')
            return response

    def command(self, cmd='at', delay=0.2):
        logger.info(f'MTM: <<{cmd}')
        cmd = cmd + '\r'
        self.ser.write(cmd.encode())
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

        self.apt_vcc_dict_fr1 = {
            'TX1CP': 0,
            'TX2CP': 1,
            'TX1DFTS': 2,
            'TX2DFTS': 3,
            'TX1Q256': 4,
            'TX2Q256': 5,
        }

        self.pa_mode = {
            'HPM': 0,
            'LPM': 2,
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

    def query_rssi_measure_gsm(self):
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
        self.command(
            f'AT+LTXSENDREQSLOAPT={self.tx_path_dict[self.tx_path]},{bw_ca_index[self.bw_combo_lte]},'
            f'{self.tx_freq_lte},'
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
                    mipi_num, usid, addr = 0, 4, 1
                elif band in [1, 2, 3, 4, 66, 7, 25, 30, 38, 41, 40, 39, 34, 70, 75, 76, ]:
                    mipi_num, usid, addr = 2, 5, 'b'
                elif band in [42, 48, 77, 78, 79, ]:
                    mipi_num, usid, addr = 0, 4, 1

            elif tx_path == 'TX2':
                if band in [1, 2, 3, 4, 66, 7, 25, 30, 38, 41, 40, 39, 34, 70, 75, 76, ]:
                    mipi_num, usid, addr = 0, 4, 1
                elif band in [42, 48, 77, 78, 79, ]:
                    mipi_num, usid, addr = 2, 5, 'b'
                elif band in [26, 5, 8, 12, 13, 14, 17, 18, 19, 20, 28, 29, 71, 24]:
                    mipi_num, usid, addr = 0, 4, 1

        elif tech in ['WCDMA']:
            if band in [1, 2, 4]:
                mipi_num, usid, addr = 2, 5, 'b'
            elif band in [5, 8, 6, 19]:
                mipi_num, usid, addr = 0, 4, 1

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

        res = self.command(f'AT+MIPIREAD={mipi_num},{usid},{addr}', delay=0.2)
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
        volt_lowest_list = [0.2]
        count = 10
        if tech == 'FR1':
            volt_list = self.query_voltage_fr1_sky51001(band, tx_path)
            while volt_lowest_list == volt_list:
                volt_list = self.query_voltage_fr1_sky51001(band, tx_path)
                count -= 1
                if count == 0:
                    break

            return volt_list

        elif tech == 'LTE':
            volt_list = self.query_voltage_lte_sky51001(band, tx_path)
            while volt_lowest_list == volt_list:
                volt_list = self.query_voltage_lte_sky51001(band, tx_path)
                count -= 1
                if count == 0:
                    break

            return volt_list

        elif tech == 'WCDMA':
            volt_list = self.query_voltage_wcdma_sky51001(band)
            while volt_lowest_list == volt_list:
                volt_list = self.query_voltage_wcdma_sky51001(band)
                count -= 1
                if count == 0:
                    break

            return volt_list

    def query_voltage_selector_qm81052(self, tech, band, tx_path):
        volt_lowest_list = [0.4]
        count = 10
        if tech == 'FR1':
            volt_list = self.query_voltage_fr1_qm81052(band, tx_path)
            while volt_lowest_list == volt_list:
                volt_list = self.query_voltage_fr1_qm81052(band, tx_path)
                count -= 1
                if count == 0:
                    break

            return volt_list

        elif tech == 'LTE':
            volt_list = self.query_voltage_lte_qm81052(band, tx_path)
            while volt_lowest_list == volt_list:
                volt_list = self.query_voltage_lte_qm81052(band, tx_path)
                count -= 1
                if count == 0:
                    break

            return volt_list

        elif tech == 'WCDMA':
            volt_list = self.query_voltage_wcdma_qm81052(band)
            while volt_lowest_list == volt_list:
                volt_list = self.query_voltage_wcdma_qm81052(band)
                count -= 1
                if count == 0:
                    break

            return volt_list

    def query_voltage_collection(self, module='qm81052'):
        if module == 'sky51001':
            return self.query_voltage_selector_sky51001
        elif module == 'qm81052':
            return self.query_voltage_selector_qm81052

    def query_rssi_scan(self, rssi_dict):
        rx_rat = rssi_dict["rx_rat"]
        rx_band = rssi_dict["rx_band"]
        rx_bw = rssi_dict["rx_bw"]
        scan_mode = rssi_dict["scan_mode"]
        start_rx_freq = rssi_dict["start_rx_freq"]
        stop_rx_freq = rssi_dict["stop_rx_freq"]
        step_freq = rssi_dict["step_freq"]
        antenna_selection = rssi_dict["antenna_selection"]
        sampling_count = rssi_dict["sampling_count"]
        tx1_enable = rssi_dict["tx1_enable"]
        tx1_rat = rssi_dict["tx1_rat"]
        tx1_band = rssi_dict["tx1_band"]
        tx1_bw = rssi_dict["tx1_bw"]
        tx1_freq = rssi_dict["tx1_freq"]
        tx1_pwr = rssi_dict["tx1_pwr"]
        tx1_rb_num = rssi_dict["tx1_rb_num"]
        tx1_rb_start = rssi_dict["tx1_rb_start"]
        tx1_mcs = rssi_dict["tx1_mcs"]
        tx2_enable = rssi_dict["tx2_enable"]
        tx2_rat = rssi_dict["tx2_rat"]
        tx2_band = rssi_dict["tx2_band"]
        tx2_bw = rssi_dict["tx2_bw"]
        tx2_freq = rssi_dict["tx2_freq"]
        tx2_pwr = rssi_dict["tx2_pwr"]
        tx2_rb_num = rssi_dict["tx2_rb_num"]
        tx2_rb_start = rssi_dict["tx2_rb_start"]
        tx2_mcs = rssi_dict["tx2_mcs"]

        command_rssi = f'AT+RSSISCAN=' \
                       f'{rssi.RAT[rx_rat]},' \
                       f'{rssi.rx_bands_collection(rx_rat, rx_band)},' \
                       f'{rssi.RX_BW[rx_rat][rx_bw]},' \
                       f'{rssi.SCAN_MODE[scan_mode]},' \
                       f'{start_rx_freq},' \
                       f'{stop_rx_freq},' \
                       f'{rssi.STEP_FREQ[rx_rat][step_freq]},' \
                       f'{rssi.ANTENNA_SELECTION[antenna_selection]},' \
                       f'{sampling_count},' \
                       f'0,' \
                       f'{rssi.TX1_ENABLE[tx1_enable]},' \
                       f'{tx1_band},' \
                       f'{rssi.TX_BW[tx1_rat][tx1_bw]},' \
                       f'{tx1_freq},' \
                       f'{tx1_pwr},' \
                       f'{tx1_rb_num},' \
                       f'{tx1_rb_start},' \
                       f'{rssi.MCS[tx1_mcs]},' \
                       f'{rssi.TX2_ENABLE[tx2_enable]},' \
                       f'{tx2_band},' \
                       f'{rssi.TX_BW[tx2_rat][tx2_bw]},' \
                       f'{tx2_freq},' \
                       f'{tx2_pwr},' \
                       f'{tx2_rb_num},' \
                       f'{tx2_rb_start},' \
                       f'{rssi.MCS[tx2_mcs]},'

        self.command(command_rssi)

    def set_google_nv(self, nv_name, nv_index, nv_value):
        """
        nv_value is hex not dec
        """
        # nv_value_ = hex(int(nv_value))[2:].zfill(2)  # to transfer to 2 placeholder (0x1 -> 1 -> '01')
        self.command_nv(f'AT+GOOGSETNV="{nv_name}",{nv_index},"{nv_value}"')

    def query_google_nv(self, nv_name):
        return self.command_nv(f'AT+GOOGGETNV="{nv_name}"')

    def write_regy(self, file_name):
        regy_dict = regy_parser(file_name)
        for nv_name, regy_value in regy_dict.items():
            for nv_index, nv_value in regy_value.items():
                if nv_index == 'size':
                    continue
                else:
                    # to do important transfer the format to meet LSI
                    size = regy_value['size']
                    hex_rep = self.decimal_to_hex_twos_complement(int(nv_value), size)
                    nv_value_new = self.convert_string(hex_rep, size)

                    # start to set nv
                    self.set_google_nv(nv_name, nv_index, nv_value_new)

    def write_regy_v2(self, file_name):
        regy_dict = regy_parser_v2(file_name)
        for nv_name, nv_values in regy_dict.items():
            self.set_google_nv(nv_name, 0, nv_values)

    def get_nv_index_value(self, res):
        index_value_dict = {}
        for res_ in res:
            resd = res_.decode().strip().split(',')
            if len(resd) == 3:  # size == 1
                index_value_dict[resd[1]] = str(int(resd[-1].strip('"'), 16))
            elif len(resd) == 4:  # size == 2
                hex_string = "".join((resd[-2].strip('"'), resd[-1].strip('"')))
                new_string = str(self.hex_string2dec(hex_string))
                index_value_dict[resd[1]] = new_string
            elif len(resd) == 6:  # size == 4
                hex_string = "".join(
                    (resd[-4].strip('"'), resd[-3].strip('"'), resd[-2].strip('"'), resd[-1].strip('"')))
                new_string = str(self.hex_string2dec(hex_string))
                index_value_dict[resd[1]] = new_string
        logger.debug(index_value_dict)

        return index_value_dict

    def get_used_band_index(self, used_band_name):
        """
        To transfer used_band to {band: index, ...}
        used_band_name parameter that can be valid:
        'CAL.LTE.USED_RF_BAND'
        'CAL.LTE.USED_DUALTX_RF_BAND'
        'CAL.NR_SUB6.USED_RF_BAND'
        'CAL.NR_SUB6.USED_DUALTX_RF_BAND'
        'CAL.NR_SUB6.USED_ULMIMO_RF_BAND'
        'CAL.NR_SUB6.USED_MULTICH_APT_RF_BAND'
        return:
        {band: index, ...}
        """
        index_value_dict = self.get_nv_index_value(self.query_google_nv(used_band_name))
        used_band_index = {}
        for index in index_value_dict:
            used_band_index[int(index_value_dict[index])] = int(index) + 1
        logger.debug(used_band_index)

        return used_band_index

    def get_used_band_index_by_path_fr1(self, tx_path):
        """
        To transfer used_band to {band: index, ...}
        used_band_name parameter that can be valid:
        'CAL.NR_SUB6.USED_RF_BAND'
        'CAL.NR_SUB6.USED_DUALTX_RF_BAND'
        'CAL.NR_SUB6.USED_ULMIMO_RF_BAND'
        return:
        {band: index, ...}
        """
        used_band_name = None
        if tx_path == 'TX1':
            used_band_name = 'CAL.NR_SUB6.USED_RF_BAND'
        elif tx_path == 'TX2':
            used_band_name = 'CAL.NR_SUB6.USED_DUALTX_RF_BAND'
        elif tx_path == 'MIMO':
            used_band_name = 'CAL.NR_SUB6.USED_ULMIMO_RF_BAND'

        index_value_dict = self.get_nv_index_value(self.query_google_nv(used_band_name))
        used_band_index = {}
        for index in index_value_dict:
            used_band_index[int(index_value_dict[index])] = int(index) + 1
        logger.debug(used_band_index)

        return used_band_index

    def get_mpr_value(self, mpr_nv, band, tx_path):
        """
        mpr_nv parameters:
        eg:
        !LTERF.TX.USER DSP MPR OFFSET TX{tx_path} B{band_index}, ...
        !LTERF.TX.USER DSP MPR INTRA_CA OFFSET TX B{band_index}, ...
        !NR_SUB6RF.TX.USER MPR OFFSET TX{tx_path} N{band_index}, ...
        !NR_SUB6RF.TX.USER MPR OFFSET PC2 TX{tx_path} N{band_index}, ...
        !NR_SUB6RF.TX.USER MPR OFFSET PC1p5 TX{tx_path} N{band_index}, ...
        """
        used_band_index = None
        mpr_index_value = None
        nv = None
        mpr_nv_dict = {}

        if mpr_nv == '!LTERF.TX.USER DSP MPR OFFSET TX':
            if tx_path == 'TX1':
                used_band_index = self.get_used_band_index("CAL.LTE.USED_RF_BAND")
            elif tx_path == 'TX2':
                used_band_index = self.get_used_band_index("CAL.LTE.USED_DUALTX_RF_BAND")

            nv = f'!LTERF.TX.USER DSP MPR OFFSET TX{self.tx_path_dict[self.tx_path]} ' \
                 f'B{str(used_band_index[band]).zfill(2)}'

            mpr_index_value = self.get_nv_index_value(self.query_google_nv(nv))
            logger.info(f'Band {band} MPR index_value_dict: {mpr_index_value}')

        elif mpr_nv == '!LTERF.TX.USER DSP MPR INTRA_CA OFFSET TX':
            used_band_index = self.get_used_band_index("CAL.LTE.USED_RF_BAND")
            nv = f'!LTERF.TX.USER DSP MPR INTRA_CA OFFSET TX ' \
                 f'B{str(used_band_index[band]).zfill(2)}'

            mpr_index_value = self.get_nv_index_value(self.query_google_nv(nv))
            logger.info(f'Band {band}C MPR index_value_dict: {mpr_index_value}')

        elif mpr_nv == '!NR_SUB6RF.TX.USER MPR OFFSET TX':
            if tx_path == 'TX1':
                used_band_index = self.get_used_band_index("CAL.NR_SUB6.USED_RF_BAND")
            elif tx_path == 'TX2':
                used_band_index = self.get_used_band_index("CAL.NR_SUB6.USED_DUALTX_RF_BAND")

            nv = f'!NR_SUB6RF.TX.USER MPR OFFSET TX{self.tx_path_dict[self.tx_path]}_' \
                 f'N{str(used_band_index[band]).zfill(2)}'

            mpr_index_value = self.get_nv_index_value(self.query_google_nv(nv))
            logger.info(f'Band {band} MPR index_value_dict: {mpr_index_value}')

        elif mpr_nv == '!NR_SUB6RF.TX.USER MPR OFFSET PC2 TX':
            if tx_path == 'TX1':
                used_band_index = self.get_used_band_index("CAL.NR_SUB6.USED_RF_BAND")
            elif tx_path == 'TX2':
                used_band_index = self.get_used_band_index("CAL.NR_SUB6.USED_DUALTX_RF_BAND")

            nv = f'!NR_SUB6RF.TX.USER MPR OFFSET PC2 TX{self.tx_path_dict[self.tx_path]}_' \
                 f'N{str(used_band_index[band]).zfill(2)}'

            mpr_index_value = self.get_nv_index_value(self.query_google_nv(nv))
            logger.info(f'Band {band} MPR index_value_dict: {mpr_index_value}')

        elif mpr_nv == '!NR_SUB6RF.TX.USER MPR OFFSET PC1p5 TX':
            if tx_path == 'TX1':
                used_band_index = self.get_used_band_index("CAL.NR_SUB6.USED_RF_BAND")
            elif tx_path == 'TX2':
                used_band_index = self.get_used_band_index("CAL.NR_SUB6.USED_DUALTX_RF_BAND")

            nv = f'!NR_SUB6RF.TX.USER MPR OFFSET PC1p5 TX{self.tx_path_dict[self.tx_path]}_' \
                 f'N{str(used_band_index[band]).zfill(2)}'

            mpr_index_value = self.get_nv_index_value(self.query_google_nv(nv))
            logger.info(f'Band {band} MPR index_value_dict: {mpr_index_value}')

        mpr_nv_dict[nv] = mpr_index_value

        return mpr_nv_dict

    def mpr_nvs_check(self, band):
        used_band_tx1_index_lte = self.get_used_band_index("CAL.LTE.USED_RF_BAND")
        used_band_tx2_index_lte = self.get_used_band_index("CAL.LTE.USED_DUALTX_RF_BAND")
        used_band_tx1_index_fr1 = self.get_used_band_index("CAL.NR_SUB6.USED_RF_BAND")
        used_band_tx2_index_fr1 = self.get_used_band_index("CAL.NR_SUB6.USED_DUALTX_RF_BAND")
        # mpr_nvs = [
        #     f'!LTERF.TX.USER DSP MPR OFFSET TX0 B{str(used_band_tx1_index_lte[band]).zfill(2)}',
        #     f'!LTERF.TX.USER DSP MPR OFFSET TX1 B{str(used_band_tx2_index_lte[band]).zfill(2)}',
        #     f'!LTERF.TX.USER DSP MPR INTRA_CA OFFSET TX B{str(used_band_tx1_index_lte[band]).zfill(2)}',
        #     f'!NR_SUB6RF.TX.USER MPR OFFSET TX0_N{str(used_band_tx1_index_fr1[band]).zfill(2)}',
        #     f'!NR_SUB6RF.TX.USER MPR OFFSET TX1_N{str(used_band_tx2_index_fr1[band]).zfill(2)}',
        #     f'!NR_SUB6RF.TX.USER MPR OFFSET PC2 TX0_N{str(used_band_tx1_index_fr1[band]).zfill(2)}',
        #     f'!NR_SUB6RF.TX.USER MPR OFFSET PC2 TX1_N{str(used_band_tx2_index_fr1[band]).zfill(2)}',
        #     f'!NR_SUB6RF.TX.USER MPR OFFSET PC1p5 TX0_N{str(used_band_tx1_index_fr1[band]).zfill(2)}',
        #     f'!NR_SUB6RF.TX.USER MPR OFFSET PC1p5 TX1_N{str(used_band_tx2_index_fr1[band]).zfill(2)}',
        #
        # ]

        mpr_nvs = [
            f'!LTERF.TX.USER DSP MPR OFFSET TX0 B',
            f'!LTERF.TX.USER DSP MPR OFFSET TX1 B',
            f'!LTERF.TX.USER DSP MPR INTRA_CA OFFSET TX B',
            f'!NR_SUB6RF.TX.USER MPR OFFSET TX0_N',
            f'!NR_SUB6RF.TX.USER MPR OFFSET TX1_N',
            f'!NR_SUB6RF.TX.USER MPR OFFSET PC2 TX0_N',
            f'!NR_SUB6RF.TX.USER MPR OFFSET PC2 TX1_N',
            f'!NR_SUB6RF.TX.USER MPR OFFSET PC1p5 TX0_N',
            f'!NR_SUB6RF.TX.USER MPR OFFSET PC1p5 TX1_N',

        ]
        mpr_nvs_new = []
        for mpr_nv in mpr_nvs:
            try:
                if mpr_nv == '!LTERF.TX.USER DSP MPR OFFSET TX0 B' or mpr_nv == '!LTERF.TX.USER DSP MPR INTRA_CA OFFSET TX B':
                    mpr_nvs_new.append(mpr_nv + f'{str(used_band_tx1_index_lte[band]).zfill(2)}')

                elif mpr_nv == '!LTERF.TX.USER DSP MPR OFFSET TX1 B':
                    mpr_nvs_new.append(mpr_nv + f'{str(used_band_tx2_index_lte[band]).zfill(2)}')

                elif 'TX0_N' in mpr_nv:
                    mpr_nvs_new.append(mpr_nv + f'{str(used_band_tx1_index_fr1[band]).zfill(2)}')

                elif 'TX1_N' in mpr_nv:
                    mpr_nvs_new.append(mpr_nv + f'{str(used_band_tx2_index_fr1[band]).zfill(2)}')
            except KeyError:
                logger.info(f'Band {band} does not in the {mpr_nv}')

        return mpr_nvs_new

    def get_mpr_value_all(self, band):
        """
        Directly transfer all possible MPR NV with union all bands you select
        """

        mpr_nv_all_dict = {}

        for mpr_nv in self.mpr_nvs_check(band):
            mpr_index_value = self.get_nv_index_value(self.query_google_nv(mpr_nv))
            mpr_nv_all_dict[mpr_nv] = mpr_index_value

        return mpr_nv_all_dict

    def set_stop_network_cal(self):
        """
        Network stop command for 2G/3G/4G mode
        """
        self.command('AT+HNSSTOP')

    def set_postcal_fr1(self, band):
        """
        This is postcal for FR1
        """
        self.command(f'AT+NPOSTCALSTART={band}')

    def set_rfcal_start_wcdma(self):
        """
        This is postcal for wcdma
        """
        self.command('AT+HSPARFCALSTART=7')

    def set_apt_internal_calibration_fr1(self, tx_path, freq):
        """
        AT+NTXSAINTERNALAPT=P0, P1
        Run TX internal APT calibration

        P0 : Tx_path_no: (0: PCC, 1: SCC)
        P1 : Tx Calibration frequency (kHz)

        R00~R39 : HPM1 ~ HPM40 : APT calibration result of high
        power mode (dBm * 100)
        R40~R79 : MPM1 ~ MPM40 : APT calibration result of mid
        power mode (dBm * 100)
        R80~R119 : LPM1 ~ LPM40 : APT calibration result of low
        power mode (dBm * 100)
        """
        self.command(f'AT+NTXSAINTERNALAPT={self.tx_path_dict[tx_path]},{freq}', delay=0.5)

    def set_calibration_finish_fr1(self):
        """
        Calibration mode finished
        """
        self.command(f'AT+NRFCALFINISH', 0.5)

    def apt_calibration_process_fr1(self, band, tx_path, freq):
        self.set_stop_network_cal()
        self.set_postcal_fr1(band)
        self.set_apt_internal_calibration_fr1(tx_path, freq)
        self.set_calibration_finish_fr1()

    def set_apt_vcc_nv_fr1(self, vcc_para_dict):
        """
        AT+NTXAPTVOLNVWRITE=P0,P1,~P37
        """
        band = vcc_para_dict['band']
        scheme = self.apt_vcc_dict_fr1[vcc_para_dict['scheme']]
        pa_mode = vcc_para_dict['pa_mode']
        vcc_value = ','.join(vcc_para_dict['vcc_value_list'])

        self.command(f'AT+NTXAPTVOLNVWRITE={band},{scheme},{pa_mode},0,{vcc_value}')

    def set_apt_bias_nv_fr1(self, bias_num, bias_para_dict):
        """
        AT+NTXAPTBIASNVWRITE=P0,P1,~P38
        """
        band = bias_para_dict['band']
        scheme = self.apt_vcc_dict_fr1[bias_para_dict['scheme']]
        pa_mode = bias_para_dict['pa_mode']
        bias_value = ','.join(bias_para_dict['bias_value_list'])

        self.command(f'AT+NTXAPTBIASNVWRITE={band},{scheme},{pa_mode},0,{bias_num},{bias_value}')

    def set_apt_mode_force(self, band, tx_path, mode=0):
        """
        force apt into APT mode before doing APT sweep
        mode = 0, which is APT mode
        mode = 1, which is ET/SAPT mode
        """
        pa_mode_dict = {
            0: 'APT',
            1: 'ET/SAPT',
        }
        used_band_index = None

        if tx_path == 'TX1':
            used_band_index = self.get_used_band_index("CAL.NR_SUB6.USED_RF_BAND")
        elif tx_path == 'TX2':
            used_band_index = self.get_used_band_index("CAL.NR_SUB6.USED_DUALTX_RF_BAND")

        nv = f'CAL.NR_SUB6.TX_PA_Range_Map_EN_TX{self.tx_path_dict[self.tx_path]}_' \
             f'N{str(used_band_index[band]).zfill(2)}'

        logger.info(f'========== Force to set {pa_mode_dict[mode]} mode ==========')
        self.set_google_nv(nv, 0, str(mode).zfill(2))

    def set_apt_trymode(self, trymode):
        self.command(f'AT+NTXAPTTUNESET={trymode}')

    def set_apt_vcc_trymode(self, tx_path, vcc10):
        self.command(f'AT+NAPTVOLSET={self.tx_path_dict[tx_path]},1,{vcc10}')

    def set_apt_bias_trymode(self, tx_path, icq1, icq2):
        self.command(f'AT+NTXPABIASSET={self.tx_path_dict[tx_path]},2,{icq1},{icq2}')

    def set_pa_range_mode(self, mode='H'):
        """
        HPM
        AT+NTXPARANGEMAPSET=0,-1,-3,-5,-7
        LPM
        AT+NTXPARANGEMAPSET=0,25,23,21,19
        """
        pa_range = None
        if mode == 'H':
            pa_range = '0,-1,-3,-5,-7'
        elif mode == 'L':
            pa_range = '0,25,23,21,19'
        self.command(f'AT+NTXPARANGEMAPSET={pa_range}')

    def set_apt_vcc_nv_each_cp_fr1(self, band, tx_path, pa_mode, index_wanted, value_wanted):
        """
        used for the NV:
        CAL.NR_SUB6.TX_APT_DC_TABLE_MIDCH_HPM_TX0_Nxx
        CAL.NR_SUB6.TX_APT_DC_TABLE_MIDCH_LPM_TX0_Nxx
        CAL.NR_SUB6.TX_APT_DC_TABLE_MIDCH_HPM_TX1_Nxx
        CAL.NR_SUB6.TX_APT_DC_TABLE_MIDCH_LPM_TX1_Nxx

        pa_mode: use 'H' and 'L to be representative
        index_wanted: use integer or string 1, 2, 3,...
        value_wanted: use decimal value or string
        """
        # query the used_band and get the band index
        used_band_index_fr1 = None
        if tx_path == 'TX1':
            used_band_index_fr1 = self.get_used_band_index('CAL.NR_SUB6.USED_RF_BAND')
        elif tx_path == 'TX2':
            used_band_index_fr1 = self.get_used_band_index('CAL.NR_SUB6.USED_DUALTX_RF_BAND')

        # get the NV we want
        vcc_nv_wanted = f'CAL.NR_SUB6.TX_APT_DC_TABLE_MIDCH_{pa_mode}PM_TX{self.tx_path_dict[self.tx_path]}' \
                        f'_N{str(used_band_index_fr1[band]).zfill(2)}'

        # set the value we want in vcc_nv
        hex_rep = self.decimal_to_hex_twos_complement(int(value_wanted), 2)  # vcc nv size is 2
        nv_value_new = self.convert_string(hex_rep, 2)  # vcc nv size is 2
        self.set_google_nv(vcc_nv_wanted, int(index_wanted) - 1, nv_value_new)
        logger.info(f'Set value: {value_wanted} at index: {index_wanted}')

    def set_apt_bias_nv_each_cp_fr1(self, band, tx_path, bias_num, pa_mode, index_wanted, value_wanted):
        """
        used for the NV:
        CAL.NR_SUB6.TX_PA_BIAS0_MIDCH_HPM_TX0_Nxx
        CAL.NR_SUB6.TX_PA_BIAS0_MIDCH_LPM_TX0_Nxx
        CAL.NR_SUB6.TX_PA_BIAS0_MIDCH_HPM_TX1_Nxx
        CAL.NR_SUB6.TX_PA_BIAS0_MIDCH_LPM_TX1_Nxx
        CAL.NR_SUB6.TX_PA_BIAS1_MIDCH_HPM_TX0_Nxx
        CAL.NR_SUB6.TX_PA_BIAS1_MIDCH_LPM_TX0_Nxx
        CAL.NR_SUB6.TX_PA_BIAS1_MIDCH_HPM_TX1_Nxx
        CAL.NR_SUB6.TX_PA_BIAS1_MIDCH_LPM_TX1_Nxx

        pa_mode: use 'H' and 'L to be representative
        index_wanted: use integer or string 1, 2, 3,...
        value_wanted: use decimal value or string
        """
        # query the used_band and get the band index
        used_band_index_fr1 = self.get_used_band_index_by_path_fr1(tx_path)

        # get the NV we want
        bias_nv_wanted = f'CAL.NR_SUB6.TX_PA_BIAS{bias_num}_MIDCH' \
                         f'_{pa_mode}PM_TX{self.tx_path_dict[self.tx_path]}' \
                         f'_N{str(used_band_index_fr1[band]).zfill(2)}'

        # set the value we want in vcc_nv
        hex_rep = self.decimal_to_hex_twos_complement(int(value_wanted), 1)  # bias nv size is 1
        nv_value_new = self.convert_string(hex_rep, 1)  # bias nv size is 1
        self.set_google_nv(bias_nv_wanted, int(index_wanted) - 1, nv_value_new)
        logger.info(f'Set value: {value_wanted} at index: {index_wanted}')

    def get_pa_sw_rise_level(self, band, tx_path, index) -> int:
        """
        index 1: max power level for apt nv -> index 34
        index 4: sw point power level for apt nv
        """
        used_band_index = self.get_used_band_index_by_path_fr1(tx_path)
        pa_map_rise_nv = f'CAL.NR_SUB6.TX_PA_Range_Map_Rise_TX{self.tx_path_dict[self.tx_path]}' \
                         f'_N{str(used_band_index[band]).zfill(2)}'
        level_pa_rise = int(self.get_nv_index_value(self.query_google_nv(pa_map_rise_nv))[f'{index - 1}'])
        if index == 1:
            logger.info(f'The max level of index 34 for APT NV for VCC/BIAS is: {level_pa_rise}')
        elif index == 4:
            logger.info(f'The sw point level for APT NV for VCC/BIAS is: {level_pa_rise}')
        else:
            logger.info(f'there is tentatively no function at this index: {index}')

        return level_pa_rise

    def get_pa_sw_fall_level(self, band, tx_path, index) -> int:
        """

        """
        pass

    @staticmethod
    def decimal_to_hex_twos_complement(num, size):
        """
        This is used for transfer negative and positive value to what LSI format is
        """
        bit_length = size * 8  # 1 byte = 1 size = 2 nibbles = 8 bits
        twos_complement = (1 << bit_length) + num
        hex_representation = hex(twos_complement & (2 ** bit_length - 1))[2:].zfill(bit_length // 4)
        return hex_representation

    @staticmethod
    def convert_string(string, size):
        """
        This feature is used for register value transferred to at command use
        """
        # Convert the hex string to an integer
        n = int(string, 16)

        # Convert the integer to a byte array
        b = n.to_bytes(size, 'little')

        # Convert the byte array to a string
        # result = ",".join(["{:02x}".format(x) for x in b])
        result = ",".join([f"{x:02x}" for x in b])

        return result

    @staticmethod
    def hex_string2dec(hex_string, byteorder='little', signed_bool=True):
        """
        This is for from get nv index value(hex string and uses little byteorder) and change to dec with signed
        """
        bytes_value = bytes.fromhex(hex_string)
        int_signed_value = int.from_bytes(bytes_value, byteorder=byteorder, signed=signed_bool)
        logger.debug(f'From hex_string {hex_string} to dec {int_signed_value}')

        return int_signed_value


if __name__ == '__main__':
    # import csv

    # NV_NAME = 'CAL.LTE.USED_RF_BAND'
    # NV_INDEX = 0
    # NV_VALUE = '00'
    #
    command = AtCmd()
    # command.apt_calibration_process_fr1(1, 'TX1', 1950000)
    # command.get_pa_sw_rise_level(41, 'TX1', 4)
    command.hex_string2dec('0A00')
