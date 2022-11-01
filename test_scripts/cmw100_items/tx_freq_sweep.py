def tx_freq_sweep_pipline_gsm(self):
    self.rx_level = wt.init_rx_sync_level
    self.tx_level = wt.tx_level
    self.port_tx = wt.port_tx
    # self.chan = wt.channel
    self.mod_gsm = wt.mod_gsm
    self.tsc = 0 if self.mod_gsm == 'GMSK' else 5
    for tech in wt.tech:
        if tech == 'GSM' and wt.gsm_bands != []:
            self.tech = tech
            for band in wt.gsm_bands:
                self.pcl = wt.tx_pcl_lb if band in [850, 900] else wt.tx_pcl_mb
                self.band_gsm = band
                self.tx_freq_sweep_progress_gsm(plot=False)
            self.txp_aclr_evm_plot(self.filename, mode=0)


def tx_freq_sweep_pipline_wcdma(self):
    self.rx_level = wt.init_rx_sync_level
    self.tx_level = wt.tx_level
    self.port_tx = wt.port_tx
    # self.chan = wt.channel
    for tech in wt.tech:
        if tech == 'WCDMA' and wt.wcdma_bands != []:
            self.tech = tech
            for band in wt.wcdma_bands:
                self.band_wcdma = band
                self.tx_freq_sweep_progress_wcdma(plot=False)
            self.txp_aclr_evm_plot(self.filename, mode=0)


def tx_freq_sweep_pipline_lte(self):
    self.rx_level = wt.init_rx_sync_level
    self.tx_level = wt.tx_level
    self.port_tx = wt.port_tx
    # self.chan = wt.channel
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
                self.tx_freq_sweep_progress_lte(plot=False)
            else:
                logger.info(f'B{self.band_lte} does not have BW {self.bw_lte}MHZ')

    for bw in wt.lte_bandwidths:
        try:
            self.filename = f'Freq_sweep_{bw}MHZ_{self.tech}.xlsx'
            self.txp_aclr_evm_plot(self.filename, mode=0)
        except TypeError:
            logger.info(f'there is no data to plot because the band does not have this BW ')
        except FileNotFoundError:
            logger.info(f'there is not file to plot BW{bw} ')


def tx_freq_sweep_pipline_fr1(self):
    self.rx_level = wt.init_rx_sync_level
    self.tx_level = wt.tx_level
    self.port_tx = wt.port_tx
    # self.chan = wt.channel
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
                self.tx_freq_sweep_progress_fr1(plot=False)
            else:
                logger.info(f'B{self.band_fr1} does not have BW {self.bw_fr1}MHZ')
    for bw in wt.fr1_bandwidths:
        try:
            self.filename = f'Freq_sweep_{bw}MHZ_{self.tech}.xlsx'
            self.txp_aclr_evm_plot(self.filename, mode=0)
        except TypeError:
            logger.info(f'there is no data to plot because the band does not have this BW ')
        except FileNotFoundError:
            logger.info(f'there is not file to plot BW{bw} ')

def tx_freq_sweep_progress_gsm(self, plot=True):
    """
    band_gsm:
    tx_freq_gsm:
    tx_pcl:
    rf_port:
    freq_range_list: [freq_level_1, freq_level_2, freq_step]
    tx_path:
    data: {tx_freq: [power, phase_err_rms, phase_peak, ferr,orfs_mod_-200,orfs_mod_200,...orfs_sw-400,orfs_sw400,...], ...}
    """
    logger.info('----------Freq Sweep progress ---------')
    rx_chan_list = cm_pmt_ftm.dl_chan_select_gsm(self.band_gsm)

    self.preset_instrument()
    self.set_test_mode_gsm()
    self.set_test_end_gsm()

    rx_chan_range_list = [rx_chan_list[0], rx_chan_list[2], 0.2]
    step = int(rx_chan_range_list[2] * 1000 * 5)
    rx_freq_range_list = [cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, rx_chan) for rx_chan in
                          rx_chan_range_list[:2]]
    rx_freq_range_list.append(step)

    for script in ext_pmt_ftm.scripts:
        if script == 'GENERAL':
            self.script = script
            data = {}
            for rx_freq_gsm in range(rx_freq_range_list[0], rx_freq_range_list[1] + 1, step):
                self.rx_freq_gsm = rx_freq_gsm
                self.tx_freq_gsm = cm_pmt_ftm.transfer_freq_rx2tx_gsm(self.band_gsm, self.rx_freq_gsm)
                self.rx_chan_gsm = cm_pmt_ftm.transfer_freq2chan_gsm(self.band_gsm, self.rx_freq_gsm)
                self.loss_rx = get_loss(self.rx_freq_gsm)
                self.loss_tx = get_loss(self.tx_freq_gsm)
                self.set_test_mode_gsm()
                self.antenna_switch_v2()
                self.sig_gen_gsm()
                self.sync_gsm()
                self.tx_set_gsm()
                aclr_mod_results = self.tx_measure_gsm()
                logger.debug(aclr_mod_results)
                data[self.rx_freq_gsm] = aclr_mod_results
            logger.debug(data)
            self.filename = self.tx_power_relative_test_export_excel(data, self.band_gsm, 0,
                                                                     self.pcl, mode=0)
    self.set_test_end_gsm()
    if plot:
        self.txp_aclr_evm_plot(self.filename, mode=0)
    else:
        pass

