#!/usr/bin/python3
import pathlib
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / pathlib.Path('gui') / "main_v2_25_1.ui"


class MainV2251App:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)

        self.instrument = None
        self.general = None
        self.sa_nsa = None
        self.volt_mipi_en = None
        self.get_temp_en = None
        self.fdc_en = None
        self.fbrx_en = None
        self.mipi_read_en = None
        self.port_tx = None
        self.port_table_enable = None
        self.sync_path = None
        self.asw_path_enable = None
        self.asw_path = None
        self.srs_path_enable = None
        self.srs_path = None
        self.tx_level_spin = None
        self.tx1 = None
        self.tx2 = None
        self.ulmimo = None
        self.rx0 = None
        self.rx1 = None
        self.rx2 = None
        self.rx3 = None
        self.rx0_rx1 = None
        self.rx2_rx3 = None
        self.rx_all_path = None
        self.tech_FR1 = None
        self.tech_LTE = None
        self.tech_WCDMA = None
        self.tech_GSM = None
        self.bw1p4 = None
        self.bw3 = None
        self.bw5 = None
        self.bw10 = None
        self.bw15 = None
        self.bw20 = None
        self.TxMax = None
        self.TxLow = None
        self.tx = None
        self.rx = None
        self.tx_level_sweep = None
        self.tx_freq_sweep = None
        self.tx_1rb_sweep = None
        self.rx_quick_enable = None
        self.qpsk_lte = None
        self.q16_lte = None
        self.q64_lte = None
        self.q256_lte = None
        self.chan_L = None
        self.chan_M = None
        self.chan_H = None
        self.prb0_lte = None
        self.frb_lte = None
        self.one_rb0_lte = None
        self.one_rbmax_lte = None
        self.prbmax_lte = None
        self.bw5_fr1 = None
        self.bw10_fr1 = None
        self.bw15_fr1 = None
        self.bw20_fr1 = None
        self.bw25_fr1 = None
        self.bw30_fr1 = None
        self.bw40_fr1 = None
        self.bw50_fr1 = None
        self.bw60_fr1 = None
        self.bw80_fr1 = None
        self.bw90_fr1 = None
        self.bw100_fr1 = None
        self.bw70_fr1 = None
        self.bw35_fr1 = None
        self.bw45_fr1 = None
        self.qpsk_fr1 = None
        self.q16_fr1 = None
        self.q64_fr1 = None
        self.q256_fr1 = None
        self.bpsk_fr1 = None
        self.dfts = None
        self.cp = None
        self.inner_full_fr1 = None
        self.outer_full_fr1 = None
        self.inner_1rb_left_fr1 = None
        self.inner_1rb_right_fr1 = None
        self.edge_1rb_left_fr1 = None
        self.edge_1rb_right_fr1 = None
        self.edge_full_left_fr1 = None
        self.edge_full_right_fr1 = None
        self.B5 = None
        self.B8 = None
        self.B12 = None
        self.B13 = None
        self.B14 = None
        self.B17 = None
        self.B18 = None
        self.B19 = None
        self.B20 = None
        self.B26 = None
        self.B28 = None
        self.B29 = None
        self.B32 = None
        self.B71 = None
        self.LB_all = None
        self.band_segment = None
        self.B24 = None
        self.B1 = None
        self.B2 = None
        self.B3 = None
        self.B4 = None
        self.B7 = None
        self.B30 = None
        self.B25 = None
        self.B66 = None
        self.B39 = None
        self.B40 = None
        self.B38 = None
        self.B41 = None
        self.MHB_all = None
        self.B21 = None
        self.B23 = None
        self.B42 = None
        self.B48 = None
        self.UHB_all = None
        self.W1 = None
        self.W2 = None
        self.WCDMA_all = None
        self.W4 = None
        self.W5 = None
        self.W8 = None
        self.W6 = None
        self.W19 = None
        self.GSM850 = None
        self.GSM900 = None
        self.GSM_all = None
        self.GSM1800 = None
        self.GSM1900 = None
        self.pcl_lb = None
        self.mod_gsm = None
        self.pcl_mb = None
        self.N5 = None
        self.N8 = None
        self.N12 = None
        self.N13 = None
        self.N14 = None
        self.N18 = None
        self.N20 = None
        self.N26 = None
        self.N28 = None
        self.N29 = None
        self.N32 = None
        self.N71 = None
        self.LB_all_fr1 = None
        self.band_segment_fr1 = None
        self.N24 = None
        self.N1 = None
        self.N2 = None
        self.N3 = None
        self.N7 = None
        self.N30 = None
        self.N25 = None
        self.N66 = None
        self.N39 = None
        self.N40 = None
        self.N38 = None
        self.N41 = None
        self.MHB_all_fr1 = None
        self.N34 = None
        self.N70 = None
        self.N75 = None
        self.N76 = None
        self.N255 = None
        self.N256 = None
        self.N77 = None
        self.N78 = None
        self.UHB_all_fr1 = None
        self.N48 = None
        self.N79 = None
        self.part_number = None
        self.freq_sweep_step = None
        self.freq_sweep_start = None
        self.freq_sweep_stop = None
        self.tx_level_start = None
        self.tx_level_stop = None
        self.fcc = None
        self.tx_level = None
        self.prb_lte = None
        self.ce = None
        self.endc = None
        self.port_tx_lte = None
        self.tx_level_endc_lte = None
        self.tx_level_endc_fr1 = None
        self.B3_N78 = None
        self.B2_N77 = None
        self.B66_N77 = None
        self.B66_N2 = None
        self.B66_N5 = None
        self.B12_N78 = None
        self.B5_N78 = None
        self.B28_N78 = None
        self.B5_N77 = None
        self.B13_N5 = None
        self.port_tx_fr1 = None
        self.rx0_endc_lte = None
        self.rx1_endc_lte = None
        self.rx2_endc_lte = None
        self.rx3_endc_lte = None
        self.rx0_rx1_endc_lte = None
        self.rx2_rx3_endc_lte = None
        self.rx_all_path_endc_lte = None
        self.endc_tx_path_lte = None
        self.endc_tx_path_fr1 = None
        self.rx0_endc_fr1 = None
        self.rx1_endc_fr1 = None
        self.rx2_endc_fr1 = None
        self.rx3_endc_fr1 = None
        self.rx0_rx1_endc_fr1 = None
        self.rx2_rx3_endc_fr1 = None
        self.rx_all_path_endc_fr1 = None
        self.tech_HSUPA = None
        self.tech_HSDPA = None
        self.rx_freq_sweep = None
        self.rfout_anritsu = None
        self.U1 = None
        self.U2 = None
        self.HSUPA_all = None
        self.U4 = None
        self.U5 = None
        self.U8 = None
        self.U6 = None
        self.U19 = None
        self.D1 = None
        self.D2 = None
        self.HSDPA_all = None
        self.D4 = None
        self.D5 = None
        self.D8 = None
        self.D6 = None
        self.D19 = None
        self.tempcham_enable = None
        self.hthv = None
        self.htlv = None
        self.ntnv = None
        self.lthv = None
        self.ltlv = None
        self.wait_time = None
        self.psu_enable = None
        self.hv = None
        self.nv = None
        self.lv = None
        self.odpm_enable = None
        self.record_current_enable = None
        self.count = None
        self.ht_arg = None
        self.nt_arg = None
        self.lt_arg = None
        self.hv_arg = None
        self.nv_arg = None
        self.lv_arg = None
        self.cse = None
        self.tx_harmonics = None
        self.tx_cbe = None
        self.cbe_limit_margin = None
        self.ulca = None
        self.debug_enable = None
        self.bw20_5 = None
        self.bw20_10 = None
        self.bw20_15 = None
        self.bw20_20 = None
        self.bw15_15 = None
        self.bw15_10 = None
        self.bw15_20 = None
        self.bw10_20 = None
        self.bw10_15 = None
        self.bw5_20 = None
        self.bw5_10 = None
        self.bw10_10 = None
        self.bw10_5 = None
        self.bw5_15 = None
        self.bw15_5 = None
        self.bw40 = None
        self.BW_CA_all = None
        self.tx_ca = None
        self.tx_ca_cbe = None
        self.one_rb0_null = None
        self.prb_null = None
        self.frb_null = None
        self.frb_frb = None
        self.one_rb0_one_rbmax = None
        self.one_rbmax_one_rb0 = None
        self.criteria_ulca_lte = None
        self.B5B = None
        self.B1C = None
        self.B3C = None
        self.B7C = None
        self.B66B = None
        self.B66C = None
        self.B40C = None
        self.B38C = None
        self.B41C = None
        self.MHB_CA_all = None
        self.B42C = None
        self.B48C = None
        self.rssi_rx_rat = None
        self.rssi_rx_band = None
        self.rssi_rx_bw = None
        self.rssi_scan_mode = None
        self.rssi_start_rx_freq = None
        self.rssi_stop_rx_freq = None
        self.rssi_step_freq = None
        self.rssi_antenna_selection = None
        self.rssi_sampling_count = None
        self.rssi_tx1_rat = None
        self.rssi_tx1_enable = None
        self.rssi_tx1_band = None
        self.rssi_tx1_bw = None
        self.rssi_tx1_freq = None
        self.rssi_tx1_power = None
        self.rssi_tx1_rb_num = None
        self.rssi_tx1_rb_start = None
        self.rssi_tx1_mcs = None
        self.rssi_tx2_rat = None
        self.rssi_tx2_enable = None
        self.rssi_tx2_band = None
        self.rssi_tx2_bw = None
        self.rssi_tx2_freq = None
        self.rssi_tx2_power = None
        self.rssi_tx2_rb_num = None
        self.rssi_tx2_rb_start = None
        self.rssi_tx2_mcs = None
        self.mpr_nv = None
        self.apt = None
        self.apt_sweep_version = None
        self.apt_level_start_hpm = None
        self.apt_level_stop_hpm = None
        self.apt_level_step_hpm = None
        self.bias0_start_hpm = None
        self.bias0_stop_hpm = None
        self.bias0_step_hpm = None
        self.bias1_start_hpm = None
        self.bias1_stop_hpm = None
        self.bias1_step_hpm = None
        self.vcc_start_hpm = None
        self.vcc_stop_hpm = None
        self.vcc_step_hpm = None
        self.apt_level_start_lpm = None
        self.apt_level_stop_lpm = None
        self.apt_level_step_lpm = None
        self.bias0_start_lpm = None
        self.bias0_stop_lpm = None
        self.bias0_step_lpm = None
        self.bias1_start_lpm = None
        self.bias1_stop_lpm = None
        self.bias1_step_lpm = None
        self.vcc_start_lpm = None
        self.vcc_stop_lpm = None
        self.vcc_step_lpm = None
        self.vcc_count_apt = None
        self.aclr_limit_apt = None
        self.evm_limit_apt = None
        self.base_regy = None
        self.changed_regy = None
        self.base_regy_sep = None
        self.separate_txt = None
        self.base_regy_parse = None
        self.parse_cfg = None
        builder.import_variables(
            self,
            [
                "instrument",
                "general",
                "sa_nsa",
                "volt_mipi_en",
                "get_temp_en",
                "fdc_en",
                "fbrx_en",
                "mipi_read_en",
                "port_tx",
                "port_table_enable",
                "sync_path",
                "asw_path_enable",
                "asw_path",
                "srs_path_enable",
                "srs_path",
                "tx_level_spin",
                "tx1",
                "tx2",
                "ulmimo",
                "rx0",
                "rx1",
                "rx2",
                "rx3",
                "rx0_rx1",
                "rx2_rx3",
                "rx_all_path",
                "tech_FR1",
                "tech_LTE",
                "tech_WCDMA",
                "tech_GSM",
                "bw1p4",
                "bw3",
                "bw5",
                "bw10",
                "bw15",
                "bw20",
                "TxMax",
                "TxLow",
                "tx",
                "rx",
                "tx_level_sweep",
                "tx_freq_sweep",
                "tx_1rb_sweep",
                "rx_quick_enable",
                "qpsk_lte",
                "q16_lte",
                "q64_lte",
                "q256_lte",
                "chan_L",
                "chan_M",
                "chan_H",
                "prb0_lte",
                "frb_lte",
                "one_rb0_lte",
                "one_rbmax_lte",
                "prbmax_lte",
                "bw5_fr1",
                "bw10_fr1",
                "bw15_fr1",
                "bw20_fr1",
                "bw25_fr1",
                "bw30_fr1",
                "bw40_fr1",
                "bw50_fr1",
                "bw60_fr1",
                "bw80_fr1",
                "bw90_fr1",
                "bw100_fr1",
                "bw70_fr1",
                "bw35_fr1",
                "bw45_fr1",
                "qpsk_fr1",
                "q16_fr1",
                "q64_fr1",
                "q256_fr1",
                "bpsk_fr1",
                "dfts",
                "cp",
                "inner_full_fr1",
                "outer_full_fr1",
                "inner_1rb_left_fr1",
                "inner_1rb_right_fr1",
                "edge_1rb_left_fr1",
                "edge_1rb_right_fr1",
                "edge_full_left_fr1",
                "edge_full_right_fr1",
                "B5",
                "B8",
                "B12",
                "B13",
                "B14",
                "B17",
                "B18",
                "B19",
                "B20",
                "B26",
                "B28",
                "B29",
                "B32",
                "B71",
                "LB_all",
                "band_segment",
                "B24",
                "B1",
                "B2",
                "B3",
                "B4",
                "B7",
                "B30",
                "B25",
                "B66",
                "B39",
                "B40",
                "B38",
                "B41",
                "MHB_all",
                "B21",
                "B23",
                "B42",
                "B48",
                "UHB_all",
                "W1",
                "W2",
                "WCDMA_all",
                "W4",
                "W5",
                "W8",
                "W6",
                "W19",
                "GSM850",
                "GSM900",
                "GSM_all",
                "GSM1800",
                "GSM1900",
                "pcl_lb",
                "mod_gsm",
                "pcl_mb",
                "N5",
                "N8",
                "N12",
                "N13",
                "N14",
                "N18",
                "N20",
                "N26",
                "N28",
                "N29",
                "N32",
                "N71",
                "LB_all_fr1",
                "band_segment_fr1",
                "N24",
                "N1",
                "N2",
                "N3",
                "N7",
                "N30",
                "N25",
                "N66",
                "N39",
                "N40",
                "N38",
                "N41",
                "MHB_all_fr1",
                "N34",
                "N70",
                "N75",
                "N76",
                "N255",
                "N256",
                "N77",
                "N78",
                "UHB_all_fr1",
                "N48",
                "N79",
                "part_number",
                "freq_sweep_step",
                "freq_sweep_start",
                "freq_sweep_stop",
                "tx_level_start",
                "tx_level_stop",
                "fcc",
                "tx_level",
                "prb_lte",
                "ce",
                "endc",
                "port_tx_lte",
                "tx_level_endc_lte",
                "tx_level_endc_fr1",
                "B3_N78",
                "B2_N77",
                "B66_N77",
                "B66_N2",
                "B66_N5",
                "B12_N78",
                "B5_N78",
                "B28_N78",
                "B5_N77",
                "B13_N5",
                "port_tx_fr1",
                "rx0_endc_lte",
                "rx1_endc_lte",
                "rx2_endc_lte",
                "rx3_endc_lte",
                "rx0_rx1_endc_lte",
                "rx2_rx3_endc_lte",
                "rx_all_path_endc_lte",
                "endc_tx_path_lte",
                "endc_tx_path_fr1",
                "rx0_endc_fr1",
                "rx1_endc_fr1",
                "rx2_endc_fr1",
                "rx3_endc_fr1",
                "rx0_rx1_endc_fr1",
                "rx2_rx3_endc_fr1",
                "rx_all_path_endc_fr1",
                "tech_HSUPA",
                "tech_HSDPA",
                "rx_freq_sweep",
                "rfout_anritsu",
                "U1",
                "U2",
                "HSUPA_all",
                "U4",
                "U5",
                "U8",
                "U6",
                "U19",
                "D1",
                "D2",
                "HSDPA_all",
                "D4",
                "D5",
                "D8",
                "D6",
                "D19",
                "tempcham_enable",
                "hthv",
                "htlv",
                "ntnv",
                "lthv",
                "ltlv",
                "wait_time",
                "psu_enable",
                "hv",
                "nv",
                "lv",
                "odpm_enable",
                "record_current_enable",
                "count",
                "ht_arg",
                "nt_arg",
                "lt_arg",
                "hv_arg",
                "nv_arg",
                "lv_arg",
                "cse",
                "tx_harmonics",
                "tx_cbe",
                "cbe_limit_margin",
                "ulca",
                "debug_enable",
                "bw20_5",
                "bw20_10",
                "bw20_15",
                "bw20_20",
                "bw15_15",
                "bw15_10",
                "bw15_20",
                "bw10_20",
                "bw10_15",
                "bw5_20",
                "bw5_10",
                "bw10_10",
                "bw10_5",
                "bw5_15",
                "bw15_5",
                "bw40",
                "BW_CA_all",
                "tx_ca",
                "tx_ca_cbe",
                "one_rb0_null",
                "prb_null",
                "frb_null",
                "frb_frb",
                "one_rb0_one_rbmax",
                "one_rbmax_one_rb0",
                "criteria_ulca_lte",
                "B5B",
                "B1C",
                "B3C",
                "B7C",
                "B66B",
                "B66C",
                "B40C",
                "B38C",
                "B41C",
                "MHB_CA_all",
                "B42C",
                "B48C",
                "rssi_rx_rat",
                "rssi_rx_band",
                "rssi_rx_bw",
                "rssi_scan_mode",
                "rssi_start_rx_freq",
                "rssi_stop_rx_freq",
                "rssi_step_freq",
                "rssi_antenna_selection",
                "rssi_sampling_count",
                "rssi_tx1_rat",
                "rssi_tx1_enable",
                "rssi_tx1_band",
                "rssi_tx1_bw",
                "rssi_tx1_freq",
                "rssi_tx1_power",
                "rssi_tx1_rb_num",
                "rssi_tx1_rb_start",
                "rssi_tx1_mcs",
                "rssi_tx2_rat",
                "rssi_tx2_enable",
                "rssi_tx2_band",
                "rssi_tx2_bw",
                "rssi_tx2_freq",
                "rssi_tx2_power",
                "rssi_tx2_rb_num",
                "rssi_tx2_rb_start",
                "rssi_tx2_mcs",
                "mpr_nv",
                "apt",
                "apt_sweep_version",
                "apt_level_start_hpm",
                "apt_level_stop_hpm",
                "apt_level_step_hpm",
                "bias0_start_hpm",
                "bias0_stop_hpm",
                "bias0_step_hpm",
                "bias1_start_hpm",
                "bias1_stop_hpm",
                "bias1_step_hpm",
                "vcc_start_hpm",
                "vcc_stop_hpm",
                "vcc_step_hpm",
                "apt_level_start_lpm",
                "apt_level_stop_lpm",
                "apt_level_step_lpm",
                "bias0_start_lpm",
                "bias0_stop_lpm",
                "bias0_step_lpm",
                "bias1_start_lpm",
                "bias1_stop_lpm",
                "bias1_step_lpm",
                "vcc_start_lpm",
                "vcc_stop_lpm",
                "vcc_step_lpm",
                "vcc_count_apt",
                "aclr_limit_apt",
                "evm_limit_apt",
                "base_regy",
                "changed_regy",
                "base_regy_sep",
                "separate_txt",
                "base_regy_parse",
                "parse_cfg",
            ],
        )

        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def inst_select(self, option):
        pass

    def wanted_scripts(self):
        pass

    def thermal_dis(self):
        pass

    def t_measure(self):
        pass

    def t_stop(self):
        pass

    def fr1_mode_select(self):
        pass

    def volt_mipi_status(self):
        pass

    def get_temp_status(self):
        pass

    def fdc_en_status(self):
        pass

    def fbrx_en_status(self):
        pass

    def mipi_read_en_status(self):
        pass

    def select_tx_port(self, option):
        pass

    def pt_enable(self):
        pass

    def select_sync_path(self, option):
        pass

    def asw_enable(self):
        pass

    def select_asw_path(self, option):
        pass

    def srs_enable(self):
        pass

    def select_tx_level_spin(self):
        pass

    def wanted_tx_path(self):
        pass

    def wanted_rx_path(self):
        pass

    def wanted_tech(self):
        pass

    def wanted_bw(self):
        pass

    def wanted_ue_pwr(self):
        pass

    def wanted_tx_rx_sweep(self):
        pass

    def rx_auto_check_ue_pwr(self, event=None):
        pass

    def rx_quick_select(self):
        pass

    def wanted_mcs_lte(self):
        pass

    def wanted_chan(self):
        pass

    def wanted_ftm_rb_lte(self):
        pass

    def wanted_bw_fr1(self):
        pass

    def wanted_mcs_fr1(self):
        pass

    def wanted_type(self):
        pass

    def wanted_ftm_rb_fr1(self):
        pass

    def wanted_band_LTE(self):
        pass

    def off_all_none_LB(self, event=None):
        pass

    def LB_all_state(self):
        pass

    def segment_select(self):
        pass

    def off_all_none_MHB(self, event=None):
        pass

    def MHB_all_state(self):
        pass

    def off_all_none_UHB(self, event=None):
        pass

    def UHB_all_state(self):
        pass

    def wanted_band_WCDMA(self):
        pass

    def off_all_none_WCDMA(self, event=None):
        pass

    def WCDMA_all_state(self):
        pass

    def wanted_band_GSM(self):
        pass

    def off_all_none_GSM(self, event=None):
        pass

    def GSM_all_state(self):
        pass

    def select_pcl_gsm(self, option):
        pass

    def mod_gsm_select(self):
        pass

    def wanted_band_FR1(self):
        pass

    def LB_all_state_fr1(self):
        pass

    def segment_select_fr1(self):
        pass

    def MHB_all_state_fr1(self):
        pass

    def UHB_all_state_fr1(self):
        pass

    def select_tx_level(self, option):
        pass

    def select_tx_port_lte(self, option):
        pass

    def select_tx_level_endc(self, option):
        pass

    def wanted_band_ENDC(self):
        pass

    def select_tx_port_fr1(self, option):
        pass

    def wanted_endc_rx_path_lte(self):
        pass

    def wanted_endc_tx_path_lte(self):
        pass

    def wanted_endc_tx_path_fr1(self):
        pass

    def wanted_endc_rx_path_fr1(self):
        pass

    def sweep_auto_check_ue_pwr(self, event=None):
        pass

    def select_rfout_anritsu(self, option):
        pass

    def wanted_band_HSUPA(self):
        pass

    def off_all_none_HSUPA(self, event=None):
        pass

    def HSUPA_all_state(self):
        pass

    def wanted_band_HSDPA(self):
        pass

    def off_all_none_HSDPA(self, event=None):
        pass

    def HSDPA_all_state(self):
        pass

    def temp_enable_status(self):
        pass

    def wanted_temp_volts(self):
        pass

    def select_wait_time(self, option):
        pass

    def temp_power_off(self):
        pass

    def psu_enable_status(self):
        pass

    def wanted_volts(self):
        pass

    def odpm_enable_status(self):
        pass

    def record_current_enable_status(self):
        pass

    def count_select(self, option):
        pass

    def wanted_bw_ca(self):
        pass

    def BW_CA_all_state(self):
        pass

    def wanted_ftm_rb_ulca_lte(self):
        pass

    def criteria_ulca_lte_select(self):
        pass

    def wanted_band_ca_LTE(self):
        pass

    def MHB_CA_all_state(self):
        pass

    def rssi_scan(self):
        pass

    def t_mpr_nv_generate(self):
        pass

    def merge_nv(self):
        pass

    def separate_nv(self):
        pass

    def separate_nv_2(self):
        pass


if __name__ == "__main__":
    app = MainV2251App()
    app.run()

