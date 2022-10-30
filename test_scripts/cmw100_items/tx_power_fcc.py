def tx_power_pipline_fcc_fr1(self):  # band > bw > mcs > rb
    self.tx_level = wt.tx_level
    self.port_tx = wt.port_tx
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
                self.tx_power_fcc_fr1()
            else:
                logger.info(f'B{self.band_fr1} does not have BW {self.bw_fr1}MHZ')

    def tx_power_fcc_fr1(self):
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('FR1', self.band_fr1,
                                                   self.bw_fr1)  # [L_rx_freq, M_rx_ferq, H_rx_freq]
        self.rx_freq_fr1 = rx_freq_list[1]
        self.loss_rx = get_loss(rx_freq_list[1])
        logger.info('----------Test FCC LMH progress---------')
        self.preset_instrument()
        self.set_gprf_measurement()
        self.set_test_end_fr1()
        self.set_test_mode_fr1()
        if self.srs_path_enable:
            self.srs_switch()
        else:
            self.antenna_switch_v2()
        self.command_cmw100_query('*OPC?')

        tx_freq_select_list = []
        try:
            tx_freq_select_list = [int(freq * 1000) for freq in
                                   fcc.tx_freq_list_fr1[self.band_fr1][self.bw_fr1]]  # band > bw > tx_fre1_list
        except KeyError as err:
            logger.info(f"this Band: {err} don't have to  test this BW: {self.bw_fr1} for FCC")

        for mcs in wt.mcs_fr1:
            self.mcs_fr1 = mcs
            for script in wt.scripts:
                if script == 'FCC':
                    self.script = script
                    self.rb_state = 'FCC'
                    try:
                        for self.rb_size_fr1, self.rb_start_fr1 in scripts.FCC_FR1[self.band_fr1][self.bw_fr1][self.mcs_fr1]:
                            data = {}
                            for num, tx_freq_fr1 in enumerate(tx_freq_select_list):
                                chan_mark = f'chan{num}'
                                self.tx_freq_fr1 = tx_freq_fr1
                                self.loss_tx = get_loss(self.tx_freq_fr1)
                                self.set_gprf_tx_freq()
                                self.set_duty_cycle()
                                self.tx_set_no_sync_fr1()
                                power_results = self.get_gprf_power()
                                data[self.tx_freq_fr1] = (
                                    chan_mark, power_results)  # data = {tx_freq:(chan_mark, power)}
                            logger.debug(data)
                            # ready to export to excel
                            self.filename = self.tx_power_fcc_ce_export_excel(data)
                    except KeyError as err:
                        logger.debug(f'show error: {err}')
                        logger.info(
                            f"Band {self.band_fr1}, BW: {self.bw_fr1} don't need to test this MCS: {self.mcs_fr1} for FCC")

        self.set_test_end_fr1()
        # if plot == True:
        #     self.txp_aclr_evm_plot(self.filename, mode=1)  # mode=1: LMH mode
        # else:
        #     pass
