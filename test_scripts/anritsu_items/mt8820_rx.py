from equipments.anritsu8820 import Anritsu8820
from equipments.series_basis.modem_usb_serial.serial_series import AtCmd


class RxTestGenre(AtCmd, Anritsu8820):
    def __init__(self):
        AtCmd.__init__(self)
        Anritsu8820.__init__(self)

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
            self.set_rf_out_port(ext_pmt.rfout_anritsu)
            if power_selected == 1:
                self.set_tpc('ALL1')
                self.set_input_level(30)
                sens_list = self.get_sensitivity(standard, band, dl_ch, bw)
                logger.debug(f'Sensitivity list:{sens_list}')
                self.excel_path = fill_values_rx(sens_list, band, dl_ch, power_selected, bw)
                self.set_output_level(-70)
            elif power_selected == 0:
                if standard == 'LTE':
                    self.set_tpc('AUTO')
                elif standard == 'WCDMA':
                    self.set_tpc('ILPC')
                self.set_input_level(-10)
                sens_list = self.get_sensitivity(standard, band, dl_ch, bw)
                logger.debug(f'Sensitivity list:{sens_list}')
                self.excel_path = fill_values_rx(sens_list, band, dl_ch, power_selected, bw)
                self.set_output_level(-70)
            self.set_rf_out_port('MAIN')

    def run(self):
        self.set_rf_out_port('MAIN')
        for tech in ext_pmt.tech:
            if tech == 'LTE' and ext_pmt.lte_bands != []:
                standard = self.set_switch_to_lte()
                logger.info(standard)
                self.chcoding = None
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
                                self.rx_core(standard, band, dl_ch, bw)
                            time.sleep(1)
                    fill_desens(self.excel_path)
                    excel_plot_line(standard, self.chcoding, self.excel_path)

            elif tech == 'WCDMA' and ext_pmt.wcdma_bands != []:
                standard = self.set_switch_to_wcdma()
                for band in ext_pmt.wcdma_bands:
                    ch_list = []
                    for wt_ch in ext_pmt.channel:
                        if wt_ch == 'L':
                            ch_list.append(cm_pmt_anritsu.dl_ch_selected(standard, band)[0])
                        elif wt_ch == 'M':
                            ch_list.append(cm_pmt_anritsu.dl_ch_selected(standard, band)[1])
                        elif wt_ch == 'H':
                            ch_list.append(cm_pmt_anritsu.dl_ch_selected(standard, band)[2])
                    logger.debug(f'Test Channel List: {band}, downlink channel list:{ch_list}')
                    for dl_ch in ch_list:
                        self.rx_core(standard, band, dl_ch)
                fill_desens(self.excel_path)
                excel_plot_line(standard, self.chcoding, self.excel_path)
            elif tech == ext_pmt.gsm_bands:
                pass
            else:
                logger.info(f'Finished')