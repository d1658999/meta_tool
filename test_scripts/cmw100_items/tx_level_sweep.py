def tx_power_relative_test_initial_gsm(self):
    logger.info('----------Relatvie test initial----------')
    self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:SCO:PVT 5')
    self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:SCO:MOD 5')
    self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:SCO:SMOD 5')
    self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:SCO:SSW 5')
    self.command_cmw100_write(f'CONF:GSM:MEAS:SCEN:ACT STAN')
    self.command_cmw100_query(f'*OPC?')
    self.command_cmw100_write(f'ROUT:WCDMA:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
    self.command_cmw100_write(f'CONF:WCDMA:MEAS:RFS:EATT {self.loss_tx}')
    self.command_cmw100_write(f'CONF:WCDMA:MEAS:RFS:UMAR 10.00')
    self.command_cmw100_write(f"TRIG:GSM:MEAS:MEV:SOUR 'Power'")
    self.command_cmw100_write(f'TRIG:WCDM:MEAS:MEV:THR -30')
    self.command_cmw100_write(f'TRIG:GSM:MEAS:MEV:THR -20.0')
    self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:REP SING')
    self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:RES:ALL ON, ON, ON, ON, ON, ON, ON, ON, ON, ON, OFF, ON')
    self.command_cmw100_query(f'*OPC?')
    self.command_cmw100_write(
        f'CONF:GSM:MEAS:MEV:SMOD:OFR 100KHZ,200KHZ,250KHZ,400KHZ,600KHZ,800KHZ,1600KHZ,1800KHZ,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
    self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:SMOD:EAR ON,6,45,ON,90,129')
    self.command_cmw100_write(
        f'CONF:GSM:MEAS:MEV:SSW:OFR 400KHZ,600KHZ,1200KHZ,1800KHZ,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
    self.command_cmw100_query(f'SYST:ERR:ALL?')


def tx_power_relative_test_initial_wcdma(self):
    logger.info('----------Relatvie test initial----------')
    self.command_cmw100_write(f'*CLS')
    self.command_cmw100_write(f'CONF:WCDM:MEAS:MEV:SCO:MOD 5')
    self.command_cmw100_write(f'CONF:WCDM:MEAS:MEV:SCO:SPEC 5')
    self.command_cmw100_write(f'ROUT:WCDMA:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
    self.command_cmw100_write(f'CONF:WCDMA:MEAS:RFS:EATT {self.loss_tx}')
    self.command_cmw100_write(f'CONF:WCDMA:MEAS:RFS:UMAR 10.00')
    self.command_cmw100_write(f"TRIG:WCDM:MEAS:MEV:SOUR 'Free Run (Fast sync)'")
    self.command_cmw100_write(f'TRIG:WCDM:MEAS:MEV:THR -30')
    self.command_cmw100_write(f'CONF:WCDM:MEAS:MEV:REP SING')
    self.command_cmw100_write(f'CONF:WCDM:MEAS:MEV:RES:ALL ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON')
    self.command_cmw100_query(f'*OPC?')
    self.command_cmw100_query(f'SYST:ERR:ALL?')
    self.command_cmw100_write(f'CONF:WCDM:MEAS:BAND OB{self.band_wcdma}')
    self.command_cmw100_write(f'CONF:WCDM:MEAS:RFS:FREQ {self.tx_chan_wcdma} CH')
    self.command_cmw100_write(f'CONF:WCDM:MEAS:UES:DPDC ON')
    self.command_cmw100_write(f'CONF:WCDM:MEAS:UES:SFOR 0')
    self.command_cmw100_write(f'CONF:WCDM:MEAS:UES:SCOD 13496235')
    self.command_cmw100_write(f'CONF:WCDM:MEAS:UES:ULC WCDM')
    self.command_cmw100_query(f'SYST:ERR:ALL?')


def tx_power_relative_test_initial_lte(self):
    logger.info('----------Relatvie test initial----------')
    mode = 'TDD' if self.band_lte in [38, 39, 40, 41, 42, 48] else 'FDD'
    self.command_cmw100_write(f'CONF:LTE:MEAS:DMODe {mode}')
    self.command_cmw100_write(f'CONF:LTE:MEAS:BAND OB{self.band_lte}')
    self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:FREQ {self.tx_freq_lte}KHz')
    self.command_cmw100_query(f'*OPC?')
    rb = f'0{self.bw_lte * 10}' if self.bw_lte < 10 else f'{self.bw_lte * 10}'
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:CBAN B{rb}')
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MOD:MSCH {self.mcs_lte}')
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:NRB {self.rb_size_lte}')
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:ORB {self.rb_start_lte}')
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:CPR NORM')
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:PLC 0')
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:DSSP 0')
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:AUTO OFF')
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MOEX ON')
    lim1 = -10 if self.bw_lte == 1.4 else -13 if self.bw_lte == 3 else -15 if self.bw_lte == 5 else -18 if self.bw_lte == 10 else -20 if self.bw_lte == 15 else -21
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM1:CBAN{self.bw_lte * 10} ON,0MHz,1MHz,{lim1},K030')
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM2:CBAN{self.bw_lte * 10} ON,1MHz,2.5MHz,-10,M1')
    self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM3:CBAN{self.bw_lte * 10} ON,2.5MHz,2.8MHz,-25,M1') if self.bw_lte < 3 else self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM3:CBAN{self.bw_lte * 10} ON,2.5MHz,2.8MHz,-10,M1')
    self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM4:CBAN{self.bw_lte * 10} ON,2.8MHz,5MHz,-10,M1') if self.bw_lte >= 3 else self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM4:CBAN{self.bw_lte * 10} OFF,2.8MHz,5MHz,-25,M1')
    self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM5:CBAN{self.bw_lte * 10} ON,5MHz,6MHz,-13,M1') if self.bw_lte > 3 else self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM5:CBAN{self.bw_lte * 10} OFF,5MHz,6MHz,-25,M1') if self.bw_lte < 3 else self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM5:CBAN{self.bw_lte * 10} ON,5MHz,6MHz,-25,M1')
    self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM6:CBAN{self.bw_lte * 10} ON,6MHz,10MHz,-13,M1') if self.bw_lte > 5 else self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM6:CBAN{self.bw_lte * 10} OFF,6MHz,10MHz,-25,M1') if self.bw_lte < 5 else self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM6:CBAN{self.bw_lte * 10} ON,6MHz,10MHz,-25,M1')
    self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM7:CBAN{self.bw_lte * 10} ON,10MHz,15MHz,-13,M1') if self.bw_lte > 10 else self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM7:CBAN{self.bw_lte * 10} OFF,10MHz,15MHz,-25,M1') if self.bw_lte < 10 else self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM7:CBAN{self.bw_lte * 10} ON,10MHz,15MHz,-25,M1')
    self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM8:CBAN{self.bw_lte * 10} ON,15MHz,20MHz,-13,M1') if self.bw_lte > 15 else self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM8:CBAN{self.bw_lte * 10} OFF,15MHz,20MHz,-25,M1') if self.bw_lte < 15 else self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM8:CBAN{self.bw_lte * 10} ON,15MHz,20MHz,-25,M1')
    self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM9:CBAN{self.bw_lte * 10} ON,20MHz,25MHz,-25,M1') if self.bw_lte == 20 else self.command_cmw100_write(
        f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM9:CBAN{self.bw_lte * 10} OFF,20MHz,25MHz,-25,M1')

    self.command_cmw100_query(f'SYST:ERR:ALL?')
    self.command_cmw100_write(f'CONFigure:LTE:MEAS:MEValuation:MSLot ALL')
    self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:UMAR 10.000000')
    self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:ENP {self.tx_level + 5}')
    self.command_cmw100_write(f'ROUT:LTE:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
    self.command_cmw100_query(f'*OPC?')
    self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:UMAR 10.000000')
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:AUTO ON')
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:SCO:MOD 5')
    self.command_cmw100_query(f'*OPC?')
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:SCO:SPEC:ACLR 5')
    self.command_cmw100_query(f'*OPC?')
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:SCO:SPEC:SEM 5')
    self.command_cmw100_query(f'*OPC?')
    self.command_cmw100_write(f"TRIG:LTE:MEAS:MEV:SOUR 'GPRF Gen1: Restart Marker'")
    self.command_cmw100_write(f'TRIG:LTE:MEAS:MEV:THR -20.0')
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:REP SING')
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RES:ALL ON, ON, ON, ON, ON, ON, ON, ON, ON, ON')
    self.command_cmw100_query(f'*OPC?')
    self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MSUB 2, 10, 0')
    self.command_cmw100_write(f'CONF:LTE:MEAS:SCEN:ACT SAL')
    self.command_cmw100_query(f'SYST:ERR:ALL?')
    self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:EATT {self.loss_tx}')
    self.command_cmw100_query(f'*OPC?')
    self.command_cmw100_write(f'ROUT:GPRF:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
    self.command_cmw100_write(f'CONF:GPRF:MEAS:POW:SCO 2')
    self.command_cmw100_write(f'CONF:GPRF:MEAS:POW:REP SING')
    self.command_cmw100_write(f'CONF:GPRF:MEAS:POW:LIST OFF')
    self.command_cmw100_write(f"TRIGger:GPRF:MEAS:POWer:SOURce 'Free Run'")
    self.command_cmw100_write(f'CONF:GPRF:MEAS:POW:TRIG:SLOP REDG')
    self.command_cmw100_write(f'CONF:GPRF:MEAS:POW:SLEN 5.0e-3')
    self.command_cmw100_write(f'CONF:GPRF:MEAS:POW:MLEN 8.0e-4')
    self.command_cmw100_write(f'TRIGger:GPRF:MEAS:POWer:OFFSet 2.1E-3')
    self.command_cmw100_write(f'TRIG:GPRF:MEAS:POW:MODE ONCE')
    self.command_cmw100_write(f'CONF:GPRF:MEAS:RFS:UMAR 10.000000')
    self.command_cmw100_write(f'CONF:GPRF:MEAS:RFS:ENP {self.tx_level + 5}.00')


def tx_power_relative_test_initial_fr1(self):
    scs = 1 if self.band_fr1 in [34, 38, 39, 40, 41, 42, 48, 75, 76, 77, 78,
                                 79] else 0  # for now FDD is forced to 15KHz and TDD is to be 30KHz
    scs = 15 * (2 ** scs)  # for now TDD only use 30KHz, FDD only use 15KHz
    logger.info('----------Relatvie test initial----------')
    mode = 'TDD' if self.band_fr1 in [34, 38, 39, 40, 41, 42, 48, 75, 76, 77, 78, 79] else 'FDD'
    self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:DMODe {mode}')
    self.command_cmw100_write(f'CONF:NRS:MEAS:BAND OB{self.band_fr1}')
    self.command_cmw100_write(f'CONF:NRS:MEAS:RFS:FREQ {self.tx_freq_fr1}KHz')
    self.command_cmw100_query(f'*OPC?')
    self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:PLC 0')
    self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:MOEX ON')
    bw = f'00{self.bw_fr1}' if self.bw_fr1 < 10 else f'0{self.bw_fr1}' if 10 <= self.bw_fr1 < 100 else self.bw_fr1
    self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:BWC S{scs}K, B{bw}')
    self.command_cmw100_write(
        f'CONF:NRS:MEAS:MEV:LIM:SEM:AREA1:CBAN{self.bw_fr1}   ON, 0.015MHz, 0.0985MHz, {round(-13.5 - 10 * math.log10(self.bw_fr1 / 5), 1)},K030')
    self.command_cmw100_write(
        f'CONF:NRS:MEAS:MEV:LIM:SEM:AREA2:CBAN{self.bw_fr1}   ON,   1.5MHz,    4.5MHz,  -8.5,  M1')
    self.command_cmw100_write(
        f'CONF:NRS:MEAS:MEV:LIM:SEM:AREA3:CBAN{self.bw_fr1}   ON,   5.5MHz,   {round(-0.5 + self.bw_fr1, 1)}MHz, -11.5,  M1')
    self.command_cmw100_write(
        f'CONF:NRS:MEAS:MEV:LIM:SEM:AREA4:CBAN{self.bw_fr1}   ON, 0 {round(0.5 + self.bw_fr1, 1)}MHz,  {round(4.5 + self.bw_fr1, 1)}MHz, -23.5,  M1')
    _256Q_flag = 2 if self.mcs_fr1 == 'Q256' else 0
    self.command_cmw100_write(
        f'CONFigure:NRSub:MEASurement:MEValuation:PUSChconfig {self.mcs_fr1},A,OFF,{self.rb_size_fr1},{self.rb_start_fr1},14,0,T1,SING,{_256Q_flag},2')
    type_ = 'ON' if self.type_fr1 == 'DFTS' else 'OFF'  # DFTS: ON, CP: OFF
    self.command_cmw100_write(f'CONFigure:NRSub:MEASurement:MEValuation:DFTPrecoding {type_}')
    self.command_cmw100_write(f'CONFigure:NRSub:MEASurement:MEValuation:PCOMp OFF, 6000E+6')
    self.command_cmw100_query(f'*OPC?')
    self.command_cmw100_write(f'CONFigure:NRSub:MEASurement:MEValuation:REPetition SING')
    self.command_cmw100_write(f'CONFigure:NRSub:MEASurement:MEValuation:PLCid 0')
    self.command_cmw100_write(f'CONFigure:NRSub:MEASurement:MEValuation:CTYPe PUSC')
    self.command_cmw100_write(f'CONF:NRS:MEAS:ULDL:PER MS25')
    self.command_cmw100_write(f'CONF:NRS:MEAS:ULDL:PATT S{scs}K, 3,0,1,14 ')
    self.command_cmw100_write(f'CONFigure:NRSub:MEASurement:MEValuation:MSLot ALL')
    self.command_cmw100_write(f'ROUT:NRS:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
    self.command_cmw100_write(f'CONF:NRS:MEAS:RFS:UMAR 10.000000')
    self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:SCO:MOD 5')
    self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:SCO:SPEC:ACLR 5')
    self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:SCO:SPEC:SEM 5')
    self.command_cmw100_write(f"TRIG:NRS:MEAS:MEV:SOUR 'GPRF GEN1: Restart Marker'")
    self.command_cmw100_write(f'TRIG:NRS:MEAS:MEV:THR -20.0')
    self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:REP SING')
    self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:RES:ALL ON, ON, ON, ON, ON, ON, ON, ON, ON, ON')
    self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:NSUB 10')
    self.command_cmw100_write(f'CONFigure:NRSub:MEASurement:MEValuation:MSLot ALL')
    self.command_cmw100_write(f'CONF:NRS:MEAS:SCEN:ACT SAL')
    self.command_cmw100_write(f'CONF:NRS:MEAS:RFS:EATT {self.loss_tx}')
    self.command_cmw100_query(f'*OPC?')

    def tx_level_sweep_pipeline_gsm(self):
        self.rx_level = wt.init_rx_sync_level
        self.tx_level = wt.tx_level
        self.port_tx = wt.port_tx
        self.chan = wt.channel
        self.mod_gsm = wt.mod_gsm
        self.tsc = 0 if self.mod_gsm == 'GMSK' else 5
        for tech in wt.tech:
            if tech == 'GSM' and wt.gsm_bands != []:
                self.tech = tech
                for band in wt.gsm_bands:
                    self.pcl = wt.tx_pcl_lb if band in [850, 900] else wt.tx_pcl_mb
                    self.band_gsm = band
                    self.tx_level_sweep_progress_gsm(plot=False)
                self.txp_aclr_evm_plot(self.filename, mode=0)

    def tx_level_sweep_pipeline_wcdma(self):
        self.rx_level = wt.init_rx_sync_level
        self.tx_level = wt.tx_level
        self.port_tx = wt.port_tx
        self.chan = wt.channel
        for tech in wt.tech:
            if tech == 'WCDMA' and wt.wcdma_bands != []:
                self.tech = tech
                for tx_path in wt.tx_paths:
                    self.tx_path = tx_path
                    for band in wt.wcdma_bands:
                        self.band_wcdma = band
                        self.tx_level_sweep_progress_wcdma(plot=False)
                    self.txp_aclr_evm_plot(self.filename, mode=0)

    def tx_level_sweep_pipeline_lte(self):
        self.rx_level = wt.init_rx_sync_level
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
                    self.tx_level_sweep_progress_lte(plot=False)
                else:
                    logger.info(f'B{self.band_lte} does not have BW {self.bw_lte}MHZ')
        for bw in wt.lte_bandwidths:
            try:
                self.filename = f'Tx_level_sweep_{bw}MHZ_{self.tech}.xlsx'
                self.txp_aclr_evm_plot(self.filename, mode=0)
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundError:
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_level_sweep_pipeline_fr1(self):
        self.rx_level = wt.init_rx_sync_level
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
                    self.tx_level_sweep_progress_fr1(plot=False)
                else:
                    logger.info(f'B{self.band_fr1} does not have BW {self.bw_fr1}MHZ')
        for bw in wt.fr1_bandwidths:
            try:
                self.filename = f'Tx_level_sweep_{bw}MHZ_{self.tech}.xlsx'
                self.txp_aclr_evm_plot(self.filename, mode=0)
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundError:
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_1rb_sweep_progress_fr1(self, plot=True):
        logger.info('----------1RB Sweep progress ---------')
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('FR1', self.band_fr1, self.bw_fr1)
        # tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq) for rx_freq in rx_freq_list]
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

        for mcs in wt.mcs_fr1:
            self.mcs_fr1 = mcs
            for script in wt.scripts:
                if script == 'GENERAL':
                    self.script = script
                    tx_freq_select_list = []
                    for chan in self.chan:
                        if chan == 'L':
                            tx_freq_select_list.append(
                                cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq_list[0]))
                        elif chan == 'M':
                            tx_freq_select_list.append(
                                cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq_list[1]))
                        elif chan == 'H':
                            tx_freq_select_list.append(
                                cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq_list[2]))

                    for tx_freq_select in tx_freq_select_list:
                        self.tx_freq_fr1 = tx_freq_select
                        self.rb_size_fr1, rb_sweep_fr1 = scripts.GENERAL_FR1[self.bw_fr1][self.scs][self.type_fr1][
                            self.rb_alloc_fr1_dict['EDGE_1RB_RIGHT']]  # capture EDGE_1RB_RIGHT
                        self.rb_state = '1rb_sweep'
                        data = {}
                        for rb_start in range(rb_sweep_fr1 + 1):
                            self.rb_start_fr1 = rb_start
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

    def tx_level_sweep_progress_gsm(self, plot=True):
        """
        band_gsm:
        tx_freq_gsm:
        pwr:
        rf_port:
        loss:
        tx_path:
        data {tx_pcl: [power, phase_err_rms, phase_peak, ferr,orfs_mod_-200,orfs_mod_200,...orfs_sw-400,orfs_sw400,...], ...}
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
                #  initial all before tx level prgress
                for rx_chan_gsm in rx_chan_select_list:
                    self.rx_chan_gsm = rx_chan_gsm
                    self.rx_freq_gsm = cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, self.rx_chan_gsm, 'rx')
                    self.tx_freq_gsm = cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, self.rx_chan_gsm, 'tx')
                    self.loss_rx = get_loss(self.rx_freq_gsm)
                    self.loss_tx = get_loss(self.tx_freq_gsm)
                    self.set_test_mode_gsm()
                    self.antenna_switch_v2()
                    self.sig_gen_gsm()
                    self.sync_gsm()

                    # self.tx_power_relative_test_initial_gsm()

                    tx_range_list = wt.tx_pcl_range_list_lb if self.band_gsm in [850,
                                                                                 900] else wt.tx_pcl_range_list_mb  # [tx_pcl_1, tx_pcl_2]

                    logger.info('----------TX Level Sweep progress---------')
                    logger.info(f'----------from PCL{tx_range_list[0]} to PCL{tx_range_list[1]}----------')

                    step = -1 if tx_range_list[0] > tx_range_list[1] else 1

                    #  following is real change tx pcl prgress

                    data = {}
                    for tx_pcl in range(tx_range_list[0], tx_range_list[1] + step, step):
                        self.pcl = tx_pcl
                        logger.info(f'========Now Tx PCL = PCL{self.pcl} ========')
                        self.tx_set_gsm()
                        mod_orfs_current_results = mod_orfs_results = self.tx_measure_gsm()
                        logger.debug(mod_orfs_results)
                        mod_orfs_current_results.append(self.measure_current())
                        data[tx_pcl] = mod_orfs_current_results
                    logger.debug(data)
                    self.filename = self.tx_power_relative_test_export_excel(data, self.band_gsm, 0,
                                                                             self.rx_freq_gsm)
        self.set_test_end_gsm()
        if plot:
            self.txp_aclr_evm_plot(self.filename, mode=0)
        else:
            pass

    def tx_level_sweep_progress_wcdma(self, plot=True):
        """
        band_wcdma:
        bw_wcdma:
        tx_freq_wcdma:
        rb_num:
        rb_start:
        mcs:
        pwr:
        rf_port:
        loss:
        tx_path:
        data {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
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
                #  initial all before tx level prgress
                for tx_rx_chan_wcdma in tx_rx_chan_select_list:
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

                    # self.tx_power_relative_test_initial_wcdma()

                    tx_range_list = wt.tx_level_range_list  # [tx_level_1, tx_level_2]

                    logger.info('----------TX Level Sweep progress---------')
                    logger.info(f'----------from {tx_range_list[0]} dBm to {tx_range_list[1]} dBm----------')

                    step = -1 if tx_range_list[0] > tx_range_list[1] else 1

                    #  following is real change tx level prgress

                    data = {}
                    for tx_level in range(tx_range_list[0], tx_range_list[1] + step, step):
                        self.tx_level = tx_level
                        logger.info(f'========Now Tx level = {self.tx_level} dBm========')
                        self.tx_set_wcdma()
                        # self.command(f'AT+HTXPERSTART={self.tx_chan_wcdma}')
                        # self.command(f'AT+HSETMAXPOWER={self.tx_level * 10}')
                        self.antenna_switch_v2()
                        spectrum_mod_current_results = spectrum_mod_results = self.tx_measure_wcdma()
                        # self.command_cmw100_write(f'CONF:WCDMA:MEAS:RFS:UMAR 10.00')
                        # self.command_cmw100_write(f'CONF:WCDM:MEAS:RFS:ENP {self.tx_level + 5}')
                        # mod_results = self.command_cmw100_query(
                        #     f'READ:WCDM:MEAS:MEV:MOD:AVER?')  # P1 is EVM, P4 is Ferr, P8 is IQ Offset
                        # mod_results = mod_results.split(',')
                        # mod_results = [mod_results[1], mod_results[4], mod_results[8]]
                        # mod_results = [eval(m) for m in mod_results]
                        # logger.info(
                        #     f'EVM: {mod_results[0]:.2f}, FREQ_ERR: {mod_results[1]:.2f}, IQ_OFFSET: {mod_results[2]:.2f}')
                        # self.command_cmw100_write(f'INIT:WCDM:MEAS:MEV')
                        # self.command_cmw100_query(f'*OPC?')
                        # f_state = self.command_cmw100_query(f'FETC:WCDM:MEAS:MEV:STAT?')
                        # while f_state != 'RDY':
                        #     time.sleep(0.2)
                        #     f_state = self.command_cmw100_query('FETC:WCDM:MEAS:MEV:STAT?')
                        #     self.command_cmw100_query('*OPC?')
                        # spectrum_results = self.command_cmw100_query(
                        #     f'FETC:WCDM:MEAS:MEV:SPEC:AVER?')  # P1: Power, P2: ACLR_-2, P3: ACLR_-1, P4:ACLR_+1, P5:ACLR_+2, P6:OBW
                        # spectrum_results = spectrum_results.split(',')
                        # spectrum_results = [
                        #     round(eval(spectrum_results[1]), 2),
                        #     round(eval(spectrum_results[3]) - eval(spectrum_results[1]), 2),
                        #     round(eval(spectrum_results[4]) - eval(spectrum_results[1]), 2),
                        #     round(eval(spectrum_results[2]) - eval(spectrum_results[1]), 2),
                        #     round(eval(spectrum_results[5]) - eval(spectrum_results[1]), 2),
                        #     round(eval(spectrum_results[6]) / 1000000, 2)
                        # ]
                        # logger.info(
                        #     f'Power: {spectrum_results[0]:.2f}, ACLR_-1: {spectrum_results[2]:.2f}, ACLR_1: {spectrum_results[3]:.2f}, ACLR_-2: {spectrum_results[1]:.2f}, ACLR_+2: {spectrum_results[4]:.2f}, OBW: {spectrum_results[5]:.2f}MHz')
                        # self.command_cmw100_write(f'STOP:WCDM:MEAS:MEV')
                        # self.command_cmw100_query(f'*OPC?')

                        logger.debug(spectrum_mod_results)
                        spectrum_mod_current_results.append(self.measure_current())
                        data[tx_level] = spectrum_mod_current_results
                    logger.debug(data)
                    self.filename = self.tx_power_relative_test_export_excel(data, self.band_wcdma, 5,
                                                                             self.tx_freq_wcdma)
        self.set_test_end_wcdma()
        if plot:
            self.txp_aclr_evm_plot(self.filename, mode=0)
        else:
            pass

    def tx_level_sweep_progress_lte(self, plot=True):
        """
        band_lte:
        bw_lte:
        tx_freq_lte:
        rb_num:
        rb_start:
        mcs:
        pwr:
        rf_port:
        loss:
        tx_path:
        data {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('LTE', self.band_lte, self.bw_lte)
        tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, rx_freq) for rx_freq in rx_freq_list]
        self.rx_freq_lte = rx_freq_list[1]
        self.tx_freq_lte = tx_freq_list[1]
        self.loss_rx = get_loss(rx_freq_list[1])
        self.preset_instrument()
        self.set_test_end_lte()
        self.set_test_mode_lte()
        self.antenna_switch_v2()
        self.command_cmw100_query('*OPC?')
        self.sig_gen_lte()
        self.sync_lte()

        for mcs in wt.mcs_lte:
            self.mcs_lte = mcs
            for script in wt.scripts:
                if script == 'GENERAL':
                    self.script = script
                    for rb_ftm in wt.rb_ftm_lte:  # PRB, FRB
                        self.rb_size_lte, self.rb_start_lte = scripts.GENERAL_LTE[self.bw_lte][
                            self.rb_select_lte_dict[rb_ftm]]  # PRB: 0, # FRB: 1
                        self.rb_state = rb_ftm  # PRB, FRB

                        tx_freq_select_list = []
                        for chan in self.chan:
                            if chan == 'L':
                                tx_freq_select_list.append(
                                    cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, rx_freq_list[0]))
                            elif chan == 'M':
                                tx_freq_select_list.append(
                                    cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, rx_freq_list[1]))
                            elif chan == 'H':
                                tx_freq_select_list.append(
                                    cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, rx_freq_list[2]))

                        #  initial all before tx level prgress
                        for tx_freq_select in tx_freq_select_list:
                            self.tx_freq_lte = tx_freq_select
                            self.loss_tx = get_loss(self.tx_freq_lte)
                            self.tx_set_lte()
                            self.tx_power_relative_test_initial_lte()

                            tx_range_list = wt.tx_level_range_list  # [tx_level_1, tx_level_2]

                            logger.info('----------TX Level Sweep progress---------')
                            logger.info(f'----------from {tx_range_list[0]} dBm to {tx_range_list[1]} dBm----------')

                            step = -1 if tx_range_list[0] > tx_range_list[1] else 1

                            #  following is real change tx level prgress

                            data = {}
                            for tx_level in range(tx_range_list[0], tx_range_list[1] + step, step):
                                self.tx_level = tx_level
                                logger.info(f'========Now Tx level = {self.tx_level} dBm========')
                                self.command(f'AT+LTXPWRLVLSET={self.tx_level}')
                                self.command(f'AT+LTXCHNSDREQ')
                                self.command_cmw100_write('CONF:LTE:MEAS:RFS:UMAR 10.000000')
                                self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:ENP {self.tx_level + 5}.00')
                                mod_results = self.command_cmw100_query(f'READ:LTE:MEAS:MEV:MOD:AVER?')
                                mod_results = mod_results.split(',')
                                mod_results = [mod_results[3], mod_results[15], mod_results[14]]
                                mod_results = [eval(m) for m in mod_results]
                                # logger.info(f'mod_results = {mod_results}')
                                logger.info(
                                    f'EVM: {mod_results[0]:.2f}, FREQ_ERR: {mod_results[1]:.2f}, IQ_OFFSET: {mod_results[2]:.2f}')
                                self.command_cmw100_write('INIT:LTE:MEAS:MEV')
                                self.command_cmw100_query('*OPC?')
                                f_state = self.command_cmw100_query('FETC:LTE:MEAS:MEV:STAT?')
                                while f_state != 'RDY':
                                    f_state = self.command_cmw100_query('FETC:LTE:MEAS:MEV:STAT?')
                                    self.command_cmw100_query('*OPC?')
                                aclr_results = self.command_cmw100_query('FETC:LTE:MEAS:MEV:ACLR:AVER?')
                                aclr_results = aclr_results.split(',')[1:]
                                aclr_results = [eval(aclr) * -1 if eval(aclr) > 30 else eval(aclr) for aclr in
                                                aclr_results]  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2
                                logger.info(
                                    f'Power: {aclr_results[3]:.2f}, E-UTRA: [{aclr_results[2]:.2f}, {aclr_results[4]:.2f}], UTRA_1: [{aclr_results[1]:.2f}, {aclr_results[5]:.2f}], UTRA_2: [{aclr_results[0]:.2f}, {aclr_results[6]:.2f}]')
                                iem_results = self.command_cmw100_query('FETC:LTE:MEAS:MEV:IEM:MARG?')
                                iem_results = iem_results.split(',')
                                logger.info(f'InBandEmissions Margin: {eval(iem_results[2]):.2f}dB')
                                # logger.info(f'IEM_MARG results: {iem_results}')
                                esfl_results = self.command_cmw100_query(f'FETC:LTE:MEAS:MEV:ESFL:EXTR?')
                                esfl_results = esfl_results.split(',')
                                ripple1 = f'{eval(esfl_results[2]):.2f}' if esfl_results[2] != 'NCAP' else 'NCAP'
                                ripple2 = f'{eval(esfl_results[3]):.2f}' if esfl_results[3] != 'NCAP' else 'NCAP'
                                logger.info(
                                    f'Equalize Spectrum Flatness: Ripple1:{ripple1} dBpp, Ripple2:{ripple2} dBpp')
                                time.sleep(0.2)
                                # logger.info(f'ESFL results: {esfl_results}')
                                sem_results = self.command_cmw100_query(f'FETC:LTE:MEAS:MEV:SEM:MARG?')
                                logger.info(f'SEM_MARG results: {sem_results}')
                                sem_avg_results = self.command_cmw100_query(f'FETC:LTE:MEAS:MEV:SEM:AVER?')
                                sem_avg_results = sem_avg_results.split(',')
                                logger.info(
                                    f'OBW: {eval(sem_avg_results[2]) / 1000000:.3f} MHz, Total TX Power: {eval(sem_avg_results[3]):.2f} dBm')
                                # logger.info(f'SEM_AVER results: {sem_avg_results}')
                                self.command_cmw100_write(f'STOP:LTE:MEAS:MEV')
                                self.command_cmw100_query('*OPC?')
                                aclr_mod_current_results = aclr_mod_results = aclr_results + mod_results
                                logger.debug(aclr_mod_results)
                                aclr_mod_current_results.append(self.measure_current())
                                data[tx_level] = aclr_mod_current_results
                            logger.debug(data)
                            self.filename = self.tx_power_relative_test_export_excel(data, self.band_lte, self.bw_lte,
                                                                                     self.tx_freq_lte)
        self.set_test_end_lte()
        if plot:
            self.txp_aclr_evm_plot(self.filename, mode=0)
        else:
            pass

    def tx_level_sweep_progress_fr1(self, plot=True):
        """
        band_fr1:
        bw_fr1:
        tx_freq_fr1:
        rb_num:
        rb_start:
        mcs:
        pwr:
        rf_port:
        loss:
        tx_path:
        data {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('FR1', self.band_fr1, self.bw_fr1)
        tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq) for rx_freq in rx_freq_list]
        self.rx_freq_fr1 = rx_freq_list[1]
        self.tx_freq_fr1 = tx_freq_list[1]
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

        for mcs in wt.mcs_fr1:
            self.mcs_fr1 = mcs
            for script in wt.scripts:
                if script == 'GENERAL':
                    self.script = script
                    for rb_ftm in wt.rb_ftm_fr1:  # INNER, OUTER
                        self.rb_size_fr1, self.rb_start_fr1 = scripts.GENERAL_FR1[self.bw_fr1][self.scs][self.type_fr1][
                            self.rb_alloc_fr1_dict[rb_ftm]]  # INNER: 0, # OUTER: 1
                        self.rb_state = rb_ftm  # INNER, OUTER

                        tx_freq_select_list = []
                        for chan in self.chan:
                            if chan == 'L':
                                tx_freq_select_list.append(
                                    cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq_list[0]))
                            elif chan == 'M':
                                tx_freq_select_list.append(
                                    cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq_list[1]))
                            elif chan == 'H':
                                tx_freq_select_list.append(
                                    cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq_list[2]))

                        #  initial all before tx level prgress
                        for tx_freq_select in tx_freq_select_list:
                            self.tx_freq_fr1 = tx_freq_select
                            self.loss_tx = get_loss(self.tx_freq_fr1)
                            self.tx_set_fr1()
                            self.tx_power_relative_test_initial_fr1()

                            tx_range_list = wt.tx_level_range_list  # [tx_level_1, tx_level_2]

                            logger.info('----------TX Level Sweep progress---------')
                            logger.info(f'----------from {tx_range_list[0]} dBm to {tx_range_list[1]} dBm----------')

                            step = -1 if tx_range_list[0] > tx_range_list[1] else 1

                            #  following is real change tx level prgress

                            data = {}
                            for tx_level in range(tx_range_list[0], tx_range_list[1] + step, step):
                                self.tx_level = tx_level
                                logger.info(f'========Now Tx level = {self.tx_level} dBm========')
                                self.command(f'AT+NTXPWRLVLSET={self.tx_level}')
                                self.command_cmw100_write('CONF:NRS:MEAS:RFS:UMAR 10.000000')
                                self.command_cmw100_write(f'CONF:NRS:MEAS:RFS:ENP {self.tx_level + 5}.00')
                                self.command_cmw100_write(f'INIT:NRS:MEAS:MEV')
                                self.command_cmw100_query('*OPC?')
                                f_state = self.command_cmw100_query('FETC:NRS:MEAS:MEV:STAT?')
                                while f_state != 'RDY':
                                    f_state = self.command_cmw100_query('FETC:NRS:MEAS:MEV:STAT?')
                                    self.command_cmw100_query('*OPC?')
                                mod_results = self.command_cmw100_query(
                                    f'FETC:NRS:MEAS:MEV:MOD:AVER?')  # P3 is EVM, P15 is Ferr, P14 is IQ Offset
                                mod_results = mod_results.split(',')
                                mod_results = [mod_results[3], mod_results[15], mod_results[14]]
                                mod_results = [eval(m) for m in mod_results]
                                # logger.info(f'mod_results = {mod_results}')
                                logger.info(
                                    f'EVM: {mod_results[0]:.2f}, FREQ_ERR: {mod_results[1]:.2f}, IQ_OFFSET: {mod_results[2]:.2f}')
                                aclr_results = self.command_cmw100_query('FETC:NRS:MEAS:MEV:ACLR:AVER?')
                                aclr_results = aclr_results.split(',')[1:]
                                aclr_results = [eval(aclr) * -1 if eval(aclr) > 30 else eval(aclr) for aclr in
                                                aclr_results]  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2
                                logger.info(
                                    f'Power: {aclr_results[3]:.2f}, E-UTRA: [{aclr_results[2]:.2f}, {aclr_results[4]:.2f}], UTRA_1: [{aclr_results[1]:.2f}, {aclr_results[5]:.2f}], UTRA_2: [{aclr_results[0]:.2f}, {aclr_results[6]:.2f}]')
                                iem_results = self.command_cmw100_query('FETC:NRS:MEAS:MEV:IEM:MARG:AVER?')
                                iem_results = iem_results.split(',')
                                iem = f'{eval(iem_results[2]):.2f}' if iem_results[2] != 'INV' else 'INV'
                                logger.info(f'InBandEmissions Margin: {iem}dB')
                                # logger.info(f'IEM_MARG results: {iem_results}')
                                esfl_results = self.command_cmw100_query(f'FETC:NRS:MEAS:MEV:ESFL:EXTR?')
                                esfl_results = esfl_results.split(',')
                                ripple1 = f'{eval(esfl_results[2]):.2f}' if esfl_results[2] != 'NCAP' else 'NCAP'
                                ripple2 = f'{eval(esfl_results[3]):.2f}' if esfl_results[3] != 'NCAP' else 'NCAP'
                                logger.info(
                                    f'Equalize Spectrum Flatness: Ripple1:{ripple1} dBpp, Ripple2:{ripple2} dBpp')
                                time.sleep(0.2)
                                # logger.info(f'ESFL results: {esfl_results}')
                                sem_results = self.command_cmw100_query(f'FETC:NRS:MEAS:MEV:SEM:MARG:ALL?')
                                logger.info(f'SEM_MARG results: {sem_results}')
                                sem_avg_results = self.command_cmw100_query(f'FETC:NRS:MEAS:MEV:SEM:AVERage?')
                                sem_avg_results = sem_avg_results.split(',')
                                logger.info(
                                    f'OBW: {eval(sem_avg_results[2]) / 1000000:.3f} MHz, Total TX Power: {eval(sem_avg_results[3]):.2f} dBm')
                                # logger.info(f'SEM_AVER results: {sem_avg_results}')
                                self.command_cmw100_write(f'STOP:NRS:MEAS:MEV')
                                self.command_cmw100_query('*OPC?')
                                aclr_mod_current_results = aclr_mod_results = aclr_results + mod_results
                                logger.debug(aclr_mod_results)
                                aclr_mod_current_results.append(self.measure_current())
                                data[tx_level] = aclr_mod_current_results
                            logger.debug(data)
                            self.filename = self.tx_power_relative_test_export_excel(data, self.band_fr1, self.bw_fr1,
                                                                                     self.tx_freq_fr1)
        self.set_test_end_fr1()
        if plot:
            self.txp_aclr_evm_plot(self.filename, mode=0)
        else:
            pass

    def run_tx_level_sweep(self):
        for tech in wt.tech:
            if tech == 'LTE':
                self.tx_level_sweep_pipeline_lte()
            elif tech == 'FR1':
                self.tx_level_sweep_pipeline_fr1()
            elif tech == 'WCDMA':
                self.tx_level_sweep_pipeline_wcdma()
            elif tech == 'GSM':
                self.tx_level_sweep_pipeline_gsm()
