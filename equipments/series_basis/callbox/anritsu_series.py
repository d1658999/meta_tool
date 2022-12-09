import time
from decimal import Decimal
from connection_interface.connection_visa import VisaComport
from utils.log_init import log_set
import utils.parameters.common_parameters_anritsu as cm_pmt_anritsu

logger = log_set('Anritsu_series')


class Anritsu:
    def __init__(self, equipment):
        self.anritsu = VisaComport(equipment)

    def anritsu_query(self, command):
        response = self.anritsu.query(command).strip()
        logger.info(f'Visa::<<{command}')
        logger.info(f'Visa::>>{response}')
        return response

    def anritsu_write(self, command):
        self.anritsu.write(command)
        logger.info(f'Visa::<<{command}')

    def preset_3gpp(self):
        """
        preest to 3GPP spec (for WCDMA)
        """
        self.anritsu_write("PRESET_3GPP")

    def preset_extarb(self):
        """
        preset extARB that might some pattern
        """
        self.anritsu_write('PRESET_EXTARB')

    def set_end(self):
        """
        Set END on equipment
        """
        self.anritsu_write('CALLSO')

    def set_connecting(self):
        """
        To connect to Test Mode
        """
        self.anritsu_write('CALLSA')

    def set_standard(self, standard='LTE'):
        """
         <standard> LTE | WCDMA | GSM
        """
        self.anritsu_write(f'STDSEL {standard}')

    def set_lvl_status(self, on_off='ON'):
        """
        Set output power on/off
        <on_off> ON | OFF
        """
        self.anritsu_write(f'LVL {on_off}')

    def set_all_measurement_items_off(self):
        """
        set all fundamental measurement items to OFF
        """
        self.anritsu_write('ALLMEASITEMS_OFF')

    def set_test_parameter(self, prm='NORMAL'):
        """
        Set test parameter such as NORMAL, TX_MAXPWR_Q_1,  TX_MAXPWR_Q_F, ...
        """
        self.anritsu_write(f'TESTPRM {prm}')

    def set_ulrmc_64QAM(self, enable='DISABLED'):
        """
         set ULRMC – 64QAM
         <enable> ENABLE | DISABLED
        """
        self.anritsu_write(f'ULRMC_64QAM {enable}')

    def set_ulrmc_256QAM(self, enable='DISABLED'):
        """
         set ULRMC – 256QAM
         <enable> ENABLE | DISABLED
        """
        self.anritsu_write(f'ULRMC_256QAM {enable}')

    def set_band_cal(self):
        """
        set the calibration for temp?
        """
        self.anritsu_query(f'BANDCAL_TEMP 2.0;*OPC?')

    def set_screen(self, on_off='OFF'):
        """
        set the screen is on or off
        """
        self.anritsu_write(f'SCREEN {on_off}')

    def set_display_remain(self, mode='REMAIN'):
        """
        Error Display Mode
        <display mode> NORMAL | REMAIN | REMAIN_LAST
        """
        self.anritsu_write(f'REMDISP {mode}')

    def set_test_mode(self, on_off='ON'):
        """
        This is to set call progress ON
        <on_off> ON | OFF for signaling | non-signaling
        """
        self.anritsu_write(f'CALLPROC {on_off}')

    def set_integrity(self, standard, status):
        """
        for signaling use:
        snow3G for lTE default
        on for WCDMA
        """
        s = standard
        if s == 'LTE':
            self.anritsu_write(f'INTEGRITY {status}')  # SNOW3G | NULL | OFF
        elif s == 'WCDMA':
            self.anritsu_write(f'INTEGRITY {status}')  # ON | OFF
        elif s == 'GSM':
            pass

    def set_scenario(self, mode='NORMAL'):
        """
        set the scenario
        <mode> NORMAL | type1, 2, 3, ...
        """
        self.anritsu_write(f'SCENARIO {mode}')

    def set_pdn_type(self, mode='AUTO'):
        """
        The PDN connectivity procedure is an important process when the LTE communication system accesses to
        packet data network. The purpose of PDN connectivity procedure is to set up a default EPS bearer between a UE
        and a packet data network.
        <mode> AUTO | IPV4 | IPV6 | IPV4V6
        """
        self.anritsu_write(f'PDNTYPE {mode}')

    def set_mcc_mnc(self, mcc='001', mnc='01'):
        """
        set the mcc and mnc
        """
        self.anritsu_write(f'MCC {mcc}')
        self.anritsu_write(f'MNC {mnc} ')

    def set_ant_config(self, ant='SINGLE'):
        """
        set the config of antenna
        <ant> SINGLE | RX_DIVERSITY | OPEN_LOOP | CLOSED_LOOP_MULTI
        """
        self.anritsu_write(f'ANTCONFIG {ant}')

    def set_imsi(self, imsi=cm_pmt_anritsu.IMSI):
        """
        set teh IMSI
        """
        self.anritsu_write(f'IMSI {imsi}')

    def set_authentication(self, on_off='ON'):
        """
        set authentication on or off
        """
        self.anritsu_write(f'AUTHENT {on_off}')

    def set_authentication_algorithm(self, mode='XOR'):
        """
        set the authentication algorithm
        <mode> XOR | Milenage
        """
        self.anritsu_write(f'AUTHENT_ALGO {mode}')

    def set_authentication_key(self, key='00112233,44556677,8899AABB,CCDDEEFF'):
        """
        set the authentication key
        <key> 00112233,44556677,8899AABB,CCDDEEFF for anritsu default key
        """
        self.anritsu_write(f'AUTHENT_KEYALL {key}')

    def set_opc(self, num='00000000,00000000,00000000,00000000'):
        """
        set opc number
        <num> 00000000,00000000,00000000,00000000 for anritsu default
        """
        self.anritsu_write(f'OPC_ALL {num}')


    def set_bandwidth(self, bw=5):
        """
        set bandwidth
        """
        self.anritsu_write(f'BANDWIDTH {bw}MHZ')

    def set_tpc(self, tpc='ILPC'):
        """
        set UL target power control mode, default is ILPC(inner loop control)
        WCDMA: ILPC | ALL1 | ALL0 | ALT | UCMD
        LTE: AUTO | ALL3 |ALL1 | ALL0 | ALLM1| ALT | UCMD
        """
        self.anritsu_write(f'TPCPAT {tpc}')

    def set_tpc_algorithm(self, algo=2):
        """
         set [Power Control Algorithm]
         <algo> 2 for HSUPA | HSDPA most setting
        """
        self.anritsu_write(f'TPCALGO {algo}')

    def set_uplink_channel(self, standard, ul_ch):
        """
        Use this function only in FDD test mode.
        For Anritsu8820C, it could be used in link mode
        """
        s = standard
        if s == 'LTE' or s == 'WCDMA':
            return self.set_ul_chan(ul_ch)

        elif s == 'GSM':
            pass

    def set_downlink_channel(self, standard, dl_ch):
        """
        Use this function only in FDD test mode
        For Anritsu8820C, it could be used in link mode
        """
        s = standard
        if s == 'LTE' or s == 'WCDMA':
            return self.set_dl_chan(dl_ch)
        elif s == 'GSM':
            pass

    def set_fdd_tdd_mode(self, fdd_tdd):
        """
        set the dulplexer or frametype
        <fdd_tdd> FDD|TDD
        """
        self.anritsu_write(f'FRAMETYPE {fdd_tdd}')

    def set_input_level(self, input_level=5):
        """
        set the input level of equipment, that is same as the tx_power level for DUT
        """
        self.anritsu_query(f'ILVL {input_level};*OPC?;*ESR?')

    def set_output_level(self, output_level=-60.0):
        """
        set the output level of equipment, that is same as the rx_power level for DUT
        """
        self.anritsu_query(f'OLVL {output_level};*OPC?;*ESR?')

    def set_rf_out_port(self, port='MAIN'):
        """
        set the output port of equipment(8820), that is same as the rx port level for DUT
        <port> MAIN | AUX
        """
        self.anritsu_write(f'RFOUT {port}')

    def set_phone1_tx_out(self, tx_out=1, port='MAIN'):
        """
        set phone1 area TX<tx_out> on <port> of equipment(8821), that is same as the rx port level for DUT
        <tx_out> 1 | 2 | 3 | 4
        <port> MAIN | AUX
        """
        self.anritsu_write(f'TXOUT {tx_out}, {port}')

    def set_phone2_tx_out(self, tx_out=1, port='MAIN'):
        """
        set phone2 area TX<tx_out> on <port> of equipment(8821), that is same as the rx port level for DUT
        <tx_out> 1 | 2 | 3 | 4
        <port> MAIN | AUX
        """
        self.anritsu_write(f'TXOUT_P2 {tx_out}, {port}')

    def set_phone3_tx_out(self, tx_out=1, port='MAIN'):
        """
        set phone1 area TX<tx_out> on <port> of equipment(8821), that is same as the rx port level for DUT
        <tx_out> 1 | 2 | 3 | 4
        <port> MAIN | AUX
        """
        self.anritsu_write(f'TXOUT_P3 {tx_out}, {port}')

    def set_phone4_tx_out(self, tx_out=1, port='MAIN'):
        """
        set phone4 area TX<tx_out> on <port> of equipment(8821), that is same as the rx port level for DUT
        <tx_out> 1 | 2 | 3 | 4
        <port> MAIN | AUX
        """
        self.anritsu_write(f'TXOUT_P4 {tx_out}, {port}')

    def set_rrc_update(self, mode='PAGING'):
        """
        Execute RRC Connection Reconfiguration:
        Notify the broadcast information update using the RRC Connection Reconfiguration message.
        It updates information without ending a call. Use this procedure.

        Execute Paging
        Notify the broadcast information update using Paging.
        It updates information without ending a call. The MT8820C waits until the Paging information is reflected.
        Use this procedure when procedure A cannot be used.

        <mode> PAGING | RRCMSG
        """
        self.anritsu_write(f'RRCUPDATE {mode}')

    def set_power_trigger_source(self, mode='FRAME'):
        """
        I don't know what it is
        <mode> FRAME
        """
        self.anritsu_write(f'PT_TRGSRC {mode}')

    def set_modified_period(self, mode='N2'):
        """
        I don't know what it is
        <mode> N2
        """
        self.anritsu_write(f'MODIFPERIOD {mode}')

    def set_paging_cycle(self, cycle=32):
        """
        The paging cycle duration in milliseconds.
        <cycle> 32
        """
        self.anritsu_write(f'PCYCLE {cycle}')

    def set_rrc_release(self, mode='OFF'):
        """
        release RRC source
        <mode> ON | OFF
        """
        self.anritsu_write(f'RRCRELEASE {mode}')

    def set_freq_err_range(self, mode='NORMAL'):
        """
        set the freq error range, anritsu default is NORMAL
        <mode> NORMAL | NARROW | WIDE
        """
        self.anritsu_write(f'FREQERRRNG {mode}')

    def set_robust_connection(self, mode='OFF'):
        """
        set the connection is robust
        <mode> ON | OFF
        """
        self.anritsu_write(f'ROBUSTCON {mode}')

    def set_ue_category(self, num=3):
        """
        set the UE category
        <num> the default is 3
        """
        self.anritsu_write(f'UECAT CAT{num}')

    def set_additional_spectrum_emission_ns(self, ns_num='01'):
        """
        This is set to special scenario, that is also called NS_xx
        <ns_num> the default is NS_01
        """
        self.anritsu_write(f'SIB2_NS NS_{ns_num}')

    def set_band_indicator(self, mode='AUTO'):
        """
        Set band indicator
        <mode> AUTO | OFF
        """
        self.anritsu_write(f'BANDIND {mode}')

    def set_drx_cycling(self, length=64):
        """
        Set DRX Cycle Length
        <length>
        """
        self.anritsu_write(f'DRXCYCLNG {length}')

    def set_ber_sample(self, sample=10000):
        """
        Set the sample of BER
        <sample>
        """
        self.anritsu_write(f'BER_SAMPLE {sample}')

    def set_config_measurement(self, mode='ON'):
        """
        set the config measurement
        <mode> ON | OFF
        """
        self.anritsu_write(f'CONF_MEAS {mode}')

    def set_rx_timeout(self, timeout=5):
        """
        Set the timout of RX
        <timeout>
        """
        self.anritsu_write(f'RX_TIMEOUT {timeout}')

    def set_domain_drmc(self, mode='CS'):
        """
        This might select the drmc path
        <mode> CS | PS
        """
        self.anritsu_write(f'DOMAINIDRMC {mode}')

    def set_register_mode(self, mode='AUTO'):
        """
        WCDMA: AUTO
        HSUPA/HSDPA: COMBINED
        """
        self.anritsu_write(f'REGMODE {mode}')

    def set_loss_table_delete(self):
        """
        Delete the unknown loss table
        """
        self.anritsu_write(f'DELLOSSTBL')

    def set_loss_table_delete_phone2(self):
        """
        Delete the unknown loss table on 8821 another table in phone2
        """
        self.anritsu_write(f'DELLOSSTBL_P2')

    def set_loss_table_8820(self, loss_title, freq, loss_dl, loss_ul, loss_aux):
        """
        This is only suitable for 8820
        """
        self.anritsu_write(f'{loss_title} {freq}MHz, {loss_dl}, {loss_ul}, {loss_aux}')
        logger.info(f'{loss_title}, {freq}MHz, dl_loss: {loss_dl}, ul_loss: {loss_ul}, aux_loss: {loss_aux}')

    def set_loss_table_8821(self, loss_title, freq, loss_dl, loss_ul, loss_aux):
        """
        This is only suitable for 8821
        """
        self.anritsu_write(f'{loss_title}, {freq}MHz, {loss_dl}, {loss_ul},,, {loss_aux},,,')
        logger.info(f'{loss_title}, {freq}MHz, dl_loss: {loss_dl}, ul_loss: {loss_ul}, aux_loss: {loss_aux}')

    def set_loss_common(self, standard):
        """
        loss status to set common for 8820
        """
        if standard == 'LTE':
            self.anritsu_write("EXTLOSSW COMMON")
            self.anritsu_query('*OPC?')
        elif standard == 'WCDMA':
            self.anritsu_write("DLEXTLOSSW COMMON")  # Set DL external loss to COMMON
            self.anritsu_write("ULEXTLOSSW COMMON")  # Set UL external loss to COMMON
            self.anritsu_write("AUEXTLOSSW COMMON")  # Set AUX external loss to COMMON
            self.anritsu_query('*OPC?')
        elif standard == "GSM":
            self.anritsu_write("EXTLOSSW COMMON")
            self.anritsu_query('*OPC?')

    def set_calling_threshold(self, hold=1):
        """
        This might be calling ready and start?
        """
        self.anritsu_write(f'CALLTHLD  {hold}')

    def set_calling_clear(self):
        """
        To clear UE Report and call processing.
        or to initialize the UE Report value
        """
        self.anritsu_write('CALLRFR')

    def set_to_measure(self):
        """
        Anritsu8820 use 'SWP' to measure no matter what the test items are
        """
        self.anritsu_query('*OPC?')
        self.anritsu_write('SWP')
        self.anritsu_query('*OPC?')

    def set_ber_measure_on_off(self, switch='ON'):
        """
        Set [BER Measurement] to [On]
        """
        self.anritsu_write(f'BER_MEAS {switch}')

    def set_power_measure_on_off(self, switch='ON'):
        """
        Set [Power Measurement] to [On]
        """
        self.anritsu_write(f'PWR_MEAS {switch}')

    def set_aclr_measure_on_off(self, switch='ON'):
        """
        Set [ACLR Measurement] to [On] for LTE
        """
        self.anritsu_write(f'ACLR_MEAS {switch}')

    def set_adj_measure_on_off(self, switch='ON'):
        """
        Set [ACLR Measurement] to [On] for WCDMA
        """
        self.anritsu_write(f'ADJ_MEAS {switch}')

    def set_sem_measure_on_off(self, switch='ON'):
        """
        Set [SEM Measurement] to [On]
        """
        self.anritsu_write(f'SEM_MEAS {switch}')

    def set_obw_measure_on_off(self, switch='ON'):
        """
        Set [OBW Measurement] to [On]
        """
        self.anritsu_write(f'OBW_MEAS {switch}')

    def set_mod_measure_on_off(self, switch='ON'):
        """
        Set [MOD Measurement] to [On]
        """
        self.anritsu_write(f'MOD_MEAS {switch}')

    def set_evm_origin_offset_on_off(self, switch='ON'):
        """
        Set [EVM include Origin Offset] to [On]
        """
        self.anritsu_write(f'INC_ORGNOFS {switch}')

    def set_power_template_on_off(self, switch='ON'):
        """
        Set [Power template] to [On] for LTE
        """
        self.anritsu_write(f'PWRTEMP {switch}')

    def set_power_wdr_on_off(self, switch='ON'):
        """
        Set [Power template] to [On] for WCDMA
        """
        self.anritsu_write(f'PT_WDR {switch}')

    def set_throughput_hsdpa_on_off(self, switch='OFF'):
        """
        Set throughput measurement to On or OFF for HSDPA
        """
        self.anritsu_write(f'TPUT_MEAS {switch}')

    def set_throughput_hsupa_on_off(self, switch='OFF'):
        """
        Set throughput measurement to On or OFF for HSUPA
        """
        self.anritsu_write(f'TPUTU_MEAS {switch}')

    def set_throughput_early_on_off(self, switch='ON'):
        """
        set throughput_early on/off
        """
        self.anritsu_write(f'TPUT_EARLY {switch}')

    def set_power_count(self, count=1):
        """
        Set the average count of power
        """
        self.anritsu_write(f'PWR_AVG {count}')

    def set_aclr_count(self, count=1):
        """
        Set the average count of power for LTE
        """
        self.anritsu_write(f'ACLR_AVG {count}')

    def set_adj_count(self, count=1):
        """
        Set the average count of power for WCDMA
        """
        self.anritsu_write(f'ADJ_AVG {count}')

    def set_sem_count(self, count=1):
        """
        Set the average count of spectrum mask
        """
        self.anritsu_write(f'SEM_AVG {count}')

    def set_obw_count(self, count=1):
        """
        Set the average count of OBW
        """
        self.anritsu_write(f'OBW_AVG {count}')

    def set_mod_count(self, count=1):
        """
        Set the average count of Modulation
        """
        self.anritsu_write(f'MOD_AVG {count}')

    def set_power_template_count(self, count=1):
        """
        Set [Power template] to [count] times for LTE
        """
        self.anritsu_write(f'PWRTEMP_AVG {count}')

    def set_dl_chan(self, dl_ch):
        """
        Set downlink chan for LTE and WCDMA
        """
        self.anritsu_write(f'DLCHAN {dl_ch}')

    def set_ul_chan(self, ul_ch):
        """
        Set uplink chan for LTE and WCDMA
        """
        self.anritsu_write(f'ULCHAN {str(ul_ch)}')

    def set_power_wdr_count(self, count=1):
        """
        Set [Power template] to [count] times for WCDMA
        """
        self.anritsu_write(f'PT_WDR_AVG {count}')

    def set_channel_coding(self, mode):
        """
        Set [Channel Coding] to [<mode> RF Test]
        <mode> REFMEASCH | FIXREFCH | EDCHTEST for WCDMA | HSDPA | HSUPA
        """
        self.anritsu_write(f'CHCODING {mode}')

    def set_dpch_timing_offset(self, offset=6):
        """
        Set DPCH Timing Offset
        """
        self.anritsu_write(f'DDPCHTOFS {offset}')

    def set_screen_select(self, func):
        """
        display the measurement
        <func> FMEAS | TDMEAS
        """
        self.anritsu_write(f'SCRSEL {func}')

    def ser_ber_sample(self, sample=10000):
        """
        Set number of sample for [WCDMA] and [GSM]
        """
        self.anritsu_write(f'BER_SAMPLE {sample}')

    def set_rx_sample(self, sample=1000):
        """
        Set number of sample for [LTE] and [HSDPA] Throughput measurement
        """
        self.anritsu_write(f'TPUT_SAMPLE {sample}')

    def set_throughput_sample_hsupa(self, sample=15):
        """
        Set HSUPA throughput - number of sample
        """
        self.anritsu_write(f'TPUTU_SAMPLE {sample}')

    def set_ehich_pattern(self, pattern='ACK'):
        """
        Set E-hich pattern
        """
        self.anritsu_write(f'EHICHPAT {pattern}')

    def set_power_pattern(self, pattern='HSMAXPWR'):
        """
        Set power pattern
        <pattern> HSMAXPWR | HSPC
        HSPC:  set [CQI Feedback Cycle] to [4 ms], [Ack-Nack Repetition Factor] to [1], [CQI
        Repetition Factor] to [1], and [TPC Algorithm] to [2]
        HSMAXPWR:  set [CQI Feedback Cycle] to [4 ms], [Ack-Nack Repetition Factor] to [3],
        [CQI Repetition Factor] to [2], and [TPC Algorithm] to [2]
        """
        self.anritsu_write(f'SET_PWRPAT {pattern}')

    def set_max_ul_tx_power(self, allowed=21):
        """
         set [Maximum Allowed UL TX Power] for HSUPA
        """
        self.anritsu_write(f'MAXULPWR {allowed}')

    def set_hsupa_setting(self, setting='TTI10_QPSK '):
        """
         set [HSUPA Set of Parameters]
         <setting> HSET1_QPSK | TTI10_QPSK
         HSET1_QPSK: HSDPA
         TTI10_QPSK: HSUPA
        """
        self.anritsu_write(f'HSHSET {setting}')

    def set_ul_rb_size(self, size):
        """
        Set RB size or RB numbers
        """
        self.anritsu_write(f'ULRMC_RB {size}')

    def set_ul_rb_start(self, start):
        """
        Set RB start or RB offset
        """
        self.anritsu_write(f'ULRB_START {start}')

    def set_ul_rb_position(self, pos='MIN'):
        """
        set the UL RB position
        <pos> MIN | MID | MAX
        """
        self.anritsu_write(f'ULRB_POS {pos}')

    def set_delta_cqi(self, delta=8):
        """
        Set [Delta CQI setting] for HSUPA
        """
        self.anritsu_write(f'SET_HSDELTA_CQI {delta}')

    def set_subtest(self, subtest):
        """
        Set subtest item
        """
        self.anritsu_write(f'SET_HSSUBTEST {subtest}')

    def set_tpc_cmd_down(self):
        """
        Reduce [TxPower] only 1 dB and wait 150 ms.
        """
        self.anritsu_write('TPC_CMD_DOWN')

    def set_tpc_cmd_up(self):
        """
        raise [TxPower] only 1 dB and wait 150 ms.
        """
        self.anritsu_write('TPC_CMD_UP')

    def set_dtch_data_pattern(self, pattern='PN09'):
        """
        DTCH Data Pattern
        """
        self.anritsu_write(f'DTCHPAT {pattern}')

    def set_measurement_object(self, ob='HSDPCCH_MA'):
        """
        Set [Measurement Object] to [HS-DPCCH Modulation Analysis]
        <ob> HSDPCCH_MA | HSDPCCH_PC
        HSDPCCH_PC: HS-DPCCH Power Control
        HSDPCCH_MA: HS-DPCCH Modulation Analysis
        OUTSYNC_AUTO: Out of Synchronisation(Auto)
        PHASEDISC: Phase Discontinuity
        ILPC_AUTO: Inner Loop Power Control (Auto)
        RACHTMSK: RACH with Time Mask
        COMPRESS: Compressed Mode
        ILPC: Inner Loop Power Control
        8PSK: 8PSK
        MSNB: GMSK
        """
        self.anritsu_write(f'MEASOBJ {ob}')

    def set_hsma_item(self, mode):
        """
        Set measurement result of HS-DPCCH (Modulation Analysis)
        <mode> EVMPHASE | CDP
        EVMPHASE: [EVM to Phase Disc]
        CDP: [CDP Ratio]
        """
        self.anritsu_write(f'HMA_ITEM {mode}')

    def set_rrc_filter(self, mode='OFF'):
        """
        set rrc filter
        """
        self.anritsu_write(f'TDM_RRC {mode}')

    def set_subtest5_versin(self, ver='NEW'):
        """
        <ver> NEW | OLD
        OLD: [Subtest5 –before v8.7.0]
        NEW: [Sub-test5 – after v8.8.0]
        """
        self.anritsu_write(f'SUBTEST5_VER {ver}')

    def set_ulmcs(self, num=21):
        """
        set mcs num
        """
        self.anritsu_write(f'ULIMCS {num}')

    def set_uplink_terminal_phone1(self, main_port=1):
        """
        Set to Main<main_port> at Phone1 UL terminal for 8821
        """
        self.anritsu_write(f'ULTPSEL {main_port}')

    def set_downlink_terminal_phone1(self, main_port=1):
        """
        Set to Main<main_port> at Phone1 DL terminal for 8821
        """
        self.anritsu_write(f'DLTPSEL {main_port}')

    def set_uplink_terminal_phone2(self, main_port=1):
        """
        Set to Main<main_port> at Phone1 UL terminal for 8821
        """
        self.anritsu_write(f'ULTPSEL_P2 {main_port}')

    def set_downlink_terminal_phone2(self, main_port=1):
        """
        Set to Main<main_port> at Phone1 DL terminal for 8821
        """
        self.anritsu_write(f'DLTPSEL_P2 {main_port}')

    def set_sem_additional_request_version(self, release=11):
        """
        I don't know what it is, it show up in 8821 command
        """
        self.anritsu_write(f'SEM_ADDREQ REL{release}')

    def get_standard_query(self):
        """
        To check the standard in equipment
        return: LTE | WCDMA | GSM
        """
        return self.anritsu_query("STDSEL?").strip()

    def get_calling_state_query(self):
        """
         To confirm the call processing status
        """
        return self.anritsu_query('CALLSTAT?').strip()

    def get_measure_state_query(self):
        """
        Response the state of measuring
        """
        return self.anritsu_query('MSTAT?').strip()

    def get_downlink_channel_query(self):
        """
        Resonpse the dl_chan for WCDMA
        """
        return int(self.anritsu_query('DLCHAN?').strip())

    def get_tpc_pattern_query(self):
        """
        Resonpone the tpc pattern for WCDMA
        """
        self.anritsu_query('TPCPAT?').strip()

    def get_etfci_query(self):
        """
         Read the E-TFCI measurement result
        """
        return Decimal(self.anritsu_query('AVG_ETFCI?').strip())

    def get_evm_hpm_hsdpa(self):
        """
        evm for HSDPA H-power mode
        """
        return self.anritsu_query('POINT_EVM? ALL').strip().split(',')  # p0, p1, p2, p3

    def get_phase_disc_query(self):
        """
        phase disc for HSDPA H-power mode
        """
        return self.anritsu_query('POINT_PHASEDISC? ALL').strip().split(',')  # theta0, theta1

    def get_power_average_query(self, standard='LTE'):
        if standard == 'LTE':
            """
            Get the average power for LTE
            """
            return float(self.anritsu_query('POWER? AVG').strip())
        elif standard == 'WCDMA':
            """
            Get the average power for WCDMA
            """
            return float(self.anritsu_query('AVG_POWER?').strip())

    def get_evm_query_lte(self):
        """
        Response the average evm for LTE
        """
        return float(self.anritsu_query('EVM? AVG').strip())

    def get_evm_query_wcdma(self):
        """
        Response the average evm for WCDMA
        """
        return float(self.anritsu_query('AVG_EVM?').strip())

    def get_aclr_query_lte(self):
        """
        Get the ACLR value for LTE
        """
        aclr_list = [
            round(float(self.anritsu_query('MODPWR? E_LOW1,AVG').strip()), 2),
            round(float(self.anritsu_query('MODPWR? E_UP1,AVG').strip()), 2),
            round(float(self.anritsu_query('MODPWR? LOW1,AVG').strip()), 2),
            round(float(self.anritsu_query('MODPWR? UP1,AVG').strip()), 2),
            round(float(self.anritsu_query('MODPWR? LOW2,AVG').strip()), 2),
            round(float(self.anritsu_query('MODPWR? UP2,AVG').strip()), 2),
        ]
        return aclr_list

    def get_aclr_query_wcdma(self):
        """
        Get the ACLR value for WCDMA
        """
        aclr_list = [
            round(float(self.anritsu_query('AVG_MODPWR? LOW5').strip()), 2),
            round(float(self.anritsu_query('AVG_MODPWR? UP5').strip()), 2),
            round(float(self.anritsu_query('AVG_MODPWR? LOW10').strip()), 2),
            round(float(self.anritsu_query('AVG_MODPWR? UP10').strip()), 2),
        ]
        return aclr_list

    def get_ber_per_state_query_wcdma(self):
        """
        write (BER? PER) and we can get the x % and the x will lower than 0.1 for WCDMA
        :return: PASS or FAIL
        """
        ber = float(self.get_ber_per_query_wcdma())
        if ber >= 0.1:
            return 'FAIL'
        else:
            return 'PASS'

    def get_ber_per_query_wcdma(self):
        """
        write (BER? PER) and we can get the x % and the x will lower than 0.1 for WCDMA
        :return: PASS or FAIL
        """
        return float(self.anritsu_query('BER? PER').strip())

    def get_throughput_per_query(self):
        """
        query the throughput by percent(%) for LTE
        """
        return float(self.anritsu_query('TPUT? PER').strip())

    def get_throughput_pass_query(self):
        """
        Query the state if it is pass for LTE
        """
        return self.anritsu_query('TPUTPASS?').strip()

    def get_output_level_query(self):
        """
        Query the output level
        """
        return float(self.anritsu_query('OLVL?').strip())

    def get_input_level_query(self):
        """
        Query the input level
        """
        return float(self.anritsu_query('ILVL?').strip())

    def get_channel_coding_query(self):
        """
        Query the chcoding to judge which type for WCDMA | HSUPA | HSDPA
        """
        return self.anritsu_query('CHCODING?').strip()

    def get_ue_cap_version_query(self):
        """
        I don't know what it is
        """
        return self.anritsu_query(f'UE_CAP? REL')

    def get_ul_rb_size_query(self, standard):
        """
        Query RB size or RB numbers
        """
        if standard == 'LTE':
            return int(self.anritsu_query(f'ULRMC_RB?'))
        else:
            return None

    def get_ul_rb_start_query(self, standard):
        """
        Query RB start or RB offset
        """
        if standard == 'LTE':
            return int(self.anritsu_query(f'ULRB_START?'))
        else:
            return None

    def get_ul_freq_query(self):
        """
        Query uplink frequency
        Query: freq Hz
        Return: freq khz
        """
        return int(eval(self.anritsu_query(f'ULFREQ?'))) / 1000
