import time
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

    def set_ulrmc_64QAM(self, enable='DISABLE'):
        """
         set ULRMC – 64QAM
         <enable> ENABLE | DISABLE
        """
        self.anritsu_write(f'ULRMC_64QAM {enable}')

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

    def set_authentication_all(self, standard):
        """
        set all authentication
        """
        s = standard
        if s == 'LTE':
            self.set_authentication('ON')
            self.set_authentication_algorithm()
            self.set_authentication_key()
            self.set_opc()
        elif s == 'WCDMA':
            self.set_authentication_algorithm()
            self.set_authentication_key()
            self.set_opc()

    def set_ul_rb_start(self, pos='MIN'):
        """
        set the UL RB position
        <pos> MIN | MID | MAX
        """
        self.anritsu_write(f'ULRB_POS {pos}')

    def set_bandwidth(self, bw=5):
        """
        set bandwidth
        """
        self.anritsu_write(f'BANDWIDTH {str(bw)}MHZ')

    def set_tpc(self, tpc='ILPC'):
        """
        set UL target power control mode, default is ILPC(inner loop control)
        WCDMA: ILPC | ALL1 | ALL0 | ALT | UCMD
        LTE: AUTO | ALL3 |ALL1 | ALL0 | ALLM1| ALT | UCMD
        """
        self.anritsu_write(f'TPCPAT {tpc}')

    def set_uplink_channel(self, standard, ul_ch):
        """
            Use this function only in FDD test mode.
            For Anritsu8820C, it could be used in link mode
        """
        s = standard
        if s == 'LTE' or s == 'WCDMA':
            return self.anritsu_write(f'ULCHAN {str(ul_ch)}')

        elif s == 'GSM':
            pass

    def set_downlink_channel(self, standard, dl_ch):
        """
        Use this function only in FDD test mode
        For Anritsu8820C, it could be used in link mode
        """
        s = standard
        if s == 'LTE' or s == 'WCDMA':
            return self.anritsu_write(f'DLCHAN {str(dl_ch)}')
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
        self.anritsu_write(f'ILVL {str(input_level)}')

    def set_output_level(self, output_level=-60):
        """
        set the output level of equipment, that is same as the rx_power level for DUT
        """
        self.anritsu_write(f'OLVL {str(output_level)}')

    def set_rf_out_port(self, port='MAIN'):
        """
        set the output port of equipment(8820), that is same as the rx port level for DUT
        <port> MAIN | AUX
        """
        self.anritsu_write(f'RFOUT {port}')

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

    def get_standard_query(self):
        """
        To check the standard in equipment
        return: LTE | WCDMA | GSM
        """
        return self.anritsu_query("STDSEL?").strip()



