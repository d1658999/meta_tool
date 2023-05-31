import time

from equipments.anritsu8821 import Anritsu8821
from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_anritsu as cm_pmt_anritsu
from utils.channel_handler import channel_freq_select
from utils.excel_handler import rx_power_relative_test_export_excel_sig
from utils.excel_handler import rx_desense_process_sig, rxs_relative_plot_sig
from utils.log_init import log_set

logger = log_set('8821RxSig')


class RxTestGenre(AtCmd, Anritsu8821):
    def __init__(self):
        AtCmd.__init__(self)
        self.ser.com_close()
        Anritsu8821.__init__(self)

    def get_temperature(self, state=False):
        """
        for P22, AT+GOOGTHERMISTOR=1,1 for MHB LPAMid/ MHB Rx1 LFEM, AT+GOOGTHERMISTOR=0,1
        for LB LPAMid, MHB ENDC LPAMid, UHB(n77/n79 LPAF)
        :return:
        """
        self.ser.com_open()
        if state is True:
            res0 = self.query_thermister0()
            res1 = self.query_thermister1()
            res_list = [res0, res1]
            therm_list = []
            for res in res_list:
                for r in res:
                    if 'TEMPERATURE' in r.decode().strip():
                        try:
                            temp = eval(r.decode().strip().split(':')[1]) / 1000
                            therm_list.append(temp)
                        except Exception as err:
                            logger.debug(err)
                            therm_list.append(None)
            logger.info(f'thermistor0 get temp: {therm_list[0]}')
            logger.info(f'thermistor1 get temp: {therm_list[1]}')

        else:
            therm_list = [None, None]

        return therm_list

    def rx_core(self, standard, band, dl_ch, bw=None):
        conn_state = int(self.get_calling_state_query())
        if standard == 'LTE':
            if conn_state != cm_pmt_anritsu.ANRITSU_CONNECTED:
                self.set_init_before_calling(standard, dl_ch, bw)
                self.set_registration_calling(standard)
        elif standard == 'WCDMA':
            if conn_state != cm_pmt_anritsu.ANRITSU_LOOP_MODE_1:
                self.set_init_before_calling(standard, dl_ch, bw)
                self.set_registration_calling(standard)

        if standard == 'LTE':
            logger.info(f'Start to sensitivity B{band}, bandwidth: {bw} MHz, downlink_chan: {dl_ch}')
        elif standard == 'WCDMA':
            logger.info(f'Start to sensitivity B{band}, downlink_chan: {dl_ch}')

        self.set_init_rx(standard)

        for power_selected in ext_pmt.tx_max_pwr_sensitivity:
            self.set_phone1_tx_out(1, ext_pmt.rfout_anritsu)
            if power_selected == 1:
                self.tx_level = ext_pmt.tx_level
                self.set_tpc('ALL1')
                self.set_input_level(self.tx_level + 3)

                # if rx_path is used by checking box methoc, or it is used by rf out
                if isinstance(self.rx_path, int):
                    if standard == 'LTE':
                        self.rx_path_setting_sig_lte()
                    elif standard == 'WCDMA':
                        self.rx_path_setting_sig_wcdma()

                sens_list = self.get_sensitivity(standard, band, dl_ch, bw)  # sens_list = [power, sensitivity, per]
                logger.debug(f'Sensitivity list:{sens_list}')
                self.parameters_dict = {
                    'tech': standard,
                    'bw': bw,
                    'band': band,
                    'dl_ch': dl_ch,
                    'tx_level': ext_pmt.tx_level,
                    'rx_path': self.rx_path,
                    'rb_size': self.get_ul_rb_size_query(standard),
                    'rb_start': self.get_ul_rb_start_query(standard),
                    'thermal': self.get_temperature(),
                    'mcs': 'QPSK',
                    'tx_freq': self.get_ul_freq_query(),

                }
                self.excel_path = rx_power_relative_test_export_excel_sig(sens_list, self.parameters_dict)
                self.set_output_level(-70)

            elif power_selected == 0:
                self.tx_level = -10
                if standard == 'LTE':
                    self.set_tpc('AUTO')
                elif standard == 'WCDMA':
                    self.set_tpc('ILPC')
                self.set_input_level(self.tx_level)

                # if rx_path is used by checking box methoc, or it is used by rf out
                if isinstance(self.rx_path, int):
                    if standard == 'LTE':
                        self.rx_path_setting_sig_lte()
                    elif standard == 'WCDMA':
                        self.rx_path_setting_sig_wcdma()

                sens_list = self.get_sensitivity(standard, band, dl_ch, bw)
                logger.debug(f'Sensitivity list:{sens_list}')
                self.parameters_dict = {
                    'tech': standard,
                    'bw': bw,
                    'band': band,
                    'dl_ch': dl_ch,
                    'tx_level': -10,
                    'rx_path': self.rx_path,
                    'rb_size': self.get_ul_rb_size_query(standard),
                    'rb_start': self.get_ul_rb_start_query(standard),
                    'thermal': self.get_temperature(),
                    'mcs': 'QPSK',
                    'tx_freq': self.get_ul_freq_query(),
                }
                self.excel_path = rx_power_relative_test_export_excel_sig(sens_list, self.parameters_dict)
                self.set_output_level(-70)
            self.set_phone1_tx_out(1, 'MAIN')

    def run(self):
        self.set_phone1_tx_out(1, 'MAIN')
        for tech in ext_pmt.tech:
            if tech == 'LTE' and ext_pmt.lte_bands != []:
                standard = self.set_switch_to_lte()
                logger.info(standard)
                self.chcoding = None
                try:
                    for bw in ext_pmt.lte_bandwidths:
                        for band in ext_pmt.lte_bands:
                            if ext_pmt.rx_paths:
                                for rx_path in ext_pmt.rx_paths:
                                    self.rx_path = rx_path
                                    if bw in cm_pmt_anritsu.bandwidths_selected(band):
                                        if band == 28:
                                            self.band_segment = ext_pmt.band_segment
                                        self.set_test_parameter_normal()
                                        band_ch_list = cm_pmt_anritsu.dl_ch_selected(standard, band, bw)
                                        ch_list = channel_freq_select(ext_pmt.channel, band_ch_list)

                                        # this is used for the handover smoothly by Mch when calling
                                        self.m_dl_ch = band_ch_list[1]
                                        self.set_dl_chan(self.m_dl_ch)

                                        logger.debug(f'Test Channel List: {band}, {bw}MHZ, '
                                                     f'downlink channel list:{ch_list}')
                                        for dl_ch in ch_list:
                                            self.rx_core(standard, band, dl_ch, bw)

                                        self.set_dl_chan(self.m_dl_ch)
                                        time.sleep(1)
                            else:  # if rx path is not selected, default is all path
                                self.rx_path = ext_pmt.rfout_anritsu
                                if bw in cm_pmt_anritsu.bandwidths_selected(band):
                                    if band == 28:
                                        self.band_segment = ext_pmt.band_segment
                                    self.set_test_parameter_normal()
                                    band_ch_list = cm_pmt_anritsu.dl_ch_selected(standard, band, bw)
                                    ch_list = channel_freq_select(ext_pmt.channel, band_ch_list)

                                    # this is used for the handover smoothly by Mch when calling
                                    self.m_dl_ch = ch_list[1]
                                    self.set_dl_chan(self.m_dl_ch)

                                    logger.debug(f'Test Channel List: {band}, {bw}MHZ, '
                                                 f'downlink channel list:{ch_list}')
                                    for dl_ch in ch_list:
                                        self.rx_core(standard, band, dl_ch, bw)

                                    self.set_dl_chan(self.m_dl_ch)
                                    time.sleep(1)
                        rx_desense_process_sig(standard, self.excel_path)
                        rxs_relative_plot_sig(self.excel_path, self.parameters_dict)

                except Exception as err:
                    logger.debug(err)
                    logger.info('Rx path is unchecked')
                    logger.info('It might forget to choose Band or Channel or BW or others')

            elif tech == 'WCDMA' and ext_pmt.wcdma_bands != []:
                standard = self.set_switch_to_wcdma()
                self.chcoding = 'REFMEASCH'
                try:
                    for band in ext_pmt.wcdma_bands:
                        if ext_pmt.rx_paths:
                            for rx_path in ext_pmt.rx_paths:
                                self.rx_path = rx_path
                                band_ch_list = cm_pmt_anritsu.dl_ch_selected(standard, band)
                                ch_list = channel_freq_select(ext_pmt.channel, band_ch_list)
                                logger.debug(f'Test Channel List: {band}, downlink channel list:{ch_list}')
                                for dl_ch in ch_list:
                                    self.rx_core(standard, band, dl_ch, 5)
                        else:
                            self.rx_path = ext_pmt.rfout_anritsu
                            band_ch_list = cm_pmt_anritsu.dl_ch_selected(standard, band)
                            ch_list = channel_freq_select(ext_pmt.channel, band_ch_list)
                            logger.debug(f'Test Channel List: {band}, downlink channel list:{ch_list}')
                            for dl_ch in ch_list:
                                self.rx_core(standard, band, dl_ch, 5)

                except Exception as err:
                    logger.debug(err)
                    logger.info('Rx path is unchecked')
                    logger.info('It might forget to choose Band or Channel or BW or others')

                else:
                    rx_desense_process_sig(standard, self.excel_path)
                    rxs_relative_plot_sig(self.excel_path, self.parameters_dict)

            elif tech == ext_pmt.gsm_bands:
                pass
            else:
                logger.info(f'Finished')