def tx_freq_sweep_progress_wcdma(self, plot=True):
    """
    band_lte:
    bw_lte:
    tx_freq_lte:
    rb_num:
    rb_start:
    mcs:
    tx_level:
    rf_port:
    freq_range_list: [freq_level_1, freq_level_2, freq_step]
    tx_path:
    data: {tx_freq: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
    """
    logger.info('----------Freq Sweep progress ---------')
    rx_chan_list = cm_pmt_ftm.dl_chan_select_wcdma(self.band_wcdma)
    tx_chan_list = [cm_pmt_ftm.transfer_chan_rx2tx_wcdma(self.band_wcdma, rx_chan) for rx_chan in rx_chan_list]

    self.preset_instrument()

    tx_chan_range_list = [tx_chan_list[0], tx_chan_list[2], 1]
    step = tx_chan_range_list[2]

    for script in wt.scripts:
        if script == 'GENERAL':
            self.script = script
            data = {}
            for tx_chan_wcdma in range(tx_chan_range_list[0], tx_chan_range_list[1] + step, step):
                self.tx_chan_wcdma = tx_chan_wcdma
                self.rx_chan_wcdma = cm_pmt_ftm.transfer_chan_tx2rx_wcdma(self.band_wcdma, tx_chan_wcdma)
                self.tx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.tx_chan_wcdma, 'tx')
                self.rx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.rx_chan_wcdma, 'rx')
                self.loss_rx = get_loss(self.rx_freq_wcdma)
                self.loss_tx = get_loss(self.tx_freq_wcdma)
                self.set_test_end_wcdma()
                self.set_test_mode_wcdma()
                self.command_cmw100_query('*OPC?')
                self.sig_gen_wcdma()
                self.sync_wcdma()
                # self.antenna_switch_v2()
                self.tx_set_wcdma()
                self.antenna_switch_v2()
                aclr_mod_results = self.tx_measure_wcdma()
                logger.debug(aclr_mod_results)
                data[self.tx_chan_wcdma] = aclr_mod_results
            logger.debug(data)
            self.filename = self.tx_power_relative_test_export_excel(data, self.band_wcdma, 5,
                                                                     self.tx_level, mode=0)
    self.set_test_end_wcdma()
    if plot:
        self.txp_aclr_evm_plot(self.filename, mode=0)
    else:
        pass

