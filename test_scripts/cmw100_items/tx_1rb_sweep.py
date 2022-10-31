def tx_1rb_sweep_pipeline_fr1(self):
    self.rx_level = wt.init_rx_sync_level
    self.tx_level = wt.tx_level
    self.port_tx = wt.port_tx
    self.chan = wt.channel
    self.sa_nsa_mode = wt.sa_nsa
    self.tx_1rb_filename_judge = True
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
                self.tx_1rb_sweep_progress_fr1(plot=False)
            else:
                logger.info(f'B{self.band_fr1} does not have BW {self.bw_fr1}MHZ')
    for bw in wt.fr1_bandwidths:
        try:
            self.filename = f'Tx_1RB_sweep_{bw}MHZ_{self.tech}.xlsx'
            self.txp_aclr_evm_plot(self.filename, mode=0)
        except TypeError:
            logger.info(f'there is no data to plot because the band does not have this BW ')
        except FileNotFoundError:
            logger.info(f'there is not file to plot BW{bw} ')
    self.tx_1rb_filename_judge = False

def run_tx_1rb_sweep(self):
    for tech in wt.tech:
        if tech == 'FR1':
            self.tx_1rb_sweep_pipeline_fr1()
        elif tech == 'LTE':
            pass
            else:
                pass
