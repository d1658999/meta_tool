import time
from decimal import Decimal

from equipments.series_basis.callbox.anritsu_series import Anritsu
from utils.log_init import log_set
from utils.loss_handler import read_loss_file
import utils.parameters.common_parameters_anritsu as cm_pmt_anritsu
import utils.parameters.external_paramters as ext_pmt
from utils.excel_handler import excel_plot_line, fill_desens, fill_values_tx, fill_values_rx, fill_values_rx_sweep
from utils.fly_mode import FlyMode
from equipments.anritsu8820 import Anritsu8820

logger = log_set('Anritsu8821')


class Anritsu8821(Anritsu8820):
    def __init__(self, equipment='Anristu8821'):
        Anritsu8820.__init__(self, equipment)

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
        self.set_test_mode('OFF')
        self.set_integrity('LTE', 'SNOW3G')
        self.set_scenario()
        self.set_pdn_type()
        self.set_mcc_mnc()
        self.set_ant_config()
        self.set_imsi()
        self.set_authentication()
        self.set_all_measurement_items_off()
        self.set_init_miscs('LTE')
        self.set_path_loss('LTE')
        self.set_init_level('LTE')
        self.set_handover('LTE', dl_ch, bw)
        self.set_ul_rb_start()
        self.anritsu_query('*OPC?')

    def set_path_loss(self, standard):
        logger.info('Set LOSS')
        self.set_loss_table_delete()  # delete the unknown loss table first

        loss_title = 'LOSSTBLVAL2'
        loss_dict = read_loss_file()
        freq = sorted(loss_dict.keys())
        for f in freq:
            self.set_loss_table_8821(loss_title, f, loss_dict[f], loss_dict[f], loss_dict[f])
        self.set_loss_table_delete_phone2()  # 8821 has this extra command
        logger.debug("Current Format: " + standard)  # WCDMA|GSM|LTE
        self.set_loss_common(standard)

    def set_init_miscs(self, standard):
        if standard == 'LTE':
            self.set_sem_additional_request_version(11)
            self.set_rrc_update('PAGING')
            self.set_power_trigger_source('FRAME')
            self.set_modified_period('N2')
            self.set_paging_cycle(32)
            self.set_rrc_release('OFF')
            self.set_freq_err_range('NARROW')  # NORMAL | NARROW
            self.set_robust_connection('OFF') # ON | OFF
            self.set_test_mode('OFF')
            self.set_ue_category(3)
            self.set_additional_spectrum_emission_ns('01')
            self.set_uplink_terminal_phone1(1)
            self.set_downlink_terminal_phone1(1)
            self.set_phone1_tx_out(1, 'MAIN')
            logger.debug(self.get_ue_cap_version_query())

    def set_registration_calling_lte(self, times=30):
        """
            ANRITSU_IDLE = 1	        #Idle state
            ANRITSU_REGIST = 3			# Under location registration
            ANRITSU_CONNECTED = 6	    # Under communication or connected
        """
        self.inst.write('CALLTHLD 1')
        self.set_lvl_status('ON')
        self.set_test_mode()
        conn_state = int(self.inst.query("CALLSTAT?").strip())
        while conn_state != cm_pmt_anritsu.ANRITSU_CONNECTED:  # this is for waiting connection
            self.inst.write('CALLRFR')
            while conn_state == cm_pmt_anritsu.ANRITSU_IDLE:
                self.inst.write('CALLSO')
                logger.info('IDLE')
                logger.info('Start to ON and OFF')
                self.flymode_circle()
                time.sleep(3)
                self.inst.write('CALLSA')
                while conn_state != cm_pmt_anritsu.ANRITSU_CONNECTED:
                    logger.info('Waiting for connection...')
                    time.sleep(1)
                    conn_state = int(self.inst.query("CALLSTAT?").strip())

                # logger.info('Start calling')
                # conn_state = int(self.inst.query("CALLSTAT?").strip())
            # logger.info('START CALL')
            # self.inst.write('CALLSA')
            logger.info('Connected')
            time.sleep(1)

    def get_power_aclr_evm_lte(self):
        """
            Only measure RB@min
            The format in dictionary is {Q_1: [power, aclr, evm], Q_P: [power, aclr, evm], ...}
            and ACLR format is [EUTRA-1, EUTRA+1, UTRA-1, URTA+1, UTRA-2, URTA+2,]
        """
        want_mods = [
            'TESTPRM TX_MAXPWR_Q_1',
            'TESTPRM TX_MAXPWR_Q_P',
            'TESTPRM TX_MAXPWR_Q_F',
            'TESTPRM TX_MAXPWR_16_P',
            'TESTPRM TX_MAXPWR_16_F',
            'TESTPRM TX_MAXPWR_64_P',
            'TESTPRM TX_MAXPWR_64_F',
            'TESTPRM TX_MAXPWR_256_F',
        ]

        validation_dict = {}

        self.set_init_power()
        self.set_init_aclr('LTE')
        self.set_init_mod('LTE')
        self.set_input_level(26)
        self.set_tpc('ALL3')
        self.anritsu_query('*OPC?')

        for mod in want_mods:
            self.mod = mod[18:]
            conn_state = int(self.inst.query("CALLSTAT?").strip())
            self.count = 5
            while conn_state != cm_pmt_anritsu.ANRITSU_CONNECTED:  # this is for waiting connection before change modulation if there is connection problems
                logger.info('Call drops...')
                if self.count == 0:
                    # equipment end call and start call
                    logger.info('End call and then start call')
                    self.flymode_circle()
                    time.sleep(5)
                    self.inst.write('CALLSO')
                    self.inst.query('*OPC?')
                    time.sleep(1)
                    self.inst.write('CALLSA')
                    time.sleep(10)
                    self.count = 6
                    conn_state = int(self.inst.query("CALLSTAT?").strip())

                else:
                    time.sleep(10)
                    self.count -= 1
                    logger.info('wait 10 seconds to connect')
                    logger.info(f'{6 - self.count} times to wait 10 second')
                    conn_state = int(self.inst.query("CALLSTAT?").strip())

            validation_list = []
            if ext_pmt.fdd_tdd_cross_test == 1:
                if mod in ['TESTPRM TX_MAXPWR_Q_1', 'TESTPRM TX_MAXPWR_Q_P', 'TESTPRM TX_MAXPWR_Q_F']:
                    self.inst.write(mod)
                    self.inst.write('ULRMC_64QAM ENABLED')
                    self.inst.write('ULRMC_256QAM ENABLED')
                    self.inst.write('ULIMCS 5')

                elif mod in ['TESTPRM TX_MAXPWR_16_P', 'TESTPRM TX_MAXPWR_16_F']:
                    self.inst.write(mod)
                    self.inst.write('ULRMC_64QAM ENABLED')
                    self.inst.write('ULRMC_256QAM ENABLED')
                    self.inst.write('ULIMCS 13')

                elif mod in ['TESTPRM TX_MAXPWR_64_P', 'TESTPRM TX_MAXPWR_64_F']:
                    self.inst.write(mod)
                    self.inst.write('ULRMC_64QAM ENABLED')
                    self.inst.write('ULRMC_256QAM ENABLED')
                    self.inst.write('ULIMCS 22')

                elif mod in ['TESTPRM TX_MAXPWR_256_F']:
                    self.inst.write(mod)
                    self.inst.write('ULRMC_64QAM ENABLED')
                    self.inst.write('ULRMC_256QAM ENABLED')
                    self.inst.write('ULIMCS 28')
            else:
                self.inst.write(mod)
            self.set_to_measure()
            self.inst.query('*OPC?')
            meas_status = int(self.inst.query('MSTAT?').strip())

            while meas_status == cm_pmt_anritsu.MESUREMENT_BAD:  # this is for the reference signal is not found
                logger.info('measuring status is bad(Reference signal not found)')
                logger.info('Equipment is forced to set End Call')
                self.inst.write('CALLSO')
                time.sleep(5)
                logger.info('fly on and off again')
                self.flymode_circle()
                time.sleep(10)
                self.inst.write('CALLSA')
                logger.info('waiting for 10 second to re-connect')
                logger.info('measure it again')
                self.set_to_measure()
                meas_status = int(self.inst.query('MSTAT?').strip())

            # self.inst.query('*OPC?')

            if mod == 'TESTPRM TX_MAXPWR_Q_1':  # mod[18:] -> Q_1
                logger.info(mod)
                validation_list.append(self.get_uplink_power('LTE'))
                validation_dict[mod[18:]] = validation_list
                # self.inst.query('*OPC?')
            else:  # mod[18:] -> Q_P, Q_F, 16_P, 16_F, 64_F, 256_F
                logger.info(mod)
                self.pwr = self.get_uplink_power('LTE')
                validation_list.append(self.pwr)
                self.aclr = self.get_uplink_aclr('LTE')
                validation_list.append(self.aclr)
                self.evm = self.get_uplink_evm('LTE')
                validation_list.append(self.evm)
                validation_dict[mod[18:]] = validation_list
                self.inst.query('*OPC?')
        logger.debug(validation_dict)
        return validation_dict

    @staticmethod
    def create_excel_tx(standard, bw=None):
        if standard == 'LTE':
            wb = openpyxl.Workbook()
            wb.remove(wb['Sheet'])
            wb.create_sheet('PWR_Q_1')
            wb.create_sheet('PWR_Q_P')
            wb.create_sheet('PWR_Q_F')
            wb.create_sheet('PWR_16_P')
            wb.create_sheet('PWR_16_F')
            wb.create_sheet('PWR_64_P')
            wb.create_sheet('PWR_64_F')
            wb.create_sheet('PWR_256_F')
            wb.create_sheet('ACLR_Q_P')
            wb.create_sheet('ACLR_Q_F')
            wb.create_sheet('ACLR_16_P')
            wb.create_sheet('ACLR_16_F')
            wb.create_sheet('ACLR_64_P')
            wb.create_sheet('ACLR_64_F')
            wb.create_sheet('ACLR_256_F')
            wb.create_sheet('EVM_Q_P')
            wb.create_sheet('EVM_Q_F')
            wb.create_sheet('EVM_16_P')
            wb.create_sheet('EVM_16_F')
            wb.create_sheet('EVM_64_P')
            wb.create_sheet('EVM_64_F')
            wb.create_sheet('EVM_256_F')

            for sheet in wb.sheetnames:
                if 'ACLR' in sheet:
                    sh = wb[sheet]
                    sh['A1'] = 'Band'
                    sh['B1'] = 'Channel'
                    sh['C1'] = 'EUTRA_-1'
                    sh['D1'] = 'EUTRA_+1'
                    sh['E1'] = 'UTRA_-1'
                    sh['F1'] = 'UTRA_+1'
                    sh['G1'] = 'UTRA_-2'
                    sh['H1'] = 'UTRA_+2'

                else:
                    sh = wb[sheet]
                    sh['A1'] = 'Band'
                    sh['B1'] = 'ch0'
                    sh['C1'] = 'ch1'
                    sh['D1'] = 'ch2'
            excel_path = f'results_{bw}MHZ_LTE.xlsx' if ext_pmt.condition is None else f'results_{bw}MHZ_LTE_{ext_pmt.condition}.xlsx'
            wb.save(excel_path)
            wb.close()

        elif standard == 'WCDMA':
            wb = openpyxl.Workbook()
            wb.remove(wb['Sheet'])
            wb.create_sheet('PWR')
            wb.create_sheet('ACLR')
            wb.create_sheet('EVM')

            for sheet in wb.sheetnames:
                if 'ACLR' in sheet:
                    sh = wb[sheet]
                    sh['A1'] = 'Band'
                    sh['B1'] = 'Channel'
                    sh['C1'] = 'UTRA_-1'
                    sh['D1'] = 'UTRA_+1'
                    sh['E1'] = 'UTRA_-2'
                    sh['F1'] = 'UTRA_+2'
                else:
                    sh = wb[sheet]
                    sh['A1'] = 'Band'
                    sh['B1'] = 'ch01'
                    sh['C1'] = 'ch02'
                    sh['D1'] = 'ch03'
            excel_path = f'results_WCDMA.xlsx' if ext_pmt.condition is None else f'results_WCDMA_{ext_pmt.condition}.xlsx'
            wb.save(excel_path)
            wb.close()

    def run_tx(self):
        for tech in ext_pmt.tech:
            if tech == 'LTE' and ext_pmt.lte_bands != []:
                standard = self.switch_to_lte()
                logger.info(standard)
                for bw in ext_pmt.lte_bandwidths:
                    for band in ext_pmt.lte_bands:
                        if bw in cm_pmt_anritsu.bandwidths_selected(band):
                            if band == 28:
                                self.band_segment = ext_pmt.band_segment
                            self.set_test_parameter_normal()
                            ch_list = []
                            for wt_ch in ext_pmt.channel:
                                if wt_ch == 'L':
                                    ch_list.append(cm_pmt_anritsu.dl_ch_selected(standard, band, bw)[0])
                                elif wt_ch == 'M':
                                    ch_list.append(cm_pmt_anritsu.dl_ch_selected(standard, band, bw)[1])
                                elif wt_ch == 'H':
                                    ch_list.append(cm_pmt_anritsu.dl_ch_selected(standard, band, bw)[2])
                            logger.debug(f'Test Channel List: {band}, {bw}MHZ, downlink channel list:{ch_list}')
                            for dl_ch in ch_list:
                                self.band = band

                                conn_state = int(self.inst.query("CALLSTAT?").strip())
                                if conn_state != cm_pmt_anritsu.ANRITSU_CONNECTED:
                                    self.set_init_before_calling(standard, dl_ch, bw)
                                    self.set_registration_calling(standard)
                                logger.info(f'Start to measure B{band}, bandwidth: {bw} MHz, downlink_chan: {dl_ch}')
                                self.set_handover(standard, dl_ch, bw)
                                time.sleep(2)
                                data = self.get_validation(standard)
                                self.excel_path = self.fill_values_tx(data, band, dl_ch, bw)
                                self.set_test_parameter_normal()  # this is for 8821 to be more stable
                        else:
                            logger.info(f'B{band} do not have BW {bw}MHZ')
                    self.excel_plot_line(standard, self.excel_path)
            else:
                logger.info(f'Finished')


def main():
    # start = datetime.datetime.now()

    anritsu = Anritsu8821()
    # anritsu.create_excel_rx('LTE', 5)
    # anritsu.run_rx()

    # stop = datetime.datetime.now()
    # logger.info(f'Timer: {stop - start}')


if __name__ == '__main__':
    main()
