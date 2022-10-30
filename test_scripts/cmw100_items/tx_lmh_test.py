from equipments.series_basis.serial_series import AtCmd
from equipments.cmw100_test import CMW100
from utils.log_init import log_set

logger = log_set('tx_lmh')


class TxTest(AtCmd, CMW100):
    def __init__(self):
        AtCmd.__init__(self)
        CMW100.__init__(self)

    def tx_power_aclr_evm_lmh_pipeline_gsm(self):
        self.tx_level = wt.tx_level
        self.port_tx = wt.port_tx
        self.chan = wt.channel
        self.mod_gsm = wt.mod_gsm
        self.tsc = 0 if self.mod_gsm == 'GMSK' else 5
        for tech in wt.tech:
            if tech == 'GSM' and wt.gsm_bands != []:
                self.tech = 'GSM'
                for band in wt.gsm_bands:
                    self.pcl = wt.tx_pcl_lb if band in [850, 900] else wt.tx_pcl_mb
                    self.band_gsm = band
                    self.tx_power_aclr_evm_lmh_gsm(plot=False)
                self.txp_aclr_evm_plot(self.filename, mode=1)  # mode=1: LMH mode

    def tx_power_aclr_evm_lmh_pipeline_wcdma(self):
        self.tx_level = wt.tx_level
        self.port_tx = wt.port_tx
        self.chan = wt.channel
        for tech in wt.tech:
            if tech == 'WCDMA' and wt.wcdma_bands != []:
                self.tech = 'WCDMA'
                for band in wt.wcdma_bands:
                    self.band_wcdma = band
                    self.tx_power_aclr_evm_lmh_wcdma(plot=False)
                self.txp_aclr_evm_plot(self.filename, mode=1)  # mode=1: LMH mode

    def tx_power_aclr_evm_lmh_pipeline_lte(self):
        self.tx_level = wt.tx_level
        self.port_tx = wt.port_tx
        self.chan = wt.channel
        items = [
            (tech, tx_path, bw, band)
            for tech in wt.tech
            for tx_path in wt.tx_paths
            for bw in wt.lte_bandwidths
            for band in wt.lte_bands
        ]
        for item in items:
            if item[0] == 'LTE' and wt.lte_bands != []:
                self.tech = item[0]
                self.tx_path = item[1]
                self.bw_lte = item[2]
                self.band_lte = item[3]
                if self.bw_lte in cm_pmt_ftm.bandwidths_selected_lte(self.band_lte):
                    self.tx_power_aclr_evm_lmh_lte(plot=False)
                else:
                    logger.info(f'B{self.band_lte} does not have BW {self.bw_lte}MHZ')
        for bw in wt.lte_bandwidths:
            try:
                self.filename = f'TxP_ACLR_EVM_{bw}MHZ_{self.tech}_LMH.xlsx'
                self.txp_aclr_evm_plot(self.filename, mode=1)  # mode=1: LMH mode
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundError:
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_power_aclr_evm_lmh_pipeline_fr1(self):
        self.tx_level = wt.tx_level
        self.port_tx = wt.port_tx
        self.chan = wt.channel
        self.sa_nsa_mode = wt.sa_nsa
        items = [
            (tech, tx_path, bw, band, type_)
            for tech in wt.tech
            for tx_path in wt.tx_paths
            for bw in wt.fr1_bandwidths
            for band in wt.fr1_bands
            for type_ in wt.type_fr1
        ]

        for item in items:
            if item[0] == 'FR1' and wt.fr1_bands != []:
                self.tech = item[0]
                self.tx_path = item[1]
                self.bw_fr1 = item[2]
                self.band_fr1 = item[3]
                self.type_fr1 = item[4]
                if self.bw_fr1 in cm_pmt_ftm.bandwidths_selected_fr1(self.band_fr1):
                    self.tx_power_aclr_evm_lmh_fr1(plot=False)
                else:
                    logger.info(f'B{self.band_fr1} does not have BW {self.bw_fr1}MHZ')
        for bw in wt.fr1_bandwidths:
            try:
                self.filename = f'TxP_ACLR_EVM_{bw}MHZ_{self.tech}_LMH.xlsx'
                self.txp_aclr_evm_plot(self.filename, mode=1)  # mode=1: LMH mode
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundError:
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_power_aclr_evm_lmh_gsm(self, plot=True):
        """
                order: tx_path > band > chan
                band_gsm:
                tx_pcl:
                rf_port:
                freq_select: 'LMH'
                tx_path:
                data: {rx_freq: [power, phase_err_rms, phase_peak, ferr,orfs_mod_-200,orfs_mod_200,...orfs_sw-400,orfs_sw400,...], ...}
        """
        rx_chan_list = cm_pmt_ftm.dl_chan_select_gsm(self.band_gsm)

        rx_chan_select_list = []
        for chan in self.chan:
            if chan == 'L':
                rx_chan_select_list.append(rx_chan_list[0])
            elif chan == 'M':
                rx_chan_select_list.append(rx_chan_list[1])
            elif chan == 'H':
                rx_chan_select_list.append(rx_chan_list[2])

        self.preset_instrument()
        self.set_test_mode_gsm()
        self.set_test_end_gsm()

        for script in wt.scripts:
            if script == 'GENERAL':
                self.script = script
                data_chan = {}
                for rx_chan_gsm in rx_chan_select_list:
                    logger.info('----------Test LMH progress---------')
                    self.rx_chan_gsm = rx_chan_gsm
                    self.rx_freq_gsm = cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, self.rx_chan_gsm, 'rx')
                    self.tx_freq_gsm = cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, self.rx_chan_gsm, 'tx')
                    self.loss_rx = get_loss(self.rx_freq_gsm)
                    self.loss_tx = get_loss(self.tx_freq_gsm)
                    self.set_test_mode_gsm()
                    self.antenna_switch_v2()
                    self.sig_gen_gsm()
                    self.sync_gsm()
                    self.tx_set_gsm()
                    aclr_mod_current_results = aclr_mod_results = self.tx_measure_gsm()
                    logger.debug(aclr_mod_results)
                    aclr_mod_current_results.append(self.measure_current())
                    data_chan[self.rx_freq_gsm] = aclr_mod_current_results + self.get_temperature()
                logger.debug(data_chan)
                # ready to export to excel
                self.filename = self.tx_power_relative_test_export_excel(data_chan, self.band_gsm, 0,
                                                                         self.pcl,
                                                                         mode=1)  # mode=1: LMH mode
        self.set_test_end_gsm()
        if plot:
            self.txp_aclr_evm_plot(self.filename, mode=1)  # mode=1: LMH mode
        else:
            pass

    def tx_power_aclr_evm_lmh_wcdma(self, plot=True):
        """
                order: tx_path > bw > band > mcs > rb > chan
                band_wcdma:
                tx_level:
                rf_port:
                freq_select: 'LMH'
                tx_path:
                data: {tx_level: [Pwr, U_-1, U_+1, U_-2, U_+2, OBW, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_chan_list = cm_pmt_ftm.dl_chan_select_wcdma(self.band_wcdma)
        tx_chan_list = [cm_pmt_ftm.transfer_chan_rx2tx_wcdma(self.band_wcdma, rx_chan) for rx_chan in rx_chan_list]
        tx_rx_chan_list = list(zip(tx_chan_list, rx_chan_list))  # [(tx_chan, rx_chan),...]

        tx_rx_chan_select_list = []
        for chan in self.chan:
            if chan == 'L':
                tx_rx_chan_select_list.append(tx_rx_chan_list[0])
            elif chan == 'M':
                tx_rx_chan_select_list.append(tx_rx_chan_list[1])
            elif chan == 'H':
                tx_rx_chan_select_list.append(tx_rx_chan_list[2])

        self.preset_instrument()

        for script in wt.scripts:
            if script == 'GENERAL':
                self.script = script
                data_chan = {}
                for tx_rx_chan_wcdma in tx_rx_chan_select_list:
                    logger.info('----------Test LMH progress---------')
                    self.rx_chan_wcdma = tx_rx_chan_wcdma[1]
                    self.tx_chan_wcdma = tx_rx_chan_wcdma[0]
                    self.rx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.rx_chan_wcdma, 'rx')
                    self.tx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.tx_chan_wcdma, 'tx')
                    self.loss_rx = get_loss(self.rx_freq_wcdma)
                    self.loss_tx = get_loss(self.tx_freq_wcdma)
                    self.set_test_end_wcdma()
                    self.set_test_mode_wcdma()
                    self.command_cmw100_query('*OPC?')
                    self.sig_gen_wcdma()
                    self.sync_wcdma()
                    self.tx_chan_wcdma = tx_rx_chan_wcdma[0]
                    self.tx_set_wcdma()
                    self.antenna_switch_v2()
                    aclr_mod_current_results = aclr_mod_results = self.tx_measure_wcdma()
                    logger.debug(aclr_mod_results)
                    aclr_mod_current_results.append(self.measure_current())
                    data_chan[
                        cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma,
                                                            self.tx_chan_wcdma)] = aclr_mod_current_results + self.get_temperature()
                logger.debug(data_chan)
                # ready to export to excel
                self.filename = self.tx_power_relative_test_export_excel(data_chan, self.band_wcdma, 5,
                                                                         self.tx_level,
                                                                         mode=1)  # mode=1: LMH mode
        self.set_test_end_wcdma()
        if plot:
            self.txp_aclr_evm_plot(self.filename, mode=1)  # mode=1: LMH mode
        else:
            pass

    def tx_power_aclr_evm_lmh_lte(self, plot=True):
        """
        order: tx_path > bw > band > mcs > rb > chan
        band_lte:
        bw_lte:
        tx_level:
        rf_port:
        freq_select: 'LMH'
        tx_path:
        data: {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('LTE', self.band_lte,
                                                   self.bw_lte)  # [L_rx_freq, M_rx_ferq, H_rx_freq]
        self.rx_freq_lte = rx_freq_list[1]
        self.loss_rx = get_loss(rx_freq_list[1])
        logger.info('----------Test LMH progress---------')
        self.preset_instrument()
        self.set_test_end_lte()
        self.set_test_mode_lte()
        self.antenna_switch_v2()
        self.sig_gen_lte()
        self.sync_lte()

        tx_freq_select_list = []
        for chan in self.chan:
            if chan == 'L':
                tx_freq_select_list.append(cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, rx_freq_list[0]))
            elif chan == 'M':
                tx_freq_select_list.append(cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, rx_freq_list[1]))
            elif chan == 'H':
                tx_freq_select_list.append(cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, rx_freq_list[2]))

        for mcs in wt.mcs_lte:
            self.mcs_lte = mcs
            for script in wt.scripts:
                if script == 'GENERAL':
                    self.script = script
                    for rb_ftm in wt.rb_ftm_lte:  # PRB, FRB
                        self.rb_size_lte, self.rb_start_lte = scripts.GENERAL_LTE[self.bw_lte][
                            self.rb_select_lte_dict[rb_ftm]]  # PRB: 0, # FRB: 1
                        self.rb_state = rb_ftm  # PRB, FRB
                        data_freq = {}
                        for tx_freq_lte in tx_freq_select_list:
                            self.tx_freq_lte = tx_freq_lte
                            self.loss_tx = get_loss(self.tx_freq_lte)
                            self.tx_set_lte()
                            aclr_mod_current_results = aclr_mod_results = self.tx_measure_lte()
                            logger.debug(aclr_mod_results)
                            aclr_mod_current_results.append(self.measure_current())
                            data_freq[self.tx_freq_lte] = aclr_mod_current_results + self.get_temperature()
                        logger.debug(data_freq)
                        # ready to export to excel
                        self.filename = self.tx_power_relative_test_export_excel(data_freq, self.band_lte, self.bw_lte,
                                                                                 self.tx_level,
                                                                                 mode=1)  # mode=1: LMH mode
        self.set_test_end_lte()
        if plot:
            self.txp_aclr_evm_plot(self.filename, mode=1)  # mode=1: LMH mode
        else:
            pass

    def tx_power_aclr_evm_lmh_fr1(self, plot=True):
        """
        order: tx_path > bw > band > mcs > rb > chan
        band_fr1:
        bw_fr1:
        tx_level:
        rf_port:
        freq_select: 'LMH'
        tx_path:
        data: {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('FR1', self.band_fr1,
                                                   self.bw_fr1)  # [L_rx_freq, M_rx_ferq, H_rx_freq]
        # self.rx_freq_fr1 = rx_freq_list[1]
        # self.loss_rx = get_loss(rx_freq_list[1])
        logger.info('----------Test LMH progress---------')
        self.preset_instrument()
        # self.set_test_end_fr1()
        # self.set_test_mode_fr1()
        # if self.srs_path_enable:
        #     self.srs_switch()
        # else:
        #     self.antenna_switch_v2()
        # self.sig_gen_fr1()
        # self.sync_fr1()

        scs = 1 if self.band_fr1 in [34, 38, 39, 40, 41, 42, 48, 77, 78,  # temp
                                     79] else 0  # for now FDD is forced to 15KHz and TDD is to be 30KHz  # temp
        scs = 15 * (2 ** scs)  # temp
        self.scs = scs  # temp

        tx_freq_select_list = []
        for chan in self.chan:
            if chan == 'L':
                tx_freq_select_list.append(cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq_list[0]))
            elif chan == 'M':
                tx_freq_select_list.append(cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq_list[1]))
            elif chan == 'H':
                tx_freq_select_list.append(cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq_list[2]))

        for mcs in wt.mcs_fr1:
            self.mcs_fr1 = mcs
            for script in wt.scripts:
                if script == 'GENERAL':
                    self.script = script
                    for rb_ftm in wt.rb_ftm_fr1:  # INNER_FULL, OUTER_FULL
                        self.rb_size_fr1, self.rb_start_fr1 = scripts.GENERAL_FR1[self.bw_fr1][self.scs][self.type_fr1][
                            self.rb_alloc_fr1_dict[rb_ftm]]
                        self.rb_state = rb_ftm  # INNER_FULL, OUTER_FULL
                        data_freq = {}
                        for tx_freq_fr1 in tx_freq_select_list:
                            self.tx_freq_fr1 = tx_freq_fr1
                            self.rx_freq_fr1 = cm_pmt_ftm.transfer_freq_tx2rx_fr1(self.band_fr1, tx_freq_fr1)  # temp
                            self.loss_tx = get_loss(self.tx_freq_fr1)
                            self.loss_rx = get_loss(rx_freq_list[1])  # temp
                            self.set_test_end_fr1()  # temp
                            self.set_test_mode_fr1()  # temp
                            if self.srs_path_enable:  # temp
                                self.srs_switch()  # temp
                            else:  # temp
                                self.antenna_switch_v2()  # temp
                            self.sig_gen_fr1()  # temp
                            self.sync_fr1()  # temp
                            self.tx_set_fr1()
                            aclr_mod_current_results = aclr_mod_results = self.tx_measure_fr1()
                            logger.debug(aclr_mod_results)
                            aclr_mod_current_results.append(self.measure_current())
                            data_freq[self.tx_freq_fr1] = aclr_mod_current_results + self.get_temperature()
                        logger.debug(data_freq)
                        # ready to export to excel
                        self.filename = self.tx_power_relative_test_export_excel(data_freq, self.band_fr1, self.bw_fr1,
                                                                                 self.tx_level,
                                                                                 mode=1)  # mode=1: LMH mode
        self.set_test_end_fr1()
        if plot:
            self.txp_aclr_evm_plot(self.filename, mode=1)  # mode=1: LMH mode
        else:
            pass

    def run_tx(self):
        for tech in wt.tech:
            if tech == 'LTE':
                self.tx_power_aclr_evm_lmh_pipeline_lte()
            elif tech == 'FR1':
                for script in wt.scripts:
                    if script == 'GENERAL':
                        self.tx_power_aclr_evm_lmh_pipeline_fr1()
                    elif script == 'FCC':
                        self.tx_power_pipline_fcc_fr1()
                    elif script == 'CE':
                        self.tx_power_pipline_ce_fr1()
                    elif tech == 'WCDMA':
                        self.tx_power_aclr_evm_lmh_pipeline_wcdma()
            elif tech == 'WCDMA':
                self.tx_power_aclr_evm_lmh_pipeline_wcdma()
            elif tech == 'GSM':
                self.tx_power_aclr_evm_lmh_pipeline_gsm()






def main():
    test = TxTest()


if __name__ == '__main__':
    main()


