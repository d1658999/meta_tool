from connection_interface.connection_visa import VisaComport
from utils.log_init import log_set

logger = log_set('FSW_series')


class FSW:
    def __init__(self, equipment='FSW'):
        self.fsw = VisaComport(equipment)

    def fsw_query(self, tcpip_command):
        tcpip_response = self.fsw.query(tcpip_command).strip()
        logger.info(f'TCPIP::<<{tcpip_command}')
        logger.info(f'TCPIP::>>{tcpip_response}')
        return tcpip_response

    def fsw_write(self, tcpip_command):
        self.fsw.write(tcpip_command)
        logger.info(f'TCPIP::<<{tcpip_command}')

    def instrument_reset(self):
        self.fsw_write('*RST')

    def system_preset(self):
        """
        To restore the default instrument configuration for all channels at once
        ► Press the [PRESET] key.
        To restore the default configuration for a single channel
        The default measurement settings can also be reset for an individual channel only,
        rather than resetting the entire instrument.
        ► In the "Overview", select the "Preset Channel" button.
        The factory default settings are restored to the current channel. Note that a user-
        defined recall settings file is NOT restored.
        Remote command:
        SYSTem:PRESet:CHANnel[:EXEC] on page 1322
        """
        self.fsw_write(f'SYSTem:PRESet')

    def set_reference_level(self, level=30):
        """
        DISPlay[:WINDow<n>][:SUBWindow<w>]:TRACe<t>:Y[:SCALe]:RLEVel <ReferenceLevel>
        This command defines the reference level (for all traces in all windows).
        With a reference level offset ≠ 0, the value range of the reference level is modified by
        the offset.
        Suffix:
        <n> irrelevant
        <w> subwindow
        Not supported by all applications
        <t> irrelevant
        Parameters:
        <ReferenceLevel> The unit is variable.
        Range:  see datasheet
        *RST:  0 dBm
        Default unit: DBM
        Example:  DISP:TRAC:Y:RLEV -60dBm
        """
        self.fsw_write(f'DISPlay:WINDow:TRACe:Y:SCALe:RLEVel {level}')

    def set_reference_level_offset(self, offset=30):
        """
        DISPlay[:WINDow<n>][:SUBWindow<w>]:TRACe<t>:Y[:SCALe]:RLEVel:OFFSet <Offset>
        This command defines a reference level offset (for all traces in all windows).
        Suffix:
        <n> irrelevant
        <w> subwindow
        Not supported by all applications
        <t> irrelevant
        Parameters:
        <Offset> Range:  -200 dB  to  200 dB
        *RST:  0dB
        Default unit: DB
        Example:  DISP:TRAC:Y:RLEV:OFFS -10dB
        """
        self.fsw_write(f'DISPlay:WINDow:TRACe:Y:SCALe:RLEVel:OFFSet {offset}')

    def set_input_attenuation(self, att=30):
        """
        INPut<ip>:ATTenuation
        This command defines the total attenuation for RF input.
        If an electronic attenuator is available and active, the command defines a mechanical
        attenuation (see INPut<ip>:EATT:STATe on page 1171).
        If you set the attenuation manually, it is no longer coupled to the reference level, but
        the reference level is coupled to the attenuation. Thus, if the current reference level is
        not compatible with an attenuation that has been set manually, the command also
        adjusts the reference level.
        Suffix:
        <ip> 1 | 2
        irrelevant
        Parameters:
        <Attenuation> Range:  see data sheet
        Increment:  5 dB (with optional electr. attenuator: 1 dB)
        *RST:  10 dB (AUTO is set to ON)
        Default unit: DB
        Example:  INP:ATT 30dB
        Defines a 30 dB attenuation and decouples the attenuation from
        the reference level.
        """
        self.fsw_write(f'INPut:ATTenuation {att}')

    def set_input_attenuation_auto(self, on_off='ON'):
        """
        This command couples or decouples the attenuation to the reference level. Thus, when
        the reference level is changed, the R&S FSW determines the signal level for optimal
        internal data processing and sets the required attenuation accordingly.
        Suffix:
        <ip> 1 | 2
        irrelevant
        Parameters:
        <State> ON | OFF | 0 | 1
        *RST:  1
        Example:  INP:ATT:AUTO ON
        Couples the attenuation to the reference level.
        """
        self.fsw_write(f'INPut:ATTenuation:AUTO {on_off}')

    def set_freq_start(self, start_freq):
        """
        This command defines a start frequency for measurements in the frequency domain.
        Parameters:
        <Frequency> 0 to (fmax - min span)
        *RST:  0
        Default unit: HZ
        Example:  FREQ:STAR 20MHz
        """
        self.fsw_write(f'FREQuency:STARt {start_freq} KHz')

    def set_freq_stop(self, stop_freq):
        """
        This command defines a stop frequency for measurements in the frequency domain.
        Parameters:
        <Frequency> min span to fmax
        *RST:  fmax
        Default unit: HZ
        Example:  FREQ:STOP 2000 MHz
        """
        self.fsw_write(f'FREQuency:STARt {stop_freq} KHz')

    def set_freq_span(self, span=10):
        """
        This command defines the frequency span.
        If you set a span of 0 Hz in the Spectrum application, the R&S FSW starts a measure-
        ment in the time domain.
        Parameters:
        <Span> The minimum span for measurements in the frequency domain
               is 10 Hz.
               For SEM and spurious emission measurements, the minimum
               span is 20 Hz.
               Range:  0 Hz  to  fmax
               *RST:  Full span
               Default unit: Hz
        """
        self.fsw_write(f'FREQuency:SPAN {span} MHz')

    def set_freq_center(self, center_freq):
        """
        This command defines the center frequency.
        Parameters:
        <Frequency> The allowed range and f max  is specified in the data sheet.
                    UP
                    Increases the center frequency by the step defined using the
                    [SENSe:]FREQuency:CENTer:STEP command.
                    DOWN
                    Decreases the center frequency by the step defined using the
                    [SENSe:]FREQuency:CENTer:STEP command.
                    *RST:  fmax/2
                    Default unit: Hz
        Example:  FREQ:CENT 100 MHz
                  FREQ:CENT:STEP 10 MHz
                  FREQ:CENT UP
                  Sets the center frequency to 110 MHz.
        """
        self.fsw_write(f'FREQuency:CENTer {center_freq} KHz')

    def set_freq_center_step(self, step_size=0):
        """
        This command defines the center frequency step size.
        You can increase or decrease the center frequency quickly in fixed steps using the
        SENS:FREQ UP AND SENS:FREQ DOWN commands, see [SENSe:]FREQuency:
        CENTer on page 1152.
        Parameters:
        <StepSize> f max  is specified in the data sheet.
                    Range:  1  to  fMAX
                    *RST:  0.1 x span
                    Default unit: Hz
        Example:  //Set the center frequency to 110 MHz.
                    FREQ:CENT 100 MHz
                    FREQ:CENT:STEP 10 MHz
                    FREQ:CENT UP
        """
        self.fsw_write(f'FREQuency:CENTer:STEP {step_size} MHz')

    def set_sweep_mode(self, mode='OFF'):
        """
        This command controls the sweep mode for an individual channel.
        Note that in single sweep mode, you can synchronize to the end of the measurement
        with *OPC, *OPC? or *WAI. In continuous sweep mode, synchronization to the end of
        the measurement is not possible. Thus, it is not recommended that you use continuous
        sweep mode in remote control, as results like trace data or markers are only valid after
        a single sweep end synchronization.
        For details on synchronization see Remote control via SCPI.
        Suffix:
        <n>
        .
        irrelevant
        Parameters:
        <State> ON | OFF | 0 | 1
                ON | 1
                Continuous sweep
                OFF | 0
                Single sweep
                *RST:  1
        Example:  INIT:CONT OFF
                  Switches the sweep mode to single sweep.
                  INIT:CONT ON
                  Switches the sweep mode to continuous sweep.
        """
        self.fsw_write(f'INITiate:CONTinuous {mode}')

    def set_measure(self):
        """
        This command starts a (single) new measurement.
        With sweep count or average count > 0, this means a restart of the corresponding
        number of measurements. With trace mode MAXHold, MINHold and AVERage, the
        previous results are reset on restarting the measurement.
        You can synchronize to the end of the measurement with *OPC, *OPC? or *WAI.
        For details on synchronization see Remote control via SCPI.
        Suffix:
        <n>
        .
        irrelevant
        Example:  INIT:CONT OFF
        Switches to single sweep mode.
        DISP:WIND:TRAC:MODE AVER
        Switches on trace averaging.
        SWE:COUN 20
        Sets the sweep counter to 20 sweeps.
        INIT;*WAI
        Starts the measurement and waits for the end of the 20 sweeps.
        """
        self.fsw_write(f'INIT;*WAI')

    def set_average_count(self, count=20):
        """
        [SENSe:]AVERage<n>:COUNt
        this is same as set_sweep_count
        """
        self.fsw_write(f'AVERage:COUNt {count}')

    def set_sweep_count(self, count=20):
        """
        This command defines the number of sweeps that the application uses to average
        traces.
        In continuous sweep mode, the application calculates the moving average over the
        average count.
        In single sweep mode, the application stops the measurement and calculates the aver-
        age after the average count has been reached.
        Parameters:
        <SweepCount> When you set a sweep count of 0 or 1, the R&S FSW performs
                     one single sweep in single sweep mode.
                     In continuous sweep mode, if the sweep count is set to 0, a
                     moving average over 10 sweeps is performed.
                     Range:  0  to  200000
                     *RST:  0
        Example:  SWE:COUN 64
                  Sets the number of sweeps to 64.
                  INIT:CONT OFF
                  Switches to single sweep mode.
                  INIT;*WAI
                  Starts a sweep and waits for its end
        """
        self.fsw_write(f'SWEep:COUNt {count}')

    def set_sweep_time(self, time):
        """
        This command defines the sweep time. It automatically decouples the time from any
        other settings.
        In the Spectrum application, the command decouples the sweep time from the span
        and resolution and video bandwidths. Note that this command queries only the time
        required to capture the data, not to process it. To obtain an estimation of the total cap-
        ture and processing time, use the [SENSe:]SWEep:DURation? command
        Parameters:
        <Time> refer to data sheet
        *RST:  depends on current settings (determined automati-cally)
        Default unit: S
        """
        self.fsw_write(f'SWEep:TIME {time}')

    def set_sweep_time_auto(self, on_off='ON'):
        """
        This command couples and decouples the sweep time to the span and the resolution
        and video bandwidths.
        Parameters:
        <State> ON | OFF | 0 | 1
                *RST:  1
        Example:  SWE:TIME:AUTO ON
                  Activates automatic sweep time.
        """
        self.fsw_write(f'SWEep:TIME:AUTO {on_off}')

    def set_sweep_type(self, type_='AUTO'):
        """
        This command selects the sweep type.
        Parameters:
        <Type> AUTO
               Automatic selection of the sweep type between sweep mode
               and FFT.
               FFT
               FFT mode
               SWE
               Sweep list
               *RST:  AUTO
        """
        self.fsw_write(f'SWEep:TYPE {type_}')

    def set_sweep_points(self, points=1001):
        """
        This command defines the number of sweep points to analyze after a sweep.
        For EMI measurements, 200001 sweep points are available.
        Suffix:
        <n>
        .
        Parameters:
        <SweepPoints> Range:  101  to  100001
                      *RST:  1001
        Example:  SWE:POIN 251
        """
        self.fsw_write(f'SWEep:POINts {points}')

    def set_rbw(self, bw):
        """
        This command defines the resolution bandwidth and decouples the resolution band-
        width from the span.
        In the Real-Time application, the resolution bandwidth is always coupled to the span.
        For statistics measurements, this command defines the demodulation bandwidth.
        The 6 MHz Gaussian filter is provided for special measurements, such as 5G NR spuri-
        ous emissions measurements. It is only available if you enter the value manually, not
        using the BAND:RES MAX command. It is not supported by all applications.
        """
        self.fsw_write(f'BANDwidth {bw} kHz')

    def set_rbw_auto(self, on_off='ON'):
        """
        This command couples and decouples the resolution bandwidth to the span.
        Parameters:
        <State> ON | OFF | 0 | 1
                *RST:  1
        Example:  BAND:AUTO OFF
        Switches off the coupling of the resolution bandwidth to the
        span.
        """
        self.fsw_write(f'BANDwidth:AUTO {on_off}')

    def set_rbw_span_ratio(self, ratio=0.01):
        """
        This command defines the ratio between the resolution bandwidth (Hz) and the span
        (Hz).
        Note that the ratio defined with this remote command (RBW/span) is reciprocal to that
        of the coupling ratio (span/RBW).
        Parameters:
        <Ratio> Range:  0.0001  to  1
        *RST:  0.01
        Example:  BAND:RAT 0.1
        """
        self.fsw_write(f'BANDwidth:RATio {ratio}')

    def set_rbw_type(self, type_='NORMal'):
        """
        This command selects the resolution filter type.
        When you change the filter type, the command selects the next larger filter bandwidth if
        the same bandwidth is unavailable for that filter.
        The EMI-specific filter types are available if the EMI (R&S FSW-K54) measurement
        option is installed, even if EMI measurement is not active. For details see Chap-
        ter 6.13.3.1, "Resolution bandwidth and filter types", on page 329.
        Parameters:
        <FilterType> CFILter
                     Channel filters
                     NORMal
                     Gaussian filters
                     P5
                     5-pole filters
                     The 5-pole filter is not available for FFT sweeps.
                     RRC
                     RRC filters
                     CISPr | PULSe
                     CISPR (6 dB) - requires EMI (R&S FSW-K54) option
                     Return value for query is always PULS.
                     MIL
                     MIL Std (6 dB) - requires EMI (R&S FSW-K54) option
                     *RST:  NORMal
        Example:  BAND:TYPE NORM
        """
        self.fsw_write(f'BANDwidth:TYPE {type_}')

    def set_vbw(self, bw=10):
        """
        This command defines the video bandwidth.
        The command decouples the video bandwidth from the resolution bandwidths.
        Parameters:
        <Bandwidth> refer to data sheet
        *RST:  AUTO is set to ON
        Default unit: HZ
        Example:  BAND:VID 10 kHz
        """
        self.fsw_write(f'BANDwidth:VIDeo {bw} kHz')

    def set_vbw_auto(self, on_off='ON'):
        """
        This command couples and decouples the resolution bandwidth to the span.
        Parameters:
        <State> ON | OFF | 0 | 1
                *RST:  1
        Example:  BAND:AUTO OFF
        Switches off the coupling of the resolution bandwidth to the
        span.
        """
        self.fsw_write(f'BANDwidth:VIDeo:AUTO {on_off}')

    def set_vbw_rbw_ratio(self, ratio=1):
        """
        This command defines the coupling ratio of the video bandwidth to the resolution band-
        width (VBW/RBW).
        Parameters:
        <Ratio> Range:  0,001  to  1000
                *RST:   1
        Example:  BAND:VID:RAT 3
                  Sets the video bandwidth to 3*resolution bandwidth.
        """
        self.fsw_write(f'BANDwidth:VIDeo:RATio {ratio}')

    def set_vbw_type(self, type_='LOGarithmic'):
        """
        This command enables or disables the logarithmic amplifier in front of the video filter in
        the signal path.
        Parameters:
        <Mode> LINear
        The logarithmic amplifier in front of the video filter is bypassed to
        process linear detector samples.
        LOGarithmic
        The logarithmic amplifier in front of the video filter is enabled to
        process logarithmic detector samples.
        *RST:  LOGarithmic
        """
        self.fsw_write(f'BANDwidth:VIDeo:TYPE {type_}')

    def set_display_trace(self, trace=1, on_off='ON'):
        """
        This command turns a trace on and off.
        The measurement continues in the background.
        Suffix:
        <n>
        .
        Window
        <w> subwindow
        Not supported by all applications
        <t> Trace
        Parameters:
        <State> ON | OFF | 0 | 1
        OFF | 0
        Switches the function off
        ON | 1
        Switches the function on
        Example:  DISP:TRAC3 ON
        """
        self.fsw_write(f'DISP:TRAC{trace} {on_off}')

    def set_display_trace_mode(self, trace=1, mode='AVERage'):
        """
        This command selects the trace mode. If necessary, the selected trace is also activa-
        ted.
        For max hold, min hold or average trace mode, you can set the number of single mea-
        surements with [SENSe:]SWEep:COUNt. Note that synchronization to the end of the
        measurement is possible only in single sweep mode.
        Suffix:
        <n>
        .
        Window
        <w> subwindow
        Not supported by all applications
        <t> Trace
        Parameters:
        <Mode> WRITe
               (default:) Overwrite mode: the trace is overwritten by each
               sweep.
               AVERage
               The average is formed over several sweeps. The "Sweep/Aver-
               age Count" determines the number of averaging procedures.
               MAXHold
               The maximum value is determined over several sweeps and dis-
               played. The R&S FSW saves the sweep result in the trace mem-
               ory only if the new value is greater than the previous on
               MINHold
               The minimum value is determined from several measurements
               and displayed. The R&S FSW saves the sweep result in the
               trace memory only if the new value is lower than the previous
               one.
               VIEW
               The current contents of the trace memory are frozen and dis-
               played.
               BLANk
               Hides the selected trace.
               *RST:  Trace 1: WRITe, Trace 2-6: BLANk
        Example:  INIT:CONT OFF
                  Switching to single sweep mode.
                  SWE:COUN 16
                  Sets the number of measurements to 16.
                  DISP:TRAC3:MODE WRIT
                  Selects clear/write mode for trace 3.
                  INIT;*WAI
                  Starts the measurement and waits for the end of the measure-
                  ment.
        """
        self.fsw_write(f'DISPlay:TRACe{trace}:MODE {mode}')

    def set_harmonic_preset(self):
        """
        This command initiates a measurement to determine the ideal configuration for the har-
        monic distortion measurement.
        The method depends on the span.
        ● Frequency domain (span > 0)
        Frequency and level of the first harmonic are determined and used for the mea-
        surement list.
        ● Time domain (span = 0)
        The level of the first harmonic is determined. The frequency remains unchanged.
        Suffix:
        <n> Window
        <m> Marker
        """
        self.fsw_write(f'CALCulate:MARKer:FUNCtion:HARMonics:PRESet')

    def set_harmonic_function(self, on_off='ON'):
        """
        This command turns the harmonic distortion measurement on and off.
        Note the following:
        ● If you perform the measurement in the frequency domain, the search range for the
        frequency of the first harmonic, whose power is determined, is defined by the last
        span.
        ● If you perform the measurement in the time domain, the current center frequency is
        used as the frequency of the first harmonic. Thus, the frequency search is
        bypassed. The first harmonic frequency is set by a specific center frequency in
        zero span before the harmonic measurement is started.
        """
        self.fsw_write(f'CALCulate:MARKer:FUNCtion:HARMonics {on_off}')

    def set_harmonic_number_harmonic(self, number=10):
        """
        This command selects the number of harmonics that the R&S FSW looks for.
        Suffix:
        <n> Window
        <m> Marker
        Parameters:
        <NoHarmonics> Range:  1  to  26
        *RST:  10
        """
        self.fsw_write(f'CALCulate:MARKer:FUNCtion:HARMonics:NHARmonics {number}')

    def set_harmonic_bandwidth_auto(self, on_off='OFF'):
        """
        This command selects the resolution bandwidth of the harmonic in respect to the band-
        width of the first harmonic.
        Suffix:
        <n> Window
        <m> Marker
        Parameters:
        <State> ON | OFF | 0 | 1
        OFF | 0
        identical
        ON | 1
        a multiple
        *RST:  1
        """
        self.fsw_write(f'CALCulate:MARKer:FUNCtion:HARMonics:BANDwidth:AUTO {on_off}')

    def set_peak_search_state(self, trace=1, on_off='ON'):
        """
        This command turns a peak search on and off.
        Suffix:
        <n> Window
        <m> Marker
        Parameters:
        <State> ON | OFF | 0 | 1
                OFF | 0
                Switches the function off
                ON | 1
                Switches the function on
        Example:  CALC:MARK:FUNC:FPE:STAT ON
                  Activates marker peak search
        """
        self.fsw_write(f'CALCulate:MARKer{trace}:FUNCtion:FPEaks:STATe {on_off}')

    def set_mark_peak_auto(self, trace=1,on_off='ON'):
        """
        This command turns an automatic marker peak search for a trace maximum on and
        off. The R&S FSW performs the peak search after each sweep.
        Suffix:
        <n> Window
        <m> Marker
        Parameters:
        <State> ON | OFF | 0 | 1
        OFF | 0
        Switches the function off
        ON | 1
        Switches the function on
        Example:  CALC:MARK:MAX:AUTO ON
                  Activates the automatic peak search function for marker 1 at the
                  end of each particular sweep.
        """
        self.fsw_write(f'CALCulate:MARKer{trace}:MAXimum:AUTO {on_off}')

    def set_mark_peak(self, trace=1):
        """
        CALCulate<n>:MARKer<m>:MAXimum[:PEAK]
        This command moves a marker to the highest level.
        In the spectrogram, the command moves a marker horizontally to the maximum level in
        the currently selected frame. The vertical marker position remains the same.
        If the marker is not yet active, the command first activates the marker.
        Suffix:
        <n> Window
        <m> Marker
        Manual operation:  See "Peak Search" on page 549
        """
        self.fsw_write(f'CALCulate:MARKer{trace}:MAXimum:PEAK')

    def set_peak_search_number(self, number):
        """
        CALCulate<n>:PSEarch:SUBRanges <NumberPeaks>
        CALCulate<n>:PEAKsearch:SUBRanges <NumberPeaks>
        This command defines the number of peaks included in the peak list.
        After this number of peaks has been found, the R&S FSW stops the peak search and
        continues the search in the next measurement range.
        Suffix:
        <n> Window
        Parameters:
        <NumberPeaks> Range:  1  to  50
        *RST:  25
        Example:  CALC:PSE:SUBR 10
                  Sets 10 peaks per range to be stored in the list.
        """
        self.fsw_write(f'CALCulate:PEAKsearch:SUBRanges {number}')

    def set_peak_lable_enable(self, on_off='OFF'):
        """
        CALCulate<n>:PSEarch:PSHow <State>
        CALCulate<n>:PEAKsearch:PSHow <State>
        This command turns the peak labels in the diagram on and off.
        Peak labels are blue squares.
        Suffix:
        <n> Window
        Parameters:
        <State> ON | OFF | 1 | 0
        *RST:  0
        Example:  CALC:PSE:PSH ON
                  Marks all peaks with blue squares.
        """
        self.fsw_write(f'CALCulate:PSEarch:PSHow {on_off}')

    def set_peak_list_auto(self, on_off='ON'):
        """
        CALCulate<n>:PSEarch:AUTO <State>
        CALCulate<n>:PEAKsearch:AUTO <State>
        This command turns the list evaluation on and off.
        Suffix:
        <n> Window
        Parameters:
        <State> ON | OFF | 0 | 1
        *RST:  1
        Example:  CALC:PSE:AUTO OFF
        Deactivates the list evaluation.
        Manual operation:  See "List Evaluation State" on page 283
        """
        self.fsw_write(f'CALCulate:PEAKsearch:AUTO {on_off}')

    def get_time_register_query(self):
        """
        The STATus:QUEStionable:TIMe register contains information about possible time
        errors that may occur during operation of the R&S FSW. A separate time register exists
        for each active channel.
        You can read out the register with STATus:QUEStionable:TIME:CONDition? or
        STATus:QUEStionable:TIME[:EVENt]?
        Table 12-15: Meaning of the bits used in the STATus:QUEStionable:TIMe register
        Bit No. Meaning
        0 not used
        1 Sweep time too low
        This bit is set if the sweep time is too low.
        2 to 14 Unused
        15 This bit is always 0.
        """
        return self.fsw_query(f'STATus:QUEStionable:TIME?')

    def get_time_duration_query(self):
        """
        This command provides an estimation of the total time required to capture the data and
        process it. This time span may be considerably longer than the actual sweep time (see
        [SENSe:]SWEep:TIME on page 1164).
        Tip: To determine the necessary timeout for data capturing in a remote control pro-
        gram, double the estimated time and add 1 second.
        Return values:
        <Time>
        Example:  SWE:TIME 1s
        SWE:DUR?
        Reply:
        27.9734842578
        Usage:  Query only
        """
        return self.fsw_query(f'SWEep:DURation?')

    def get_harmonics_query(self):
        """
        This command queries the total harmonic distortion of the signal.
        To get a valid result, you have to perform a complete measurement with synchroniza-
        tion to the end of the measurement before reading out the result. This is only possible
        for single sweep mode.
        See also INITiate<n>:CONTinuous on page 886.
        Suffix:
        <n> Window
        <m> Marker
        Query parameters:
        <Result> TOTal
        Return values:
        <DistortionPct>
        <DistortionDb>
        Usage:  Query only
        """
        return self.fsw_query(f'CALCulate:MARKer:FUNCtion:HARMonics:DISTortion? TOTal')

    def get_harmonics_list_query(self):
        """
        This command queries the position of the harmonics.
        To get a valid result, you have to perform a complete measurement with synchroniza-
        tion to the end of the measurement before reading out the result. This is only possible
        for single sweep mode.
        See also INITiate<n>:CONTinuous on page 886.
        Suffix:
        <n> Window
        <m> Marker
        Return values:
        <Harmonics> Returns one value for every harmonic.
        The first value is the absolute power of the first harmonic. The
        unit is variable.
        The other values are power levels relative to the first harmonic.
        The unit for these is dB.
        """
        return self.fsw_query(f'CALCulate:MARKer:FUNCtion:HARMonics:LIST')

    def get_peak_mark_x_query(self):
        """
        This command queries the position of the peaks on the x-axis.
        The order depends on the sort order that has been set with CALCulate<n>:
        MARKer<m>:FUNCtion:FPEaks:SORT.
        Suffix:
        <n>
        .
        irrelevant
        <m> irrelevant
        Return values:
        <PeakPosition> Position of the peaks on the x-axis. The unit depends on the
        measurement.
        Usage:  Query only
        """
        return self.fsw_query(f'CALCulate:MARKer:FUNCtion:FPEaks:X?')

    def get_peak_mark_y_query(self):
        """
        This command queries the position of the peaks on the y-axis.
        The order depends on the sort order that has been set with CALCulate<n>:
        MARKer<m>:FUNCtion:FPEaks:SORT.
        Suffix:
        <n> irrelevant
        <m> irrelevant
        Return values:
        <PeakPosition> Position of the peaks on the y-axis. The unit depends on the
        measurement.
        Usage:  Query only
        """
        return self.fsw_query(f'CALCulate:MARKer:FUNCtion:FPEaks:Y?')


def main():
    pass


if __name__ == '__main__':
    main()
