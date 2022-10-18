from connection_interface.connection_visa import VisaComport
from utils.log_init import log_set

logger = log_set()

class CMW:
    def __init__(self, equipment):
        self.cmw = VisaComport(equipment)

    def cmw_query(self, tcpip_command):
        tcpip_response = self.cmw.query(tcpip_command).strip()
        logger.info(f'TCPIP::<<{tcpip_command}')
        logger.info(f'TCPIP::>>{tcpip_response}')
        return tcpip_response

    def cmw_write(self, tcpip_command):
        self.cmw.write(tcpip_command)
        logger.info(f'TCPIP::<<{tcpip_command}')

    def set_gprf_if_filter(self, filter='BAND'):
        """
        Selects the IF filter type.
        Parameters:
        <FilterType> BANDpass | GAUSs | WCDMa | CDMA | TDSCdma
        BANDpass: bandpass filter
        GAUSs: Gaussian filter
        WCDMA: 3.84-MHz RRC filter for WCDMA TX tests
        CDMA: 1.2288-MHz channel filter for CDMA 2000 TX tests
        TDSCdma: 1.28-MHz RRC filter for TD-SCDMA TX tests
        """
        self.cmw_write(f'CONFigure:GPRF:MEAS:POWer:FILTer:TYPE {filter}')

    def set_gprf_bandpass_filter_bw(self, bw=10):
        """
        Selects the bandwidth for a bandpass filter.
        Parameters:
        <BandpassBW> numeric
        Only certain values can be configured, see Table 3-4. Other val-
        ues are rounded to the next allowed value.
        Default unit: Hz

        Supported values:
        Allowed kHz-values 1, 2, 3, 5, 10, 20, 30, 50, 100, 200, 300, 500 kHz
        Allowed MHz-values 1, 1.08, 2, 2.7, 3, 4.5, 5, 6, 9, 10, 12, 13.5, 17, 18, 20, 23, 28, 30, 38, 40, 45, 56,
        58, 60, 67, 80, 89, 112, 160 MHz
        The bold values require R&S CMW with TRX160
        *RST 300 kHz
        """
        self.cmw_write(f'CONFigure:GPRF:MEAS:POWer:FILTer:BANDpass:BWIDth {bw}MHz')

    def set_gprf_rf_input_path(self, port_tx=1):
        """
        Activates the standalone scenario and selects the RF input path for the measured RF
        signal.
        For possible connector and converter values, see Chapter 3.11.4, "Values for RF Path
        Selection", on page 393.
        Parameters:
        <RXConnector> RF connector for the input path
        <RFConverter> RX module for the input path
        """
        self.cmw_write(f'ROUTe:GPRF:MEAS:SCENario:SALone R1{port_tx} RX1')

    def set_gprf_power_count(self, count=2):
        """
        Specifies the statistic count of the measurement. The statistic count is equal to the
        number of measurement intervals per single shot.
        Parameters:
        <StatisticCount> numeric
        Number of measurement intervals
        Range:  1  to  100E+3
        *RST:  10
        """
        self.cmw_write(f'CONFigure:GPRF:MEAS:POWer:SCOunt {count}')

    def set_gprf_power_repetition(self, repetition='SINGleshot'):
        """
        Specifies the repetition mode of the measurement. The repetition mode specifies
        whether the measurement is stopped after a single shot or repeated continuously. Use
        CONFigure:..:MEAS<i>:...:SCOunt to determine the number of measurement
        intervals per single shot.
        Parameters:
        <Repetition> SINGleshot | CONTinuous
        SINGleshot: single-shot measurement
        CONTinuous: continuous measurement
        *RST:  SING
        """
        self.cmw_write(f'CONFigure:GPRF:MEAS:POWer:REPetition {repetition}')

    def set_gprf_power_list_mode(self, on_off='OFF'):
        """
        Enables or disables the list mode for the power measurement.
        Parameters:
        <EnableListMode> OFF | ON
        OFF: list mode off
        ON: list mode on
        *RST:  OFF
        """
        self.cmw_write(f'CONFigure:GPRF:MEAS:POWer:LIST {on_off}')

    def set_gprf_trigger_source(self, source='Free Run'):
        """
        Selects the source of the trigger events. Some values are always available. They are
        listed below. Depending on the installed options, additional values are available. You
        can query a list of all supported values via TRIGger:...:CATalog:SOURce?.
        Parameters:
        <Source> string
        'IF Power': IF power trigger
        'Free Run': free run (untriggered)
        *RST:  'Free Run'
        """
        self.cmw_write(f'TRIGger:GPRF:MEAS:POWer:SOURce {source}')

    def set_gprf_trigger_slope(self, slope='REDGe'):
        """
        Qualifies whether the trigger event is generated at the rising or at the falling edge of
        the trigger pulse (valid for external and power trigger sources).
        Parameters:
        <Event> REDGe | FEDGe
        REDGe: rising edge
        FEDGe: falling edge
        *RST:  REDG
        """
        # it also can use: <CONFigure:GPRF:MEAS:POWer:TRIGger:SLOPe>
        self.cmw_write(f'TRIGger:GPRF:MEAS:POWer:SLOPe {slope}')

    def set_gprf_trigger_step_length(self, length='576.9230769E-6'):
        """
        Sets the time between the beginning of two consecutive measurement lengths.
        Parameters:
        <StepLength> numeric
        Range:  <MeasLength>  to  1 s
        *RST:  576.9230769E-6 s
        Default unit: s
        """
        self.cmw_write(f'CONFigure:GPRF:MEAS:POWer:SLENgth {length}')

    def set_gprf_trigger_measure_length(self, length='576.9230769E-6'):
        """
        Sets the length of the evaluation interval used to measure a single set of current power
        results.
        The measurement length cannot be greater than the step length.
        Parameters:
        <MeasLength> numeric
        Default unit: s
        """
        self.cmw_write(f'CONFigure:GPRF:MEAS:POWer:MLENgth {length}')

    def preset_instrument(self):
        logger.info('----------Preset CMW----------')
        self.cmw_write('SYSTem:PRESet:ALL')
        self.cmw_query('SYSTem:BASE:OPTion:VERSion?  "CMW_NRSub6G_Meas"')
        self.cmw_write('CONFigure:FDCorrection:DEACtivate:ALL')
        self.cmw_write('CONFigure:BASE:FDCorrection:CTABle:DELete:ALL')
        self.cmw_query('*OPC?')
        self.cmw_query('SYST:ERR:ALL?')
        self.cmw_write('*RST')
        self.cmw_query('*OPC?')



    def set_gprf_tx_freq(self):
        self.command_cmw100_write(f'CONF:GPRF:MEAS:RFS:FREQ {self.tx_freq_fr1}KHz')

    def get_gprf_power(self):
        self.command_cmw100_write('INIT:GPRF:MEAS:POW')
        self.command_cmw100_query('*OPC?')
        f_state = self.command_cmw100_query('FETC:GPRF:MEAS:POW:STAT?')
        while f_state != 'RDY':
            f_state = self.command_cmw100_query('FETC:GPRF:MEAS:POW:STAT?')
            self.command_cmw100_query('*OPC?')
        power_average = round(eval(self.command_cmw100_query('FETC:GPRF:MEAS:POWer:AVER?'))[1], 2)
        logger.info(f'Get the GPRF power: {power_average}')
        return power_average

    def sig_gen_gsm(self):
        logger.info('----------Sig Gen----------')
        self.command_cmw100_query('SYSTem:BASE:OPTion:VERSion?  "CMW_NRSub6G_Meas"')
        self.command_cmw100_write('ROUT:GPRF:GEN:SCEN:SAL R118, TX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write('CONFigure:GPRF:GEN:CMWS:USAGe:TX:ALL R118, ON, ON, ON, ON, ON, ON, ON, ON')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write('SOUR:GPRF:GEN1:LIST OFF')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:RFS:EATT {self.loss_rx}')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:BBM ARB')
        waveform_2g = '2G_FINAL.wv'
        self.command_cmw100_write(f"SOUR:GPRF:GEN1:ARB:FILE 'C:\CMW100_WV\{waveform_2g}'")
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_query('SOUR:GPRF:GEN1:ARB:FILE?')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:RFS:FREQ {self.rx_freq_gsm}KHz')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:RFS:LEV {self.rx_level}')
        gprf_gen = self.command_cmw100_query('SOUR:GPRF:GEN1:STAT?')
        self.command_cmw100_query('*OPC?')
        if gprf_gen == 'OFF':
            self.command_cmw100_write('SOUR:GPRF:GEN1:STAT ON')
            self.command_cmw100_query('*OPC?')

    def sig_gen_wcdma(self):
        logger.info('----------Sig Gen----------')
        self.command_cmw100_query('SYSTem:BASE:OPTion:VERSion?  "CMW_NRSub6G_Meas"')
        self.command_cmw100_write('ROUT:GPRF:GEN:SCEN:SAL R118, TX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write('CONFigure:GPRF:GEN:CMWS:USAGe:TX:ALL R118, ON, ON, ON, ON, ON, ON, ON, ON')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write('SOUR:GPRF:GEN1:LIST OFF')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:RFS:EATT {self.loss_rx}')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:BBM ARB')
        waveform_3g = '3G_CAL_FINAL.wv'
        self.command_cmw100_write(f"SOUR:GPRF:GEN1:ARB:FILE 'C:\CMW100_WV\{waveform_3g}'")
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_query('SOUR:GPRF:GEN1:ARB:FILE?')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:RFS:FREQ {self.rx_freq_wcdma}KHz')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:RFS:LEV {self.rx_level}')
        gprf_gen = self.command_cmw100_query('SOUR:GPRF:GEN1:STAT?')
        self.command_cmw100_query('*OPC?')
        if gprf_gen == 'OFF':
            self.command_cmw100_write('SOUR:GPRF:GEN1:STAT ON')
            self.command_cmw100_query('*OPC?')

    def sig_gen_lte(self):
        logger.info('----------Sig Gen----------')
        self.command_cmw100_query('SYSTem:BASE:OPTion:VERSion?  "CMW_NRSub6G_Meas"')
        self.command_cmw100_write('ROUT:GPRF:GEN:SCEN:SAL R118, TX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write('CONFigure:GPRF:GEN:CMWS:USAGe:TX:ALL R118, ON, ON, ON, ON, ON, ON, ON, ON')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write('SOUR:GPRF:GEN1:LIST OFF')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:RFS:EATT {self.loss_rx}')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write('SOUR:GPRF:GEN1:BBM ARB')
        self.command_cmw100_query('*OPC?')
        self.band_lte = int(self.band_lte)
        if self.band_lte in [34, 38, 39, 40, 41, 42, 48]:
            self.command_cmw100_write(
                f"SOUR:GPRF:GEN1:ARB:FILE 'C:\CMW100_WV\SMU_Channel_CC0_RxAnt0_RF_Verification_10M_SIMO_01.wv'")
        else:
            # self.command_cmw100_write(f"SOUR:GPRF:GEN1:ARB:FILE 'C:\CMW100_WV\SMU_NodeB_Ant0_FRC_10MHz.wv'")
            bw_lte = '1p4' if self.bw_lte == 1.4 else '03' if self.bw_lte == 3 else self.bw_lte
            self.command_cmw100_write(f"SOUR:GPRF:GEN1:ARB:FILE 'C:\CMW100_WV\SMU_NodeB_Ant0_FRC_{bw_lte}MHz.wv'")
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_query('SOUR:GPRF:GEN1:ARB:FILE?')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:RFS:FREQ {self.rx_freq_lte}KHz')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:RFS:LEV {self.rx_level}')
        gprf_gen = self.command_cmw100_query('SOUR:GPRF:GEN1:STAT?')
        self.command_cmw100_query('*OPC?')
        if gprf_gen == 'OFF':
            self.command_cmw100_write('SOUR:GPRF:GEN1:STAT ON')
            self.command_cmw100_query('*OPC?')

    def sig_gen_fr1(self):
        """
        scs: FDD is forced to 15KHz and TDD is to be 30KHz
        """
        logger.info('----------Sig Gen----------')
        self.band_fr1 = int(self.band_fr1)
        scs = 1 if self.band_fr1 in [34, 38, 39, 40, 41, 42, 48, 77, 78,
                                     79] else 0  # for now FDD is forced to 15KHz and TDD is to be 30KHz
        scs = 15 * (2 ** scs)
        mcs_fr1_wv = 4
        self.scs = scs
        self.command_cmw100_query('SYSTem:BASE:OPTion:VERSion?  "CMW_NRSub6G_Meas"')
        self.command_cmw100_write('ROUT:GPRF:GEN:SCEN:SAL R118, TX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write('CONFigure:GPRF:GEN:CMWS:USAGe:TX:ALL R118, ON, ON, ON, ON, ON, ON, ON, ON')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write('SOUR:GPRF:GEN1:LIST OFF')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:RFS:EATT {self.loss_rx}')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write('SOUR:GPRF:GEN1:BBM ARB')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write('CONFigure:NRSub:MEAS:ULDL:PERiodicity MS10')
        self.command_cmw100_query('*OPC?')
        if self.band_fr1 in [34, 38, 39, 40, 41, 42, 48, 77, 78, 79]:
            self.command_cmw100_write(
                f"SOUR:GPRF:GEN1:ARB:FILE 'C:\CMW100_WV\SMU_NodeB_NR_Ant0_NR_{self.bw_fr1}MHz_SCS{scs}_TDD_Sens_MCS{mcs_fr1_wv}_rescale.wv'")
        else:
            self.command_cmw100_write(
                f"SOUR:GPRF:GEN1:ARB:FILE 'C:\CMW100_WV\SMU_NodeB_NR_Ant0_LTE_NR_{self.bw_fr1}MHz_SCS{scs}_FDD_Sens_MCS_{mcs_fr1_wv}.wv'")
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_query('SOUR:GPRF:GEN1:ARB:FILE?')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:RFS:FREQ {self.rx_freq_fr1}KHz')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:RFS:LEV {self.rx_level}')
        gprf_gen = self.command_cmw100_query('SOUR:GPRF:GEN1:STAT?')
        self.command_cmw100_query('*OPC?')
        if gprf_gen == 'OFF':
            self.command_cmw100_write('SOUR:GPRF:GEN1:STAT ON')
            self.command_cmw100_query('*OPC?')

    def tx_monitor_lte(self):
        logger.info('---------Tx Monitor----------')
        # self.sig_gen_lte()
        self.command_cmw100_write(f'CONFigure:LTE:MEAS:MEV:RES:PMONitor ON')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f"TRIG:LTE:MEAS:MEV:SOUR 'GPRF Gen1: Restart Marker'")
        self.command_cmw100_write(f'CONFigure:LTE:MEAS:MEValuation:MSLot ALL')
        self.command_cmw100_write(f'TRIG:LTE:MEAS:MEV:THR -20.0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:REP SING')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MOEX ON')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:CPR NORM')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MSUB 2, 10, 0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:AUTO ON')
        mode = 'TDD' if self.band_lte in [38, 39, 40, 41, 42, 48] else 'FDD'
        self.command_cmw100_write(f'CONF:LTE:MEAS:DMODe {mode}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:BAND OB{self.band_lte}')
        rb = f'0{self.bw_lte * 10}' if self.bw_lte < 10 else f'{self.bw_lte * 10}'
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:CBAN B{rb}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MOD:MSCH {self.mcs_lte}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:FREQ {self.tx_freq_lte}KHz')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:EATT {self.loss_tx}')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'ROUT:GPRF:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'ROUT:LTE:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:UMAR 10.000000')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:ENP {self.tx_level}.00')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'INIT:LTE:MEAS:MEV')
        f_state = self.command_cmw100_query('FETC:LTE:MEAS:MEV:STAT?')
        while f_state != 'RDY':
            f_state = self.command_cmw100_query('FETC:LTE:MEAS:MEV:STAT?')
            self.command_cmw100_query('*OPC?')
        self.command_cmw100_query('*OPC?')
        power_results = self.command_cmw100_query(f'FETCh:LTE:MEAS:MEV:PMON:AVER?')
        power = power_results.strip().split(',')[2]
        logger.info(f'LTE power by Tx monitor: {round(eval(power), 2)}')
        return round(eval(power), 2)

    def tx_measure_gsm(self):
        logger.info('---------Tx Measure----------')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:SCO:PVT 5')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:SCO:MOD 5')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:SCO:SMOD 5')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:SCO:SSW 5')
        self.command_cmw100_write(f'CONF:GSM:MEAS:SCEN:ACT STAN')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'ROUT:GSM:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
        self.command_cmw100_write(f'CONF:GSM:MEAS:RFS:EATT {self.loss_tx}')
        self.command_cmw100_write(f'CONF:GSM:MEAS:RFS:UMAR 10.00')
        self.command_cmw100_write(f"TRIG:GSM:MEAS:MEV:SOUR 'Power'")
        self.command_cmw100_write(f'TRIG:GSM:MEAS:MEV:THR -20.0')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:REP SING')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:RES:ALL ON, ON, ON, ON, ON, ON, ON, ON, ON, ON, OFF, ON')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(
            f'CONF:GSM:MEAS:MEV:SMOD:OFR 100KHZ,200KHZ,250KHZ,400KHZ,600KHZ,800KHZ,1600KHZ,1800KHZ,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:SMOD:EAR ON,6,45,ON,90,129')
        self.command_cmw100_write(
            f'CONF:GSM:MEAS:MEV:SSW:OFR 400KHZ,600KHZ,1200KHZ,1800KHZ,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
        self.command_cmw100_query('SYST:ERR:ALL?')
        self.command_cmw100_write(f'CONF:GSM:MEAS:BAND {self.band_tx_meas_dict_gsm[self.band_gsm]}')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:GSM:MEAS:CHAN {self.rx_chan_gsm}')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:MOEX ON')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:TSEQ TSC{self.tsc}')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:MVI {",".join([self.mod_gsm] * 8)}')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:GSM:MEAS:MEV:MSL 0,1,0')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_query('SYST:ERR:ALL?')
        self.power_init_gsm()
        self.command_cmw100_write(f'CONF:GSM:MEAS:RFS:ENP {self.pwr_init_gsm}')
        mod_results = self.command_cmw100_query(
            f'READ:GSM:MEAS:MEV:MOD:AVER?')  # P12 is Power, P6 is phase_err_rms, P2 is EVM_rms, P10 is ferr
        mod_results = mod_results.split(',')
        mod_results = [mod_results[12], mod_results[6], mod_results[7],
                       mod_results[10]]  # power, phase_err_rms, phase_peak, ferr
        mod_results = [round(eval(m), 2) for m in mod_results]
        logger.info(
            f'Power: {mod_results[0]:.2f}, Phase_err_rms: {mod_results[1]:.2f}, Phase_peak: {mod_results[2]:.2f}, Ferr: {mod_results[3]:.2f}')
        self.command_cmw100_write(f'INIT:GSM:MEAS:MEV')
        self.command_cmw100_write(f'*OPC?')
        self.command_cmw100_write(f'CONF:GSM:MEAS:RFS:ENP {mod_results[0]:.2f}')
        f_state = self.command_cmw100_query(f'FETC:GSM:MEAS:MEV:STAT?')
        while f_state != 'RDY':
            time.sleep(0.2)
            f_state = self.command_cmw100_query('FETC:GSM:MEAS:MEV:STAT?')
            self.command_cmw100_query('*OPC?')
        pvt = self.command_cmw100_query(f'FETC:GSM:MEAS:MEV:PVT:AVER:SVEC?')  # PVT, but it is of no use
        orfs_mod = self.command_cmw100_query(f'FETC:GSM:MEAS:MEV:SMOD:FREQ?')  # MOD_ORFS
        orfs_mod = [round(eval(orfs_mod), 2) for orfs_mod in orfs_mod.split(',')[13:29]]
        orfs_mod = [
            orfs_mod[6],  # -200 KHz
            orfs_mod[10],  # 200 KHz
            orfs_mod[4],  # -400 KHz
            orfs_mod[12],  # 400 KHz
            orfs_mod[3],  # -600 KHz
            orfs_mod[13],  # 600 KHz
        ]
        logger.info(f'ORFS_MOD_-200KHz: {orfs_mod[0]}, ORFS_MOD_200KHz: {orfs_mod[1]}')
        logger.info(f'ORFS_MOD_-400KHz: {orfs_mod[2]}, ORFS_MOD_400KHz: {orfs_mod[3]}')
        logger.info(f'ORFS_MOD_-600KHz: {orfs_mod[4]}, ORFS_MOD_600KHz: {orfs_mod[5]}')
        orfs_sw = self.command_cmw100_query(f'FETC:GSM:MEAS:MEV:SSW:FREQ?')  # SW_ORFS
        orfs_sw = [round(eval(orfs_sw), 2) for orfs_sw in orfs_sw.split(',')[17:25]]
        orfs_sw = [
            orfs_sw[3],  # -400 KHz
            orfs_sw[5],  # 400 KHz
            orfs_sw[2],  # -600 KHz
            orfs_sw[6],  # 600 KHz
            orfs_sw[1],  # -1200 KHz
            orfs_sw[7],  # 1200 KHz
        ]
        logger.info(f'ORFS_SW_-400KHz: {orfs_sw[0]}, ORFS_SW_400KHz: {orfs_sw[1]}')
        logger.info(f'ORFS_SW_-600KHz: {orfs_sw[2]}, ORFS_SW_600KHz: {orfs_sw[3]}')
        logger.info(f'ORFS_SW_-1200KHz: {orfs_sw[4]}, ORFS_SW_1200KHz: {orfs_sw[5]}')
        self.command_cmw100_write(f'STOP:WCDM:MEAS:MEV')
        self.command_cmw100_query('*OPC?')

        return mod_results + orfs_mod + orfs_sw  # [0~3] + [4~10] + [11~17]

    def tx_measure_wcdma(self):
        logger.info('---------Tx Measure----------')
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
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_query('SYST:ERR:ALL?')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:BAND OB{self.band_wcdma}')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:RFS:FREQ {self.tx_chan_wcdma} CH')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:UES:DPDC ON')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:UES:SFOR 0')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:UES:SCOD 13496235')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:UES:ULC WCDM')
        self.command_cmw100_query('SYST:ERR:ALL?')
        self.command_cmw100_write(f'CONF:WCDMA:MEAS:RFS:UMAR 10.00')
        self.command_cmw100_write(f'CONF:WCDM:MEAS:RFS:ENP {self.tx_level + 5}')
        mod_results = self.command_cmw100_query(
            f'READ:WCDM:MEAS:MEV:MOD:AVER?')  # P1 is EVM, P4 is Ferr, P8 is IQ Offset
        mod_results = mod_results.split(',')
        mod_results = [mod_results[1], mod_results[4], mod_results[8]]
        mod_results = [eval(m) for m in mod_results]
        logger.info(f'EVM: {mod_results[0]:.2f}, FREQ_ERR: {mod_results[1]:.2f}, IQ_OFFSET: {mod_results[2]:.2f}')
        self.command_cmw100_write(f'INIT:WCDM:MEAS:MEV')
        self.command_cmw100_write(f'*OPC?')
        f_state = self.command_cmw100_query(f'FETC:WCDM:MEAS:MEV:STAT?')
        while f_state != 'RDY':
            time.sleep(0.2)
            f_state = self.command_cmw100_query('FETC:WCDM:MEAS:MEV:STAT?')
            self.command_cmw100_query('*OPC?')
        spectrum_results = self.command_cmw100_query(
            f'FETC:WCDM:MEAS:MEV:SPEC:AVER?')  # P1: Power, P2: ACLR_-2, P3: ACLR_-1, P4:ACLR_+1, P5:ACLR_+2, P6:OBW
        spectrum_results = spectrum_results.split(',')
        spectrum_results = [
            round(eval(spectrum_results[1]), 2),
            round(eval(spectrum_results[3]) - eval(spectrum_results[1]), 2),
            round(eval(spectrum_results[4]) - eval(spectrum_results[1]), 2),
            round(eval(spectrum_results[2]) - eval(spectrum_results[1]), 2),
            round(eval(spectrum_results[5]) - eval(spectrum_results[1]), 2),
            round(eval(spectrum_results[6]) / 1000000, 2)
        ]
        logger.info(
            f'Power: {spectrum_results[0]:.2f}, ACLR_-1: {spectrum_results[2]:.2f}, ACLR_1: {spectrum_results[3]:.2f}, ACLR_-2: {spectrum_results[1]:.2f}, ACLR_+2: {spectrum_results[4]:.2f}, OBW: {spectrum_results[5]:.2f}MHz')
        self.command_cmw100_write(f'STOP:WCDM:MEAS:MEV')
        self.command_cmw100_query('*OPC?')

        return spectrum_results + mod_results

    def tx_measure_lte(self):
        logger.info('---------Tx Measure----------')
        mode = 'TDD' if self.band_lte in [38, 39, 40, 41, 42, 48] else 'FDD'
        self.command_cmw100_write(f'CONF:LTE:MEAS:DMODe {mode}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:BAND OB{self.band_lte}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:FREQ {self.tx_freq_lte}KHz')
        self.command_cmw100_query('*OPC?')
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
        self.command_cmw100_query('SYST:ERR:ALL?')
        self.command_cmw100_write(f'CONFigure:LTE:MEAS:MEValuation:MSLot ALL')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:UMAR 10.000000')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:ENP {self.tx_level + 5}.00')
        self.command_cmw100_write(f'ROUT:LTE:MEAS:SCEN:SAL R11, RX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:UMAR 10.000000')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:AUTO ON')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:SCO:MOD 5')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:SCO:SPEC:ACLR 5')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:SCO:SPEC:SEM 5')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f"TRIG:LTE:MEAS:MEV:SOUR 'GPRF Gen1: Restart Marker'")
        self.command_cmw100_write(f'TRIG:LTE:MEAS:MEV:THR -20.0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:REP SING')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RES:ALL ON, ON, ON, ON, ON, ON, ON, ON, ON, ON')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MSUB 2, 10, 0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:SCEN:ACT SAL')
        self.command_cmw100_query('SYST:ERR:ALL?')
        self.command_cmw100_write(f'ROUT:GPRF:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'ROUT:LTE:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:EATT {self.loss_tx}')
        self.command_cmw100_query('*OPC?')
        time.sleep(0.2)
        mod_results = self.command_cmw100_query(
            'READ:LTE:MEAS:MEV:MOD:AVER?')  # P3 is EVM, P15 is Ferr, P14 is IQ Offset
        mod_results = mod_results.split(',')
        mod_results = [mod_results[3], mod_results[15], mod_results[14]]
        mod_results = [eval(m) for m in mod_results]
        logger.info(f'EVM: {mod_results[0]:.2f}, FREQ_ERR: {mod_results[1]:.2f}, IQ_OFFSET: {mod_results[2]:.2f}')
        self.command_cmw100_write(f'INIT:LTE:MEAS:MEV')
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
        ripple1 = round(eval(esfl_results[2]), 2) if esfl_results[2] != 'NCAP' else esfl_results[2]
        ripple2 = round(eval(esfl_results[3]), 2) if esfl_results[3] != 'NCAP' else esfl_results[3]
        logger.info(f'Equalize Spectrum Flatness: Ripple1:{ripple1} dBpp, Ripple2:{ripple2} dBpp')
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

        logger.debug(aclr_results + mod_results)
        return aclr_results + mod_results  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET

    def tx_measure_fr1(self):
        scs = 1 if self.band_fr1 in [34, 38, 39, 40, 41, 42, 48, 75, 76, 77, 78,
                                     79] else 0  # for now FDD is forced to 15KHz and TDD is to be 30KHz
        scs = 15 * (2 ** scs)  # for now TDD only use 30KHz, FDD only use 15KHz
        logger.info('---------Tx Measure----------')
        mode = "TDD" if self.band_fr1 in [34, 38, 39, 40, 41, 42, 48, 75, 76, 77, 78, 79] else "FDD"
        self.command_cmw100_query(f'SYSTem:BASE:OPTion:VERSion?  "CMW_NRSub6G_Meas"')
        self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:DMODe {mode}')
        self.command_cmw100_write(f'CONF:NRS:MEAS:BAND OB{self.band_fr1}')
        self.command_cmw100_write(f'CONF:NRS:MEAS:RFS:FREQ {self.tx_freq_fr1}KHz')
        self.command_cmw100_query(f'*OPC?')
        self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:PLC 0')
        self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:MOEX ON')
        bw = f'00{self.bw_fr1}' if self.bw_fr1 < 10 else f'0{self.bw_fr1}' if 10 <= self.bw_fr1 < 100 else self.bw_fr1
        self.command_cmw100_write(f'CONF:NRS:MEAS:MEV:BWC S{scs}K, B{bw}')
        self.command_cmw100_write(
            f'CONF:NRS:MEAS:MEV:LIM:SEM:AREA1:CBAN{self.bw_fr1} ON,0.015MHz,0.0985MHz,{round(-13.5 - 10 * math.log10(self.bw_fr1 / 5), 1)},K030')
        self.command_cmw100_write(
            f'CONF:NRS:MEAS:MEV:LIM:SEM:AREA2:CBAN{self.bw_fr1} ON,1.5MHz,4.5MHz,-8.5,M1')
        self.command_cmw100_write(
            f'CONF:NRS:MEAS:MEV:LIM:SEM:AREA3:CBAN{self.bw_fr1} ON,5.5MHz,{round(-0.5 + self.bw_fr1, 1)}MHz,-11.5,M1')
        self.command_cmw100_write(
            f'CONF:NRS:MEAS:MEV:LIM:SEM:AREA4:CBAN{self.bw_fr1} ON,{round(0.5 + self.bw_fr1, 1)}MHz,{round(4.5 + self.bw_fr1, 1)}MHz,-23.5,M1')
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
        self.command_cmw100_write(f'CONF:NRS:MEAS:RFS:UMAR 10.000000')
        self.command_cmw100_write(f'CONF:NRS:MEAS:RFS:ENP {self.tx_level + 5}.00')
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
        self.command_cmw100_write(f'ROUT:GPRF:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
        self.command_cmw100_query(f'*OPC?')
        self.command_cmw100_write(f'ROUT:NRS:MEAS:SCEN:SAL R1{self.port_tx}, RX1')
        self.command_cmw100_query(f'*OPC?')
        self.command_cmw100_write(f'INIT:NRS:MEAS:MEV')
        self.command_cmw100_query(f'*OPC?')
        f_state = self.command_cmw100_query(f'FETC:NRS:MEAS:MEV:STAT?')
        while f_state != 'RDY':
            f_state = self.command_cmw100_query(f'FETC:NRS:MEAS:MEV:STAT?')
            self.command_cmw100_query('*OPC?')
        mod_results = self.command_cmw100_query(
            'FETC:NRS:MEAS:MEV:MOD:AVER?')  # P3 is EVM, P15 is Ferr, P14 is IQ Offset
        mod_results = mod_results.split(',')
        mod_results = [mod_results[3], mod_results[15], mod_results[14]]
        mod_results = [eval(m) for m in mod_results]
        logger.info(f'EVM: {mod_results[0]:.2f}, FREQ_ERR: {mod_results[1]:.2f}, IQ_OFFSET: {mod_results[2]:.2f}')
        aclr_results = self.command_cmw100_query('FETC:NRS:MEAS:MEV:ACLR:AVER?')
        aclr_results = aclr_results.split(',')[1:]
        aclr_results = [eval(aclr) * -1 if eval(aclr) > 30 else eval(aclr) for aclr in
                        aclr_results]  # UTRA2(-), UTRA1(-), NR(-), TxP, NR(+), UTRA1(+), UTRA2(+)
        logger.info(
            f'Power: {aclr_results[3]:.2f}, E-UTRA: [{aclr_results[2]:.2f}, {aclr_results[4]:.2f}], UTRA_1: [{aclr_results[1]:.2f}, {aclr_results[5]:.2f}], UTRA_2: [{aclr_results[0]:.2f}, {aclr_results[6]:.2f}]')
        iem_results = self.command_cmw100_query('FETC:NRS:MEAS:MEV:IEM:MARG:AVER?')
        iem_results = iem_results.split(',')
        iem = f'{eval(iem_results[2]):.2f}' if iem_results[2] != 'INV' else 'INV'
        logger.info(f'InBandEmissions Margin: {iem}dB')
        # logger.info(f'IEM_MARG results: {iem_results}')
        esfl_results = self.command_cmw100_query(f'FETC:NRS:MEAS:MEV:ESFL:EXTR?')
        esfl_results = esfl_results.split(',')
        ripple1 = round(eval(esfl_results[2]), 2) if esfl_results[2] != 'NCAP' else esfl_results[2]
        ripple2 = round(eval(esfl_results[3]), 2) if esfl_results[3] != 'NCAP' else esfl_results[3]
        logger.info(f'Equalize Spectrum Flatness: Ripple1:{ripple1} dBpp, Ripple2:{ripple2} dBpp')
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

        logger.debug(aclr_results + mod_results)
        return aclr_results + mod_results  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET

    def set_rx_level(self):
        logger.info(f'==========Search: {self.rx_level} dBm==========')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:RFS:LEV {self.rx_level}')
        # self.command_cmw100_query('*OPC?')
