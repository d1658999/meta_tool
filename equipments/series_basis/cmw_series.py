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
        return self.cmw_query(f'SYSTem:BASE:OPTion:VERSion? {application}')

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

    def set_gprf_if_filter(self, flt='BAND'):
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
        self.cmw_write(f'CONFigure:GPRF:MEASurement:POWer:FILTer:BANDpass:BWIDth {bw}MHz')

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
        self.cmw_write(f'ROUTe:GPRF:MEASurement:SCENario:SALone R1{port_tx} RX1')

    def set_gprf_rf_output_path(self, port_rx=18):
        """
        Activates the standalone scenario and selects the output path for the generated RF
        signal.
        For possible connector and converter values, see Chapter 2.5.1.2, "Values for Signal
        Path Selection", on page 65.
        Parameters:
        <TXConnector> RF connector for the output path
        <RFConverter> TX module for the output path
        """
        self.cmw_write(f'ROUTe:GPRF:GENerator:SCENario:SALone R1{port_rx} TX1')

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
        self.cmw_write(f'CONFigure:GPRF:MEASurement:POWer:SCOunt {count}')

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
        self.cmw_write(f'CONFigure:GPRF:MEASurement:POWer:REPetition {repetition}')

    def set_gprf_power_list_mode(self, on_off='OFF'):
        """
        Enables or disables the list mode for the power measurement.
        Parameters:
        <EnableListMode> OFF | ON
        OFF: list mode off
        ON: list mode on
        *RST:  OFF
        """
        self.cmw_write(f'CONFigure:GPRF:MEASurement:POWer:LIST {on_off}')

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
        self.cmw_write(f'TRIGger:GPRF:MEASurement:POWer:SOURce {source}')

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
        # it also can use: <CONFigure:GPRF:MEASurement:POWer:TRIGger:SLOPe>
        self.cmw_write(f'TRIGger:GPRF:MEASurement:POWer:SLOPe {slope}')

    def set_gprf_trigger_step_length(self, length='576.9230769E-6'):
        """
        Sets the time between the beginning of two consecutive measurement lengths.
        Parameters:
        <StepLength> numeric
        Range:  <MeasLength>  to  1 s
        *RST:  576.9230769E-6 s
        Default unit: s
        """
        self.cmw_write(f'CONFigure:GPRF:MEASurement:POWer:SLENgth {length}')

    def set_gprf_trigger_measure_length(self, length='576.9230769E-6'):
        """
        Sets the length of the evaluation interval used to measure a single set of current power
        results.
        The measurement length cannot be greater than the step length.
        Parameters:
        <MeasLength> numeric
        Default unit: s
        """
        self.cmw_write(f'CONFigure:GPRF:MEASurement:POWer:MLENgth {length}')

    def set_gprf_trigger_offset(self, offset=100E-6):
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

    def set_gprf_trigger_mode(self, mode='SWE'):
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

    def set_gprf_expect_power(self, exp_nom_pwr=0):
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

    def set_gprf_rx_level(self, rx_level=-70):
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

    def set_gprf_rf_setting_user_margin(self, margin=0):
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

    def set_gprf_rf_setting_external_input_attenuation(self, attenuation):
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

    def set_gprf_rf_setting_external_output_attenuation(self, attenuation):
        """
        Defines an external attenuation (or gain, if the value is negative), to be applied to the
        output connector.
        Parameters:
        <ExtRFOutAtt> numeric
        Range:  -50 dB  to  90 dB
        *RST:  0 dB
        Default unit: dB
        """
        self.cmw_write(f'SOURce:GPRF:GENerator:RFSettings:EATTenuation {attenuation}')

    def set_gprf_tx_freq(self, tx_freq):  # this is KHz
        """
        Selects the center frequency of the RF analyzer.
        For the supported frequency range, see Chapter 3.11.5, "Frequency Ranges",
        on page 395.
        Parameters:
        <AnalyzerFreq> numeric
        Default unit: Hz
        """
        self.cmw_write(f'CONFigure:GPRF:MEASurement:RFSettings:FREQuency {tx_freq}KHz')

    def set_gprf_rx_freq(self, rx_freq):  # this is KHz
        """
        Sets the frequency of the unmodulated RF carrier.
        For the supported frequency range, see Chapter 2.5.1.3, "Frequency Ranges",
        on page 67.
        Parameters:
        <Frequency> numeric
        Default unit: Hz
        """
        self.cmw_write(f'SOURce:GPRF:GENerator1:RFSettings:FREQuency {rx_freq}KHz')

    def set_gprf_measure_start_on(self):
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
        FETCh:GPRF:MEAS:POWer = INIT:GPRF:MEAS:POWer and then READ:GPRF:MEAS:POWer
        """
        self.cmw_write(f'INIT:GPRF:MEASurement:POWer')

    def set_gprf_generator_base_band_mode(self, mode='ARB'):
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

    def set_gprf_generator_cmw_port_uasge_all(self):
        """
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
        self.cmw_write(f'CONFigure:GPRF:GENerator:CMWS:USAGe:TX:ALL ON, ON, ON, ON, ON, ON, ON, ON')

    def set_gprf_arb_file(self, file_path):
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
        self.cmw_write(f'SOURce:GPRF:GENerator1:ARB:FILE {file_path}')

    def set_gprf_generator_state(self, state='ON'):
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
        return self.cmw_query(f'SOUR:GPRF:GENerator1:STAT {state}')

    def get_gprf_power_state_query(self):
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
        return self.cmw_query('FETC:GPRF:MEASurement:POW:STAT?')

    def get_gprf_power_average_query(self):
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
        return self.cmw_query('FETC:GPRF:MEASurement:POWer:AVER?')

    def get_gprf_arb_file_query(self):
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

    def get_gprf_generator_state_query(self):
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
        self.cmw_write(f'CONFigure:NRSub::MEASurement:ULDL:PERiodicity {periodicity}')

    def set_duplexer_mode_fr1(self, mode='FDD'):
        """
        Selects the duplex mode of the signal: FDD or TDD.
        Parameters:
        <Mode> FDD | TDD
        *RST:  FDD
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:DMODe {mode}')

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

    def set_band_wcdma(self, band):
        """
        Selects the Operating Band (OB) for ver3.0.30.
        Parameters:
        <Band> OB1 | ... | OB14 | OB19 | ... | OB21 | OBS1 | ... | OBS3 | OBL1
        OB1, ..., OB14: Operating Band I to XIV
        OB19, ..., OB21: Operating Band XIX to XXI
        OBS1: Operating Band S
        OBS2: Operating Band S 170 MHz
        OBS3: Operating Band S 190 MHz
        OBL1: Operating Band L
        *RST:  OB1
        CONFigure:WCDMa:MEASurement<i>:CARRier<c>:BAND for ver3.7.22
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

    def set_statistic_count_fr1(self, count=5):
        """
        DBT
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:SCOunt:MODulation {count}')

    def set_statistic_count_lte(self, count=5):
        """
        DBT
        """
        self.cmw_write(f'CONFigure:LTE:MEASurement:MEValuation:SCOunt:MODulation {count}')

    def set_statistic_count_wcdma(self, count=5):
        """
        Specifies the statistic count of the measurement. The statistic count is equal to the
        number of measurement intervals per single shot.
        Parameters:
        <StatisticCount> Number of measurement intervals
        Range:  1  to  1000
        *RST:  10
        """
        self.cmw_write(f'CONFigure:WCDMa:MEASurement:MEValuation:SCOunt:MODulation {count}')

    def set_statistic_count_gsm(self, count=5):
        """
        DBT
        """
        self.cmw_write(f'CONFigure:GSM:MEASurement:MEValuation:SCOunt:MODulation {count}')

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
        self.cmw_write(f'CONFigure:NRSub:MEASurement:RFSettings:FREQuency {tx_freq}KHz')

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
        self.cmw_write(f'CONFigure:LTE:MEASurement:RFSettings:FREQuency {tx_freq}KHz')

    def set_tx_freq_wcdma(self, tx_freq):  # this is KHz
        """
        DBT
        """
        self.cmw_write(f'CONFigure:WCDMa:MEASurement:RFSettings:FREQuency {tx_freq}KHz')

    def set_tx_freq_gsm(self, tx_freq):  # this is KHz
        """
        DBT
        """
        self.cmw_write(f'CONFigure:GSM:MEASurement:RFSettings:FREQuency {tx_freq}KHz')

    def set_plc_fr1(self, id=0):
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
        self.cmw_write(f'CONFigure:NRSub:MEASurement:PLCid {id}')

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
        self.cmw_write(f'CONF:NRS:MEAS:MEV:BWC S{scs}K, B{bw}')

    def set_spectrum_limit_fr1(self, area, bw, start_freq, stop_freq, level, rbw):
        """
        ● CONFigure:NRSub:MEAS<i>:MEValuation:LIMit:SEMask:AREA<area>:CBANdwidth<bw>
          + <Enable>, <FrequencyStart>, <FrequencyEnd>, <Level>, <RBW>
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
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:LIMit:SEMask:AREA{area}:CBANdwidth{bw} '
                       f'ON, {start_freq}MHz, {stop_freq}MHz, {level}, {rbw}'
                       )

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

    def set_precoding_fr1(self, on_off='OFF'):
        """
        Specifies whether the signal uses a transform precoding function performing DFT-
        spreading.

        Parameters:
        <OnOff> OFF | ON
        *RST: OFF
        DFTS: ON, CP: OFF
        """
        on_off = 'ON' if self.type_fr1 == 'DFTS' else 'OFF'  # DFTS: ON, CP: OFF
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:DFTPrecoding {on_off}')

    def set_phase_compensation(self, phase_comp='OFF', user_freq=6E0):
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

    def set_channel_type_fr1(self, ctype='PUSC'):
        """
        for now only support PSUCH
        <channel_type> PUSCh or PUCCh
        """
        self.cmw_write(f'CONFigure:NRSub:MEASurement:MEValuation:CTYPe')

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