def tx_freq_sweep_progress_lte(self, plot=True):
    """
    band_lte:
    bw_lte:
    tx_freq_lte:
    rb_num:
    rb_start:
    mcs:
    tx_level:
    rf_port:
    freq_range_list: [freq_level_1, freq_level_2, freq_step]
    tx_path:
    data: {tx_freq: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
    """
    logger.info('----------Freq Sweep progress ---------')
    rx_freq_list = cm_pmt_ftm.dl_freq_selected('LTE', self.band_lte, self.bw_lte)
    tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, rx_freq) for rx_freq in rx_freq_list]
    self.rx_freq_lte = rx_freq_list[1]
    self.loss_rx = get_loss(rx_freq_list[1])
    self.preset_instrument()
    self.set_test_end_lte()
    self.set_test_mode_lte()
    self.antenna_switch_v2()
    self.sig_gen_lte()
    self.sync_lte()

    freq_range_list = [tx_freq_list[0], tx_freq_list[2], 1000]
    step = freq_range_list[2]

    for mcs in wt.mcs_lte:
        self.mcs_lte = mcs
        for script in wt.scripts:
            if script == 'GENERAL':
                self.script = script
                for rb_ftm in wt.rb_ftm_lte:  # PRB, FRB
                    self.rb_size_lte, self.rb_start_lte = scripts.GENERAL_LTE[self.bw_lte][
                        self.rb_select_lte_dict[rb_ftm]]  # PRB: 0, # FRB: 1
                    self.rb_state = rb_ftm  # PRB, FRB
                    data = {}
                    for tx_freq_lte in range(freq_range_list[0], freq_range_list[1] + step, step):
                        self.tx_freq_lte = tx_freq_lte
                        self.loss_tx = get_loss(self.tx_freq_lte)
                        self.tx_set_lte()
                        aclr_mod_results = self.tx_measure_lte()
                        logger.debug(aclr_mod_results)
                        data[self.tx_freq_lte] = aclr_mod_results
                    logger.debug(data)
                    self.filename = self.tx_power_relative_test_export_excel(data, self.band_lte, self.bw_lte,
                                                                             self.tx_level, mode=0)
    self.set_test_end_lte()
    if plot:
        self.txp_aclr_evm_plot(self.filename, mode=0)
    else:
        pass

def tx_freq_sweep_progress_fr1(self, plot=True):
    """
    band_fr1:
    bw_fr1:
    tx_freq_fr1:
    rb_num:
    rb_start:
    mcs:
    tx_level:
    rf_port:
    freq_range_list: [freq_level_1, freq_level_2, freq_step]
    tx_path:
    data: {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
    """
    logger.info('----------Freq Sweep progress ---------')
    rx_freq_list = cm_pmt_ftm.dl_freq_selected('FR1', self.band_fr1, self.bw_fr1)
    tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq) for rx_freq in rx_freq_list]
    self.rx_freq_fr1 = rx_freq_list[1]
    self.loss_rx = get_loss(rx_freq_list[1])
    self.preset_instrument()
    self.set_test_end_fr1()
    self.set_test_mode_fr1()
    if self.srs_path_enable:
        self.srs_switch()
    else:
        self.antenna_switch_v2()
    self.sig_gen_fr1()
    self.sync_fr1()

    freq_range_list = [tx_freq_list[0], tx_freq_list[2], 1000]
    step = freq_range_list[2]

    for mcs in wt.mcs_fr1:
        self.mcs_fr1 = mcs
        for script in wt.scripts:
            if script == 'GENERAL':
                self.script = script
                for rb_ftm in wt.rb_ftm_fr1:  # PRB, FRB
                    self.rb_size_fr1, self.rb_start_fr1 = scripts.GENERAL_FR1[self.bw_fr1][self.scs][self.type_fr1][
                        self.rb_alloc_fr1_dict[rb_ftm]]  # PRB: 0, # FRB: 1
                    self.rb_state = rb_ftm  # PRB, FRB
                    data = {}
                    for tx_freq_fr1 in range(freq_range_list[0], freq_range_list[1] + step, step):
                        self.tx_freq_fr1 = tx_freq_fr1
                        self.loss_tx = get_loss(self.tx_freq_fr1)
                        self.tx_set_fr1()
                        aclr_mod_results = self.tx_measure_fr1()
                        logger.debug(aclr_mod_results)
                        data[self.tx_freq_fr1] = aclr_mod_results
                    logger.debug(data)
                    self.filename = self.tx_power_relative_test_export_excel(data, self.band_fr1, self.bw_fr1,
                                                                             self.tx_level, mode=0)
    self.set_test_end_fr1()
    if plot:
        self.txp_aclr_evm_plot(self.filename, mode=0)
    else:
        pass

def run_tx_freq_sweep(self):
    for tech in wt.tech:
        if tech == 'LTE':
            self.tx_freq_sweep_pipline_lte()
        elif tech == 'FR1':
            self.tx_freq_sweep_pipline_fr1()
        elif tech == 'WCDMA':
            self.tx_freq_sweep_pipline_wcdma()
        elif tech == 'GSM':
            self.tx_freq_sweep_pipline_gsm()
