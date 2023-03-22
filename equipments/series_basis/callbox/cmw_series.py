from connection_interface.connection_visa import VisaComport
from utils.log_init import log_set

logger = log_set('Cmw_series')


class CMW:
    def __init__(self, equipment):
        self.cmw = VisaComport(equipment)

    def cmw_query(self, tcpip_command):
        tcpip_response = self.cmw.query(tcpip_command).strip()
        logger.info(f'TCPIP::<<{tcpip_command}')
        logger.info(f'TCPIP::>>{tcpip_response}')
        return tcpip_response

    def cmw_query_2(self, command):
        response = self.cmw.query_2(command)
        return response

    def cmw_write(self, tcpip_command):
        self.cmw.write(tcpip_command)
        logger.info(f'TCPIP::<<{tcpip_command}')

    def system_preset_all(self):
        """
        A PRESet sets the parameters of all sub-instruments and the base settings to default
        values suitable for local/manual interaction. A RESet sets them to default values suitable
        for remote operation.
        Example: SYSTem:PRESet:ALL
        Force the entire R&S CMW500 to a preset state optimized for
        manual operation
        """
        self.cmw_write(f'SYSTem:PRESet:ALL')

    def system_base_option_version_query(self, application='nonsense'):
        """
        Returns version information for installed software packages. The "Setup" dialog provides
        this information in section "SW/HW-Equipment > Installed Software".
        You can either query a list of all installed packages and their versions or you can query
        the version of a single package specified via parameter <Application>:
        ● <Application> specified: A string is returned, indicating the version of the <Application>.
          If the specified <Application> is unknown / not installed, "0" is returned.
        ● <Application> omitted: A string is returned, containing a list of all installed software
        packages and their version in the format "<PackageName1>,<Version1>;<PackageName2>,<Version2>;..."
        Query parameters:
        <Application> String selecting the software package for which the version shall
        be queried
        Return values:
        <SoftwareVersion> String containing a single version or a list of applications and versions
        Example: SYSTem:BASE:OPTion:VERSion?
        Returns a list of all packages, for example
        "CMW BASE,V3.0.10;CMW GPRF Gen,V3.0.10;CMW GPRF
        Meas,V3.0.10"
        Example: SYSTem:BASE:OPTion:VERSion? "CMW GPRF Gen"
        Returns the version of the GPRF generator software, for example
        "V3.0.10"
        Example: SYSTem:BASE:OPTion:VERSion? "nonsense"
        Returns "0"
        Usage: Query only
        """
        if application == "CMW_NRSub6G_Meas":
            message = 'SYSTem:BASE:OPTion:VERSion? "CMW_NRSub6G_Meas"'
        else:
            message = 'SYSTem:BASE:OPTion:VERSion? "nonesense"'
        return self.cmw_query(message)

    def system_err_all_query(self):
        """
        To show upw the system if there is error message
        """
        return self.cmw_query('SYST:ERR:ALL?')

    def set_fd_correction_deactivate_all(self):
        """
        it might be FreqCorrection commands group definition
        from: https://rscmwbase.readthedocs.io/en/latest/Configure_FreqCorrection.html?highlight=fdcorrection
        """
        self.cmw_write('CONFigure:FDCorrection:DEACtivate:ALL')

    def set_fd_correction_ctable_delete(self):
        """
        Deletes all correction tables for the addressed sub-instrument from the hard disk
        """
        self.cmw_write('CONFigure:BASE:FDCorrection:CTABle:DELete:ALL')

    def set_if_filter_gprf(self, flt='BAND'):
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
        self.cmw_write(f'CONFigure:GPRF:MEASurement:POWer:FILTer:TYPE {flt}')

    def set_bandpass_filter_bw_gprf(self, bw=10):
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
        self.cmw_write(f'CONFigure:GPRF:MEASurement:POWer:FILTer:BANDpass:BWIDth {bw}MHz')

    def set_rf_tx_port_gprf(self, port_tx=1):
        """
        Activates the standalone scenario and selects the RF input path for the measured RF
        signal.
        For possible connector and converter values, see Chapter 3.11.4, "Values for RF Path
        Selection", on page 393.
        Parameters:
        <RXConnector> RF connector for the input path
        <RFConverter> RX module for the input path
        """
        self.cmw_write(f'ROUTe:GPRF:MEASurement:SCENario:SALone R1{port_tx}, RX1')

    def set_rf_tx_port_fr1(self, port_tx=1):
        """
        Activates the standalone scenario and selects the RF input path for the measured RF
        signal.
        For possible connector and converter values, see Chapter 6.1.4, "Values for RF Path
        Selection", on page 99.
        Parameters:
        <RXConnector> RF connector for the input path
        <RFConverter> RX module for the input path
        """
        self.cmw_write(f'ROUTe:NRSub:MEASurement:SCENario:SALone R1{port_tx}, RX1')

    def set_rf_tx_port_lte(self, port_tx=1):
        """
        Activates the standalone scenario and selects the RF input path for the measured RF
        signal.
        For possible connector and converter values, see Chapter 5.5.1.4, "Values for RF Path
        Selection", on page 1019.
        Parameters:
        <RXConnector> RF connector for the input path
        <RFConverter> RX module for the input path
        """
        self.cmw_write(f'ROUTe:LTE:MEASurement:SCENario:SALone R1{port_tx}, RX1')

    def set_rf_tx_port_wcdma(self, port_tx=1):
        """
        Activates the standalone scenario and selects the RF input path for the measured RF
        signal.
        For possible connector and converter values, see Chapter 5.5.1.4, "Values for RF Path
        Selection", on page 1019.
        Parameters:
        <RXConnector> RF connector for the input path
        <RFConverter> RX module for the input path
        """
        self.cmw_write(f'ROUTe:WCDMa:MEASurement:SCENario:SALone R1{port_tx}, RX1')

    def set_rf_tx_port_gsm(self, port_tx=1):
        """
        Activates the standalone scenario and selects the RF input path for the measured RF
        signal.
        For possible connector and converter values, see Chapter 5.5.1.4, "Values for RF Path
        Selection", on page 1019.
        Parameters:
        <RXConnector> RF connector for the input path
        <RFConverter> RX module for the input path
        """
        self.cmw_write(f'ROUTe:GSM:MEASurement:SCENario:SALone R1{port_tx}, RX1')

    def set_rf_rx_port_gprf(self, port_rx=18):
        """
        Activates the standalone scenario and selects the output path for the generated RF
        signal.
        For possible connector and converter values, see Chapter 2.5.1.2, "Values for Signal
        Path Selection", on page 65.
        Parameters:
        <TXConnector> RF connector for the output path
        <RFConverter> TX module for the output path
        """
        self.cmw_write(f'ROUTe:GPRF:GENerator:SCENario:SALone R1{port_rx}, TX1')

    def set_rf_rx_port_fr1(self, port_rx=18):
        """
        Activates the standalone scenario and selects the output path for the generated RF
        signal.
        For possible connector and converter values, see Chapter 2.5.1.2, "Values for Signal
        Path Selection", on page 65.
        Parameters:
        <TXConnector> RF connector for the output path
        <RFConverter> TX module for the output path
        """
        self.cmw_write(f'ROUTe:NRsub:GENerator:SCENario:SALone R1{port_rx}, TX1')

    def set_rf_rx_port_lte(self, port_rx=18):
        """
        Activates the standalone scenario and selects the output path for the generated RF
        signal.
        For possible connector and converter values, see Chapter 2.5.1.2, "Values for Signal
        Path Selection", on page 65.
        Parameters:
        <TXConnector> RF connector for the output path
        <RFConverter> TX module for the output path
        """
        self.cmw_write(f'ROUTe:LTE:GENerator:SCENario:SALone R1{port_rx}, TX1')

    def set_rf_rx_port_wcdma(self, port_rx=18):
        """
        Activates the standalone scenario and selects the output path for the generated RF
        signal.
        For possible connector and converter values, see Chapter 2.5.1.2, "Values for Signal
        Path Selection", on page 65.
        Parameters:
        <TXConnector> RF connector for the output path
        <RFConverter> TX module for the output path
        """
        self.cmw_write(f'ROUTe:WCDMa:GENerator:SCENario:SALone R1{port_rx}, TX1')

    def set_power_count_gprf(self, count=2):
        """
        Specifies the statistic count of the measurement. The statistic count is equal to the
        number of measurement intervals per single shot.
        Parameters:
        <StatisticCount> numeric
        Number of measurement intervals
        Range:  1  to  100E+3
        *RST:  10
        """
        self.cmw_write(f'CONFigure:GPRF:MEASurement:POWer:SCOunt {count}')

    def set_repetition_gprf(self, repetition='SINGleshot'):
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
        self.cmw_write(f'CONFigure:GPRF:MEASurement:POWer:REPetition {repetition}')

    def set_repetition_fr1(self, rep='SING'):
        """
        Specifies the repetition mode of the measurement. The repetition mode specifies
        whether the measurement is stopped after a single shot or repeated continuously. Use
        CONFigure:..:MEAS<i>:...:SCOunt to determine the number of measurement
        intervals per single shot.
        Parameters:
        <Repetition> SINGleshot | CONTinuous
        SINGleshot: Single-shot measurement
        CONTinuous: Continuous measurement
        *RST:  SING
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:REPetition {rep}')

    def set_repetition_lte(self, rep='SING'):
        """
        Specifies the repetition mode of the measurement. The repetition mode specifies
        whether the measurement is stopped after a single shot or repeated continuously. Use
        CONFigure:..:MEAS<i>:...:SCOunt to determine the number of measurement
        intervals per single shot.
        Parameters:
        <Repetition> SINGleshot | CONTinuous
        SINGleshot: Single-shot measurement
        CONTinuous: Continuous measurement
        *RST:  SING
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:REPetition {rep}')

    def set_repetition_wcdma(self, rep='SING'):
        """
        Specifies the repetition mode of the measurement. The repetition mode specifies
        whether the measurement is stopped after a single shot or repeated continuously. Use
        CONFigure:..:MEAS<i>:...:SCOunt to determine the number of measurement
        intervals per single shot.
        Parameters:
        <Repetition> SINGleshot | CONTinuous
        SINGleshot: Single-shot measurement
        CONTinuous: Continuous measurement
        *RST:  SING
        """
        self.cmw_write(f'CONFigure:WCDMa:MEASurement:MEValuation:REPetition {rep}')

    def set_repetition_gsm(self, rep='SING'):
        """
        Specifies the repetition mode of the measurement. The repetition mode specifies
        whether the measurement is stopped after a single shot or repeated continuously. Use
        CONFigure:..:MEAS<i>:...:SCOunt to determine the number of measurement
        intervals per single shot.
        Parameters:
        <Repetition> SINGleshot | CONTinuous
        SINGleshot: Single-shot measurement
        CONTinuous: Continuous measurement
        *RST:  SING
        """
        self.cmw_write(f'CONFigure:GSM:MEASurement:MEValuation:REPetition {rep}')

    def set_power_list_mode_gprf(self, on_off='OFF'):
        """
        Enables or disables the list mode for the power measurement.
        Parameters:
        <EnableListMode> OFF | ON
        OFF: list mode off
        ON: list mode on
        *RST:  OFF
        """
        self.cmw_write(f'CONFigure:GPRF:MEASurement:POWer:LIST {on_off}')

    def set_generator_list_mode_gprf(self, on_off='OFF'):
        """
        Enables or disables the list mode of the RF generator.
        Parameters:
        <EnableListMode> ON | OFF
        ON: List mode enabled
        OFF: List mode disabled (constant-frequency generator)
        *RST:  OFF
        """
        self.cmw_write(f'SOURce:GPRF:GENerator1:LIST {on_off}')

    def set_trigger_source_gprf(self, source='Free Run'):
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
        self.cmw_write(f'TRIGger:GPRF:MEASurement:POWer:SOURce "{source}"')

    def set_trigger_source_fr1(self, source='Free Run'):
        """
        Selects the source of the trigger events. Some values are always available. They are
        listed below. Depending on the installed options, additional values are available. You
        can query a list of all supported values via TRIGger:...:CATalog:SOURce?.
        Parameters:
        <Source> string
        'Free Run (Fast Sync)'
        Free run with synchronization
        'Free Run (No Sync)'
        Free run without synchronization
        'IF Power'
        Power trigger (received RF power)
        *RST:  'IF Power'
        """
        self.cmw_write(f'TRIGger:NRSub:MEASurement:MEValuation:SOURce "{source}"')

    def set_trigger_source_lte(self, source='Free Run'):
        """
        Selects the source of the trigger events. Some values are always available. They are
        listed below. Depending on the installed options, additional values are available. You
        can query a list of all supported values via TRIGger:...:CATalog:SOURce?.
        Parameters:
        <Source> string
        'Free Run (Fast Sync)'
        Free run with synchronization
        'Free Run (No Sync)'
        Free run without synchronization
        'IF Power'
        Power trigger (received RF power)
        *RST:  'IF Power'
        """
        self.cmw_write(f'TRIGger:LTE:MEASurement:MEValuation:SOURce "{source}"')

    def set_trigger_source_wcdma(self, source='Free Run'):
        """
        Selects the source of the trigger events. Some values are always available in this firm-
        ware application. They are listed below. Depending on the installed options, additional
        values are available. A complete list of all supported values can be displayed using
        TRIGger:...:CATalog:SOURce?.
        Parameters:
        <Source> 'Free Run (Standard)': Free run (standard synchronization)
        'Free Run (Fast Sync)': Free run (fast synchronization)
        'IF Power': Power trigger (normal synchronization)
        'IF Power (Sync)': Power trigger (extended synchronization)
        *RST:  'Free Run (Standard)'
        """
        self.cmw_write(f'TRIGger:WCDMa:MEASurement:MEValuation:SOURce "{source}"')

    def set_trigger_source_gsm(self, source='Free Run'):
        """
        Selects the source of the trigger events. Some values are always available in this firm-
        ware application. They are listed below. Depending on the installed options, additional
        values are available. A complete list of all supported values can be displayed using
        TRIGger:...:CATalog:SOURce?.
        Parameters:
        <Source> 'Power': Power trigger (received RF power)
        'Acquisition': Frame trigger according to defined burst pattern
        'Free Run': Free run (untriggered)
        *RST:  'Power'
        """
        self.cmw_write(f'TRIGger:GSM:MEASurement:MEValuation:SOURce "{source}"')

    def set_trigger_slope_gprf(self, slope='REDGe'):
        """
        Qualifies whether the trigger event is generated at the rising or at the falling edge of
        the trigger pulse (valid for external and power trigger sources).
        Parameters:
        <Event> REDGe | FEDGe
        REDGe: rising edge
        FEDGe: falling edge
        *RST:  REDG
        """
        # it also can use: <CONFigure:GPRF:MEASurement:POWer:TRIGger:SLOPe>
        self.cmw_write(f'TRIGger:GPRF:MEASurement:POWer:SLOPe {slope}')

    def set_trigger_step_length_gprf(self, length='576.9230769E-6'):
        """
        Sets the time between the beginning of two consecutive measurement lengths.
        Parameters:
        <StepLength> numeric
        Range:  <MeasLength>  to  1 s
        *RST:  576.9230769E-6 s
        Default unit: s
        """
        self.cmw_write(f'CONFigure:GPRF:MEASurement:POWer:SLENgth {length}')

    def set_trigger_measure_length_gprf(self, length='576.9230769E-6'):
        """
        Sets the length of the evaluation interval used to measure a single set of current power
        results.
        The measurement length cannot be greater than the step length.
        Parameters:
        <MeasLength> numeric
        Default unit: s
        """
        self.cmw_write(f'CONFigure:GPRF:MEASurement:POWer:MLENgth {length}')

    def set_trigger_offset_gprf(self, offset=100E-6):
        """
        Defines a delay time for triggered measurements. The trigger offset delays the start of
        the measurement relative to the trigger event.
        Parameters:
        <Offset> numeric
        Range:  0 s  to  1 s
        *RST:  100E-6 s
        Default unit: s
        """
        self.cmw_write(f'TRIGger:GPRF:MEASurement:POWer:OFFSet {offset}')

    def set_trigger_mode_gprf(self, mode='SWE'):
        """
        Selects the measurement sequence that is triggered by each single trigger event. This
        setting is not valid for free run measurements.
        Parameters:
        <Mode> ONCE | SWEep | ALL | PRESelect
        ONCE: "Trigger Once"
        SWEep: "Retrigger Sweep"
        ALL: "Retrigger All"
        PRESelect: "Retrigger Preselect"
        *RST:  SWE
        """
        self.cmw_write(f'TRIGger:GPRF:MEASurement:POWer:MODE {mode}')

    def set_expect_power_gprf(self, exp_nom_pwr=0.00):
        """
        Sets the expected nominal power of the measured RF signal.
        Parameters:
        <ExpNomPwr> numeric
        The range of the expected nominal power can be calculated as
        follows:
        Range (Expected Nominal Power) = Range (Input Power) +
        External Attenuation - User Margin
        The input power range is stated in the data sheet.
        *RST:  0 dBm
        Default unit: dBm
        """
        self.cmw_write(f'CONFigure:GPRF:MEASurement:RFSettings:ENPower {exp_nom_pwr}')

    def set_expect_power_fr1(self, exp_nom_pwr=0.00):
        """
        Sets the expected nominal power of the measured RF signal.
        Parameters:
        <ExpNomPow> numeric
        The range of the expected nominal power can be calculated as
        follows:
        Range (Expected Nominal Power) = Range (Input Power) +
        External Attenuation - User Margin
        The input power range is stated in the data sheet.
        *RST:  0 dBm
        Default unit: dBm
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:RFSettings:ENPower {exp_nom_pwr}')

    def set_expect_power_lte(self, exp_nom_pwr=0.00):
        """
        Sets the expected nominal power of the measured RF signal.
        For the combined signal path scenario, use:
        ● CONFigure:LTE:SIGN<i>:RFSettings[:PCC]:ENPMode
        ● CONFigure:LTE:SIGN<i>:RFSettings[:PCC]:ENPower
        ● CONFigure:LTE:SIGN<i>:RFSettings:SCC<c>:ENPMode
        ● CONFigure:LTE:SIGN<i>:RFSettings:SCC<c>:ENPower
        Parameters:
        <ExpNomPow> The range of the expected nominal power can be calculated as
        follows:
        Range (Expected Nominal Power) = Range (Input Power) +
        External Attenuation - User Margin
        The input power range is stated in the data sheet.
        *RST:  0 dBm
        Default unit: dBm
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:RFSettings:ENPower {exp_nom_pwr}')

    def set_expect_power_wcdma(self, exp_nom_pwr=0.00):
        """
        Sets the expected nominal power of the measured RF signal.
        For the combined signal path scenario, use:
        ● CONFigure:WCDMa:SIGN<i>:RFSettings:ENPMode
        ● CONFigure:WCDMa:SIGN<i>:RFSettings:ENPower
        Parameters:
        <ExpNomPower> The range of the expected nominal power can be calculated as
        follows:
        Range (Expected Nominal Power) = Range (Input Power) +
        External Attenuation - User Margin
        The input power range is stated in the data sheet.
        *RST:  0 dBm
        Default unit: dBm
        """
        self.cmw_write(f'CONFigure:WCDMa:MEASurement:RFSettings:ENPower {exp_nom_pwr}')

    def set_expect_power_gsm(self, exp_nom_pwr=0.00):
        """
        Sets the expected nominal power of the measured RF signal.
        For the combined signal path scenario, use:
        ● CONFigure:GSM:SIGN<i>:RFSettings:ENPMode
        ● CONFigure:GSM:SIGN<i>:RFSettings:ENPower
        Parameters:
        <ExpNomPower> The range of the expected nominal power can be calculated as
        follows:
        Range (Expected Nominal Power) = Range (Input Power) +
        External Attenuation - User Margin
        The input power range is stated in the data sheet.
        *RST:  0 dBm
        Default unit: dBm
        """
        _exp_nom_pwr = round(exp_nom_pwr, 2)
        self.cmw_write(f'CONFigure:GSM:MEASurement:RFSettings:ENPower {_exp_nom_pwr}')

    def set_rx_level_gprf(self, rx_level=-70.0):
        """
        Sets the base RMS level of the RF generator.
        Parameters:
        <Level> numeric
        Range:  Please notice the ranges quoted in the data sheet.
        Increment:  0.01 dB
        *RST:  -30 dBm
        Default unit: dBm
        """
        self.cmw_write(f'SOURce:GPRF:GENerator1:RFSettings:LEVel {rx_level}')

    def set_rf_setting_user_margin_gprf(self, margin=10.00):
        """
        Sets the margin that the measurement adds to the expected nominal power to deter-
        mine the reference power. The reference power minus the external input attenuation
        must be within the power range of the selected input connector. Refer to the data
        sheet.
        Parameters:
        <UserMargin> numeric
        Range:  0 dB to (55 dB + External Attenuation - Expected
        Nominal Power)
        *RST:  0 dB
        Default unit: dB
        """
        self.cmw_write(f'CONFigure:GPRF:MEASurement:RFSettings:UMARgin {margin}')

    def set_rf_setting_user_margin_fr1(self, margin=10.00):
        """
        Sets the margin that the measurement adds to the expected nominal power to deter-
        mine the reference power. The reference power minus the external input attenuation
        must be within the power range of the selected input connector. Refer to the data
        sheet.
        Parameters:
        <UserMargin> numeric
        Range:  0 dB to (55 dB + external attenuation - expected
        nominal power)
        *RST:  0 dB
        Default unit: dB
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:RFSettings:UMARgin {margin}')

    def set_rf_setting_user_margin_lte(self, margin=10.00):
        """
        Sets the margin that the measurement adds to the expected nominal power to deter-
        mine the reference power. The reference power minus the external input attenuation
        must be within the power range of the selected input connector. Refer to the data
        sheet.
        Parameters:
        <UserMargin> numeric
        Range:  0 dB to (55 dB + external attenuation - expected
        nominal power)
        *RST:  0 dB
        Default unit: dB
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:RFSettings:UMARgin {margin}')

    def set_rf_setting_user_margin_wcdma(self, margin=10.00):
        """
        Sets the margin that the measurement adds to the expected nominal power to deter-
        mine the reference power. The reference power minus the external input attenuation
        must be within the power range of the selected input connector. Refer to the data
        sheet.
        Parameters:
        <UserMargin> numeric
        Range:  0 dB to (55 dB + external attenuation - expected
        nominal power)
        *RST:  0 dB
        Default unit: dB
        """
        self.cmw_write(f'CONFigure:WCDMa:MEASurement:RFSettings:UMARgin {margin}')

    def set_rf_setting_user_margin_gsm(self, margin=10.00):
        """
        Sets the margin that the measurement adds to the expected nominal power to deter-
        mine the reference power. The reference power minus the external input attenuation
        must be within the power range of the selected input connector. Refer to the data
        sheet.
        Parameters:
        <UserMargin> numeric
        Range:  0 dB to (55 dB + external attenuation - expected
        nominal power)
        *RST:  0 dB
        Default unit: dB
        """
        self.cmw_write(f'CONFigure:GSM:MEASurement:RFSettings:UMARgin {margin}')

    def set_rf_setting_external_tx_port_attenuation_gprf(self, attenuation):
        """
        Defines an external attenuation (or gain, if the value is negative), to be applied to the
        input connector.
        Parameters:
        <RFInputExtAtt> numeric
        Range:  -50 dB  to  90 dB
        *RST:  0 dB
        Default unit: dB
        """
        self.cmw_write(f'CONFigure:GPRF:MEASurement:RFSettings:EATTenuation {attenuation}')

    def set_rf_setting_external_tx_port_attenuation_fr1(self, attenuation):
        """
        Defines an external attenuation (or gain, if the value is negative), to be applied to the
        input connector.
        Parameters:
        <RFinputExtAtt> numeric
        Range:  -50 dB  to  90 dB
        *RST:  0 dB
        Default unit: dB
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:RFSettings:EATTenuation {attenuation}')

    def set_rf_setting_external_tx_port_attenuation_lte(self, attenuation):
        """
        Defines an external attenuation (or gain, if the value is negative), to be applied to the
        RF input connector.
        For the combined signal path scenario, use:
        ● CONFigure:LTE:SIGN<i>:RFSettings[:PCC]:EATTenuation:INPut
        ● CONFigure:LTE:SIGN<i>:RFSettings:SCC<c>:EATTenuation:INPut
        Parameters:
        <RFinputExtAtt> Range:  -50 dB  to  90 dB
        *RST:  0 dB
        Default unit: dB
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:RFSettings:EATTenuation {attenuation}')

    def set_rf_setting_external_tx_port_attenuation_wcdma(self, attenuation):
        """
        Defines an external attenuation (or gain, if the value is negative), to be applied to the
        RF input connector.
        For the combined signal path scenario, use CONFigure:WCDMa:SIGN<i>:
        RFSettings:CARRier<c>:EATTenuation:INPut.
        Parameters:
        <RFInputExtAtt> Range:  -50 dB  to  90 dB
        *RST:  0 dB
        Default unit: dB
        """
        self.cmw_write(f'CONFigure:WCDMa:MEASurement:RFSettings:EATTenuation {attenuation}')

    def set_rf_setting_external_tx_port_attenuation_gsm(self, attenuation):
        """
        Defines an external attenuation (or gain, if the value is negative), to be applied to the
        RF input connector.
        For the combined signal path scenario, useCONFigure:GSM:SIGN<i>:
        RFSettings:EATTenuation:INPut.
        Parameters:
        <ExternalAtt> Range:  -50 dB  to  90 dB
        *RST:  0 dB
        Default unit: dB
        """
        self.cmw_write(f'CONFigure:GSM:MEASurement:RFSettings:EATTenuation {attenuation}')

    def set_rf_setting_external_rx_port_attenuation_gprf(self, attenuation):
        """
        Defines an external attenuation (or gain, if the value is negative), to be applied to the
        output connector.
        Parameters:
        <ExtRFOutAtt> numeric
        Range:  -50 dB  to  90 dB
        *RST:  0 dB
        Default unit: dB
        """
        self.cmw_write(f'SOURce:GPRF:GENerator1:RFSettings:EATTenuation {attenuation}')

    def set_tx_freq_gprf(self, tx_freq):  # this is KHz
        """
        Selects the center frequency of the RF analyzer.
        For the supported frequency range, see Chapter 3.11.5, "Frequency Ranges",
        on page 395.
        Parameters:
        <AnalyzerFreq> numeric
        Default unit: Hz
        """
        self.cmw_write(f'CONFigure:GPRF:MEASurement:RFSettings:FREQuency {int(tx_freq)}KHz')

    def set_rx_freq_gprf(self, rx_freq):  # this is KHz
        """
        Sets the frequency of the unmodulated RF carrier.
        For the supported frequency range, see Chapter 2.5.1.3, "Frequency Ranges",
        on page 67.
        Parameters:
        <Frequency> numeric
        Default unit: Hz
        """
        self.cmw_write(f'SOURce:GPRF:GENerator1:RFSettings:FREQuency {int(rx_freq)}KHz')

    def set_measure_start_on_gprf(self):
        """
        INITiate:GPRF:MEAS:POWer
        STOP:GPRF:MEAS:POWer
        ABORt:GPRF:MEAS:POWer
        Starts, stops, or aborts the measurement:
        ● INITiate... starts or restarts the measurement. The measurement enters the
        "RUN" state.
        ● STOP... halts the measurement immediately. The measurement enters the "RDY"
        state. Measurement results are kept. The resources remain allocated to the mea-
        surement.
        ● ABORt... halts the measurement immediately. The measurement enters the
        "OFF" state. All measurement values are set to NAV. Allocated resources are
        released.
        Use FETCh...STATe? to query the current measurement state.
        ==================================================================================
        Use READ:GPRF:MEAS:POWer...? to initiate a measurement and to retrieve the
        results. You can also start the measurement using INIT:GPRF:MEAS:POWer and
        retrieve the results using FETCh:GPRF:MEAS:POWer...
        READ:GPRF:MEAS:POWer = INIT:GPRF:MEAS:POWer and then FETCh:GPRF:MEAS:POWer
        """
        self.cmw_write(f'INIT:GPRF:MEASurement:POWer')

    def set_measure_start_on_fr1(self):
        """
        Starts, stops, or aborts the measurement:
        ● INITiate... starts or restarts the measurement. The measurement enters the
        "RUN" state.
        ● STOP... halts the measurement immediately. The measurement enters the "RDY"
        state. Measurement results are kept. The resources remain allocated to the mea-
        surement.
        ● ABORt... halts the measurement immediately. The measurement enters the
        "OFF" state. All measurement values are set to NAV. Allocated resources are
        released.
        Use FETCh...STATe? to query the current measurement state.
        ==================================================================================
        The NR multi-evaluation measurement is programmed as follows:
        ● The measurement is controlled by SCPI commands with the following syn-
        tax: ...NRSub:MEAS:MEValuation...
        ● Use general commands of the type ...:NRSub:MEAS... (no :MEValuation
        mnemonic) to define the signal routing and to perform RF and analyzer settings.
        ● After a *RST, the measurement is switched off. Use
        READ:NRSub:MEAS:MEValuation...? to initiate a measurement and to retrieve
        the results. You can also start the measurement using
        INIT:NRSub:MEAS:MEValuation and retrieve the results using
        FETCh:NRSub:MEAS:MEValuation...?.
        """
        self.cmw_write(f'INIT:NRSub:MEASurement:MEValuation')

    def set_measure_start_on_lte(self):
        """
        Starts, stops, or aborts the measurement:
        ● INITiate... starts or restarts the measurement. The measurement enters the
        "RUN" state.
        ● STOP... halts the measurement immediately. The measurement enters the "RDY"
        state. Measurement results are kept. The resources remain allocated to the mea-
        surement.
        ● ABORt... halts the measurement immediately. The measurement enters the
        "OFF" state. All measurement values are set to NAV. Allocated resources are
        released.
        Use FETCh...STATe? to query the current measurement state.
        ==================================================================================
        The LTE multi-evaluation measurement is programmed as follows:
        ● The measurement is controlled by SCPI commands with the following syn-
        tax: ...LTE:MEAS:MEValuation...
        ● Use general commands of the type ...:NRSub:MEAS... (no :MEValuation
        mnemonic) to define the signal routing and to perform RF and analyzer settings.
        ● After a *RST, the measurement is switched off. Use
        READ:LTE:MEAS:MEValuation...? to initiate a measurement and to retrieve
        the results. You can also start the measurement using
        INIT:LTE:MEAS:MEValuation and retrieve the results using
        FETCh:LTE:MEAS:MEValuation...?.
        """
        self.cmw_write(f'INIT:LTE:MEASurement:MEValuation')

    def set_measure_start_on_wcdma(self):
        """
        INITiate:WCDMa:MEAS<i>:MEValuation
        STOP:WCDMa:MEAS<i>:MEValuation
        ABORt:WCDMa:MEAS<i>:MEValuation
        ===================================================================================
        Starts, stops, or aborts the measurement:
        ● INITiate... starts or restarts the measurement. The measurement enters the
        "RUN" state.
        ● STOP... halts the measurement immediately. The measurement enters the "RDY"
        state. Measurement results are kept. The resources remain allocated to the mea-
        surement.
        ● ABORt... halts the measurement immediately. The measurement enters the
        "OFF" state. All measurement values are set to NAV. Allocated resources are
        released.
        Use FETCh...STATe? to query the current measurement state.
        """
        self.cmw_write(f'INIT:WCDMa:MEASurement:MEValuation')

    def set_measure_start_on_gsm(self):
        """
        Starts, stops, or aborts the measurement:
        ● INITiate... starts or restarts the measurement. The measurement enters the
        "RUN" state.
        ● STOP... halts the measurement immediately. The measurement enters the "RDY"
        state. Measurement results are kept. The resources remain allocated to the mea-
        surement.
        ● ABORt... halts the measurement immediately. The measurement enters the
        "OFF" state. All measurement values are set to NAV. Allocated resources are
        released.
        Use FETCh...STATe? to query the current measurement state.
        """
        self.cmw_write(f'INIT:GSM:MEASurement:MEValuation')

    def set_measure_stop_fr1(self):
        """
        Starts, stops, or aborts the measurement:
        ● INITiate... starts or restarts the measurement. The measurement enters the
        "RUN" state.
        ● STOP... halts the measurement immediately. The measurement enters the "RDY"
        state. Measurement results are kept. The resources remain allocated to the mea-
        surement.
        ● ABORt... halts the measurement immediately. The measurement enters the
        "OFF" state. All measurement values are set to NAV. Allocated resources are
        released.
        Use FETCh...STATe? to query the current measurement state.
        """
        self.cmw_write(f'STOP:NRSub:MEASurement:MEValuation')

    def set_measure_stop_lte(self):
        """
        Starts, stops, or aborts the measurement:
        ● INITiate... starts or restarts the measurement. The measurement enters the
        "RUN" state.
        ● STOP... halts the measurement immediately. The measurement enters the "RDY"
        state. Measurement results are kept. The resources remain allocated to the mea-
        surement.
        ● ABORt... halts the measurement immediately. The measurement enters the
        "OFF" state. All measurement values are set to NAV. Allocated resources are
        released.
        Use FETCh...STATe? to query the current measurement state.
        """
        self.cmw_write(f'STOP:LTE:MEASurement:MEValuation')

    def set_measure_stop_wcdma(self):
        """
        Starts, stops, or aborts the measurement:
        ● INITiate... starts or restarts the measurement. The measurement enters the
        "RUN" state.
        ● STOP... halts the measurement immediately. The measurement enters the "RDY"
        state. Measurement results are kept. The resources remain allocated to the mea-
        surement.
        ● ABORt... halts the measurement immediately. The measurement enters the
        "OFF" state. All measurement values are set to NAV. Allocated resources are
        released.
        Use FETCh...STATe? to query the current measurement state.
        """
        self.cmw_write(f'STOP:WCDMa:MEASurement:MEValuation')

    def set_measure_stop_gsm(self):
        """
        Starts, stops, or aborts the measurement:
        ● INITiate... starts or restarts the measurement. The measurement enters the
        "RUN" state.
        ● STOP... halts the measurement immediately. The measurement enters the "RDY"
        state. Measurement results are kept. The resources remain allocated to the mea-
        surement.
        ● ABORt... halts the measurement immediately. The measurement enters the
        "OFF" state. All measurement values are set to NAV. Allocated resources are
        released.
        Use FETCh...STATe? to query the current measurement state.
        """
        self.cmw_write(f'STOP:GSM:MEASurement:MEValuation')

    def set_generator_base_band_mode_gprf(self, mode='ARB'):
        """
        Selects the baseband mode for the generator signal.
        Parameters:
        <BaseBandMode> CW | DTONe | ARB
        CW: unmodulated CW signal
        DTONe: dual-tone signal
        ARB: ARB generator processing a waveform file
        *RST:  CW
        """
        self.cmw_write(f'SOURce:GPRF:GENerator1:BBMode {mode}')

    def set_generator_cmw_port_uasge_all_gprf(self, port=18):
        """
        CONFigure:GPRF:GEN<i>:CMWS:USAGe:TX:ALL <TXConnBench>, <Usage>...
        Activates or deactivates the individual RF connectors of a connector bench.
        For possible bench values, see Chapter 2.5.1.2, "Values for Signal Path Selection",
        on page 65.
        Parameters:
        <Usage> OFF | ON
        Comma-separated list of 4 or 8 values, one for each connector
        of the bench
        ON: activate the connector
        OFF: deactivate the connector
        Parameters for setting and query:
        <TXConnBench> Selects a bench with 4 or 8 connectors
        """
        self.cmw_write(f'CONFigure:GPRF:GENerator:CMWS:USAGe:TX:ALL R1{port}, ON, ON, ON, ON, ON, ON, ON, ON')

    def set_arb_file_gprf(self, waveform_path):
        """
        Selects a waveform file for the ARB baseband mode.
        This command supports path aliases (e.g. @WAVEFORM). Use MMEMory:ALIases? to
        query the available path aliases.
        If the selected file does not exist or no file has been selected, a query returns "No
        File Selected".
        If the selected file does exist, a query returns:
        ● Without <PathType>: The string used to select the file. If an alias has been used,
        the alias is not substituted.
        ● With <PathType>: The absolute path of the file. If an alias has been used, the alias
        is substituted.
        Parameters:
        <ARBFile> string
        Name of the waveform file to be used (.wv).
        Query parameters:
        <PathType> ABSPath
        Optional parameter, specifying that a query returns the absolute
        path.
        """
        self.cmw_write(f'SOURce:GPRF:GEN1:ARB:FILE "{waveform_path}"')

    def set_generator_state_gprf(self, state='ON'):
        """
        Turns the generator on or off.
        Setting parameters:
        <Control> ON | OFF
        Switch the generator ON or OFF.
        *RST:  OFF
        Return values:
        <GeneratorState> OFF | PENDing | ON | RDY
        OFF: generator switched off
        PEND: generator switched on but no signal available yet
        ON: generator switched on, signal available
        RDY: generator switched off, ARB file processing complete in
        smart channel mode
        *RST:  OFF
        """
        self.cmw_write(f'SOUR:GPRF:GENerator1:STAT {state}')

    def get_power_state_query_gprf(self):
        """
        Queries the main measurement state. Use FETCh:...:STATe:ALL? to query the
        measurement state including the substates. Use INITiate..., STOP...,
        ABORt... to change the measurement state.
        Return values:
        <MeasState> OFF | RUN | RDY
        OFF: measurement off, no resources allocated, no results
        RUN: measurement running, synchronization pending or adjus-
        ted, resources active or queued
        RDY: measurement finished
        *RST:  OFF
        """
        return self.cmw_query('FETCh:GPRF:MEASurement:POW:STAT?')

    def get_power_state_query_fr1(self):
        """
        Queries the main measurement state. Use FETCh:...:STATe:ALL? to query the
        measurement state including the substates. Use INITiate..., STOP...,
        ABORt... to change the measurement state.
        Return values:
        <MeasStatus> OFF | RUN | RDY
        OFF: measurement off, no resources allocated, no results
        RUN: measurement running, synchronization pending or adjus-
        ted, resources active or queued
        RDY: measurement terminated, valid results can be available
        *RST:  OFF
        Usage:  Query only
        """
        return self.cmw_query('FETCh:NRSub:MEASurement:MEValuation:STATe?')

    def get_power_state_query_lte(self):
        """
        Queries the main measurement state. Use FETCh:...:STATe:ALL? to query the
        measurement state including the substates. Use INITiate..., STOP...,
        ABORt... to change the measurement state.
        Return values:
        <MeasStatus> OFF | RUN | RDY
        OFF: measurement off, no resources allocated, no results
        RUN: measurement running, synchronization pending or adjus-
        ted, resources active or queued
        RDY: measurement terminated, valid results can be available
        *RST:  OFF
        Usage:  Query only
        """
        return self.cmw_query('FETCh:LTE:MEASurement:MEValuation:STATe?')

    def get_power_state_query_wcdma(self):
        """
        Queries the main measurement state. Use FETCh:...:STATe:ALL? to query the
        measurement state including the substates. Use INITiate..., STOP...,
        ABORt... to change the measurement state.
        Return values:
        <MeasStatus> OFF | RUN | RDY
        OFF: measurement off, no resources allocated, no results
        RUN: measurement running, synchronization pending or adjus-
        ted, resources active or queued
        RDY: measurement terminated, valid results can be available
        *RST:  OFF
        Usage:  Query only
        """
        return self.cmw_query('FETCh:WCDMa:MEASurement:MEValuation:STATe?')

    def get_power_state_query_gsm(self):
        """
        Queries the main measurement state. Use FETCh:...:STATe:ALL? to query the
        measurement state including the substates. Use INITiate..., STOP...,
        ABORt... to change the measurement state.
        Return values:
        <MeasStatus> OFF | RUN | RDY
        OFF: measurement switched off, no resources allocated, no
        results available (when entered after ABORt...)
        RUN: measurement running (after INITiate..., READ...),
        synchronization pending or adjusted, resources active or queued
        RDY: measurement has been terminated, valid results are avail-
        able
        *RST:  OFF
        """
        return self.cmw_query('FETCh:GSM:MEASurement:MEValuation:STATe?')

    def get_power_average_query_gprf(self):
        """
        The following results can be retrieved:
        ● "Power Current RMS" (...:POWer:CURRent?)
        ● "Power Current Min." (...:MINimum:CURRent?)
        ● "Power Current Max." (...:MAXimum:CURRent?)
        ● "Power Average RMS" (...:AVERage?)
        ● "Power Minimum" (...:PEAK:MINimum?)
        ● "Power Maximum" (...:PEAK:MAXimum?)
        ● "Standard Deviation" (...:SDEViation?)
        The values described below are returned by FETCh and READ commands. CALCulate
        commands return error codes instead, one value for each result listed below.
        Return values:
        <Reliability> decimal
        See Reliability Indicator
        <Power> float
        Power value
        Default unit: dBm (SDEViation: dB)
        """
        return self.cmw_query('FETCh:GPRF:MEASurement:POWer:AVER?').split(',')

    def get_power_monitor_average_query_lte(self):
        """
        Returns the total TX power of all carriers.
        Return values:
        <Reliability> Reliability Indicator
        <OutOfTolerance> Out of tolerance result, i.e. percentage of measurement intervals
        of the statistic count that exceed the specified limits
        Default unit: %
        <TXpower> Default unit: dBm
        """
        return self.cmw_query(f'FETCh:LTE:MEASurement:MEValuation:PMONitor:AVERage?')

    def get_arb_file_query_gprf(self):
        """
        Selects a waveform file for the ARB baseband mode.
        This command supports path aliases (e.g. @WAVEFORM). Use MMEMory:ALIases? to
        query the available path aliases.
        If the selected file does not exist or no file has been selected, a query returns "No
        File Selected".
        If the selected file does exist, a query returns:
        ● Without <PathType>: The string used to select the file. If an alias has been used,
        the alias is not substituted.
        ● With <PathType>: The absolute path of the file. If an alias has been used, the alias
        is substituted.
        Parameters:
        <ARBFile> string
        Name of the waveform file to be used (.wv).
        Query parameters:
        <PathType> ABSPath
        Optional parameter, specifying that a query returns the absolute
        path.
        """
        return self.cmw_query(f'SOURce:GPRF:GENerator1:ARB:FILE?')

    def get_generator_state_query_gprf(self):
        """
        Turns the generator on or off.
        Setting parameters:
        <Control> ON | OFF
        Switch the generator ON or OFF.
        *RST:  OFF
        Return values:
        <GeneratorState> OFF | PENDing | ON | RDY
        OFF: generator switched off
        PEND: generator switched on but no signal available yet
        ON: generator switched on, signal available
        RDY: generator switched off, ARB file processing complete in
        smart channel mode
        *RST:  OFF
        """
        return self.cmw_query(f'SOUR:GPRF:GENerator1:STAT?')

    def set_uldl_periodicity_fr1(self, periodicity='MS10'):
        """
        Configures the periodicity of the TDD UL-DL pattern.
        Parameters:
        <Periodicity> MS05 | MS1 | MS125 | MS2 | MS25 | MS3 | MS4 | MS5 | MS10
        0.5 ms, 1 ms, 1.25 ms, 2 ms, 2.5 ms, 3 ms, 4 ms, 5 ms, 10 ms
        *RST:  MS5
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:ULDL:PERiodicity {periodicity}')

    def set_duplexer_mode_fr1(self, mode='FDD'):
        """
        Selects the duplex mode of the signal: FDD or TDD.
        Parameters:
        <Mode> FDD | TDD
        *RST:  FDD
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:DMODe {mode}')

    def set_duplexer_mode_lte(self, mode='FDD'):
        """
        Selects the duplex mode of the signal: FDD or TDD.
        Parameters:
        <Mode> FDD | TDD
        *RST:  FDD
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:DMODe {mode}')

    def set_band_fr1(self, band):
        """
        Selects the operating band (OB). The allowed input range depends on the duplex
        mode (FDD or TDD).
        Parameters:
        <Band> FDD: OB1 | OB2 | OB3 | OB5 | OB7 | OB8 | OB12 | OB14 |
        OB18 | OB20 | OB25 | OB26 | OB28 | OB30 | OB65 | OB66 |
        OB70 | OB71 | OB74 | OB80 | ... | OB84 | OB86 | OB89 | OB91
        | ... | OB95
        TDD: OB34 | OB38 | ... | OB41 | OB48 | OB50 | OB51 | OB53 |
        OB77 | ... | OB84 | OB86 | OB89 | OB90 | OB95
        *RST:  OB1
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:BAND OB{band}')

    def set_band_lte(self, band):
        """
        Selects the operating band (OB).
        The allowed input range has dependencies:
        ● FDD UL: OB1 | ... | OB28 | OB30 | OB31 | OB65 | OB66 | OB68 | OB70 | ... | OB74
        | OB85
        ● TDD UL: OB33 | ... | OB45 | OB48 | OB50 | ... | OB53 | OB250
        ● Sidelink: OB47
        For the combined signal path scenario, use:
        ● CONFigure:LTE:SIGN<i>[:PCC]:BAND
        ● CONFigure:LTE:SIGN<i>:SCC<c>:BAND
        Parameters:
        <Band> OB1 to OB250, see list above
        *RST:  OB1 (OB33 for TDD UL, OB47 for sidelink)
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:BAND OB{band}')

    def set_cc_bw_lte(self, carrier_num, bw='5'):
        """
        Selects the channel bandwidth of component carrier CC<no>. Without carrier aggrega-
        tion, you can omit <no>.
        For the combined signal path scenario, use:
        ● CONFigure:LTE:SIGN<i>:CELL:BANDwidth[:PCC]:DL
        ● CONFigure:LTE:SIGN<i>:CELL:BANDwidth:SCC<c>:DL
        Suffix:
        <no>
        .
        1..4
        Parameters:
        <ChannelBW> B014 | B030 | B050 | B100 | B150 | B200
        B014: 1.4 MHz
        B030: 3 MHz
        B050: 5 MHz
        B100: 10 MHz
        B150: 15 MHz
        B200: 20 MHz
        *RST:  B200
        """
        bw10 = f'0{int(eval(bw) * 10)}' if eval(bw) < 10 else f'{int(eval(bw) * 10)}'
        self.cmw_write(f'CONFigure:LTE:MEASurement:CC{carrier_num}:CBANdwidth B{bw10}')

    def set_cc_channel_lte(self, carrier_num, channel=19300):
        """
        Selects the center frequency of component carrier CC<no>. Without carrier aggrega-
        tion, you can omit <no>.
        Using the unit CH, the frequency can be set via the channel number. The allowed
        channel number range depends on the operating band, see Chapter 5.2.11.4, "Fre-
        quency Bands", on page 928.
        For the combined signal path scenario, use:
        ● CONFigure:LTE:SIGN<i>:RFSettings[:PCC]:CHANnel:UL
        ● CONFigure:LTE:SIGN<i>:RFSettings:SCC<c>:CHANnel:UL
        For the supported frequency range, see Chapter 5.5.1.5, "Frequency Ranges",
        on page 1021.
        Suffix:
        <no>
        .
        1..4
        Parameters:
        <AnalyzerFreq> *RST:  Depends on <no>
        Default unit: Hz
        """
        self.cmw_write(f'CONFigure:LTE:MEAS:RFSettings:CC{carrier_num}:FREQuency {channel} Ch')

    def set_band_wcdma(self, band):
        """
        CONFigure:WCDMa:MEAS<i>:CARRier<c>:BAND <Band>
        Selects the operating band (OB).
        For the combined signal path scenario, use:
        ● CONFigure:WCDMa:SIGN<i>:CARRier<c>:BAND
        ● CONFigure:WCDMa:SIGN<i>:RFSettings:DBDC
        Suffix:
        <c>
        .
        1..2
        Selects the affected carrier - only relevant for dual band dual
        carrier measurement
        Parameters:
        <Band> OB1 | ... | OB14 | OB19 | ... | OB22 | OB25 | OB26 | OBS1 | ... |
        OBS3 | OBL1
        OB1, ..., OB14: operating band I to XIV
        OB19, ..., OB22: operating band XIX to XXII
        OB25, OB26: operating band XXV and XXVI
        OBS1: operating band S
        OBS2: operating band S 170 MHz
        OBS3: operating band S 190 MHz
        OBL1: operating band L
        Default unit: OB1
        """
        self.cmw_write(f'CONFigure:WCDMa:MEASurement:BAND OB{band}')

    def set_band_gsm(self, band):
        """
        Selects the GSM frequency band.
        For the combined signal path scenario, use:
        ● CONFigure:GSM:SIGN<i>:BAND:BCCH
        ● SENSe:GSM:SIGN<i>:BAND:TCH?
        Parameters:
        <Band> G04 | G085 | G09 | G18 | G19 | GG08
        G04: GSM400
        G085: GSM850
        G09: GSM900
        G18: GSM1800
        G19: GSM1900
        """
        band_tx_meas_dict_gsm = {
            900: 'G09',
            1800: 'G18',
            1900: 'G19',
            850: 'G085',
        }
        self.cmw_write(f'CONFigure:GSM:MEASurement:BAND {band_tx_meas_dict_gsm[band]}')

    def set_modulation_count_fr1(self, count=5):
        """
        Specifies the statistic count of the measurement. The statistic count is equal to the
        number of measurement intervals per single shot.
        Parameters:
        <StatisticCount> numeric
        Range:  1 slot  to  1000 slots
        *RST:  20 slots
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:SCOunt:MODulation {count}')

    def set_modulation_count_lte(self, count=5):
        """
        Specifies the statistic count of the measurement. The statistic count is equal to the
        number of measurement intervals per single shot.
        Parameters:
        <StatisticCount> Number of measurement intervals (slots)
        Range:  1 slot  to  1000 slots
        *RST:  20 slots
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:SCOunt:MODulation {count}')

    def set_modulation_count_wcdma(self, count=5):
        """
        Specifies the statistic count of the measurement. The statistic count is equal to the
        number of measurement intervals per single shot.
        Parameters:
        <StatisticCount> Number of measurement intervals
        Range:  1  to  1000
        *RST:  10
        """
        self.cmw_write(f'CONFigure:WCDMa:MEASurement:MEValuation:SCOunt:MODulation {count}')

    def set_modulation_count_gsm(self, count=5):
        """
        Specifies the statistic count of the measurement. The statistic count is equal to the
        number of measurement intervals per single shot.
        Parameters:
        <StatisticCount> Number of measurement intervals for the modulation measure-
        ment
        Range:  1  to  1000
        *RST:  10
        """
        self.cmw_write(f'CONFigure:GSM:MEASurement:MEValuation:SCOunt:MODulation {count}')

    def set_pvt_count_gsm(self, count=5):
        """
        Specifies the statistic count of the measurement. The statistic count is equal to the
        number of measurement intervals per single shot.
        Parameters:
        <StatisticCount> Number of measurement intervals for the power vs. time mea-
        surement
        Range:  1  to  1000
        *RST:  10
        """
        self.cmw_write(f'CONFigure:GSM:MEASurement:MEValuation:SCOunt:PVTime {count}')

    def set_spectrum_modulation_count_gsm(self, count=5):
        """
        Specifies the statistic count of the measurement. The statistic count is equal to the
        number of measurement intervals per single shot.
        Parameters:
        <StatisticCount> Number of measurement intervals for the spectrum modulation
        measurement
        Range:  1  to  1000
        *RST:  20
        """
        self.cmw_write(f'CONFigure:GSM:MEASurement:MEValuation:SCOunt:SMODulation {count}')

    def set_spectrum_switching_count_gsm(self, count=5):
        """
        Specifies the statistic count of the measurement. The statistic count is equal to the
        number of measurement intervals per single shot.
        Parameters:
        <StatisticCount> Number of measurement intervals for the spectrum switching
        measurement
        Range:  1  to  100
        *RST:  10
        """
        self.cmw_write(f'CONFigure:GSM:MEASurement:MEValuation:SCOunt:SSWitching {count}')

    def set_tx_freq_fr1(self, tx_freq):  # this is KHz
        """
        Selects the center frequency of the measured carrier.
        Using the unit CH, the frequency can be set via the channel number. The allowed
        channel number range depends on the operating band, see Chapter 3.3.3, "Frequency
        Bands", on page 19.
        For the supported frequency range, see Chapter 6.1.5, "Frequency Ranges",
        on page 100.
        Parameters:
        <AnalyzerFreq> numeric
        Default unit: Hz
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:RFSettings:FREQuency {int(tx_freq)}KHz')

    def set_tx_freq_lte(self, tx_freq):  # this is KHz
        """
        Selects the center frequency of component carrier CC<no>. Without carrier aggrega-
        tion, you can omit <no>.
        Using the unit CH, the frequency can be set via the channel number. The allowed
        channel number range depends on the operating band, see Chapter 5.2.11.4, "Fre-
        quency Bands", on page 928.
        For the combined signal path scenario, use:
        ● CONFigure:LTE:SIGN<i>:RFSettings[:PCC]:CHANnel:UL
        ● CONFigure:LTE:SIGN<i>:RFSettings:SCC<c>:CHANnel:UL
        For the supported frequency range, see Chapter 5.5.1.5, "Frequency Ranges",
        on page 1021.
        Suffix:
        <no>   1..4
        Parameters:
        <AnalyzerFreq> *RST:  Depends on <no>
        Default unit: Hz
        CONFigure:LTE:MEAS<i>:RFSettings:CC<no>:FREQuency <AnalyzerFreq> for after 3.7.30
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:RFSettings:FREQuency {int(tx_freq)}KHz')

    def set_tx_freq_wcdma(self, tx_chan):  # this is CH
        """
        CONFigure:WCDMa:MEAS<i>:RFSettings:CARRier<c>:FREQuency <Frequency>
        Selects the center frequency of the RF analyzer.
        For the combined signal path scenario, use:
        ● CONFigure:WCDMa:SIGN<i>:RFSettings:CARRier<c>:FREQuency:UL
        ● CONFigure:WCDMa:SIGN<i>:RFSettings:CARRier<c>:FOFFset:UL
        ● CONFigure:WCDMa:SIGN<i>:RFSettings:CARRier<c>:CHANnel:UL
        The supported frequency range depends on the instrument model and the available
        options. The supported range can be smaller than stated here. Refer to the preface of
        your model-specific base unit manual.
        Suffix:
        <c>
        .
        1..2
        Uplink carrier
        Parameters:
        <Frequency> Range:  70E+6 Hz  to  6E+9 Hz
        *RST:  1.9226E+9 Hz
        Default unit: Hz
        Using the unit CH the frequency can be set via the channel num-
        ber. The allowed channel number range depends on the operat-
        ing band, see Chapter 3.2.4.3, "Operating Bands", on page 714.
        """
        self.cmw_write(f'CONFigure:WCDMa:MEASurement:RFSettings:FREQuency {tx_chan}CH')

    def set_tx_freq_gsm(self, tx_freq):  # this is KHz
        """
        Selects the center frequency of the RF analyzer.
        If the center frequency is valid for the current frequency band, the corresponding chan-
        nel number is also calculated and set.
        See also:
        ● GSM Frequency Bands and Channels
        ● CONFigure:GSM:MEAS<i>:BAND
        ● CONFigure:GSM:MEAS<i>:CHANnel
        For the combined signal path scenario, use:
        ● CONFigure:GSM:SIGN<i>:RFSettings:CHANnel:TCH[:CARRier<c>]
        ● CONFigure:GSM:SIGN<i>:RFSettings:CHCCombined:TCH:CSWitched
        ● CONFigure:GSM:SIGN<i>:RFSettings:HOPPing:ENABle:TCH[:
        CARRier<c>]
        ● CONFigure:GSM:SIGN<i>:RFSettings:HOPPing:MAIO:TCH[:
        CARRier<c>]
        ● CONFigure:GSM:SIGN<i>:RFSettings:HOPPing:HSN:TCH[:CARRier<c>]
        ● CONFigure:GSM:SIGN<i>:RFSettings:HOPPing:SEQuence:TCH[:
        CARRier<c>]
        The supported frequency range depends on the instrument model and the available
        options. The supported range can be smaller than stated here. Refer to the preface of
        your model-specific base unit manual.
        Parameters:
        <Frequency> Range:  70E+6 Hz to 6E+9 Hz
        *RST:  903E+6 Hz
        Default unit: Hz
        """
        self.cmw_write(f'CONFigure:GSM:MEASurement:RFSettings:FREQuency {int(tx_freq)}KHz')

    def set_chan_gsm(self, rx_chan):  # this is channel
        """
        Selects the channel number. The channel number must be valid for the current fre-
        quency band, for dependencies see GSM Frequency Bands and Channels.
        The corresponding center frequency (CONFigure:GSM:MEAS<i>:RFSettings:
        FREQuency) is calculated and set.
        For the combined signal path scenario, use:
        ● CONFigure:GSM:SIGN<i>:RFSettings:CHANnel:TCH[:CARRier<c>]
        ● CONFigure:GSM:SIGN<i>:RFSettings:CHCCombined:TCH:CSWitched
        ● CONFigure:GSM:SIGN<i>:RFSettings:HOPPing:ENABle:TCH[:
        CARRier<c>]
        ● CONFigure:GSM:SIGN<i>:RFSettings:HOPPing:MAIO:TCH[:
        CARRier<c>]
        ● CONFigure:GSM:SIGN<i>:RFSettings:HOPPing:HSN:TCH[:CARRier<c>]
        ● CONFigure:GSM:SIGN<i>:RFSettings:HOPPing:SEQuence:TCH[:
        CARRier<c>]
        Parameters:
        <Channel> GSM channel number
        Range:  depends on frequency band
        *RST:  65
        """
        self.cmw_write(f'CONFigure:GSM:MEASurement:CHANnel {rx_chan}')

    def set_plc_fr1(self, plc_id=0):
        """
        Specifies the physical cell ID of carrier <no>.
        Suffix:
        <no>    1
        Parameters:
        <PhysicalCellID> numeric
        Range:  0  to  1007
        *RST:  0
        origainl name: CONFigure:NRSub:MEAS<i>[:CC<no>]:PLCid
        """
        # self.cmw_write(f'CONFigure:NRSub:MEASurement:PLCid {plc_id}')  # V3.8.10
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:PLCid {plc_id}')  # V3.7.10 / V3.7.40

    def set_plc_lte(self, plc_id=0):
        """
        Specifies the physical layer cell ID of component carrier CC<no>. Without carrier
        aggregation, you can omit <no>.
        For the combined signal path scenario, use:
        ● CONFigure:LTE:SIGN<i>:CELL[:PCC]:PCID
        ● CONFigure:LTE:SIGN<i>:CELL:SCC<c>:PCID
        Suffix:
        <no>
        .
        1..4
        Parameters:
        <PhsLayerCellID> Range:  0  to  503
        *RST:  0
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:PLCid {plc_id}')

    def set_meas_on_exception_fr1(self, meas_on_exception='ON'):
        """
        Specifies whether measurement results identified as faulty or inaccurate are rejected.
        Parameters:
        <MeasOnException> OFF | ON
        OFF: Faulty results are rejected.
        ON: Results are never rejected.
        *RST:  OFF
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:MOEXception {meas_on_exception}')

    def set_meas_on_exception_lte(self, meas_on_exception='ON'):
        """
        Specifies whether measurement results identified as faulty or inaccurate are rejected.
        Parameters:
        <MeasOnException> OFF | ON
        OFF: Faulty results are rejected.
        ON: Results are never rejected.
        *RST:  OFF
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:MOEXception {meas_on_exception}')

    def set_meas_on_exception_gsm(self, meas_on_exception='ON'):
        """
        Specifies whether measurement results identified as faulty or inaccurate are rejected.
        Parameters:
        <MeasOnException> OFF | ON
        OFF: Faulty results are rejected.
        ON: Results are never rejected.
        *RST:  OFF
        """
        self.cmw_write(f'CONFigure:GSM:MEASurement:MEValuation:MOEXception {meas_on_exception}')

    def set_scs_bw_fr1(self, scs, bw):
        """
        this command from LSI cannot find in the doc of R&S
        it just can reference:
        ● CONFigure:NRSub:MEAS<i>:CCALl:TXBWidth:SCSPacing <UsedSCS>
        Selects the subcarrier spacing for the measurement, for all carriers.
        Parameters:
        <UsedSCS> S15K | S30K | S60K
        *RST:  S30K
        ● CONFigure:NRSub:MEAS<i>[:CC<no>]:CBANdwidth <ChannelBW>
        Specifies the channel bandwidth of carrier <no>.
        Suffix:
        <no>  1
        Parameters:
        <ChannelBW> B005 | B010 | B015 | B020 | B025 | B030 | B040 | B050 | B060 |
        B080 | B090 | B100
        Channel bandwidth 5 MHz to 100 MHz (Bxxx = xxx MHz).
        *RST:  B020
        """
        bw = f'00{bw}' if bw < 10 else f'0{bw}' if 10 <= bw < 100 else bw
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:BWC S{scs}K, B{bw}')

    def set_bw_lte(self, bw):
        """
        CONFigure:LTE:MEAS<i>:CC<no>:CBANdwidth
        Selects the channel bandwidth of component carrier CC<no>. Without carrier aggrega-
        tion, you can omit <no>.
        For the combined signal path scenario, use:
        ● CONFigure:LTE:SIGN<i>:CELL:BANDwidth[:PCC]:DL
        ● CONFigure:LTE:SIGN<i>:CELL:BANDwidth:SCC<c>:DL
        Suffix:
        <no>
        .
        1..4
        Parameters:
        <ChannelBW> B014 | B030 | B050 | B100 | B150 | B200
        B014: 1.4 MHz
        B030: 3 MHz
        B050: 5 MHz
        B100: 10 MHz
        B150: 15 MHz
        B200: 20 MHz
        *RST:  B200
        """
        bw10 = f'0{int(bw * 10)}' if bw < 10 else f'{bw * 10}'
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:CBANdwidth B{bw10}')

    def set_spectrum_limit_fr1(self, area, bw10, start_freq, stop_freq, level, rbw):
        """
        ● CONFigure:NRSub:MEAS<i>:MEValuation:LIMit:SEMask:AREA<area>:CBANdwidth<bw>
           <Enable>, <FrequencyStart>, <FrequencyEnd>, <Level>, <RBW>
        Defines general requirements for the emission mask area number <area> (for NR SA).
        The activation state, the area borders, an upper limit and the resolution bandwidth
        must be specified.
        The emission mask applies to the channel bandwidth <bw>.
        Suffix:
        <bw>
        5, 10, 15, 20, 25, 30, 40, 50, 60, 80, 90, 100 Channel bandwidth in MHz
        <area> 1..12
        Number of the emission mask area
        Parameters:
        <Enable> OFF | ON
        OFF: disables the check of these requirements
        ON: enables the check of these requirements
        *RST:  ON (<area> = 1 to 4) / OFF (<area> = 5 to 12)
        <FrequencyStart> numeric
        Start frequency of the area, relative to the edges of the channel
        bandwidth
        Range:  0 MHz  to  105 MHz (less, depending on <bw>)
        *RST:  depends on <bw> and <area>
        Default unit: Hz
        <FrequencyEnd> numeric
        Stop frequency of the area, relative to the edges of the channel
        bandwidth
        Range:  0 MHz  to  105 MHz (less, depending on <bw>)
        *RST:  depends on <bw> and <area>
        Default unit: Hz
        <Level> numeric
        Upper limit for the area
        Range:  -256 dBm  to  256 dBm
        *RST:  depends on <bw> and <area>
        Default unit: dBm
        <RBW> K030 | PC1 | M1
        Resolution bandwidth to be used for the area
        Only a subset of the values is allowed, depending on <bw>.
        K030: 30 kHz
        PC1: 1 % of channel bandwidth
        M1: 1 MHz
        *RST:  K030 (<area> = 1) / M1 (<area> = 2 to 12)
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:LIMit:SEMask:AREA{area}:CBANdwidth{bw10} '
                       f'ON, {start_freq}MHz, {stop_freq}MHz, {level}, {rbw}')

    def set_spectrum_limit_lte(self, no, bw10, enable, start_freq, stop_freq, level, rbw):
        """
        CONFigure:LTE:MEAS<i>:MEValuation:LIMit:SEMask:LIMit<no>:
        CBANdwidth<Band> <Enable>, <FrequencyStart>, <FrequencyEnd>, <Level>,
        <RBW>
        Defines general requirements for the emission mask area <no>. The activation state,
        the area borders, an upper limit and the resolution bandwidth must be specified.
        The emission mask applies to the channel bandwidth <Band>.
        Suffix:
        <Band>
        .
        14, 30, 50, 100, 150, 200
        <no> 1..12
        Number of the emission mask area
        Parameters:
        <Enable> OFF | ON
        OFF: disables the check of these requirements
        ON: enables the check of these requirements
        *RST:  depends on channel bandwidth and area number
        <FrequencyStart> Start frequency of the area, relative to the edges of the channel
        bandwidth
        Range:  see table below
        *RST:  depends on channel bandwidth and area number
        Default unit: Hz
        <FrequencyEnd> Stop frequency of the area, relative to the edges of the channel
        bandwidth
        Range:  see table below
        *RST:  depends on channel bandwidth and area number
        Default unit: Hz
        <Level> Upper limit for the area
        Range:  -256 dBm  to  256 dBm
        *RST:  depends on channel bandwidth and area number
        Default unit: dBm
        <RBW> K030 | K100 | M1
        Resolution bandwidth to be used for the area
        K030: 30 kHz
        K100: 100 kHz
        M1: 1 MHz
        *RST:  K030 (<no> = 1) / M1 (<no> = 2 to 12)
        """
        self.cmw_write(f'CONFigure:LTE:MEAS:MEValuation:LIMit:SEMask:LIMit{no}:CBANdwidth{bw10} '
                       f'{enable}, {start_freq}MHz, {stop_freq}MHz, {level}, {rbw}')

    def set_pusch_fr1(self, mcs, rb_size, rb_start):
        """
        Specifies settings related to the PUSCH.
        Parameters:
        <ModScheme> AUTO | BPSK | BPWS | QPSK | Q16 | Q64 | Q256

        Modulation scheme
        AUTO: Auto-detection
        BPSK, BPWS: π/2-BPSK, π/2-BPSK with shaping
        QPSK, Q16, Q64, Q256: QPSK, 16-QAM, 64-QAM, 256-QAM
        *RST: QPSK

        <MappingType> A | B
        *RST: A
        <NRBAuto> OFF | ON

        Automatic detection of <NoRB> and <StartRB>
        *RST: ON
        <NoRB> numeric

        Number of allocated RBs in the measured slot.

        The allowed values depend on the SC spacing and on the chan-
        nel bandwidth, see "Resource block allocation" on page 25.

        *RST: 51
        <StartRB> numeric

        Index of the first allocated RB in the measured slot.
        Range: 0 to max(<NoRB>) - <NoRB>
        *RST: 0
        <NoSymbols> numeric

        Number of allocated OFDM symbols in the measured slot.
        The allowed values depend on the mapping type, see "Symbol
        allocation" on page 25.
        *RST: 14
        <StartSymbol> numeric

        Index of the first allocated symbol in the measured slot.
        The input range depends on the mapping type and the number
        of symbols, see "Symbol allocation" on page 25.
        *RST: 0
        <ConfigType> T1 | T2

        DM-RS setting "dmrs-Type".
        *RST: T1
        <MaxLength> SINGle

        DM-RS setting "maxLength".
        *RST: SING
        <AddPosition> numeric

        DM-RS setting "dmrs-AdditionalPosition".
        Range: 0 to 2
        *RST: 2
        <lZero> numeric
        DM-RS setting l0
        .

        Range: Mapping type A: 2 to 3, type B: 0
        *RST: 2
        """
        _256Q_flag = 2 if mcs == 'Q256' else 0
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:PUSChconfig '
                       f'{mcs}, A, OFF, {rb_size}, {rb_start}, 14, 0, T1, SING, {_256Q_flag}, 2')

    def set_mcs_lte(self, mcs):
        """
        Selects the modulation scheme used by the measured signal.
        Parameters:
        <ModScheme> AUTO | QPSK | Q16 | Q64 | Q256
        Auto-detection, QPSK, 16-QAM, 64-QAM, 256-QAM
        *RST:  QPSK
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:MODulation:MSCHeme {mcs}')

    def set_rb_size_lte(self, rb_size=100):
        """
        Specifies the number of allocated RBs in the measured slot. For manual RB allocation
        definition, for uplink signals without multi-cluster allocation.
        Parameters:
        <NoRB> For the allowed input range, see Chapter 5.2.11.2, "Uplink
        Resource Block Allocation", on page 925.
        *RST:  100
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:RBALlocation:NRB {rb_size}')

    def set_rb_start_lte(self, rb_start=0):
        """
        Specifies the offset of the first allocated resource block for manual RB allocation defini-
        tion, for uplink signals without multi-cluster allocation.
        Parameters:
        <OffsetRB> For the maximum number of RBs depending on the channel BW,
        see Chapter 5.2.11.2, "Uplink Resource Block Allocation",
        on page 925.
        Range:  0 to maximum number of RBs minus 1
        *RST:  0
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:RBALlocation:ORB {rb_start}')

    def set_rb_auto_detect_lte(self, on_off='ON'):
        """
        Enables or disables the automatic detection of the RB configuration.
        Parameters:
        <Auto> OFF | ON
        OFF: manual definition
        ON: automatic detection
        *RST:  ON
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:RBALlocation:AUTO {on_off}')

    def set_precoding_fr1(self, _type_fr1):
        """
        Specifies whether the signal uses a transform precoding function performing DFT-
        spreading.

        Parameters:
        <OnOff> OFF | ON
        *RST: OFF
        DFTS: ON, CP: OFF
        """
        on_off = 'ON' if _type_fr1 == 'DFTS' else 'OFF'  # DFTS: ON, CP: OFF
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:DFTPrecoding {on_off}')

    def set_phase_compensation_fr1(self, phase_comp='OFF', user_freq=6000000000):
        """
        Specifies the phase compensation applied by the UE during the modulation and
        upconversion.
        Parameters:
        <PhaseComp> OFF | CAF | UDEF
        OFF: no phase compensation
        CAF: phase compensation for carrier frequency
        UDEF: phase compensation for frequency <UserDefFreq>
        *RST:  OFF
        <UserDefFreq> numeric
        Frequency for <PhaseComp> = UDEF
        Range:  0 Hz  to  10E+9 Hz
        *RST:  1.95E+9 Hz
        Default unit: Hz
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:PCOMp {phase_comp}, {user_freq}')

    def set_channel_type_fr1(self, ctype='PUSC'):
        """
        for now only support PSUCH
        <channel_type> PUSCh or PUCCh
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:CTYPe {ctype}')

    def set_uldl_pattern_fr1(self, scs):
        """
        CONFigure:NRSub:MEAS<i>:ULDL:PATTern <SCSpacing>, <DLSlots>,
        <DLSymbols>, <ULSlots>, <ULSymbols>
        CONFigure:NRSub:MEAS<i>:ULDL:PATTern? <SCSpacing>
        Configures the TDD UL-DL pattern for the <SCSpacing>.
        The ranges have dependencies, see "TDD UL-DL configuration" on page 16.
        Parameters:
        <DLSlots> numeric
        Specifies "nrofDownlinkSlots".
        Range:  0  to  38
        <DLSymbols> numeric
        Specifies "nrofDownlinkSymbols".
        Range:  0  to  14
        <ULSlots> numeric
        Specifies "nrofUplinkSlots".
        Range:  1  to  40
        <ULSymbols> numeric
        Specifies "nrofUplinkSymbols".
        Range:  0  to  14
        Parameters for setting and query:
        <SCSpacing> S15K | S30K | S60K
        Subcarrier spacing for which the other settings apply.
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:ULDL:PATTern S{scs}K, 3,0,1,14 ')

    def set_aclr_count_fr1(self, count=5):
        """
        Specifies the statistic count of the measurement. The statistic count is equal to the
        number of measurement intervals per single shot.
        Separate statistic counts for ACLR and spectrum emission mask measurements are
        supported.
        Parameters:
        <StatisticCount> numeric
        Number of measurement intervals (slots)
        Range:  1 slot  to  1000 slots
        *RST:  20 slots
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:SCOunt:SPECtrum:ACLR {count}')

    def set_aclr_count_lte(self, count=5):
        """
        Specifies the statistic count of the measurement. The statistic count is equal to the
        number of measurement intervals per single shot.
        Separate statistic counts for ACLR and spectrum emission mask measurements are
        supported.
        Parameters:
        <StatisticCount> Number of measurement intervals (slots)
        Range:  1 slot  to  1000 slots
        *RST:  20 slots
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:SCOunt:SPECtrum:ACLR {count}')

    def set_aclr_count_wcdma(self, count=5):
        """
        Specifies the statistic count of the measurement. The statistic count is equal to the
        number of measurement intervals per single shot.
        Parameters:
        <StatisticCount> Number of measurement intervals
        Range:  1  to  1000
        *RST:  10
        """
        self.cmw_write(f'CONFigure:WCDMa:MEASurement:MEValuation:SCOunt:SPECtrum {count}')

    def set_sem_count_fr1(self, count=5):
        """
        Specifies the statistic count of the measurement. The statistic count is equal to the
        number of measurement intervals per single shot.
        Separate statistic counts for ACLR and spectrum emission mask measurements are
        supported.
        Parameters:
        <StatisticCount> numeric
        Number of measurement intervals (slots)
        Range:  1 slot  to  1000 slots
        *RST:  20 slots
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:SCOunt:SPECtrum:SEMask {count}')

    def set_sem_count_lte(self, count=5):
        """
        Specifies the statistic count of the measurement. The statistic count is equal to the
        number of measurement intervals per single shot.
        Separate statistic counts for ACLR and spectrum emission mask measurements are
        supported.
        Parameters:
        <StatisticCount> Number of measurement intervals (slots)
        Range:  1 slot  to  1000 slots
        *RST:  20 slots
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:SCOunt:SPECtrum:SEMask {count}')

    def set_sem_count_wcdma(self, count=5):
        """
        DBT
        """
        self.cmw_write(f'CONFigure:WCDMa:MEASurement:MEValuation:SCOunt:SPECtrum:SEMask {count}')

    def set_trigger_threshold_fr1(self, threshold=-20.0):
        """
        Defines the trigger threshold for power trigger sources.
        Parameters:
        <TrigThreshold> numeric
        Range:  -50 dB  to  0 dB
        *RST:  -20 dB
        Default unit: dB (full scale, i.e. relative to reference level minus
        external attenuation)
        """
        self.cmw_write(f'TRIGger:NRSub:MEASurement:MEValuation:THReshold {threshold}')

    def set_trigger_threshold_lte(self, threshold=-20.0):
        """
        Defines the trigger threshold for power trigger sources.
        Parameters:
        <TrigThreshold> numeric
        Range:  -50 dB  to  0 dB
        *RST:  -20 dB
        Default unit: dB (full scale, i.e. relative to reference level minus
        external attenuation)
        """
        self.cmw_write(f'TRIGger:LTE:MEASurement:MEValuation:THReshold {threshold}')

    def set_trigger_threshold_wcdma(self, threshold=-20.0):
        """
        Defines the trigger threshold for power trigger sources.
        Parameters:
        <TrigThreshold> numeric
        Range:  -50 dB  to  0 dB
        *RST:  -20 dB
        Default unit: dB (full scale, i.e. relative to reference level minus
        external attenuation)
        """
        self.cmw_write(f'TRIGger:WCDMa:MEASurement:MEValuation:THReshold {threshold}')

    def set_trigger_threshold_gsm(self, threshold=-20.0):
        """
        Defines the trigger threshold for power trigger sources.
        Parameters:
        <TrigThreshold> numeric
        Range:  -50 dB  to  0 dB
        *RST:  -20 dB
        Default unit: dB (full scale, i.e. relative to reference level minus
        external attenuation)
        """
        self.cmw_write(f'TRIGger:GSM:MEASurement:MEValuation:THReshold {threshold}')

    def set_measurements_enable_all_fr1(self):
        """
        CONFigure:NRSub:MEAS<i>:MEValuation:RESult[:ALL] <EVM>, <MagnitudeError>, <PhaseError>, <InbandEmissions>,
        <EVMversusC>, <IQ>, <EquSpecFlatness>, <TXMeasurement>, <SpecEmMask>, <ACLR>[, <PowerMonitor>, <PowerDynamics>]
        Enables or disables the evaluation of results in the multi-evaluation measurement. This
        command combines most other
        CONFigure:NRSub:MEAS<i>:MEValuation:RESult... commands.
        Parameters:
        <EVM> OFF | ON
        Error vector magnitude
        OFF: Do not evaluate results
        ON: Evaluate results
        *RST:  ON
        <MagnitudeError> OFF | ON
        *RST:  OFF
        <PhaseError> OFF | ON
        *RST:  OFF
        <InbandEmissions> OFF | ON
        *RST:  ON
        <EVMversusC> OFF | ON
        EVM vs. subcarrier
        *RST:  OFF
        <IQ> OFF | ON
        I/Q constellation diagram
        *RST:  OFF
        <EquSpecFlatness> OFF | ON
        Equalizer spectrum flatness
        *RST:  ON
        <TXMeasurement> OFF | ON
        TX measurement statistical overview
        *RST:  ON
        <SpecEmMask> OFF | ON
        Spectrum emission mask
        *RST:  ON
        <ACLR> OFF | ON
        Adjacent channel leakage power ratio
        *RST:  ON
        <PowerMonitor> OFF | ON
        *RST:  OFF
        <PowerDynamics> OFF | ON
        *RST:  OFF
        """
        items_en = 'ON, ON, ON, ON, ON, ON, ON, ON, ON, ON'
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:RESult:ALL {items_en}')

    def set_measurements_enable_all_lte(self):
        """
        CONFigure:NRSub:MEAS<i>:MEValuation:RESult[:ALL] <EVM>, <MagnitudeError>, <PhaseError>, <InbandEmissions>,
        <EVMversusC>, <IQ>, <EquSpecFlatness>, <TXMeasurement>, <SpecEmMask>, <ACLR>[, <PowerMonitor>, <PowerDynamics>]
        Enables or disables the evaluation of results in the multi-evaluation measurement. This
        command combines most other
        CONFigure:NRSub:MEAS<i>:MEValuation:RESult... commands.
        Parameters:
        <EVM> OFF | ON
        Error vector magnitude
        OFF: Do not evaluate results
        ON: Evaluate results
        *RST:  ON
        <MagnitudeError> OFF | ON
        *RST:  OFF
        <PhaseError> OFF | ON
        *RST:  OFF
        <InbandEmissions> OFF | ON
        *RST:  ON
        <EVMversusC> OFF | ON
        EVM vs. subcarrier
        *RST:  OFF
        <IQ> OFF | ON
        I/Q constellation diagram
        *RST:  OFF
        <EquSpecFlatness> OFF | ON
        Equalizer spectrum flatness
        *RST:  ON
        <TXMeasurement> OFF | ON
        TX measurement statistical overview
        *RST:  ON
        <SpecEmMask> OFF | ON
        Spectrum emission mask
        *RST:  ON
        <ACLR> OFF | ON
        Adjacent channel leakage power ratio
        *RST:  ON
        <PowerMonitor> OFF | ON
        *RST:  OFF
        <PowerDynamics> OFF | ON
        *RST:  OFF
        """
        items_en = 'ON, ON, ON, ON, ON, ON, ON, ON, ON, ON'
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:RESult:ALL {items_en}')

    def set_measurements_enable_all_wcdma(self):
        """
        CONFigure:WCDMa:MEAS<i>:MEValuation:RESult[:ALL] <EnableEVM>,
        <EnableMagError>, <EnablePhaseErr>, <EnableACLR>, <EnableEMask>,
        <EnableCDmonitor>, <EnableCDP>, <EnableCDE>, <EnableEVMchip>,
        <EnableMErrChip>, <EnablePhErrChip>, <EnableUEpower>,
        <EnableFreqError>, <EnablePhaseDisc>, <EnablePowSteps>, <EnableBER>[,
        <EnableIQ>, <EnableRCDE>]
        CONFigure:NRSub:MEAS<i>:MEValuation:RESult[:ALL] <EVM>, <MagnitudeError>, <PhaseError>, <InbandEmissions>,
        Enables or disables the evaluation of results and shows or hides the views in the multi-
        evaluation measurement. This command combines all other
        CONFigure:WCDMa:MEAS<i>:MEValuation:RESult... commands.
        Parameters:
        <EnableEVM> OFF | ON
        Error vector magnitude
        OFF: Do not evaluate results, hide the view
        ON: Evaluate results and show the view
        *RST:  ON
        <EnableMagError> OFF | ON
        Magnitude error
        *RST:  OFF
        <EnablePhaseErr> OFF | ON
        Phase error
        *RST:  OFF
        <EnableACLR> OFF | ON
        Adjacent channel leakage power ratio
        *RST:  ON
        <EnableEMask> OFF | ON
        Spectrum emission mask
        *RST:  ON
        <EnableCDmonitor> OFF | ON
        Code domain monitor
        *RST:  ON
        <EnableCDP> OFF | ON
        Code domain power
        *RST:  ON
        <EnableCDE> OFF | ON
        Code domain error
        *RST:  OFF
        <EnableEVMchip> OFF | ON
        EVM vs. chip
        *RST:  ON
        <EnableMErrChip> OFF | ON
        Magnitude error vs. chip
        *RST:  OFF
        <EnablePhErrChip> OFF | ON
        Phase error vs. chip
        *RST:  OFF
        <EnableUEpower> OFF | ON
        UE power
        *RST:  ON
        <EnableFreqError> OFF | ON
        Frequency error
        *RST:  ON
        <EnablePhaseDisc> OFF | ON
        Phase discontinuity
        *RST:  OFF
        <EnablePowSteps> OFF | ON
        Power steps
        *RST:  ON
        <EnableBER> OFF | ON
        Bit error rate
        *RST:  OFF
        <EnableIQ> OFF | ON
        I/Q constellation diagram
        *RST:  OFF
        <EnableRCDE> OFF | ON
        Relative CDE
        *RST:  OFF
        """
        items_en = 'ON, ON, ON, ON, ON, ON, ON, ON, ON, ON, ON, ON, ON, ON, ON, ON, ON, ON'
        self.cmw_write(f'CONFigure:WCDMa:MEASurement:MEValuation:RESult:ALL {items_en}')

    def set_measurements_enable_all_gsm(self):
        """
        CONFigure:GSM:MEAS<i>:MEValuation:RESult[:ALL] <PvT>, <EVM>,
        <MagnitudeError>, <PhaseError>, <IQ>, <ACPModFrequency>,
        <ACPModTime>, <ACPSwitFreq>, <ACPSwitTime>, <ModScalar>, <BER>,
        <AMPM>
        Enables or disables the evaluation of results and shows or hides the views in the multi-
        evaluation measurement. This command combines all other
        CONFigure:GSM:MEAS<i>:MEValuation:RESult... commands.
        Parameters:
        <PvT> OFF | ON
        Power vs. time
        ON: Evaluate results and show the view
        OFF: Do not evaluate results, hide the view (if applicable)
        *RST:  ON
        <EVM> OFF | ON
        Error vector magnitude
        *RST:  ON
        <MagnitudeError> OFF | ON
        Magnitude error
        *RST:  OFF
        <PhaseError> OFF | ON
        Phase error
        *RST:  ON
        <IQ> OFF | ON
        I/Q constellation
        *RST:  OFF
        <ACPModFrequency>OFF | ON
        ACP spectrum modulation frequency
        *RST:  ON
        <ACPModTime> OFF | ON
        ACP spectrum modulation time
        *RST:  OFF
        <ACPSwitFreq> OFF | ON
        ACP spectrum switching frequency
        *RST:  ON
        <ACPSwitTime> OFF | ON
        ACP spectrum switching time
        *RST:  OFF
        <ModScalar> OFF | ON
        Scalar modulation results
        *RST:  ON
        <BER> OFF | ON
        Bit error rate
        *RST:  OFF
        <AMPM> OFF | ON
        AM-PM
        *RST:  OFF
        """
        items_en = 'ON, ON, ON, ON, ON, ON, ON, ON, ON, ON, OFF, ON'
        self.cmw_write(f'CONFigure:GSM:MEASurement:MEValuation:RESult:ALL {items_en}')

    def set_measured_subframe_fr1(self, subframe=10):
        """
        Configures how many subframes of each radio frame are measured.
        Parameters:
        <NoSubframe> decimal
        Range:  1  to  10
        *RST:  10
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:NSUBframes {subframe}')

    def set_measured_subframe_lte(self, offset=2, length=10, subframe=0):
        """
        CONFigure:LTE:MEAS<i>:MEValuation:MSUBframes <SubframeOffset>, <SubframeCount>, <MeasSubframe>
        Configures the scope of the measurement, i.e. which subframes are measured.
        Parameters:
        <SubframeOffset> Start of the measured subframe range relative to the trigger
        event
        Range:  0  to  9
        *RST:  0
        <SubframeCount> Length of the measured subframe range
        Range:  1  to  320
        *RST:  1
        <MeasSubframe> Subframe containing the measured slots for modulation and
        spectrum results
        Range:  0  to  <SubframeCount>-1
        *RST:  0
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:MSUBframes {offset}, {length}, {subframe}')

    def set_measured_slot_fr1(self, measured_slot='ALL'):
        """
        CONFigure:NRSub:MEAS<i>:MEValuation:MSLot <MeasureSlot>[, <MeasSlotNo>]
        Selects which slots of the measured subframe range are evaluated.
        Parameters:
        <MeasureSlot> ALL | UDEF
        ALL
        Evaluate all slots of the measured subframe range.
        UDEF
        Evaluate only one slot of the measured subframe range,
        selected via <MeasSlotNo>.
        *RST:  ALL
        <MeasSlotNo> numeric
        Index of a single slot, for <MeasureSlot> = UDEF.
        The allowed maximum is limited by <no of measured sub-
        frames> * <no of slots per subframe> - 1.
        The number of slots per subframe depends on the SC spacing:
        15 kHz one slot, 30 kHz two slots, 60 kHz four slots.
        Range:  0  to  39
        *RST:  0

        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:MSLot {measured_slot}')

    def set_measured_slot_lte(self, measured_slot='ALL'):
        """
        CONFigure:LTE:MEAS<i>:MEValuation:MSLot <MeasureSlot>
        Selects which slots of the "Measure Subframe" are measured.
        Parameters:
        <MeasureSlot> MS0 | MS1 | ALL
        MS0: slot number 0 only
        MS1: slot number 1 only
        ALL: both slots
        *RST:  ALL

        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:MSLot {measured_slot}')

    def set_scenario_activate_fr1(self, scenario='SAL'):
        """
        CONF:NRS:MEAS:SCEN:ACT <senario>
        This cannot find from the manual of R&S
        guess:
        <senario>  SAL | CSP
        SAL: StandAlone
        CSP: CombindSignalPath

        As to CMW100, it only can select SAL.If selecting CSP, it will shutdown
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:SCENario:ACT {scenario}')

    def set_scenario_activate_lte(self, scenario='SAL'):
        """
        CONF:LTE:MEAS:SCEN:ACT <senario>
        This cannot find from the manual of R&S
        guess:
        <senario>  SAL | CSP
        SAL: StandAlone
        CSP: CombindSignalPath

        As to CMW100, it only can select SAL.If selecting CSP, it will shutdown
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:SCENario:ACT {scenario}')

    def set_scenario_activate_gsm(self, scenario='STAN'):
        """
        CONF:GSM:MEAS:SCEN:ACT <senario>
        This cannot find from the manual of R&S
        guess:
        <senario>  STAN | CSP
        STAN: StandAlone
        CSP: CombindSignalPath

        As to CMW100, it only can select SAL.If selecting CSP, it will shutdown
        """
        self.cmw_write(f'CONFigure:GSM:MEASurement:SCENario:ACT {scenario}')

    def set_type_cyclic_prefix_lte(self, cyclic_prefix='NORM'):
        """
        Selects the type of cyclic prefix of the LTE signal.
        For the combined signal path scenario, use CONFigure:LTE:SIGN<i>:CELL:
        CPRefix.
        Parameters:
        <CyclicPrefix> NORMal | EXTended
        *RST:  NORM
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:CPRefix {cyclic_prefix}')

    def get_modulation_average_query_fr1(self):
        """
        Return the current, average and standard deviation single value results.
        The values described below are returned by FETCh and READ commands. CALCulate
        commands return limit check results instead, one value for each result listed below.
        Return values:
        <1_Reliability> decimal
        Reliability Indicator
        <2_OutOfTol> decimal
        Out of tolerance result, i.e. percentage of measurement inter-
        vals of the statistic count for modulation measurements exceed-
        ing the specified modulation limits.
        Default unit: %
        <3_EVM_RMSlow> float
        EVM RMS value, low EVM window position
        Default unit: %
        <4_EVM_RMShigh> float
        EVM RMS value, high EVM window position
        Default unit: %
        <5_EVMpeakLow> float
        EVM peak value, low EVM window position
        Default unit: %
        <6_EVMpeakHigh> float
        EVM peak value, high EVM window position
        Default unit: %
        <7_MErr_RMSlow> float
        Magnitude error RMS value, low EVM window position
        Default unit: %
        <8_MErr_RMShigh> float
        Magnitude error RMS value, high EVM window position
        Default unit: %
        <9_MErrPeakLow> float
        Magnitude error peak value, low EVM window position
        Default unit: %
        <10_MErrPeakHigh> float
        Magnitude error peak value, high EVM window position
        Default unit: %
        <11_PErr_RMSlow> float
        Phase error RMS value, low EVM window position
        Default unit: deg
        <12_PErr_RMSh> float
        Phase error RMS value, high EVM window position
        Default unit: deg
        <13_PErrPeakLow> float
        Phase error peak value, low EVM window position
        Default unit: deg
        <14_PErrPeakHigh> float
        Phase error peak value, high EVM window position
        Default unit: deg
        <15_IQoffset> float
        I/Q origin offset
        Default unit: dBc
        <16_FreqError> float
        Carrier frequency error
        Default unit: Hz
        <17_TimingError> float
        Transmit time error
        Default unit: Ts (basic time unit)
        <18_TXpower> float
        User equipment power
        Default unit: dBm
        <19_PeakPower> float
        User equipment peak power
        Default unit: dBm
        <20_RBpower> float
        RB power
        Default unit: dBm
        <21_EVM_DMRSl> float
        EVM DMRS value, low EVM window position
        Default unit: %
        <22_EVM_DMRSh> float
        EVM DMRS value, high EVM window position
        Default unit: %
        <23_MErr_DMRSl> float
        Magnitude error DMRS value, low EVM window position
        Default unit: %
        <24_MErr_DMRSh> float
        Magnitude error DMRS value, high EVM window position
        Default unit: %
        <25_PErr_DMRS> float
        Phase error DMRS value, low EVM window position
        Default unit: deg
        <26_PErr_DMRSh> float
        Phase error DMRS value, high EVM window position
        Default unit: deg
        <27_FreqErrorPpm> float
        Carrier frequency error in ppm
        Default unit: ppm
        <28_SampleClockE> float
        Sample clock error
        Default unit: ppm
        """
        return self.cmw_query(f'FETCh:NRSub:MEASurement:MEValuation:MODulation:AVERage?')

    def get_modulation_average_query_lte(self):
        """
        Return the current, average and standard deviation single value results.
        The values described below are returned by FETCh and READ commands. CALCulate
        commands return limit check results instead, one value for each result listed below.
        Return values:
        <1_Reliability> decimal
        Reliability Indicator
        <2_OutOfTol> decimal
        Out of tolerance result, i.e. percentage of measurement inter-
        vals of the statistic count for modulation measurements exceed-
        ing the specified modulation limits.
        Default unit: %
        <3_EVM_RMSlow> float
        EVM RMS value, low EVM window position
        Default unit: %
        <4_EVM_RMShigh> float
        EVM RMS value, high EVM window position
        Default unit: %
        <5_EVMpeakLow> float
        EVM peak value, low EVM window position
        Default unit: %
        <6_EVMpeakHigh> float
        EVM peak value, high EVM window position
        Default unit: %
        <7_MErr_RMSlow> float
        Magnitude error RMS value, low EVM window position
        Default unit: %
        <8_MErr_RMShigh> float
        Magnitude error RMS value, high EVM window position
        Default unit: %
        <9_MErrPeakLow> float
        Magnitude error peak value, low EVM window position
        Default unit: %
        <10_MErrPeakHigh> float
        Magnitude error peak value, high EVM window position
        Default unit: %
        <11_PErr_RMSlow> float
        Phase error RMS value, low EVM window position
        Default unit: deg
        <12_PErr_RMSh> float
        Phase error RMS value, high EVM window position
        Default unit: deg
        <13_PErrPeakLow> float
        Phase error peak value, low EVM window position
        Default unit: deg
        <14_PErrPeakHigh> float
        Phase error peak value, high EVM window position
        Default unit: deg
        <15_IQoffset> float
        I/Q origin offset
        Default unit: dBc
        <16_FreqError> float
        Carrier frequency error
        Default unit: Hz
        <17_TimingError> float
        Transmit time error
        Default unit: Ts (basic time unit)
        <18_TXpower> float
        User equipment power
        Default unit: dBm
        <19_PeakPower> float
        User equipment peak power
        Default unit: dBm
        <20_RBpower> float
        RB power
        Default unit: dBm
        <21_EVM_DMRSl> float
        EVM DMRS value, low EVM window position
        Default unit: %
        <22_EVM_DMRSh> float
        EVM DMRS value, high EVM window position
        Default unit: %
        <23_MErr_DMRSl> float
        Magnitude error DMRS value, low EVM window position
        Default unit: %
        <24_MErr_DMRSh> float
        Magnitude error DMRS value, high EVM window position
        Default unit: %
        <25_PErr_DMRS> float
        Phase error DMRS value, low EVM window position
        Default unit: deg
        <26_PErr_DMRSh> float
        Phase error DMRS value, high EVM window position
        Default unit: deg
        <27_GainImbal> Gain imbalance
        Default unit: dB
        <28_QuadError> Quadrature error
        Default unit: deg
        <29_EVM_SRS> Error vector magnitude result for SRS signals
        Default unit: %
        """
        return self.cmw_query(f'READ:LTE:MEASurement:MEValuation:MODulation:AVERage?')

    def get_modulation_average_query_wcdma(self):
        """
        Return the current, average, maximum and standard deviation single value results.
        The return values described below are returned by FETCh and READ commands.
        CALCulate commands return limit check results instead, one value for each of the
        first 14 results listed below. The TX time alignment is only returned by FETCh and
        READ commands.
        The ranges indicated below apply to all results except standard deviation results. The
        minimum for standard deviation results equals 0. The maximum equals the width of the
        indicated range divided by two. Exceptions are explicitly stated.
        The number to the left of each result parameter is provided for easy identification of the
        parameter position within the result array.
        Suffix:
        <c>
        .
        1..2
        Selects the carrier to be queried - only relevant for dual carrier
        HSUPA
        Return values:
        <1_Reliability> Reliability Indicator
        <2_EVMrms>
        <3_EVMpeak>
        Error vector magnitude RMS and peak value
        Range:  0 %  to  100 %
        Default unit: %
        <4_MagErrorRMS> Magnitude error RMS value
        Range:  0 %  to  100 %
        Default unit: %
        <5_MagErrorPeak> Magnitude error peak value
        Range:  -100 % to 100 % (AVERage: 0% to 100 %, SDEVia-
        tion: 0 % to 50 %)
        Default unit: %
        <6_PhErrorRMS> Phase error RMS value
        Range:  0 deg  to  180 deg
        Default unit: deg
        <7_PhErrorPeak> Phase error peak value
        Range:  -180 deg to 180 deg (AVERage: 0 deg to 180 deg,
        SDEViation: 0 deg to 90 deg)
        Default unit: deg
        <8_IQoffset> I/Q origin offset
        Range:  -100 dB  to  0 dB
        Default unit: dB
        <9_IQimbalance> I/Q imbalance
        Range:  -100 dB  to  0 dB
        Default unit: dB
        <10_CarrFreqErr> Carrier frequency error
        Range:  -60000 Hz  to  60000 Hz
        Default unit: Hz
        <11_TransTimeErr> Transmit time error
        Range:  -250 chips  to  250 chips
        Default unit: chip
        <12_UEpower> User equipment power
        Range:  -100 dBm  to  55 dBm
        Default unit: dBm
        <13_PowerSteps> User equipment power step
        Range:  -50 dB  to  50 dB
        Default unit: dB
        <14_PhaseDisc> Phase discontinuity
        Range:  -180 deg  to  180 deg
        Default unit: deg
        <15_TxTimeAlign> Time difference between the two UL carriers
        Range:  -150 chips  to  100 chips
        Default unit: chip
        """
        return self.cmw_query(f'READ:WCDMa:MEASurement:MEValuation:MODulation:AVERage?')

    def get_modulation_average_query_gsm(self):
        """
        Returns the average single slot modulation results of the multi-evaluation measure-
        ment.
        The values described below are returned by FETCh and READ commands. CALCulate
        commands return limit check results instead, one value for each result listed below.
        The number to the left of each result parameter is provided for easy identification of the
        parameter position within the result array.
        Return values:
        <1_Reliability> Reliability Indicator
        <2_OutOfTolerance> Percentage of measurement intervals / bursts of the statistic
        count (CONFigure:GSM:MEAS<i>:MEValuation:SCOunt:
        MODulation) exceeding the specified modulation limits.
        Range:  0 %  to  100 %
        Default unit: %
        <3_EVMRMS>
        <4_EVMpeak>
        Error vector magnitude RMS and peak value
        Range:  0 %  to  100 %
        Default unit: %
        <5_MagErrorRMS>
        <6_MagErrorPeak>
        Magnitude error RMS and peak value
        Range:  0 %  to  100 %
        Default unit: %
        <7_PhaseErrorRMS>
        <8_PhaseErrorPeak>
        Phase error RMS and peak value
        Range:  0 deg  to  180 deg
        Default unit: deg
        <9_IQoffset> I/Q origin offset
        Range:  -100 dB  to  0 dB
        Default unit: dB
        <10_IQimbalance> I/Q imbalance
        Range:  -100 dB  to  0 dB
        Default unit: dB
        <11_FrequencyError> Carrier frequency error
        Range:  -56000 Hz  to  56000 Hz
        Default unit: Hz
        <12_TimingError> Transmit time error
        Range:  -100 Sym  to  100 Sym
        Default unit: Symbol
        <13_BurstPower> Burst power
        Range:  -100 dBm  to  55 dBm
        Default unit: dBm
        <14_AMPMdelay> AMPM delay (determined for 8PSK and 16-QAM modulation
        only - for GMSK zeros are returned)
        Range:  -0.9225E-6 s  to  0.9225E-6 s
        Default unit: s
        """
        return self.cmw_query(f'READ:GSM:MEASurement:MEValuation:MODulation:AVERage?')

    def get_aclr_average_query_fr1(self):
        """
        Returns the relative ACLR values for NR standalone, as displayed in the table below
        the ACLR diagram. The current and average values can be retrieved.
        See also Chapter 4.2.8, "View Spectrum ACLR", on page 39.
        The values described below are returned by FETCh and READ commands. CALCulate
        commands return limit check results instead, one value for each result listed below.
        Return values:
        <Reliability> decimal
        Reliability Indicator
        <UTRA2neg> float
        ACLR for the second UTRA channel with lower frequency
        Default unit: dB
        <UTRA1neg> float
        ACLR for the first UTRA channel with lower frequency
        Default unit: dB
        <NRneg> float
        ACLR for the first NR channel with lower frequency
        Default unit: dB
        <Carrier> float
        Power in the allocated NR channel
        Default unit: dBm
        <NRpos> float
        ACLR for the first NR channel with higher frequency
        Default unit: dB
        <UTRA1pos> float
        ACLR for the first UTRA channel with higher frequency
        Default unit: dB
        <UTRA2pos> float
        ACLR for the second UTRA channel with higher frequency
        Default unit: dB
        """
        return self.cmw_query(f'FETCh:NRSub:MEASurement:MEValuation:ACLR:AVERage?')

    def get_aclr_average_query_lte(self):
        """
        Returns the relative ACLR values for NR standalone, as displayed in the table below
        the ACLR diagram. The current and average values can be retrieved.
        See also Chapter 4.2.8, "View Spectrum ACLR", on page 39.
        The values described below are returned by FETCh and READ commands. CALCulate
        commands return limit check results instead, one value for each result listed below.
        Return values:
        <Reliability> decimal
        Reliability Indicator
        <UTRA2neg> float
        ACLR for the second UTRA channel with lower frequency
        Default unit: dB
        <UTRA1neg> float
        ACLR for the first UTRA channel with lower frequency
        Default unit: dB
        <NRneg> float
        ACLR for the first NR channel with lower frequency
        Default unit: dB
        <Carrier> float
        Power in the allocated NR channel
        Default unit: dBm
        <NRpos> float
        ACLR for the first NR channel with higher frequency
        Default unit: dB
        <UTRA1pos> float
        ACLR for the first UTRA channel with higher frequency
        Default unit: dB
        <UTRA2pos> float
        ACLR for the second UTRA channel with higher frequency
        Default unit: dB
        """
        return self.cmw_query(f'FETCh:LTE:MEASurement:MEValuation:ACLR:AVERage?')

    def get_aclr_average_query_wcdma(self):
        """
        Returns the ACLR power and spectrum emission single value results of the multi-eval-
        uation measurement. The current, average and maximum values can be retrieved.
        See also Chapter 3.2.6.8, "Detailed Views: ACLR", on page 735 and Chapter 3.2.6.9,
        "Detailed Views: Spectrum Emission Mask", on page 737
        The return values described below are returned by FETCh and READ commands.
        CALCulate commands return limit check results instead, one value for each of the
        results 1 to 18, 29 and 30 listed below. The frequency positions are only returned by
        FETCh and READ commands.
        The number to the left of each result parameter is provided for easy identification of the
        parameter position within the result array.
        Query parameters:
        <ACLRMode> ABSolute | RELative
        ABSolute: ACLR power displayed in dBm as absolute value
        RELative: ACLR power displayed in dB relative to carrier power
        Query parameter is only relevant for FETCh and READ com-
        mands. CALCulate commands return a limit check independent
        from the used <ACLRMode>.
        Return values:
        <1_Reliability> Reliability Indicator
        <2_CarrierPower> Power at the nominal carrier UL frequency
        Range:  -100 dBm  to  55 dBm
        Default unit: dBm
        <3_ACLRminus2>
        <4_ACLRminus1>
        <5_ACLRplus1>
        <6_ACLRplus2>
        Power of the adjacent channels (±1 st  adjacent channels at ±5
        MHz from the UL frequency, ±2 nd  adjacent channels at ±10 MHz
        from the UL frequency)
        Range:  -100 dBm  to  55 dBm
        Default unit: dBm
        <7_OBW> Occupied bandwidth
        Range:  0 MHz  to  10 MHz
        Default unit: Hz
        <8_MarginABIJ>
        <9_MarginBCJK>
        <10_MarginCDKL>
        <11_MarginEFMN>
        <12_MarginFENM>
        <13_MarginDCLK>
        <14_MarginCBKJ>
        <15_MarginBAJI>
        Margin between 1 MHz trace and limit line in the eight emission
        mask areas. A positive result indicates that the trace is located
        above the limit line, i.e. the limit is exceeded.
        Range:  -100 dB  to  90 dB
        Default unit: dB
        <16_UEpower> User equipment power
        Range:  -100 dBm  to  55 dBm
        Default unit: dBm
        <17_MarginHAD>
        <18_MarginHDA>
        Margin between 1 MHz trace and limit line H. A positive result
        indicates that the trace is located above the limit line, i.e. the
        limit is exceeded.
        Range:  -130 dB  to  130 dB
        Default unit: dB
        <19_FreqABIJ>
        <20_FreqBCJK>
        <21_FreqCDKL>
        <22_FreqEFMN>
        <23_FreqFENM>
        <24_FreqDCLK>
        <25_FreqCBKJ>
        <26_FreqBAJI>
        <27_FreqHAD>
        <28_FreqHDA>
        Frequency offsets between the margin points and the center fre-
        quency in the 10 emission mask areas.
        These values are only returned for FETCh and READ commands.
        They are skipped in CALCulate commands.
        Range:  -12500 kHz to 12500 kHz (for DC HSUPA: -19500
        kHz to 19500 kHz)
        Default unit: Hz
        <29_CarrierPowerL>
        <30_CarrierPowerR>
        Power at the nominal carrier frequency; left/right carrier of the
        dual carrier HSPA connection
        Range:  -90 dBm  to  0 dBm
        Default unit: dBm
        """
        return self.cmw_query(f'FETCh:WCDMa:MEASurement:MEValuation:SPECtrum:AVERage?')

    def get_orfs_modulation_gsm(self):
        """
        Returns the average burst power measured at a series of frequencies. The frequencies
        are determined by the offset values defined via the command CONFigure:GSM:
        MEAS<i>:MEValuation:SMODulation:OFRequence. All defined offset values are
        considered (irrespective of their activation status).
        The values described below are returned by FETCh and READ commands. CALCulate
        commands return limit check results instead, one value for each result listed below.
        The number to the left of each result parameter is provided for easy identification of the
        parameter position within the result array.
        Return values:
        <1_Reliability> Reliability Indicator
        <2_PowOffsetM19>
        ...
        <21_PowOffsetM0>
        <22_PowCarrier>
        <23_PowOffsetP0> ...
        <42_PowOffsetP19>
        <PowOffsetM/P n> refers to the average burst power at the
        carrier frequency minus/plus the frequency offset value number
        n.
        Range:  -100 dB  to  100 dB
        Default unit: dB
        """
        return self.cmw_query('FETCh:GSM:MEASurement:MEValuation:SMODulation:FREQuency?')

    def get_orfs_switching_gsm(self):
        """
        Returns the maximum burst power measured at a series of frequencies. The frequen-
        cies are determined by the offset values defined via the command CONFigure:GSM:
        MEAS<i>:MEValuation:SSWitching:OFRequence. All defined offset values are
        considered (irrespective of their activation status).
        The values described below are returned by FETCh and READ commands. CALCulate
        commands return limit check results instead, one value for each result listed below.
        The number to the left of each result parameter is provided for easy identification of the
        parameter position within the result array.
        Return values:
        <1_Reliability> Reliability Indicator
        <2_PowOffsetM19>
        ...
        <21_PowOffsetM0>
        <22_PowCarrier>
        <23_PowOffsetP0> ...
        <42_PowOffsetP19>
        <PowOffset M/P n> refers to the maximum burst power at
        the carrier frequency minus/plus the frequency offset value num-
        ber n.
        Range:  -100 dBm  to  55 dBm
        Default unit: dBm
        """
        return self.cmw_query('FETCh:GSM:MEASurement:MEValuation:SSWitching:FREQuency?')

    def get_in_band_emission_query_fr1(self):
        """
        Return the limit line margin results. The CURRent margin indicates the minimum (verti-
        cal) distance between the inband emissions limit line and the current trace. A negative
        result indicates that the limit is exceeded.
        The AVERage, EXTReme and SDEViation values are calculated from the current mar-
        gins. The margin results cannot be displayed at the GUI.
        Return values:
        <Reliability> decimal
        Reliability Indicator
        <OutOfTolerance> decimal
        Out of tolerance result, i.e. percentage of measurement inter-
        vals of the statistic count for modulation measurements exceed-
        ing the specified modulation limits.
        Default unit: %
        <Margin> float
        Margin over all non-allocated RBs (scope of general limit com-
        ponent)
        Default unit: dB
        <IQImage> float
        Margin at image frequencies of allocated RBs (scope of IQ
        image limit component)
        Default unit: dB
        <CarrLeakage> float
        Margin at the carrier frequency (scope of IQ offset limit compo-
        nent)
        Default unit: dB
        """
        return self.cmw_query(f'FETCh:NRSub:MEASurement:MEValuation:IEMission:MARGin:AVERage?')

    def get_in_band_emission_query_lte(self):
        """
        Return the limit line margin results. The CURRent margin indicates the minimum (verti-
        cal) distance between the inband emissions limit line and the current trace. A negative
        result indicates that the limit is exceeded.
        The AVERage, EXTReme and SDEViation values are calculated from the current mar-
        gins. The margin results cannot be displayed at the GUI.
        Return values:
        <Reliability> decimal
        Reliability Indicator
        <OutOfTolerance> decimal
        Out of tolerance result, i.e. percentage of measurement inter-
        vals of the statistic count for modulation measurements exceed-
        ing the specified modulation limits.
        Default unit: %
        <Margin> float
        Margin over all non-allocated RBs (scope of general limit com-
        ponent)
        Default unit: dB
        <IQImage> float
        Margin at image frequencies of allocated RBs (scope of IQ
        image limit component)
        Default unit: dB
        <CarrLeakage> float
        Margin at the carrier frequency (scope of IQ offset limit compo-
        nent)
        Default unit: dB
        """
        return self.cmw_query(f'FETCh:LTE:MEASurement:MEValuation:IEMission:MARGin:AVERage?')

    def get_flatness_extreme_query_fr1(self):
        """
        Return current, average, extreme and standard deviation single value results of the
        equalizer spectrum flatness measurement. See also Chapter 4.7.6, "Equalizer Spec-
        trum Flatness Limits", on page 72.
        Return values:
        <1_Reliability> decimal
        Reliability Indicator
        <2_OutOfTol> decimal
        Out of tolerance result, i.e. percentage of measurement inter-
        vals of the statistic count for modulation measurements exceed-
        ing the specified modulation limits.
        Default unit: %
        <3_Ripple1> float
        Max (range 1) - min (range 1)
        Default unit: dB
        <4_Ripple2> float
        Max (range 2) - min (range 2)
        Default unit: dB
        <5_MaxR1MinR2> float
        Max (range 1) - min (range 2)
        Default unit: dB
        <6_MaxR2MinR1> float
        Max (range 2) - min (range 1)
        Default unit: dB
        <7_MinR1> float
        Min (range 1)
        Default unit: dB
        <8_MaxR1> float
        Max (range 1)
        Default unit: dB
        <9_MinR2> float
        Min (range 2)
        Default unit: dB
        <10_MaxR2> float
        Max (range 2)
        Default unit: dB
        """
        return self.cmw_query(f'FETCh:NRSub:MEASurement:MEValuation:ESFLatness:EXTReme?')

    def get_flatness_extreme_query_lte(self):
        """
        Return current, average, extreme and standard deviation single value results of the
        equalizer spectrum flatness measurement. See also Chapter 4.7.6, "Equalizer Spec-
        trum Flatness Limits", on page 72.
        Return values:
        <1_Reliability> decimal
        Reliability Indicator
        <2_OutOfTol> decimal
        Out of tolerance result, i.e. percentage of measurement inter-
        vals of the statistic count for modulation measurements exceed-
        ing the specified modulation limits.
        Default unit: %
        <3_Ripple1> float
        Max (range 1) - min (range 1)
        Default unit: dB
        <4_Ripple2> float
        Max (range 2) - min (range 2)
        Default unit: dB
        <5_MaxR1MinR2> float
        Max (range 1) - min (range 2)
        Default unit: dB
        <6_MaxR2MinR1> float
        Max (range 2) - min (range 1)
        Default unit: dB
        <7_MinR1> float
        Min (range 1)
        Default unit: dB
        <8_MaxR1> float
        Max (range 1)
        Default unit: dB
        <9_MinR2> float
        Min (range 2)
        Default unit: dB
        <10_MaxR2> float
        Max (range 2)
        Default unit: dB
        """
        return self.cmw_query(f'FETCh:LTE:MEASurement:MEValuation:ESFLatness:EXTReme?')

    def get_sem_average_query_fr1(self):
        """
        Return the current, average and standard deviation single value results of the spec-
        trum emission measurement.
        The values described below are returned by FETCh and READ commands. CALCulate
        commands return limit check results instead, one value for each result listed below.
        Return values:
        <Reliability> decimal
        Reliability Indicator
        <OutOfTolerance> decimal
        Out of tolerance result, i.e. percentage of measurement inter-
        vals of the statistic count for spectrum emission measurements
        exceeding the specified spectrum emission mask limits.
        Default unit: %
        <OBW> float
        Occupied bandwidth
        Default unit: Hz
        <TXpower> float
        Total TX power in the slot
        Default unit: dBm
        """
        return self.cmw_query(f'FETCh:NRSub:MEASurement:MEValuation:SEMask:AVERage?')

    def get_sem_average_query_lte(self):
        """
        Return the current, average and standard deviation single value results of the spec-
        trum emission measurement.
        The values described below are returned by FETCh and READ commands. CALCulate
        commands return limit check results instead, one value for each result listed below.
        Return values:
        <Reliability> decimal
        Reliability Indicator
        <OutOfTolerance> decimal
        Out of tolerance result, i.e. percentage of measurement inter-
        vals of the statistic count for spectrum emission measurements
        exceeding the specified spectrum emission mask limits.
        Default unit: %
        <OBW> float
        Occupied bandwidth
        Default unit: Hz
        <TXpower> float
        Total TX power in the slot
        Default unit: dBm
        """
        return self.cmw_query(f'FETCh:LTE:MEASurement:MEValuation:SEMask:AVERage?')

    def get_sem_margin_all_query_fr1(self):
        """
        Returns spectrum emission mask margin results. A negative margin indicates that the
        trace is located above the limit line, i.e. the limit is exceeded.
        Results are provided for the current, average and maximum traces. For each trace, 24
        values related to the negative (Neg) and positive (Pos) offset frequencies of emission
        mask areas 1 to 12 are provided. For inactive areas, NCAP is returned.
        Return values:
        <1_Reliability> decimal
        Reliability Indicator
        <2_OutOfTol> decimal
        Out of tolerance result, i.e. percentage of measurement inter-
        vals of the statistic count for spectrum emission measurements
        exceeding the specified spectrum emission mask limits.
        Default unit: %
        <3_CurrNeg1> ...
        <14_CurrNeg12>
        float
        Margin results for current trace, negative offsets
        Default unit: dB
        <15_CurrPos1> ...
        <26_CurrPos12>
        float
        Margin results for current trace, positive offsets
        Default unit: dB
        <27_AvgNeg1> ...
        <38_AvgNeg12>
        float
        Margin results for average trace, negative offsets
        Default unit: dB
        <39_AvgPos1> ...
        <50_AvgPos12>
        float
        Margin results for average trace, positive offsets
        Default unit: dB
        <51_MinNeg1> ...
        <62_MinNeg12>
        float
        Margin results for maximum trace (resulting in minimum mar-
        gins), negative offsets
        Default unit: dB
        <63_MinPos1> ...
        <74_MinPos12>
        float
        Margin results for maximum trace (resulting in minimum mar-
        gins), positive offsets
        Default unit: dB
        """
        return self.cmw_query(f'FETCh:NRSub:MEASurement:MEValuation:SEMask:MARGin:ALL?')

    def get_sem_margin_all_query_lte(self):
        """
        FETCh:LTE:MEASurement:MEValuation:SEMask:MARGin:ALL?
        Returns spectrum emission mask margin results. A negative margin indicates that the
        trace is located above the limit line, i.e. the limit is exceeded.
        Results are provided for the current, average and maximum traces. For each trace, 24
        values related to the negative (Neg) and positive (Pos) offset frequencies of emission
        mask areas 1 to 12 are provided. For inactive areas, NCAP is returned.
        Return values:
        <1_Reliability> decimal
        Reliability Indicator
        <2_OutOfTol> decimal
        Out of tolerance result, i.e. percentage of measurement inter-
        vals of the statistic count for spectrum emission measurements
        exceeding the specified spectrum emission mask limits.
        Default unit: %
        <3_CurrNeg1> ...
        <14_CurrNeg12>
        float
        Margin results for current trace, negative offsets
        Default unit: dB
        <15_CurrPos1> ...
        <26_CurrPos12>
        float
        Margin results for current trace, positive offsets
        Default unit: dB
        <27_AvgNeg1> ...
        <38_AvgNeg12>
        float
        Margin results for average trace, negative offsets
        Default unit: dB
        <39_AvgPos1> ...
        <50_AvgPos12>
        float
        Margin results for average trace, positive offsets
        Default unit: dB
        <51_MinNeg1> ...
        <62_MinNeg12>
        float
        Margin results for maximum trace (resulting in minimum mar-
        gins), negative offsets
        Default unit: dB
        <63_MinPos1> ...
        <74_MinPos12>
        float
        Margin results for maximum trace (resulting in minimum mar-
        gins), positive offsets
        Default unit: dB
        """
        return self.cmw_query(f'FETCh:LTE:MEASurement:MEValuation:SEMask:MARGin?')

    def set_delta_sequence_shift_lte(self, delta=0):
        """
        Specifies the delta sequence shift value (Δ ss ) used to calculate the sequence shift pat-
        tern for PUSCH.
        Parameters:
        <DeltaSeqShPUSCH>Range:  0  to  29
        *RST:  0
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:DSSPusch {delta}')

    def set_ul_dpdch_wcdma(self, dpdch_on='ON'):
        """
        Defines whether the UL DPCH contains a DPDCH.
        For the combined signal path scenario, use CONFigure:WCDMa:SIGN<i>:DL:
        LEVel:DPCH.
        Parameters:
        <DPDCH> OFF | ON
        OFF: DPCCH only
        ON: DPCCH plus DPDCH
        *RST:  ON
        """
        self.cmw_write(f'CONFigure:WCDMa:MEASurement:UESignal:DPDCh {dpdch_on}')

    def set_ul_dpcch_slot_format_wcdma(self, slot_format=0):
        """
        Selects the slot format for the UL DPCCH.
        Parameters:
        <SlotFormat> Range:  0  to  5
        *RST:  0
        """
        self.cmw_write(f'CONFigure:WCDMa:MEASurement:UESignal:SFORmat  {slot_format}')

    def set_scrambling_code_wcdma(self, code=0):
        """
        CONFigure:WCDMa:MEAS<i>:UESignal:CARRier<c>:SCODe <Code>
        Selects the number of the long code that is used to scramble the received uplink
        WCDMA signal.
        For the combined signal path scenario, use CONFigure:WCDMa:SIGN<i>:UL:
        CARRier<c>:SCODe.
        Suffix:
        <c>
        .
        1..2
        Selects the carrier to be queried - only relevant for dual carrier
        HSUPA
        Parameters:
        <Code> Range:  #H0  to  #HFFFFFF
        *RST:  #H0
        """
        self.cmw_write(f'CONFigure:WCDMa:MEASurement:UESignal:SCODe {code}')

    def set_ul_signal_config_wcdma(self, ul_config='WCDM'):
        """
        Selects the uplink signal configuration.
        Parameters:
        <ULConfiguration> QPSK | WCDMa | HSDPa | HSUPa | HSPA | HSPLus | DCHS |
        HDUPlus | DDUPlus | DHDU | 3CHS | 3DUPlus | 3HDU | 4CHS |
        4DUPlus | 4HDU
        QPSK: QPSK signal
        WCDMa: WCDMA R99 signal
        HSDPa: signal with HSDPA-related channels
        HSUPa: signal with HSUPA channels
        HSPA: HSDPA related and HSUPA channels
        HSPLus: HSDPA+ related channels
        HDUPlus: HSDPA+ related and HSUPA channels
        DHDU: dual carrier HSDPA+ and dual carrier HSUPA active
        The following values cannot be set, but can be returned while
        the combined signal path scenario is active:
        DCHS: dual carrier HSDPA+ active
        DDUPlus: dual carrier HSDPA+ and HSUPA active
        3CHS: three carrier HSDPA+ active
        3DUPlus: three carrier HSDPA+ and HSUPA active
        3HDU: three carrier HSDPA+ and dual carrier HSUPA active
        4CHS: four carrier HSDPA+ active
        4DUPlus: four carrier HSDPA+ and HSUPA active
        4HDU: four carrier HSDPA+ and dual carrier HSUPA active
        *RST:  WCDM
        """
        self.cmw_write(f'CONFigure:WCDMa:MEASurement:UESignal:ULConfig {ul_config}')

    def set_spectrum_modulation_evaluation_area_gsm(self):
        """
        Defines the time intervals (evaluation areas) to be used for spectrum modulation mea-
        surements.
        Parameters:
        <Enable1> OFF | ON
        ON: Enable area 1
        OFF: Disable area 1
        *RST:  OFF
        <Start1> Start of evaluation area 1
        Range:  0 Sym  to  146 Sym
        *RST:  6 Sym
        Default unit: Symbol
        <Stop1> Stop of evaluation area 1
        Range:  1 Symbol  to  147 Symbol
        *RST:  45 Symbol
        Default unit: Symbol
        <Enable2> OFF | ON
        ON: Enable area 2
        OFF: Disable area 2
        *RST:  ON
        <Start2> Start of evaluation area 2
        Range:  0 Sym  to  146 Symbol
        *RST:  90 Symbol
        Default unit: Symbol
        <Stop2> Stop of evaluation area 2
        Range:  1 Symbol  to  147 Symbol
        *RST:  129 Symbol
        Default unit: Symbol
        """
        parameters = 'ON, 6, 45, ON, 90, 129'
        self.cmw_write(f'CONFigure:GSM:MEASurement:MEValuation:SMODulation:EARea {parameters}')

    def set_orfs_modulation_measurement_off_gsm(self):
        """
        Defines the frequency offsets to be used for spectrum modulation measurements. The
        offsets are defined relative to the analyzer frequency. Up to 20 offsets can be defined
        and enabled.
        Parameters:
        <FreqOffset0> ...
        <FreqOffset19>
        Set and enable frequency offset.
        Range:  0 Hz  to  3E+6 Hz
        *RST:  Offset 0 to 10 in MHz: 0.1, 0.2, 0.25, 0.4, 0.6, 0.8,
        1, 1.2, 1.4, 1.6, 1.8 (all ON); Offset 11 to 19: 1.9
        MHz (all OFF)
        Default unit: Hz
        Additional parameters: OFF | ON (disables / enables offset using
        the previous/default value)
        """
        freq_sample = f'100KHZ, 200KHZ, 250KHZ, 400KHZ, 600KHZ, 800KHZ, 1600KHZ, 1800KHZ, ' \
                      f'OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF'
        self.cmw_write(f'CONFigure:GSM:MEASurement:MEValuation:SMODulation:OFRequence {freq_sample}')

    def set_orfs_switching_measurement_off_gsm(self):
        """
        <FreqOffset0>, ..., <FreqOffset19>
        Defines the frequency offsets to be used for spectrum switching measurements. The
        offsets are defined relative to the analyzer frequency. Up to 20 offsets can be defined
        and enabled.
        Parameters:
        <FreqOffset0> ...
        <FreqOffset19>
        Set and enable frequency offset.
        Range:  0 Hz  to  3E+6 Hz
        *RST:  Offset 0 to 3 in MHz: 0.4, 0.6, 1.2, 1.8 (all ON); Off-
        set 4 to 19: 1.9 MHz (all OFF)
        Default unit: Hz
        Additional parameters: OFF | ON (disables / enables offset using
        the previous/default value)
        """
        freq_sample = f'400KHZ, 600KHZ, 1200KHZ, 1800KHZ, ' \
                      f'OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF'
        self.cmw_write(f'CONFigure:GSM:MEASurement:MEValuation:Sswitching:OFRequence {freq_sample}')

    def set_training_sequence_gsm(self, tsc):
        """
        Selects the training sequence of the analyzed bursts.
        For the combined signal path scenario, use CONFigure:GSM:SIGN<i>:CELL:BCC.
        Parameters:
        <TSC> OFF | TSC0 | TSC1 | TSC2 | TSC3 | TSC4 | TSC5 | TSC6 |
        TSC7 | TSCA | DUMM
        OFF: Analyze all bursts, irrespective of their training sequence
        TSC0 ... TSC7: Analyze bursts with a particular GSM training
        sequence
        TSCA: Analyze bursts with any of the GSM training sequences
        TSC0 to TSC7
        DUMMY: Analyze GSM-specific dummy bursts
        """
        self.cmw_write(f'CONFigure:GSM:MEASurement:MEValuation:TSEQuence TSC{tsc}')

    def set_modulation_view_gsm(self, mod='GMSK'):
        """
        Defines the expected modulation scheme and burst type in all timeslots and adjusts
        the power/time template accordingly.
        Parameters:
        <Timeslot0> ...
        <Timeslot7>
        ANY | OFF | GMSK | EPSK | ACCess | Q16
        ANY: Any burst type can be analyzed
        OFF: No signal expected
        GMSK: GMSK-modulated normal bursts
        EPSK: 8PSK-modulated normal bursts
        ACCess: Access bursts
        Q16: 16-QAM-modulated normal bursts
        *RST:  ANY
        """
        mod_8 = ", ".join([mod] * 8)
        self.cmw_write(f'CONFigure:GSM:MEASurement:MEValuation:MVIew {mod_8}')

    def set_measured_slot_gsm(self):
        """
        Defines settings for the measured slots.
        For the combined signal path scenario, use CONFigure:GSM:SIGN<i>:MSLot:UL.
        Parameters:
        <SlotOffset> Start of the measurement interval relative to the GSM frame
        boundary
        Range:  0  to  7
        *RST:  0
        <SlotCount> Number of slots to be measured
        Range:  1  to  8
        *RST:  1
        <MeasSlot> Slot to be measured for one-slot measurements
        Range:  0  to  7
        *RST:  0
        """
        parameters = '0, 1, 0'
        self.cmw_write(f'CONFigure:GSM:MEASurement:MEValuation:MSLots {parameters}')

    def set_ca_mode(self, mode='INTRaband'):
        """
        Selects how many component carriers with intra-band contiguous aggregation are
        measured.
        For the combined signal path scenario, use ROUTe:LTE:MEAS<i>:SCENario:
        CSPath.
        Parameters:
        <CAmode> OFF | INTRaband | ICD | ICE
        OFF: only one carrier is measured
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:CAGGregation:MODE {mode}')

    def set_select_carrier(self, carrier='CC1'):
        """
        Selects a component carrier for single-carrier measurements.
        Parameters:
        <MeasCarrier> CC1 | CC2 | CC3 | CC4
        *RST:  CC1
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:CAGGregation:MCARrier:ENHanced {carrier}')

    def set_ca_spacing(self):
        """
        Adjusts the component carrier frequencies, so that the carriers are aggregated contigu-
        ously.
        For the combined signal path scenario, use CONFigure:LTE:SIGN<i>:
        CAGGregation:SET.
        """
        self.cmw_write(f'CONFigure:LTE:MEAS:CAGGregation:ACSPacing')

    def get_pvt_average_query_gsm(self):
        """
        Returns special burst power values for the "Measure Slot".
        The number to the left of each result parameter is provided for easy identification of the
        parameter position within the result array.
        Return values:
        <1_Reliability> Reliability Indicator
        <2_UsefulPartMin>
        <3_UsefulPartMax>
        Minimum and maximum power across the useful part of the
        "Measure Slot".
        Range:  -100 dB  to  100 dB
        Default unit: dB
        <4_Subvector1> ...
        <15_Subvector12>
        Burst power at position in μs: –28 , –18, –10, 0, 2, 4, 538.2,
        540.2, 542.8, 552.8, 560.8, 570.8
        Range:  -100 dB  to  100 dB
        Default unit: dB
        Usage:  Query only
        """
        self.cmw_query(f'FETCh:GSM:MEASurement:MEValuation:PVTime:AVERage:SVECtor?')

    def set_measurement_tx_monitor_enable_lte(self, on_off='ON'):
        """
        Enables or disables the evaluation of results in the multi-evaluation measurement.
        Mnemonic    | Description                      | Mnemonic      | Description
        ------------|----------------------------------| --------------| ------------
        EVMagnitude | Error vector magnitude           | EVMC          | EVM vs. subcarrier
        MERRor      | Magnitude error                  | PERRor        | Phase error
        IEMissions  | Inband emissions                 | IQ            | I/Q constellation diagram
        ESFLatness  | Equalizer spectrum flatness      | TXM           | TX meas. statistical overview
        SEMask      | Spectrum emission mask           | ACLR          | Adj. channel leakage power ratio
        RBATable    | Resource block allocation table  | PMONitor      | Power monitor
        BLER        | Block error ratio                | PDYNamics     | Power dynamics
        -----------------------------------------------------------------------------
        For reset values, see CONFigure:LTE:MEAS<i>:MEValuation:RESult[:ALL].
        Parameters:
        <Enable> OFF | ON
        OFF: Do not evaluate results
        ON: Evaluate results
        *RST:  Depends on measurement
        """
        self.cmw_write(f'CONFigure:LTE:MEAS:MEV:RES:PMONitor {on_off}')

    def set_screenshot_format(self, f_format="PNG"):
        """
        HCOPy:DEVice:FORMat <format>

        :param f_format: BMP | JPG | PNG
        :return:
        """
        self.cmw_write(f'HCOPy:DEVice:FORMat {f_format}')
        # if f_format in ["BMP", "JPG", "PNG"]:
        #     cmd = f'HCOPy:DEVice:FORMat {f_format}'
        #     self._Send(cmd)
        # else:
        #     self._logger.error(f'HCOPy:DEVice:FORMat {f_format}, parameter error')

    def query_screenshot(self):
        """
        HCOPy:DATA? or HCOPy:INTerior:DATA?
        Use low level commands to get bytes for screenshot raw data
        Only support PNG format

        :return: PNG block data of screenshot
        """
        return self.cmw_query_2("HCOPy:IMM?")

    # self.handle.sendall("HCOPy:DATA?\r\n".encode('utf-8'))
    # resp = None
    # timeout_count = 0
    # timeout_max = 30
    # while True:
    #     try:
    #         resp_tmp = self.handle.recv(self.SOCKET_BUFFER_SIZE)
    #         if resp is None:
    #             resp = resp_tmp
    #         else:
    #             resp += resp_tmp
    #         if len(resp_tmp) < self.SOCKET_BUFFER_SIZE:
    #             break
    #     except socket.timeout:
    #         self._logger.error('Socket Timeout')
    #         timeout_count += 1
    #         if timeout_count > timeout_max:
    #             self._logger.error('Socket Timeout exceeded max trys')
    # return resp[resp.find(b'\x89PNG'):]

    def get_cc2_freq_query(self):
        return self.cmw_query(f'CONFigure:LTE:MEASurement:RFSettings:CC2:FREQuency?')

    def get_ca_freq_low_query(self):
        """
        Queries the lower edge of the aggregated bandwidth.
        Return values:
        <FrequencyLow> Default unit: Hz
        """
        return self.cmw_query(f'CONFigure:LTE:MEASurement:CAGGregation:FREQuency:AGGRegated:LOW?')

    def get_ca_freq_center_query(self):
        """
        Queries the center frequency of the aggregated bandwidth.
        Return values:
        <FrequencyLow> Default unit: Hz
        return unit: kHz
        """
        freq_str = self.cmw_query(f'CONFigure:LTE:MEASurement:CAGGregation:FREQuency:AGGRegated:CENTer?')
        freq_int = int(eval(freq_str) / 1000)
        return freq_int

    def get_ca_freq_high_query(self):
        """
        Queries the high edge of the aggregated bandwidth.
        Return values:
        <FrequencyLow> Default unit: Hz
        """
        return self.cmw_query(f'CONFigure:LTE:MEASurement:CAGGregation:FREQuency:AGGRegated:HIGH?')


def main():
    test = CMW('CMW100')
    test.set_screenshot_format()
    fileData = test.query_screenshot()

    # newFile = open('test.png', "wb")
    # newFile.write(fileData)
    # newFile.close()


if __name__ == '__main__':
    main()
