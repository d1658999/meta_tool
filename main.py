#!/usr/bin/python3
import pathlib
import tkinter
import tkinter.ttk as ttk
import pygubu
import datetime
import threading
import signal
import os
import yaml

from utils.log_init import log_set, log_clear
from utils.adb_handler import get_serial_devices
from utils.excel_handler import excel_folder_create
from equipments.power_supply import Psu
from equipments.temp_chamber import TempChamber


logger = log_set('GUI')

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / pathlib.Path('gui') / "main_v2_15_1.ui"


class MainApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object("toplevel1", master)
        self.notebook = builder.get_object("notebook1")
        button_run_ftm = builder.get_object("button_run_ftm", master)
        button_run_ftm_fcc = builder.get_object("button_run_ftm_fcc", master)
        button_run_ftm_ce = builder.get_object("button_run_ftm_ce", master)
        button_run_ftm_endc = builder.get_object("button_run_ftm_endc", master)
        button_run_signaling = builder.get_object("button_run_signaling", master)
        button_run_cse = builder.get_object("button_run_cse", master)
        button_run_ulca = builder.get_object("button_run_ulca", master)
        self.button_run_list = [button_run_ftm, button_run_ftm_fcc, button_run_ftm_ce, button_run_ftm_endc,
                                button_run_signaling, button_run_cse, button_run_ulca]
        ICON_FILE = PROJECT_PATH / pathlib.Path('utils') / pathlib.Path('Wave.ico')
        self.mainwindow.iconbitmap(ICON_FILE)
        # self.checkbox_hsupa = builder.get_object("checkbutton_WCDMA", master)
        # self.checkbox_hsdpa = builder.get_object("checkbutton_HSUPA", master)
        # self.checkbox_wcdma = builder.get_object("checkbutton_HSDPA", master)
        self.style = ttk.Style(self.mainwindow)
        self.style.theme_use('xpnative')

        self.instrument = None
        self.general = None
        self.cse = None
        self.ulca = None
        self.sa_nsa = None
        self.criteria_ulca_lte = None
        self.port_tx = None
        self.port_tx_lte = None
        self.port_tx_fr1 = None
        self.rfout_anritsu = None
        self.sync_path = None
        self.asw_path = None
        self.srs_path_enable = None
        self.asw_path_enable = None
        self.srs_path = None
        self.tx_level = None
        self.tx_level_endc_lte = None
        self.tx_level_endc_fr1 = None
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
        self.tech_HSUPA = None
        self.tech_HSDPA = None
        self.tech_GSM = None
        self.bw1p4 = None
        self.bw3 = None
        self.bw5 = None
        self.bw10 = None
        self.bw15 = None
        self.bw20 = None
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
        self.TxMax = None
        self.TxLow = None
        self.tx = None
        self.rx = None
        self.tx_level_sweep = None
        self.tx_freq_sweep = None
        self.tx_1rb_sweep = None
        self.tx_harmonics = None
        self.tx_cbe = None
        self.tx_ca = None
        self.tx_ca_cbe = None
        self.qpsk_lte = None
        self.q16_lte = None
        self.q64_lte = None
        self.q256_lte = None
        self.chan_L = None
        self.chan_M = None
        self.chan_H = None
        self.prb_lte = None
        self.frb_lte = None
        self.one_rb0_lte = None
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
        self.B5B = None
        self.B1C = None
        self.B3C = None
        self.B7C = None
        self.B66B = None
        self.B66C = None
        self.B40C = None
        self.B38C = None
        self.B41C = None
        self.B42C = None
        self.B48C = None
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
        self.B21 = None
        self.B24 = None
        self.band_segment = None
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
        self.MHB_CA_all = None
        self.B42 = None
        self.B48 = None
        self.UHB_all = None
        self.BW_CA_all = None
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
        self.N70 = None
        self.N75 = None
        self.N76 = None
        # self.N39 = None
        self.N40 = None
        self.N38 = None
        self.N41 = None
        self.MHB_all_fr1 = None
        self.N34 = None
        self.N77 = None
        self.N78 = None
        self.UHB_all_fr1 = None
        self.N48 = None
        self.N79 = None
        self.fcc = None
        self.ce = None
        self.endc = None
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
        self.rx_freq_sweep = None
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
        self.psu_enable = None
        self.hv = None
        self.nv = None
        self.lv = None
        self.psu = None
        self.odpm_enable = None
        self.record_current_enable = None
        self.count = None
        self.rx_quick_enable = None
        self.wait_time = None
        self.part_number = None
        self.freq_sweep_step = None
        self.freq_sweep_start = None
        self.freq_sweep_stop = None
        self.tpchb = None
        self.ht_arg = None
        self.nt_arg = None
        self.lt_arg = None
        self.hv_arg = None
        self.nv_arg = None
        self.lv_arg = None
        self.vol_typ = None
        self.tx_level_start = None
        self.tx_level_stop = None
        self.one_rb0_null = None
        self.prb_null = None
        self.frb_null = None
        self.frb_frb = None
        self.one_rb0_one_rbmax = None
        self.one_rbmax_one_rb0 = None
        self.endc_tx_path_lte = None
        self.endc_tx_path_fr1 = None
        self.rx0_endc_lte = None
        self.rx1_endc_lte = None
        self.rx2_endc_lte = None
        self.rx3_endc_lte = None
        self.rx0_rx1_endc_lte = None
        self.rx2_rx3_endc_lte = None
        self.rx_all_path_endc_lte = None
        self.rx0_endc_fr1 = None
        self.rx1_endc_fr1 = None
        self.rx2_endc_fr1 = None
        self.rx3_endc_fr1 = None
        self.rx0_rx1_endc_fr1 = None
        self.rx2_rx3_endc_fr1 = None
        self.rx_all_path_endc_fr1 = None
        self.volt_mipi_en = None
        self.port_table_enable = None
        builder.import_variables(
            self,
            [
                "instrument",
                "general",
                "cse",
                "ulca",
                "sa_nsa",
                "criteria_ulca_lte",
                "port_tx",
                "port_tx_lte",
                "port_tx_fr1",
                "rfout_anritsu",
                "sync_path",
                "tx_level",
                "tx_level_endc_lte",
                "tx_level_endc_fr1",
                "asw_path",
                "srs_path_enable",
                "asw_path_enable",
                "srs_path",
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
                "tech_HSDPA",
                "tech_HSUPA",
                "tech_GSM",
                "bw1p4",
                "bw3",
                "bw5",
                "bw10",
                "bw15",
                "bw20",
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
                "TxMax",
                "TxLow",
                "tx",
                "rx",
                "tx_level_sweep",
                "tx_freq_sweep",
                "tx_1rb_sweep",
                "tx_harmonics",
                "tx_cbe",
                "tx_ca",
                "tx_ca_cbe",
                "qpsk_lte",
                "q16_lte",
                "q64_lte",
                "q256_lte",
                "chan_L",
                "chan_M",
                "chan_H",
                "prb_lte",
                "frb_lte",
                "one_rb0_lte",
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
                "B5B",
                "B1C",
                "B3C",
                "B7C",
                "B66B",
                "B66C",
                "B40C",
                "B38C",
                "B41C",
                "B42C",
                "B48C",
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
                "B21",
                "B24",
                "band_segment",
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
                "MHB_CA_all",
                "B42",
                "B48",
                "UHB_all",
                "BW_CA_all",
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
                "N70",
                "N75",
                "N76",
                # "N39",
                "N40",
                "N38",
                "N41",
                "MHB_all_fr1",
                "N34",
                "N77",
                "N78",
                "UHB_all_fr1",
                "N48",
                "N79",
                "fcc",
                "ce",
                "endc",
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
                "rx_freq_sweep",
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
                "psu_enable",
                "hv",
                "nv",
                "lv",
                "odpm_enable",
                "record_current_enable",
                "count",
                "rx_quick_enable",
                "wait_time",
                "part_number",
                "freq_sweep_step",
                "freq_sweep_start",
                "freq_sweep_stop",
                "ht_arg",
                "nt_arg",
                "lt_arg",
                "hv_arg",
                "nv_arg",
                "lv_arg",
                "tx_level_start",
                "tx_level_stop",
                "one_rb0_null",
                "prb_null",
                "frb_null",
                "frb_frb",
                "one_rb0_one_rbmax",
                "one_rbmax_one_rb0",
                "endc_tx_path_lte",
                "endc_tx_path_fr1",
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
                "volt_mipi_en",
                "port_table_enable",
            ],
        )

        builder.connect_callbacks(self)
        # self.init_select()
        # self.import_ui_setting()
        log_clear()
        self.import_ui_setting_yaml()
        self.endc_tx_path_lte.set('TX1')
        self.endc_tx_path_fr1.set('TX1')
        # self.inst_to_tech()

    def run(self):
        self.mainwindow.mainloop()

    def t_stop(self):
        # t = threading.Thread(target=self.stop)
        t = threading.Thread(target=self.mainwindow.destroy())
        t.start()

    @staticmethod
    def stop():
        print('Crtrl C')
        os.kill(signal.CTRL_C_EVENT, 0)

    def fool_proof_vol(self):
        vol_cap = 4.5
        logger.info('check the voltage setting')

        if float(self.hv_arg.get()) >= vol_cap:
            self.hv_arg.set(vol_cap)
            logger.info(f'HV is limited on {vol_cap}')

        if float(self.nv_arg.get()) >= vol_cap:
            self.nv_arg.set(vol_cap)
            logger.info(f'NV is limited on {vol_cap}')

        if float(self.hv_arg.get()) >= vol_cap:
            self.lv_arg.set(vol_cap)
            logger.info(f'LV is limited on {vol_cap}')

    def mega_measure(self):
        start = datetime.datetime.now()

        self.fool_proof_vol()  # this is to avoid of mistake voltage higher than vol_cap

        temp_dict = {
            'HT': int(self.ht_arg.get()),
            'NT': int(self.nt_arg.get()),
            'LT': int(self.lt_arg.get()),
        }
        volts_dict = {
            'HV': float(self.hv_arg.get()),
            'NV': float(self.nv_arg.get()),
            'LV': float(self.lv_arg.get()),
        }
        if self.tempcham_enable.get():  # with temp chamber and PSU
            self.tpchb = TempChamber()
            self.psu = Psu()
            for temp_volt in self.wanted_temp_volts():
                self.condition = temp_volt  # HVHV, HTLV, NVNV, LTHV, LVLV
                temp = temp_dict[temp_volt[:2]]
                volt = volts_dict[temp_volt[2:]]
                self.vol_typ = volt
                wait = self.wait_time.get()
                self.tpchb.tpchb_init(temp, wait)
                self.psu.psu_init(volt)
                self.measure()
        elif self.psu_enable.get() and (self.tempcham_enable.get() is False):  # with only PSU
            self.psu = Psu()
            for volt in self.want_temp_psu_combination():
                self.condition = volt  # HV, NV, LV
                self.psu.psu_init(volts_dict[volt])
                self.vol_typ = volts_dict[volt]
                self.measure()
        else:  # wtih anything
            self.condition = None
            self.vol_typ = 3.85
            self.measure()

        stop = datetime.datetime.now()

        logger.info(f'Timer: {stop - start}')

    def t_measure(self):
        t = threading.Thread(target=self.mega_measure, daemon=True)
        t.start()

    def temp_power_off(self):
        if self.tpchb is None:
            self.tpchb = TempChamber()
        self.tpchb.power_off()

    def import_ui_setting_yaml(self):
        """
        skip bands_gsm

        """
        logger.info('Import the last setting')
        with open('gui_init.yaml', 'r') as s:
            ui_init = yaml.safe_load(s)

        # set the previous tab
        self.notebook.select(ui_init['tab'])

        # non list-like
        self.instrument.set(ui_init['instrument']['instrument'])
        self.band_segment.set(ui_init['band']['band_segment'])
        self.band_segment_fr1.set(ui_init['band']['band_segment_fr1'])
        self.tx.set(ui_init['test_items']['tx'])
        self.rx.set(ui_init['test_items']['rx'])
        self.rx_freq_sweep.set(ui_init['test_items']['rx_freq_sweep'])
        self.tx_level_sweep.set(ui_init['test_items']['tx_level_sweep'])
        self.tx_freq_sweep.set(ui_init['test_items']['tx_freq_sweep'])
        self.tx_1rb_sweep.set(ui_init['test_items']['tx_1rb_sweep'])
        self.tx_harmonics.set(ui_init['test_items']['tx_harmonics'])
        self.tx_cbe.set(ui_init['test_items']['tx_cbe'])
        self.tx_ca.set(ui_init['test_items']['tx_ca'])
        self.tx_ca_cbe.set(ui_init['test_items']['tx_ca_cbe'])
        self.port_tx.set(ui_init['port']['port_tx'])
        self.port_tx_lte.set(ui_init['port']['port_tx_lte'])
        self.port_tx_fr1.set(ui_init['port']['port_tx_fr1'])
        self.rfout_anritsu.set(ui_init['port']['rfout_anritsu'])
        self.asw_path.set(ui_init['path']['asw_path'])
        self.srs_path.set(ui_init['path']['srs_path'])
        self.srs_path_enable.set(ui_init['path']['srs_path_enable'])
        self.asw_path_enable.set(ui_init['path']['asw_path_enable'])
        self.port_table_enable.set(ui_init['port']['port_table_enable'])
        self.rx_quick_enable.set(ui_init['test_items']['rx_quick_enable'])
        self.sync_path.set(ui_init['path']['sync_path'])
        self.sa_nsa.set(ui_init['path']['sa_nsa'])
        self.criteria_ulca_lte.set(ui_init['criteria']['ulca_lte'])
        self.pcl_lb.set(ui_init['power']['lb_gsm_pcl'])
        self.pcl_mb.set(ui_init['power']['mb_gsm_pcl'])
        self.mod_gsm.set(ui_init['mcs']['modulaiton_gsm'])
        self.tx_level.set(ui_init['power']['tx_level'])
        self.tx_level_endc_lte.set(ui_init['power']['tx_level_endc_lte'])
        self.tx_level_endc_fr1.set(ui_init['power']['tx_level_endc_fr1'])
        self.wait_time.set(ui_init['external_inst']['wait_time'])
        self.count.set(ui_init['external_inst']['count'])
        self.tempcham_enable.set(ui_init['external_inst']['tempchb'])
        self.psu_enable.set(ui_init['external_inst']['psu'])
        self.odpm_enable.set(ui_init['external_inst']['odpm'])
        self.volt_mipi_en.set(ui_init['external_inst']['volt_mipi'])
        self.record_current_enable.set(ui_init['external_inst']['record_current'])
        self.hthv.set(ui_init['condition']['hthv'])
        self.htlv.set(ui_init['condition']['htlv'])
        self.ntnv.set(ui_init['condition']['ntnv'])
        self.lthv.set(ui_init['condition']['lthv'])
        self.ltlv.set(ui_init['condition']['ltlv'])
        self.hv.set(ui_init['condition']['hv'])
        self.nv.set(ui_init['condition']['mv'])
        self.lv.set(ui_init['condition']['lv'])

        # reset all the check button
        self.off_all_reset_tech()
        self.off_all_reset_bw()
        self.off_all_reset_ue_power()
        self.off_all_reset_ch()
        self.off_all_reset_GSM()
        self.off_all_reset_HSDPA()
        self.off_all_reset_HSUPA()
        self.off_all_reset_WCDMA()
        self.off_all_reset_LB()
        self.off_all_reset_MHB()
        self.off_all_reset_UHB()

        # list-like
        for band_endc in ui_init['band']['bands_endc']:
            if band_endc == '3_78':
                self.B3_N78.set(True)
            elif band_endc == '2_77':
                self.B2_N77.set(True)
            elif band_endc == '66_77':
                self.B66_N77.set(True)
            elif band_endc == '66_2':
                self.B66_N2.set(True)
            elif band_endc == '66_5':
                self.B66_N5.set(True)
            elif band_endc == '12_78':
                self.B12_N78.set(True)
            elif band_endc == '5_78':
                self.B5_N78.set(True)
            elif band_endc == '28_78':
                self.B28_N78.set(True)
            elif band_endc == '5_77':
                self.B5_N77.set(True)
            elif band_endc == '13_5':
                self.B13_N5.set(True)

        for band_fr1 in ui_init['band']['bands_fr1']:
            if band_fr1 == 1:
                self.N1.set(band_fr1)
            elif band_fr1 == 2:
                self.N2.set(band_fr1)
            elif band_fr1 == 3:
                self.N3.set(band_fr1)
            # elif band_fr1 == 4:
            #     self.N4.set(band_fr1)
            elif band_fr1 == 5:
                self.N5.set(band_fr1)
            elif band_fr1 == 7:
                self.N7.set(band_fr1)
            elif band_fr1 == 8:
                self.N8.set(band_fr1)
            elif band_fr1 == 12:
                self.N12.set(band_fr1)
            elif band_fr1 == 13:
                self.N13.set(band_fr1)
            elif band_fr1 == 14:
                self.N14.set(band_fr1)
            # elif band_fr1 == 17:
            #     self.N17.set(band_fr1)
            elif band_fr1 == 18:
                self.N18.set(band_fr1)
            elif band_fr1 == 19:
                self.N19.set(band_fr1)
            elif band_fr1 == 20:
                self.N20.set(band_fr1)
            elif band_fr1 == 21:
                self.N21.set(band_fr1)
            elif band_fr1 == 24:
                self.N24.set(band_fr1)
            elif band_fr1 == 25:
                self.N25.set(band_fr1)
            elif band_fr1 == 26:
                self.N26.set(band_fr1)
            elif band_fr1 == 28:
                self.N28.set(band_fr1)
            elif band_fr1 == 29:
                self.N29.set(band_fr1)
            elif band_fr1 == 30:
                self.N30.set(band_fr1)
            elif band_fr1 == 32:
                self.N32.set(band_fr1)
            elif band_fr1 == 34:
                self.N34.set(band_fr1)
            elif band_fr1 == 38:
                self.N38.set(band_fr1)
            # elif band_fr1 == 39:
            # self.N39.set(band_fr1)
            elif band_fr1 == 40:
                self.N40.set(band_fr1)
            elif band_fr1 == 41:
                self.N41.set(band_fr1)
            elif band_fr1 == 48:
                self.N48.set(band_fr1)
            elif band_fr1 == 66:
                self.N66.set(band_fr1)
            elif band_fr1 == 70:
                self.N70.set(band_fr1)
            elif band_fr1 == 75:
                self.N75.set(band_fr1)
            elif band_fr1 == 76:
                self.N76.set(band_fr1)
            elif band_fr1 == 71:
                self.N71.set(band_fr1)
            elif band_fr1 == 77:
                self.N77.set(band_fr1)
            elif band_fr1 == 78:
                self.N78.set(band_fr1)
            elif band_fr1 == 79:
                self.N79.set(band_fr1)

        for band_lte in ui_init['band']['bands_lte']:
            if band_lte == 1:
                self.B1.set(band_lte)
            elif band_lte == 2:
                self.B2.set(band_lte)
            elif band_lte == 3:
                self.B3.set(band_lte)
            elif band_lte == 4:
                self.B4.set(band_lte)
            elif band_lte == 5:
                self.B5.set(band_lte)
            elif band_lte == 7:
                self.B7.set(band_lte)
            elif band_lte == 8:
                self.B8.set(band_lte)
            elif band_lte == 12:
                self.B12.set(band_lte)
            elif band_lte == 13:
                self.B13.set(band_lte)
            elif band_lte == 14:
                self.B14.set(band_lte)
            elif band_lte == 17:
                self.B17.set(band_lte)
            elif band_lte == 18:
                self.B18.set(band_lte)
            elif band_lte == 19:
                self.B19.set(band_lte)
            elif band_lte == 20:
                self.B20.set(band_lte)
            elif band_lte == 21:
                self.B21.set(band_lte)
            elif band_lte == 24:
                self.B24.set(band_lte)
            elif band_lte == 25:
                self.B25.set(band_lte)
            elif band_lte == 26:
                self.B26.set(band_lte)
            elif band_lte == 28:
                self.B28.set(band_lte)
            elif band_lte == 29:
                self.B29.set(band_lte)
            elif band_lte == 30:
                self.B30.set(band_lte)
            elif band_lte == 32:
                self.B32.set(band_lte)
            elif band_lte == 38:
                self.B38.set(band_lte)
            elif band_lte == 39:
                self.B39.set(band_lte)
            elif band_lte == 40:
                self.B40.set(band_lte)
            elif band_lte == 41:
                self.B41.set(band_lte)
            elif band_lte == 42:
                self.B42.set(band_lte)
            elif band_lte == 48:
                self.B48.set(band_lte)
            elif band_lte == 66:
                self.B66.set(band_lte)
            elif band_lte == 71:
                self.B71.set(band_lte)

        for band_ca_lte in ui_init['band']['bands_ca_lte']:
            if band_ca_lte == '5B':
                self.B5B.set('5B')
            elif band_ca_lte == '1C':
                self.B1C.set('1C')
            elif band_ca_lte == '3C':
                self.B3C.set('3C')
            elif band_ca_lte == '7C':
                self.B7C.set('7C')
            elif band_ca_lte == '66B':
                self.B66B.set('66B')
            elif band_ca_lte == '66C':
                self.B66C.set('66C')
            elif band_ca_lte == '40C':
                self.B40C.set('40C')
            elif band_ca_lte == '38C':
                self.B38C.set('38C')
            elif band_ca_lte == '41C':
                self.B41C.set('41C')
            elif band_ca_lte == '42C':
                self.B42C.set('42C')
            elif band_ca_lte == '48C':
                self.B48C.set('48C')

        for band_wcdma in ui_init['band']['bands_wcdma']:
            if band_wcdma == 1:
                self.W1.set(band_wcdma)
            elif band_wcdma == 2:
                self.W2.set(band_wcdma)
            elif band_wcdma == 4:
                self.W4.set(band_wcdma)
            elif band_wcdma == 5:
                self.W5.set(band_wcdma)
            elif band_wcdma == 8:
                self.W8.set(band_wcdma)
            elif band_wcdma == 6:
                self.W6.set(band_wcdma)
            elif band_wcdma == 19:
                self.W19.set(band_wcdma)

        for band_hsupa in ui_init['band']['bands_hsupa']:
            if band_hsupa == 1:
                self.U1.set(band_hsupa)
            elif band_hsupa == 2:
                self.U2.set(band_hsupa)
            elif band_hsupa == 4:
                self.U4.set(band_hsupa)
            elif band_hsupa == 5:
                self.U5.set(band_hsupa)
            elif band_hsupa == 8:
                self.U8.set(band_hsupa)
            elif band_hsupa == 6:
                self.U6.set(band_hsupa)
            elif band_hsupa == 19:
                self.U19.set(band_hsupa)

        for band_hsdpa in ui_init['band']['bands_hsdpa']:
            if band_hsdpa == 1:
                self.D1.set(band_hsdpa)
            elif band_hsdpa == 2:
                self.D2.set(band_hsdpa)
            elif band_hsdpa == 4:
                self.D4.set(band_hsdpa)
            elif band_hsdpa == 5:
                self.D5.set(band_hsdpa)
            elif band_hsdpa == 8:
                self.D8.set(band_hsdpa)
            elif band_hsdpa == 6:
                self.D6.set(band_hsdpa)
            elif band_hsdpa == 19:
                self.D19.set(band_hsdpa)

        for band_gsm in ui_init['band']['bands_gsm']:
            if band_gsm == 850:
                self.GSM850.set(band_gsm)
            elif band_gsm == 900:
                self.GSM900.set(band_gsm)
            elif band_gsm == 1800:
                self.GSM1800.set(band_gsm)
            elif band_gsm == 1900:
                self.GSM1900.set(band_gsm)

        for tech in ui_init['tech']['tech']:
            if tech == 'LTE':
                self.tech_LTE.set(True)
            elif tech == 'WCDMA':
                self.tech_WCDMA.set(True)
            elif tech == 'HSUPA':
                self.tech_HSUPA.set(True)
            elif tech == 'HSDPA':
                self.tech_HSDPA.set(True)
            elif tech == 'FR1':
                self.tech_FR1.set(True)
            elif tech == 'GSM':
                self.tech_GSM.set(True)

        for bw in ui_init['bw']['bw_lte']:
            if bw == 1.4:
                self.bw1p4.set(True)
            elif bw == 3:
                self.bw3.set(True)
            elif bw == 5:
                self.bw5.set(True)
            elif bw == 10:
                self.bw10.set(True)
            elif bw == 15:
                self.bw15.set(True)
            elif bw == 20:
                self.bw20.set(True)
            elif bw == "20+5":
                self.bw20_5.set(True)
            elif bw == "20+10":
                self.bw20_10.set(True)
            elif bw == "20+15":
                self.bw20_15.set(True)
            elif bw == "20+20":
                self.bw20_20.set(True)
            elif bw == "15+15":
                self.bw15_15.set(True)
            elif bw == "15+10":
                self.bw15_10.set(True)
            elif bw == "15+20":
                self.bw15_20.set(True)
            elif bw == "10+20":
                self.bw10_20.set(True)
            elif bw == "10+15":
                self.bw10_15.set(True)
            elif bw == "5+20":
                self.bw5_20.set(True)
            elif bw == "5+10":
                self.bw5_10.set(True)
            elif bw == "10+10":
                self.bw10_10.set(True)
            elif bw == "10+5":
                self.bw10_5.set(True)
            elif bw == "5+15":
                self.bw5_15.set(True)
            elif bw == "15+5":
                self.bw15_5.set(True)
            elif bw == "40":
                self.bw40.set(True)

        for bw_ca in ui_init['bw']['bw_ca_lte']:
            if bw_ca == '20+5':
                self.bw20_5.set(True)
            elif bw_ca == '20+10':
                self.bw20_10.set(True)
            elif bw_ca == '20+15':
                self.bw20_15.set(True)
            elif bw_ca == '20+20':
                self.bw20_20.set(True)
            elif bw_ca == '15+15':
                self.bw15_15.set(True)
            elif bw_ca == '15+10':
                self.bw15_10.set(True)
            elif bw_ca == '15+20':
                self.bw15_20.set(True)
            elif bw_ca == '10+20':
                self.bw10_20.set(True)
            elif bw_ca == '10+15':
                self.bw10_15.set(True)
            elif bw_ca == '5+20':
                self.bw5_20.set(True)
            elif bw_ca == '5+10':
                self.bw5_10.set(True)
            elif bw_ca == '10+10':
                self.bw10_10.set(True)
            elif bw_ca == '10+5':
                self.bw10_5.set(True)
            elif bw_ca == '5+15':
                self.bw5_15.set(True)
            elif bw_ca == '15+5':
                self.bw15_5.set(True)
            elif bw_ca == '40':
                self.bw40.set(True)

        for bw in ui_init['bw']['bw_fr1']:
            if bw == 5:
                self.bw5_fr1.set(True)
            elif bw == 10:
                self.bw10_fr1.set(True)
            elif bw == 15:
                self.bw15_fr1.set(True)
            elif bw == 20:
                self.bw20_fr1.set(True)
            elif bw == 25:
                self.bw25_fr1.set(True)
            elif bw == 30:
                self.bw30_fr1.set(True)
            elif bw == 40:
                self.bw40_fr1.set(True)
            elif bw == 50:
                self.bw50_fr1.set(True)
            elif bw == 60:
                self.bw60_fr1.set(True)
            elif bw == 70:
                self.bw70_fr1.set(True)
            elif bw == 80:
                self.bw80_fr1.set(True)
            elif bw == 90:
                self.bw90_fr1.set(True)
            elif bw == 100:
                self.bw100_fr1.set(True)

        for ue_pwr in ui_init['rx_set']['ue_power']:
            if ue_pwr == 1:
                self.TxMax.set(True)
            elif ue_pwr == 0:
                self.TxLow.set(True)

        for ch in ui_init['channel']['chan']:
            if ch == 'L':
                self.chan_L.set(True)
            elif ch == 'M':
                self.chan_M.set(True)
            elif ch == 'H':
                self.chan_H.set(True)

        for script in ui_init['scripts']['scripts']:
            if script == 'GENERAL':
                self.general.set(True)
            elif script == 'FCC':
                self.fcc.set(True)
            elif script == 'CE':
                self.ce.set(True)
            elif script == 'ENDC':
                self.endc.set(True)
            elif script == 'CSE':
                self.cse.set(True)
            elif script == 'ULCA':
                self.ulca.set(True)

        for _type in ui_init['type']['type_fr1']:
            if _type == 'DFTS':
                self.dfts.set(True)
            elif _type == 'CP':
                self.cp.set(True)

        for rb_ftm in ui_init['rb_set']['rb_ftm_lte']:
            if rb_ftm == 'PRB':
                self.prb_lte.set(True)
            elif rb_ftm == 'FRB':
                self.frb_lte.set(True)
            elif rb_ftm == '1RB_0':
                self.one_rb0_lte.set(True)

        for rb_ftm in ui_init['rb_set']['rb_ftm_ulca_lte']:
            if rb_ftm == '1RB_N':
                self.one_rb0_null.set(True)
            elif rb_ftm == 'PRB_N':
                self.prb_null.set(True)
            elif rb_ftm == 'FRB_0':
                self.frb_null.set(True)
            elif rb_ftm == 'FRB_FRB':
                self.frb_frb.set(True)
            elif rb_ftm == '1RB0_1RBmax':
                self.one_rb0_one_rbmax.set(True)
            elif rb_ftm == '1RBmax_1RB0':
                self.one_rbmax_one_rb0.set(True)

        for rb_ftm in ui_init['rb_set']['rb_ftm_fr1']:
            if rb_ftm == 'INNER_FULL':
                self.inner_full_fr1.set(True)
            elif rb_ftm == 'OUTER_FULL':
                self.outer_full_fr1.set(True)
            elif rb_ftm == 'EDGE_1RB_LEFT':
                self.edge_1rb_left_fr1.set(True)
            elif rb_ftm == 'EDGE_1RB_RIGHT':
                self.edge_1rb_right_fr1.set(True)
            elif rb_ftm == 'EDGE_FULL_LEFT':
                self.edge_full_left_fr1.set(True)
            elif rb_ftm == 'EDGE_FULL_RIGHT':
                self.edge_full_right_fr1.set(True)
            elif rb_ftm == 'INNER_1RB_LEFT':
                self.inner_1rb_left_fr1.set(True)
            elif rb_ftm == 'INNER_1RB_RIGHT':
                self.inner_1rb_right_fr1.set(True)

        for tx_path in ui_init['path']['tx_paths']:
            if tx_path == 'TX1':
                self.tx1.set(True)
            elif tx_path == 'TX2':
                self.tx2.set(True)
            elif tx_path == 'MIMO':
                self.ulmimo.set(True)

        for rx_path in ui_init['path']['rx_paths']:
            if rx_path == 2:
                self.rx0.set(True)
            elif rx_path == 1:
                self.rx1.set(True)
            elif rx_path == 4:
                self.rx2.set(True)
            elif rx_path == 8:
                self.rx3.set(True)
            elif rx_path == 3:
                self.rx0_rx1.set(True)
            elif rx_path == 12:
                self.rx2_rx3.set(True)
            elif rx_path == 15:
                self.rx_all_path.set(True)

        for mcs in ui_init['mcs']['mcs_lte']:
            if mcs == 'QPSK':
                self.qpsk_lte.set(True)
            elif mcs == 'Q16':
                self.q16_lte.set(True)
            elif mcs == 'Q64':
                self.q64_lte.set(True)
            elif mcs == 'Q256':
                self.q256_lte.set(True)

        for mcs in ui_init['mcs']['mcs_fr1']:
            if mcs == 'QPSK':
                self.qpsk_fr1.set(True)
            elif mcs == 'Q16':
                self.q16_fr1.set(True)
            elif mcs == 'Q64':
                self.q64_fr1.set(True)
            elif mcs == 'Q256':
                self.q256_fr1.set(True)
            elif mcs == 'BPSK':
                self.bpsk_fr1.set(True)

    def export_ui_setting_yaml(self):
        logger.info('Export ui setting')
        yaml_file = 'gui_init.yaml'
        # tab index
        tab_index = self.notebook.index(self.notebook.select())

        # thses are list like
        tech = self.wanted_tech()
        bw_lte = self.wanted_bw()
        bw_fr1 = self.wanted_bw_fr1()
        bw_ca_lte = self.wanted_bw_ca()
        ue_power = self.wanted_ue_pwr()
        bands_fr1 = self.wanted_band_FR1()
        bands_lte = self.wanted_band_LTE()
        bands_ca_lte = self.wanted_band_ca_LTE()
        bands_wcdma = self.wanted_band_WCDMA()
        bands_hsupa = self.wanted_band_HSUPA()
        bands_hsdpa = self.wanted_band_HSDPA()
        bands_gsm = self.wanted_band_GSM()
        bands_endc = self.wanted_band_ENDC()
        scripts = self.wanted_scripts()
        type_fr1 = self.wanted_type()
        mcs_lte = self.wanted_mcs_lte()
        mcs_fr1 = self.wanted_mcs_fr1()
        rb_ftm_lte = self.wanted_ftm_rb_lte()
        rb_ftm_ulca_lte = self.wanted_ftm_rb_ulca_lte()
        rb_ftm_fr1 = self.wanted_ftm_rb_fr1()
        tx_paths = self.wanted_tx_path()
        rx_paths = self.wanted_rx_path()

        # these are not list-like
        instrument = self.instrument.get()
        pcl_lb_gsm = self.pcl_lb.get()
        pcl_mb_gsm = self.pcl_mb.get()
        tx_level = self.tx_level.get()
        tx_level_endc_lte = self.tx_level_endc_lte.get()
        tx_leve_endc_fr1 = self.tx_level_endc_fr1.get()
        wait_time = self.wait_time.get()
        count = self.count.get()
        mod_gsm = self.mod_gsm.get()
        port_tx = self.port_tx.get()
        port_tx_lte = self.port_tx_lte.get()
        port_tx_fr1 = self.port_tx_fr1.get()
        sa_nsa = self.sa_nsa.get()
        critera_ulca_lte = self.criteria_ulca_lte.get()
        asw_path = self.asw_path.get()
        srs_path = self.srs_path.get()
        srs_path_enable = self.srs_path_enable.get()
        asw_path_enable = self.asw_path_enable.get()
        port_table_enable = self.port_table_enable.get()
        rx_quick_enable = self.rx_quick_enable.get()
        sync_path = self.sync_path.get()
        rfout_anritsu = self.rfout_anritsu.get()
        band_segment = self.band_segment.get()
        band_segment_fr1 = self.band_segment_fr1.get()
        chan = self.wanted_chan()
        tx, rx, rx_freq_sweep, tx_level_sweep, tx_freq_sweep, tx_1rb_sweep, tx_harmonics, tx_cbe, \
        tx_ca, tx_ca_cbe = self.wanted_tx_rx_sweep()
        tpchb_enable = self.tempcham_enable.get()
        psu_enable = self.psu_enable.get()
        odpm_enable = self.odpm_enable.get()
        volt_mipi_en = self.volt_mipi_en.get()
        record_current_enable = self.record_current_enable.get()
        hthv = self.hthv.get()
        htlv = self.htlv.get()
        ntnv = self.ntnv.get()
        lthv = self.lthv.get()
        ltlv = self.ltlv.get()
        hv = self.hv.get()
        nv = self.nv.get()
        lv = self.lv.get()

        content = {
            'tab': tab_index,
            'port': {
                'port_tx': port_tx,
                'port_tx_lte': port_tx_lte,
                'port_tx_fr1': port_tx_fr1,
                'rfout_anritsu': rfout_anritsu,
                'port_table_enable': port_table_enable,
            },
            'path': {
                'sa_nsa': sa_nsa,
                'asw_path': asw_path,
                'srs_path': srs_path,
                'srs_path_enable': srs_path_enable,
                'asw_path_enable': asw_path_enable,
                'sync_path': sync_path,
                'tx_paths': tx_paths,
                'rx_paths': rx_paths,
            },
            'tech': {
                'tech': tech
            },
            'test_items': {
                'tx': tx,
                'rx': rx,
                'rx_quick_enable': rx_quick_enable,
                'rx_freq_sweep': rx_freq_sweep,
                'tx_level_sweep': tx_level_sweep,
                'tx_freq_sweep': tx_freq_sweep,
                'tx_1rb_sweep': tx_1rb_sweep,
                'tx_harmonics': tx_harmonics,
                'tx_cbe': tx_cbe,
                'tx_ca': tx_ca,
                'tx_ca_cbe': tx_ca_cbe,

            },
            'band': {
                'bands_fr1': bands_fr1,
                'bands_lte': bands_lte,
                'bands_ca_lte': bands_ca_lte,
                'bands_wcdma': bands_wcdma,
                'bands_hsupa': bands_hsupa,
                'bands_hsdpa': bands_hsdpa,
                'bands_gsm': bands_gsm,
                'bands_endc': bands_endc,
                'band_segment': band_segment,
                'band_segment_fr1': band_segment_fr1,
            },
            'bw': {
                'bw_fr1': bw_fr1,
                'bw_lte': bw_lte,
                'bw_ca_lte': bw_ca_lte,
            },
            'power': {
                'lb_gsm_pcl': pcl_lb_gsm,
                'mb_gsm_pcl': pcl_mb_gsm,
                'tx_level': tx_level,
                'tx_level_endc_lte': tx_level_endc_lte,
                'tx_level_endc_fr1': tx_leve_endc_fr1,
            },
            'channel': {
                'chan': chan,
            },
            'rx_set': {
                'ue_power': ue_power,
            },
            'instrument': {
                'instrument': instrument,
            },
            'scripts': {
                'scripts': scripts,
            },
            'type': {
                'type_fr1': type_fr1,
            },
            'mcs': {
                'mcs_lte': mcs_lte,
                'mcs_fr1': mcs_fr1,
                'modulaiton_gsm': mod_gsm,
            },
            'rb_set': {
                'rb_ftm_lte': rb_ftm_lte,
                'rb_ftm_ulca_lte': rb_ftm_ulca_lte,
                'rb_ftm_fr1': rb_ftm_fr1,
            },
            'external_inst': {
                'tempchb': tpchb_enable,
                'psu': psu_enable,
                'odpm': odpm_enable,
                'volt_mipi': volt_mipi_en,
                'record_current': record_current_enable,
                'count': count,
                'wait_time': wait_time,
            },
            'condition': {
                'hthv': hthv,
                'htlv': htlv,
                'ntnv': ntnv,
                'lthv': lthv,
                'ltlv': ltlv,
                'hv': hv,
                'mv': nv,
                'lv': lv,
            },
            'criteria': {
                'ulca_lte': critera_ulca_lte,
            }
        }

        with open(yaml_file, 'w', encoding='utf-8') as outfile:
            yaml.dump(content, outfile, default_flow_style=False, encoding='utf-8', allow_unicode=True)

    def temp_enable_status(self):
        if self.tempcham_enable.get():
            logger.info('=====Enable TempChamber=====')
        else:
            logger.info('=====Disable TempChamber=====')

    def psu_enable_status(self):
        if self.psu_enable.get():
            logger.info('=====Enable PSU=====')
        else:
            logger.info('=====Disable PSU=====')

    def odpm_enable_status(self):
        if self.odpm_enable.get():
            logger.info('=====Enable ODPM=====')
        else:
            logger.info('=====Disable ODPM=====')

    def volt_mipi_status(self):
        if self.volt_mipi_en.get():
            logger.info('=====Disable Volt_mipi=====')
        else:
            logger.info('=====Enable Volt_mipi=====')

    def record_current_enable_status(self):
        if self.record_current_enable.get():
            logger.info('=====Enable Record Current=====')
        else:
            logger.info('=====Disable Record Current=====')

    def off_all_reset_GSM(self):
        self.GSM_all.set(False)
        self.GSM_all_state()

    def off_all_reset_HSDPA(self):
        self.HSDPA_all.set(False)
        self.HSDPA_all_state()

    def off_all_reset_HSUPA(self):
        self.HSUPA_all.set(False)
        self.HSUPA_all_state()

    def off_all_reset_WCDMA(self):
        self.WCDMA_all.set(False)
        self.WCDMA_all_state()

    def off_all_reset_LB(self):
        self.LB_all.set(False)
        self.LB_all_fr1.set(False)
        self.LB_all_state()
        self.LB_all_state_fr1()

    def off_all_reset_MHB(self):
        self.MHB_all.set(False)
        self.MHB_all_fr1.set(False)
        self.MHB_all_state()
        self.MHB_all_state_fr1()

    def off_all_reset_MHB_CA(self):
        self.MHB_CA_all.set(False)
        self.MHB_CA_all_state()

    def off_all_reset_UHB(self):
        self.UHB_all.set(False)
        self.UHB_all_fr1.set(False)
        self.UHB_all_state()
        self.UHB_all_state_fr1()

    def off_call_reset_bw_ca(self):
        self.BW_CA_all.set(False)
        self.BW_CA_all_state()

    @staticmethod
    def thermal_dis():
        from utils.adb_handler import thermal_charger_disable
        thermal_charger_disable()

    def init_select(self):
        self.instrument.set('Anritsu8820')
        self.bw10.set(True)
        self.tech_LTE.set(True)
        self.tx.set(True)
        self.wanted_tx_rx_sweep()
        self.chan_L.set(True)
        self.chan_M.set(True)
        self.chan_H.set(True)
        self.sa_nsa.set(0)
        self.criteria_ulca_lte.set(0)

        logger.info(f'default instrument: {self.instrument.get()}')

    def want_temp_psu_combination(self):
        if self.tempcham_enable.get():
            return self.wanted_temp_volts()
        else:
            if self.psu_enable.get():
                return self.wanted_volts()
            else:
                return None

    def wanted_temp_volts(self):
        temp_volts = []
        if self.hthv.get():
            logger.debug('Enable HTHV')
            temp_volts.append('HTHV')
        if self.htlv.get():
            logger.debug('Enable HTLV')
            temp_volts.append('HTLV')
        if self.ntnv.get():
            logger.debug('Enable NTNV')
            temp_volts.append('NTNV')
        if self.lthv.get():
            logger.debug('Enable LTHV')
            temp_volts.append('LTHV')
        if self.ltlv.get():
            logger.debug('Enable LTLV')
            temp_volts.append('LTLV')
        if temp_volts == []:
            logger.debug('Nothing to select for temp and volts')
        logger.info(f'select temp and volts: {temp_volts}')
        return temp_volts

    def wanted_volts(self):
        volts = []
        if self.hv.get():
            logger.debug('Enable HV')
            volts.append('HV')
        if self.nv.get():
            logger.debug('Enable NV')
            volts.append('NV')
        if self.lv.get():
            logger.debug('Enable LV')
            volts.append('LV')
        if volts == []:
            logger.debug('Nothing to select for volts')
        logger.info(f'select volts: {volts}')
        return volts

    def wanted_band_ENDC(self):
        self.band_endc = []

        if self.B3_N78.get():
            logger.debug(self.B3_N78.get())
            self.band_endc.append('3_78')
        if self.B2_N77.get():
            logger.debug(self.B2_N77.get())
            self.band_endc.append('2_77')
        if self.B66_N77.get():
            logger.debug(self.B66_N77.get())
            self.band_endc.append('66_77')
        if self.B66_N2.get():
            logger.debug(self.B66_N2.get())
            self.band_endc.append('66_2')
        if self.B66_N5.get():
            logger.debug(self.B66_N5.get())
            self.band_endc.append('66_5')
        if self.B12_N78.get():
            logger.debug(self.B12_N78.get())
            self.band_endc.append('12_78')
        if self.B5_N78.get():
            logger.debug(self.B5_N78.get())
            self.band_endc.append('5_78')
        if self.B28_N78.get():
            logger.debug(self.B28_N78.get())
            self.band_endc.append('28_78')
        if self.B5_N77.get():
            logger.debug(self.B5_N77.get())
            self.band_endc.append('5_77')
        if self.B13_N5.get():
            logger.debug(self.B13_N5.get())
            self.band_endc.append('13_5')

        if self.band_endc == []:
            logger.debug('Nothing to select for ENDC')

        logger.info(f'select ENDC band: {self.band_endc}')
        return self.band_endc

    def wanted_band_FR1(self):
        self.band_fr1 = []

        if self.N1.get() == 1:
            logger.debug(self.N1.get())
            self.band_fr1.append(self.N1.get())
        if self.N2.get() == 2:
            logger.debug(self.N2.get())
            self.band_fr1.append(self.N2.get())
        if self.N3.get() == 3:
            logger.debug(self.N3.get())
            self.band_fr1.append(self.N3.get())
        # if self.N4.get() == 4:
        #     logger.debug(self.N4.get())
        #     self.band_fr1.append(self.N4.get())
        if self.N7.get() == 7:
            logger.debug(self.N7.get())
            self.band_fr1.append(self.N7.get())
        if self.N25.get() == 25:
            logger.debug(self.N25.get())
            self.band_fr1.append(self.N25.get())
        if self.N66.get() == 66:
            logger.debug(self.N66.get())
            self.band_fr1.append(self.N66.get())
        if self.N70.get() == 70:
            logger.debug(self.N70.get())
            self.band_fr1.append(self.N70.get())
        if self.N75.get() == 75:
            logger.debug(self.N75.get())
            self.band_fr1.append(self.N75.get())
        if self.N76.get() == 76:
            logger.debug(self.N76.get())
            self.band_fr1.append(self.N76.get())
        if self.N30.get() == 30:
            logger.debug(self.N30.get())
            self.band_fr1.append(self.N30.get())
        # if self.N39.get() == 39:
        #     logger.debug(self.N39.get())
        #     self.band_fr1.append(self.N39.get())
        if self.N40.get() == 40:
            logger.debug(self.N40.get())
            self.band_fr1.append(self.N40.get())
        if self.N38.get() == 38:
            logger.debug(self.N38.get())
            self.band_fr1.append(self.N38.get())
        if self.N41.get() == 41:
            logger.debug(self.N41.get())
            self.band_fr1.append(self.N41.get())
        if self.N34.get() == 34:
            logger.debug(self.N34.get())
            self.band_fr1.append(self.N34.get())
        if self.N5.get() == 5:
            logger.debug(self.N5.get())
            self.band_fr1.append(self.N5.get())
        if self.N8.get() == 8:
            logger.debug(self.N8.get())
            self.band_fr1.append(self.N8.get())
        if self.N12.get() == 12:
            logger.debug(self.N12.get())
            self.band_fr1.append(self.N12.get())
        if self.N13.get() == 13:
            logger.debug(self.N13.get())
            self.band_fr1.append(self.N13.get())
        if self.N14.get() == 14:
            logger.debug(self.N14.get())
            self.band_fr1.append(self.N14.get())
        if self.N18.get() == 18:
            logger.debug(self.N18.get())
            self.band_fr1.append(self.N18.get())
        if self.N20.get() == 20:
            logger.debug(self.N20.get())
            self.band_fr1.append(self.N20.get())
        if self.N24.get() == 24:
            logger.debug(self.N24.get())
            self.band_fr1.append(self.N24.get())
        if self.N26.get() == 26:
            logger.debug(self.N26.get())
            self.band_fr1.append(self.N26.get())
        if self.N28.get() == 28:
            logger.debug(self.N28.get())
            self.band_fr1.append(self.N28.get())
        if self.N29.get() == 29:
            logger.debug(self.N29.get())
            self.band_fr1.append(self.N29.get())
        if self.N32.get() == 32:
            logger.debug(self.N32.get())
            self.band_fr1.append(self.N32.get())
        if self.N71.get() == 71:
            logger.debug(self.N71.get())
            self.band_fr1.append(self.N71.get())
        if self.N48.get() == 48:
            logger.debug(self.N48.get())
            self.band_fr1.append(self.N48.get())
        if self.N77.get() == 77:
            logger.debug(self.N77.get())
            self.band_fr1.append(self.N77.get())
        if self.N78.get() == 78:
            logger.debug(self.N78.get())
            self.band_fr1.append(self.N78.get())
        if self.N79.get() == 79:
            logger.debug(self.N79.get())
            self.band_fr1.append(self.N79.get())

        if self.band_fr1 == []:
            logger.debug('Nothing to select for FR1')

        logger.info(f'select FR1 band: {self.band_fr1}')
        return self.band_fr1

    def wanted_band_LTE(self):
        band_lte = []

        if self.B1.get() == 1:
            logger.debug(self.B1.get())
            band_lte.append(self.B1.get())
        if self.B2.get() == 2:
            logger.debug(self.B2.get())
            band_lte.append(self.B2.get())
        if self.B3.get() == 3:
            logger.debug(self.B3.get())
            band_lte.append(self.B3.get())
        if self.B4.get() == 4:
            logger.debug(self.B4.get())
            band_lte.append(self.B4.get())
        if self.B7.get() == 7:
            logger.debug(self.B7.get())
            band_lte.append(self.B7.get())
        if self.B25.get() == 25:
            logger.debug(self.B25.get())
            band_lte.append(self.B25.get())
        if self.B66.get() == 66:
            logger.debug(self.B66.get())
            band_lte.append(self.B66.get())
        if self.B30.get() == 30:
            logger.debug(self.B30.get())
            band_lte.append(self.B30.get())
        if self.B39.get() == 39:
            logger.debug(self.B39.get())
            band_lte.append(self.B39.get())
        if self.B40.get() == 40:
            logger.debug(self.B40.get())
            band_lte.append(self.B40.get())
        if self.B38.get() == 38:
            logger.debug(self.B38.get())
            band_lte.append(self.B38.get())
        if self.B41.get() == 41:
            logger.debug(self.B41.get())
            band_lte.append(self.B41.get())
        if self.B5.get() == 5:
            logger.debug(self.B5.get())
            band_lte.append(self.B5.get())
        if self.B8.get() == 8:
            logger.debug(self.B8.get())
            band_lte.append(self.B8.get())
        if self.B12.get() == 12:
            logger.debug(self.B12.get())
            band_lte.append(self.B12.get())
        if self.B13.get() == 13:
            logger.debug(self.B13.get())
            band_lte.append(self.B13.get())
        if self.B14.get() == 14:
            logger.debug(self.B14.get())
            band_lte.append(self.B14.get())
        if self.B17.get() == 17:
            logger.debug(self.B17.get())
            band_lte.append(self.B17.get())
        if self.B18.get() == 18:
            logger.debug(self.B18.get())
            band_lte.append(self.B18.get())
        if self.B19.get() == 19:
            logger.debug(self.B19.get())
            band_lte.append(self.B19.get())
        if self.B20.get() == 20:
            logger.debug(self.B20.get())
            band_lte.append(self.B20.get())
        if self.B21.get() == 21:
            logger.debug(self.B21.get())
            band_lte.append(self.B21.get())
        if self.B24.get() == 24:
            logger.debug(self.B24.get())
            band_lte.append(self.B24.get())
        if self.B26.get() == 26:
            logger.debug(self.B26.get())
            band_lte.append(self.B26.get())
        if self.B28.get() == 28:
            logger.debug(self.B28.get())
            band_lte.append(self.B28.get())
        if self.B29.get() == 29:
            logger.debug(self.B29.get())
            band_lte.append(self.B29.get())
        if self.B32.get() == 32:
            logger.debug(self.B32.get())
            band_lte.append(self.B32.get())
        if self.B71.get() == 71:
            logger.debug(self.B71.get())
            band_lte.append(self.B71.get())
        if self.B42.get() == 42:
            logger.debug(self.B42.get())
            band_lte.append(self.B42.get())
        if self.B48.get() == 48:
            logger.debug(self.B48.get())
            band_lte.append(self.B48.get())

        if band_lte == []:
            logger.debug('Nothing to select for LTE')

        logger.info(f'select LTE band: {band_lte}')
        return band_lte

    def wanted_band_ca_LTE(self):
        band_ca_lte = []

        if self.B5B.get() == '5B':
            logger.debug(self.B5B.get())
            band_ca_lte.append(self.B5B.get())

        if self.B1C.get() == '1C':
            logger.debug(self.B1C.get())
            band_ca_lte.append(self.B1C.get())

        if self.B3C.get() == '3C':
            logger.debug(self.B3C.get())
            band_ca_lte.append(self.B3C.get())

        if self.B7C.get() == '7C':
            logger.debug(self.B7C.get())
            band_ca_lte.append(self.B7C.get())

        if self.B66B.get() == '66B':
            logger.debug(self.B66B.get())
            band_ca_lte.append(self.B66B.get())

        if self.B66C.get() == '66C':
            logger.debug(self.B66C.get())
            band_ca_lte.append(self.B66C.get())

        if self.B40C.get() == '40C':
            logger.debug(self.B40C.get())
            band_ca_lte.append(self.B40C.get())

        if self.B38C.get() == '38C':
            logger.debug(self.B38C.get())
            band_ca_lte.append(self.B38C.get())

        if self.B41C.get() == '41C':
            logger.debug(self.B41C.get())
            band_ca_lte.append(self.B41C.get())

        if self.B42C.get() == '42C':
            logger.debug(self.B42C.get())
            band_ca_lte.append(self.B42C.get())

        if self.B48C.get() == '48C':
            logger.debug(self.B48C.get())
            band_ca_lte.append(self.B48C.get())

        if band_ca_lte == []:
            logger.debug('Nothing to select for LTE')

        logger.info(f'select LTE_CA band: {band_ca_lte}')
        return band_ca_lte

    def wanted_band_WCDMA(self):
        self.band_wcdma = []

        if self.W1.get() == 1:
            logger.debug(self.W1.get())
            self.band_wcdma.append(self.W1.get())
        if self.W2.get() == 2:
            logger.debug(self.W2.get())
            self.band_wcdma.append(self.W2.get())
        if self.W4.get() == 4:
            logger.debug(self.W4.get())
            self.band_wcdma.append(self.W4.get())
        if self.W5.get() == 5:
            logger.debug(self.W5.get())
            self.band_wcdma.append(self.W5.get())
        if self.W8.get() == 8:
            logger.debug(self.W8.get())
            self.band_wcdma.append(self.W8.get())
        if self.W6.get() == 6:
            logger.debug(self.W6.get())
            self.band_wcdma.append(self.W6.get())
        if self.W19.get() == 19:
            logger.debug(self.W19.get())
            self.band_wcdma.append(self.W19.get())
        if self.band_wcdma == []:
            logger.debug('Nothing to select for WCDMA')

        logger.info(f'select WCDMA band: {self.band_wcdma}')
        return self.band_wcdma

    def wanted_band_HSUPA(self):
        band_hsupa = []

        if self.U1.get() == 1:
            logger.debug(self.U1.get())
            band_hsupa.append(self.U1.get())
        if self.U2.get() == 2:
            logger.debug(self.U2.get())
            band_hsupa.append(self.U2.get())
        if self.U4.get() == 4:
            logger.debug(self.U4.get())
            band_hsupa.append(self.U4.get())
        if self.U5.get() == 5:
            logger.debug(self.U5.get())
            band_hsupa.append(self.U5.get())
        if self.U8.get() == 8:
            logger.debug(self.U8.get())
            band_hsupa.append(self.U8.get())
        if self.U6.get() == 6:
            logger.debug(self.U6.get())
            band_hsupa.append(self.U6.get())
        if self.U19.get() == 19:
            logger.debug(self.U19.get())
            band_hsupa.append(self.U19.get())
        if band_hsupa == []:
            logger.debug('Nothing to select for WCDMA')

        logger.info(f'select HSUPA band: {band_hsupa}')
        return band_hsupa

    def wanted_band_HSDPA(self):
        band_hsdpa = []

        if self.D1.get() == 1:
            logger.debug(self.D1.get())
            band_hsdpa.append(self.D1.get())
        if self.D2.get() == 2:
            logger.debug(self.D2.get())
            band_hsdpa.append(self.D2.get())
        if self.D4.get() == 4:
            logger.debug(self.D4.get())
            band_hsdpa.append(self.D4.get())
        if self.D5.get() == 5:
            logger.debug(self.D5.get())
            band_hsdpa.append(self.D5.get())
        if self.D8.get() == 8:
            logger.debug(self.D8.get())
            band_hsdpa.append(self.D8.get())
        if self.D6.get() == 6:
            logger.debug(self.D6.get())
            band_hsdpa.append(self.D6.get())
        if self.D19.get() == 19:
            logger.debug(self.D19.get())
            band_hsdpa.append(self.D19.get())
        if band_hsdpa == []:
            logger.debug('Nothing to select for HSDPA')

        logger.info(f'select HSUPA band: {band_hsdpa}')
        return band_hsdpa

    def wanted_band_GSM(self):
        band_gsm = []

        if self.GSM850.get() == 850:
            logger.debug(self.GSM850.get())
            band_gsm.append(self.GSM850.get())
        if self.GSM900.get() == 900:
            logger.debug(self.GSM900.get())
            band_gsm.append(self.GSM900.get())
        if self.GSM1800.get() == 1800:
            logger.debug(self.GSM1800.get())
            band_gsm.append(self.GSM1800.get())
        if self.GSM1900.get() == 1900:
            logger.debug(self.GSM1900.get())
            band_gsm.append(self.GSM1900.get())
        if band_gsm == []:
            logger.debug('Nothing to select for GSM')

        logger.info(f'select GSM band: {band_gsm}')
        return band_gsm

    # def inst_to_tech(self):
    #     if self.instrument.get() == 'Cmw100':
    #         self.checkbox_hsupa['state'] = tkinter.DISABLED
    #         self.checkbox_hsdpa['state'] = tkinter.DISABLED
    #         self.checkbox_wcdma['state'] = tkinter.DISABLED
    #     else:
    #         self.checkbox_hsupa['state'] = tkinter.NORMAL
    #         self.checkbox_hsdpa['state'] = tkinter.NORMAL
    #         self.checkbox_wcdma['state'] = tkinter.NORMAL

    def inst_select(self, option):
        logger.info(self.instrument.get())
        # return self.instrument.get()
        # if self.instrument.get() == 'Cmw100':
        #     self.checkbox_hsupa['state'] = tkinter.DISABLED
        #     self.checkbox_hsdpa['state'] = tkinter.DISABLED
        #     self.checkbox_wcdma['state'] = tkinter.DISABLED
        # else:
        #     self.checkbox_hsupa['state'] = tkinter.NORMAL
        #     self.checkbox_hsdpa['state'] = tkinter.NORMAL
        #     self.checkbox_wcdma['state'] = tkinter.NORMAL

    def segment_select(self):
        logger.info(f'segment: {self.band_segment.get()}')

    def segment_select_fr1(self):
        logger.info(f'segment: {self.band_segment_fr1.get()}')

    def mod_gsm_select(self):
        if self.mod_gsm.get() == 'GMSK':
            self.pcl_lb.set(5)
            self.pcl_mb.set(0)
        elif self.mod_gsm.get() == 'EPSK':
            self.pcl_lb.set(8)
            self.pcl_mb.set(2)
        logger.info(f'GSM Modulation: {self.mod_gsm.get()}')

    def wanted_tx_rx_sweep(self):
        self.wanted_test = {}
        self.wanted_test.setdefault('tx', False)
        self.wanted_test.setdefault('rx', False)
        self.wanted_test.setdefault('rx_freq_sweep', False)
        self.wanted_test.setdefault('tx_level_sweep', False)
        self.wanted_test.setdefault('tx_freq_sweep', False)
        self.wanted_test.setdefault('tx_1rb_sweep', False)
        self.wanted_test.setdefault('tx_harmonics', False)
        self.wanted_test.setdefault('tx_cbe', False)
        self.wanted_test.setdefault('tx_ca', False)
        self.wanted_test.setdefault('tx_ca_cbe', False)

        if self.tx.get():
            logger.debug(self.tx.get())
            self.wanted_test['tx'] = self.tx.get()

        if self.tx_level_sweep.get():
            logger.debug(self.tx_level_sweep.get())
            self.wanted_test['tx_level_sweep'] = self.tx_level_sweep.get()

        if self.tx_freq_sweep.get():
            logger.debug(self.tx_freq_sweep.get())
            self.wanted_test['tx_freq_sweep'] = self.tx_freq_sweep.get()

        if self.tx_1rb_sweep.get():
            logger.debug(self.tx_1rb_sweep.get())
            self.wanted_test['tx_1rb_sweep'] = self.tx_1rb_sweep.get()

        if self.tx_harmonics.get():
            logger.debug(self.tx_harmonics.get())
            self.wanted_test['tx_harmonics'] = self.tx_harmonics.get()

        if self.tx_cbe.get():
            logger.debug(self.tx_cbe.get())
            self.wanted_test['tx_cbe'] = self.tx_cbe.get()

        if self.tx_ca.get():
            logger.debug(self.tx_ca.get())
            self.wanted_test['tx_ca'] = self.tx_ca.get()

        if self.tx_ca_cbe.get():
            logger.debug(self.tx_ca_cbe.get())
            self.wanted_test['tx_ca_cbe'] = self.tx_ca_cbe.get()

        if self.rx.get():
            logger.debug(self.rx.get())
            self.wanted_test['rx'] = self.rx.get()

        if self.rx_freq_sweep.get():
            logger.debug(self.rx_freq_sweep.get())
            self.wanted_test['rx_freq_sweep'] = self.rx_freq_sweep.get()

        if self.wanted_test == {}:
            logger.debug('Nothing to select for test items')

        logger.info(self.wanted_test)
        return self.tx.get(), self.rx.get(), self.rx_freq_sweep.get(), self.tx_level_sweep.get(), \
               self.tx_freq_sweep.get(), self.tx_1rb_sweep.get(), self.tx_harmonics.get(), self.tx_cbe.get(), \
               self.tx_ca.get(), self.tx_ca_cbe.get()

    def wanted_ue_pwr(self):
        self.ue_power = []

        if self.TxMax.get():
            logger.debug('TxMax for sensitivity')
            self.ue_power.append(1)

        if self.TxLow.get():
            logger.debug('-10dBm for sensitivity')
            self.ue_power.append(0)

        logger.info(f'select UE Power when sensitivity: {self.ue_power}')
        return self.ue_power

    def wanted_chan(self):
        self.chan = ''

        if self.chan_L.get():
            logger.debug('L chan')
            self.chan += 'L'

        if self.chan_M.get():
            logger.debug('M chan')
            self.chan += 'M'

        if self.chan_H.get():
            logger.debug('H chan')
            self.chan += 'H'

        if self.chan == '':
            logger.debug('Nothing to select for chan')

        logger.info(f'select channel: {self.chan}')
        return self.chan

    def wanted_bw(self):
        bw = []

        if self.bw1p4.get():
            logger.debug('Bw_1.4')
            bw.append(1.4)

        if self.bw3.get():
            logger.debug('Bw_3')
            bw.append(3)

        if self.bw5.get():
            logger.debug('Bw_5')
            bw.append(5)

        if self.bw10.get():
            logger.debug('Bw_10')
            bw.append(10)

        if self.bw15.get():
            logger.debug('Bw_15')
            bw.append(15)

        if self.bw20.get():
            logger.debug('Bw_20')
            bw.append(20)

        if bw == []:
            logger.debug('Nothing to select for Bw')

        logger.info(f'select BW: {bw}')
        return bw

    def wanted_bw_ca(self):
        bw_ca = []

        if self.bw20_5.get():
            logger.debug('20+5')
            bw_ca.append('20+5')

        if self.bw20_10.get():
            logger.debug('20+10')
            bw_ca.append('20+10')

        if self.bw20_15.get():
            logger.debug('20+15')
            bw_ca.append('20+15')

        if self.bw20_20.get():
            logger.debug('20+20')
            bw_ca.append('20+20')

        if self.bw15_15.get():
            logger.debug('15+15')
            bw_ca.append('15+15')

        if self.bw15_10.get():
            logger.debug('15+10')
            bw_ca.append('15+10')

        if self.bw15_20.get():
            logger.debug('15+20')
            bw_ca.append('15+20')

        if self.bw10_20.get():
            logger.debug('10+20')
            bw_ca.append('10+20')

        if self.bw10_15.get():
            logger.debug('10+15')
            bw_ca.append('10+15')

        if self.bw5_20.get():
            logger.debug('5+20')
            bw_ca.append('5+20')

        if self.bw5_10.get():
            logger.debug('5+10')
            bw_ca.append('5+10')

        if self.bw10_10.get():
            logger.debug('10+10')
            bw_ca.append('10+10')

        if self.bw10_5.get():
            logger.debug('10+5')
            bw_ca.append('10+5')

        if self.bw5_15.get():
            logger.debug('5+15')
            bw_ca.append('5+15')

        if self.bw15_5.get():
            logger.debug('15+5')
            bw_ca.append('15+5')

        if self.bw40.get():
            logger.debug('40')
            bw_ca.append('40')

        if bw_ca == []:
            logger.debug('Nothing to select for Bw')

        logger.info(f'select BW_CA: {bw_ca}')
        return bw_ca

    def wanted_tech(self):
        tech = []

        if self.tech_FR1.get():
            logger.debug(self.tech_FR1.get())
            tech.append('FR1')

        if self.tech_LTE.get():
            logger.debug(self.tech_LTE.get())
            tech.append('LTE')

        if self.tech_WCDMA.get():
            logger.debug(self.tech_WCDMA.get())
            tech.append('WCDMA')

        if self.tech_HSUPA.get():
            logger.debug(self.tech_HSUPA.get())
            tech.append('HSUPA')

        if self.tech_HSDPA.get():
            logger.debug(self.tech_HSDPA.get())
            tech.append('HSDPA')

        if self.tech_GSM.get():
            logger.debug(self.tech_GSM.get())
            tech.append('GSM')

        if tech == []:
            logger.debug('Nothing to select for tech')

        logger.info(f'select tech: {tech}')
        return tech

    def off_all_reset_bw(self):
        self.bw1p4.set(False)
        self.bw3.set(False)
        self.bw5.set(False)
        self.bw10.set(False)
        self.bw20.set(False)
        self.bw5_fr1.set(False)
        self.bw10_fr1.set(False)
        self.bw15_fr1.set(False)
        self.bw20_fr1.set(False)
        self.bw25_fr1.set(False)
        self.bw30_fr1.set(False)
        self.bw40_fr1.set(False)
        self.bw50_fr1.set(False)
        self.bw60_fr1.set(False)
        self.bw70_fr1.set(False)
        self.bw80_fr1.set(False)
        self.bw90_fr1.set(False)
        self.bw100_fr1.set(False)

    def off_all_reset_tech(self):
        self.tech_LTE.set(False)
        self.tech_WCDMA.set(False)
        self.tech_HSDPA.set(False)
        self.tech_HSUPA.set(False)
        self.tech_GSM.set(False)
        self.tech_FR1.set(False)

    def off_all_reset_ue_power(self):
        self.TxMax.set(False)
        self.TxLow.set(False)

    def off_all_reset_ch(self):
        self.chan_L.set(False)
        self.chan_M.set(False)
        self.chan_H.set(False)

    def off_all_none_LB(self, event=None):
        self.LB_all.set(False)

    def BW_CA_all_state(self):
        logger.debug(self.BW_CA_all.get())
        if self.BW_CA_all.get():
            logger.debug("CA band all are checked")
            self.bw20_5.set(True)
            self.bw20_10.set(True)
            self.bw20_15.set(True)
            self.bw20_20.set(True)
            self.bw15_15.set(True)
            self.bw15_10.set(True)
            self.bw15_20.set(True)
            self.bw10_20.set(True)
            self.bw10_15.set(True)
            self.bw5_20.set(True)
            self.bw5_10.set(True)
            self.bw10_10.set(True)
            self.bw10_5.set(True)
            self.bw5_15.set(True)
            self.bw15_5.set(True)
            # self.bw40.set(True)

        else:
            logger.debug("CA band all are unchecked")
            self.bw20_5.set(False)
            self.bw20_10.set(False)
            self.bw20_15.set(False)
            self.bw20_20.set(False)
            self.bw15_15.set(False)
            self.bw15_10.set(False)
            self.bw15_20.set(False)
            self.bw10_20.set(False)
            self.bw10_15.set(False)
            self.bw5_20.set(False)
            self.bw5_10.set(False)
            self.bw10_10.set(False)
            self.bw10_5.set(False)
            self.bw5_15.set(False)
            self.bw15_5.set(False)
            # self.bw40.set(True)

        self.wanted_bw_ca()

    def LB_all_state(self):
        logger.debug(self.LB_all.get())
        if self.LB_all.get():
            logger.debug("LB band all are checked")
            self.B5.set(5)
            self.B8.set(8)
            self.B12.set(12)
            self.B13.set(13)
            self.B14.set(14)
            self.B17.set(17)
            self.B18.set(18)
            self.B19.set(19)
            self.B20.set(20)
            self.B24.set(24)
            self.B26.set(26)
            self.B28.set(28)
            self.B29.set(29)
            self.B32.set(32)
            self.B71.set(71)

        else:
            logger.debug("LB band all are unchecked")
            self.B5.set(0)
            self.B8.set(0)
            self.B12.set(0)
            self.B13.set(0)
            self.B14.set(0)
            self.B17.set(0)
            self.B18.set(0)
            self.B19.set(0)
            self.B20.set(0)
            self.B24.set(0)
            self.B26.set(0)
            self.B28.set(0)
            self.B29.set(0)
            self.B32.set(0)
            self.B71.set(0)

        self.wanted_band_LTE()

    def LB_all_state_fr1(self):
        logger.debug(self.LB_all_fr1.get())
        if self.LB_all_fr1.get():
            logger.debug("LB band all are checked for FR1")
            self.N5.set(5)
            self.N8.set(8)
            self.N12.set(12)
            self.N13.set(13)
            self.N14.set(14)
            # self.N18.set(18)
            self.N20.set(20)
            self.N24.set(24)
            self.N26.set(26)
            self.N28.set(28)
            self.N29.set(29)
            self.N32.set(32)
            self.N71.set(71)

        else:
            logger.debug("LB band all are unchecked for FR1")
            self.N5.set(0)
            self.N8.set(0)
            self.N12.set(0)
            self.N13.set(0)
            self.N14.set(0)
            self.N18.set(0)
            self.N20.set(0)
            self.N24.set(0)
            self.N26.set(0)
            self.N28.set(0)
            self.N29.set(0)
            self.N32.set(0)
            self.N71.set(0)

        self.wanted_band_FR1()

    def off_all_none_MHB(self, event=None):
        self.MHB_all.set(False)

    def MHB_all_state(self):
        if self.MHB_all.get():
            logger.debug("MHB band all are checked")
            self.B1.set(1)
            self.B2.set(2)
            self.B25.set(25)
            self.B3.set(3)
            self.B4.set(4)
            self.B66.set(66)
            self.B21.set(21)
            self.B7.set(7)
            self.B30.set(30)
            self.B39.set(39)
            self.B40.set(40)
            self.B38.set(38)
            self.B41.set(41)

        else:
            logger.debug("MHB band all are unchecked")
            self.B1.set(0)
            self.B2.set(0)
            self.B25.set(0)
            self.B3.set(0)
            self.B4.set(0)
            self.B66.set(0)
            self.B21.set(0)
            self.B7.set(0)
            self.B30.set(0)
            self.B39.set(0)
            self.B40.set(0)
            self.B38.set(0)
            self.B41.set(0)

        self.wanted_band_LTE()

    def MHB_CA_all_state(self):
        if self.MHB_CA_all.get():
            logger.debug("MHB_CA band all are checked")
            self.B1C.set('1C')
            self.B3C.set('3C')
            self.B7C.set('7C')
            self.B66B.set('66B')
            self.B66C.set('66C')
            self.B40C.set('40C')
            self.B38C.set('38C')
            self.B41C.set('41C')

        else:
            logger.debug("MHB_CA band all are unchecked")
            self.B1C.set('')
            self.B3C.set('')
            self.B7C.set('')
            self.B66B.set('')
            self.B66C.set('')
            self.B40C.set('')
            self.B38C.set('')
            self.B41C.set('')

        self.wanted_band_ca_LTE()

    def MHB_all_state_fr1(self):
        logger.debug(self.MHB_all_fr1.get())
        if self.MHB_all_fr1.get():
            logger.debug("MHB band all are checked for FR1")
            self.N1.set(1)
            self.N2.set(2)
            self.N25.set(25)
            self.N3.set(3)
            # self.N4.set(4)
            self.N66.set(66)
            self.N70.set(70)
            self.N75.set(75)
            self.N76.set(76)
            self.N7.set(7)
            self.N30.set(30)
            # self.N39.set(39)
            self.N40.set(40)
            self.N38.set(38)
            self.N41.set(41)
            self.N34.set(34)

        else:
            logger.debug("MHB band all are unchecked for FR1")
            self.N1.set(0)
            self.N2.set(0)
            self.N25.set(0)
            self.N3.set(0)
            # self.N4.set(0)
            self.N66.set(0)
            self.N70.set(0)
            self.N75.set(0)
            self.N76.set(0)
            self.N7.set(0)
            self.N30.set(0)
            # self.N39.set(0)
            self.N40.set(0)
            self.N38.set(0)
            self.N41.set(0)
            self.N34.set(0)

        self.wanted_band_FR1()

    def off_all_none_UHB(self, event=None):
        self.UHB_all.set(False)

    def UHB_all_state(self):
        if self.UHB_all.get():
            logger.debug("UHB band all are checked")
            self.B48.set(48)
            self.B42.set(42)

        else:
            logger.debug("UHB band all are unchecked")
            self.B48.set(0)
            self.B42.set(0)

        self.wanted_band_LTE()

    def UHB_all_state_fr1(self):
        logger.debug(self.UHB_all_fr1.get())
        if self.UHB_all_fr1.get():
            logger.debug("UHB band all is checked for FR1")
            self.N48.set(48)
            self.N77.set(77)
            self.N78.set(78)
            self.N79.set(79)

        else:
            logger.debug("UHB band all is unchecked for FR1")
            self.N48.set(0)
            self.N77.set(0)
            self.N78.set(0)
            self.N79.set(0)

        self.wanted_band_FR1()

    def off_all_none_WCDMA(self, event=None):
        self.WCDMA_all.set(False)

    def off_all_none_HSUPA(self, event=None):
        self.HSUPA_all.set(False)

    def off_all_none_HSDPA(self, event=None):
        self.HSDPA_all.set(False)

    def WCDMA_all_state(self):
        if self.WCDMA_all.get():
            logger.debug("now is true")
            self.W1.set(1)
            self.W2.set(2)
            self.W4.set(4)
            self.W5.set(5)
            self.W8.set(8)
            self.W6.set(6)
            self.W19.set(19)

        else:
            logger.debug("now is false")
            self.W1.set(0)
            self.W2.set(0)
            self.W4.set(0)
            self.W5.set(0)
            self.W8.set(0)
            self.W6.set(0)
            self.W19.set(0)

        self.wanted_band_WCDMA()

    def off_all_none_GSM(self, event=None):
        self.GSM_all.set(False)

    def GSM_all_state(self):
        if self.GSM_all.get():
            logger.debug("now is true")
            self.GSM850.set(850)
            self.GSM900.set(900)
            self.GSM1800.set(1800)
            self.GSM1900.set(1900)

        else:
            logger.debug("now is false")
            self.GSM850.set(0)
            self.GSM900.set(0)
            self.GSM1800.set(0)
            self.GSM1900.set(0)

        self.wanted_band_GSM()

    def HSUPA_all_state(self):
        if self.HSUPA_all.get():
            logger.debug("now is true")
            self.U1.set(1)
            self.U2.set(2)
            self.U4.set(4)
            self.U5.set(5)
            self.U8.set(8)
            self.U6.set(6)
            self.U19.set(19)

        else:
            logger.debug("now is false")
            self.U1.set(0)
            self.U2.set(0)
            self.U4.set(0)
            self.U5.set(0)
            self.U8.set(0)
            self.U6.set(0)
            self.U19.set(0)

        self.wanted_band_HSUPA()

    def HSDPA_all_state(self):
        if self.HSDPA_all.get():
            logger.debug("now is true")
            self.D1.set(1)
            self.D2.set(2)
            self.D4.set(4)
            self.D5.set(5)
            self.D8.set(8)
            self.D6.set(6)
            self.D19.set(19)

        else:
            logger.debug("now is false")
            self.D1.set(0)
            self.D2.set(0)
            self.D4.set(0)
            self.D5.set(0)
            self.D8.set(0)
            self.D6.set(0)
            self.D19.set(0)

        self.wanted_band_HSDPA()

    def wanted_bw_fr1(self):
        self.bw_fr1 = []

        if self.bw5_fr1.get():
            logger.debug('Bw_5')
            self.bw_fr1.append(5)

        if self.bw10_fr1.get():
            logger.debug('Bw_10')
            self.bw_fr1.append(10)

        if self.bw15_fr1.get():
            logger.debug('Bw_15')
            self.bw_fr1.append(15)

        if self.bw20_fr1.get():
            logger.debug('Bw_20')
            self.bw_fr1.append(20)

        if self.bw25_fr1.get():
            logger.debug('Bw_25')
            self.bw_fr1.append(25)

        if self.bw30_fr1.get():
            logger.debug('Bw_30')
            self.bw_fr1.append(30)

        if self.bw40_fr1.get():
            logger.debug('Bw_40')
            self.bw_fr1.append(40)

        if self.bw50_fr1.get():
            logger.debug('Bw_50')
            self.bw_fr1.append(50)

        if self.bw60_fr1.get():
            logger.debug('Bw_60')
            self.bw_fr1.append(60)

        if self.bw70_fr1.get():
            logger.debug('Bw_70')
            self.bw_fr1.append(70)

        if self.bw80_fr1.get():
            logger.debug('Bw_80')
            self.bw_fr1.append(80)

        if self.bw90_fr1.get():
            logger.debug('Bw_90')
            self.bw_fr1.append(90)

        if self.bw100_fr1.get():
            logger.debug('Bw_100')
            self.bw_fr1.append(100)

        if self.bw_fr1 == []:
            logger.debug('Nothing to select for Bw')

        logger.info(f'fr1 select BW: {self.bw_fr1}')
        return self.bw_fr1

    def wanted_mcs_fr1(self):
        self.mcs_fr1 = []
        if self.bpsk_fr1.get():
            logger.debug('BPSK')
            self.mcs_fr1.append('BPSK')

        if self.qpsk_fr1.get():
            logger.debug('QPSK')
            self.mcs_fr1.append('QPSK')

        if self.q16_fr1.get():
            logger.debug('Q16')
            self.mcs_fr1.append('Q16')

        if self.q64_fr1.get():
            logger.debug('Q64')
            self.mcs_fr1.append('Q64')

        if self.q256_fr1.get():
            logger.debug('Q256')
            self.mcs_fr1.append('Q256')

        if self.mcs_fr1 == []:
            logger.debug('Nothing to select for mcs_fr1')

        logger.info(f'FR1 select MCS: {self.mcs_fr1}')
        return self.mcs_fr1

    def wanted_mcs_lte(self):
        self.mcs_lte = []
        if self.qpsk_lte.get():
            logger.debug('QPSK')
            self.mcs_lte.append('QPSK')

        if self.q16_lte.get():
            logger.debug('Q16')
            self.mcs_lte.append('Q16')

        if self.q64_lte.get():
            logger.debug('Q64')
            self.mcs_lte.append('Q64')

        if self.q256_lte.get():
            logger.debug('Q256')
            self.mcs_lte.append('Q256')

        if self.mcs_lte == []:
            logger.debug('Nothing to select for mcs_lte')

        logger.info(f'LTE select MCS: {self.mcs_lte}')
        return self.mcs_lte

    def wanted_type(self):
        self.type_ = []
        if self.dfts.get():
            logger.debug('DFTS')
            self.type_.append('DFTS')

        if self.cp.get():
            logger.debug('CP')
            self.type_.append('CP')

        if self.type_ == []:
            logger.debug('Nothing to select for type')

        logger.info(f'type select: {self.type_}')
        return self.type_

    def fr1_mode_select(self):
        if self.sa_nsa.get() == 0:
            logger.info('select mode: SA')
        elif self.sa_nsa.get() == 1:
            logger.info('select mode: NSA')
        # return self.instrument.get()

    def criteria_ulca_lte_select(self):
        if self.criteria_ulca_lte.get() == 0:
            logger.info('select ULCA LTE criteria: 3GPP')
        elif self.criteria_ulca_lte.get() == 1:
            logger.info('select ULCA LTE criteria: FCC')

    def wanted_scs(self):
        pass

    def wanted_scripts(self):
        self.script = []
        if self.general.get():
            logger.debug('GENERAL')
            self.script.append('GENERAL')

        if self.fcc.get():
            logger.debug('FCC')
            self.script.append('FCC')

        if self.ce.get():
            logger.debug('CE')
            self.script.append('CE')

        if self.endc.get():
            logger.debug('ENDC')
            self.script.append('ENDC')

        if self.cse.get():
            logger.debug('CSE')
            self.script.append('CSE')

        if self.ulca.get():
            logger.debug('ULCA')
            self.script.append('ULCA')

        if self.script == []:
            logger.debug('Nothing to select for script')

        logger.info(f'Script to select : {self.script}')
        return self.script

    def select_tx_port(self, option):
        logger.info(self.port_tx.get())
        # return self.tx_port.get()

    def select_tx_port_lte(self, option):
        logger.info(self.port_tx_lte.get())
        # return self.tx_port_lte.get()

    def select_tx_port_fr1(self, option):
        logger.info(self.port_tx_fr1.get())
        # return self.tx_port_fr1.get()

    def select_pcl_gsm(self, option):
        logger.info(f'LB: PCL{self.pcl_lb.get()}, MB: PCL{self.pcl_mb.get()}')

    def wanted_endc_tx_path_lte(self):
        logger.info(f'Switch to endc LTE tx path: {self.endc_tx_path_lte.get()}')
        return self.endc_tx_path_lte.get()

    def wanted_endc_tx_path_fr1(self):
        logger.info(f'Switch to endc FR1 tx path: {self.endc_tx_path_fr1.get()}')
        return self.endc_tx_path_fr1.get()

    def wanted_tx_path(self):
        self.tx_path = []
        if self.tx1.get():
            logger.debug('TX1')
            self.tx_path.append('TX1')

        if self.tx2.get():
            logger.debug('TX2')
            self.tx_path.append('TX2')

        if self.ulmimo.get():
            logger.debug('MIMO')
            self.tx_path.append('MIMO')

        if self.tx_path == []:
            logger.debug('Nothing to select for tx path')

        logger.info(f'script select tx path: {self.tx_path}')
        return self.tx_path

    def wanted_endc_rx_path_lte(self):
        rx_path = []
        rx_path_show = []
        if self.rx0_endc_lte.get():
            rx_path_show.append('RX0')
            rx_path.append(2)

        if self.rx1_endc_lte.get():
            rx_path_show.append('RX1')
            rx_path.append(1)

        if self.rx2_endc_lte.get():
            rx_path_show.append('RX2')
            rx_path.append(4)

        if self.rx3_endc_lte.get():
            rx_path_show.append('RX3')
            rx_path.append(8)

        if self.rx0_rx1_endc_lte.get():
            rx_path_show.append('RX0+RX1')
            rx_path.append(3)

        if self.rx2_rx3_endc_lte.get():
            rx_path_show.append('RX2+RX3')
            rx_path.append(12)

        if self.rx_all_path_endc_lte.get():
            rx_path_show.append('ALL PATH')
            rx_path.append(15)

        if rx_path == []:
            logger.debug('Nothing to select for endc LTE rx path')

        logger.info(f'RX path select ENDC LTE: {rx_path_show}')

        return rx_path

    def wanted_endc_rx_path_fr1(self):
        rx_path = []
        rx_path_show = []
        if self.rx0_endc_fr1.get():
            rx_path_show.append('RX0')
            rx_path.append(2)

        if self.rx1_endc_fr1.get():
            rx_path_show.append('RX1')
            rx_path.append(1)

        if self.rx2_endc_fr1.get():
            rx_path_show.append('RX2')
            rx_path.append(4)

        if self.rx3_endc_fr1.get():
            rx_path_show.append('RX3')
            rx_path.append(8)

        if self.rx0_rx1_endc_fr1.get():
            rx_path_show.append('RX0+RX1')
            rx_path.append(3)

        if self.rx2_rx3_endc_fr1.get():
            rx_path_show.append('RX2+RX3')
            rx_path.append(12)

        if self.rx_all_path_endc_fr1.get():
            rx_path_show.append('ALL PATH')
            rx_path.append(15)

        if rx_path == []:
            logger.debug('Nothing to select for endc LTE rx path')

        logger.info(f'RX path select ENDC FR1: {rx_path_show}')

        return rx_path

    def wanted_rx_path(self):
        self.rx_path = []
        self.rx_path_show = []
        if self.rx0.get():
            logger.debug('RX0')
            self.rx_path_show.append('RX0')
            self.rx_path.append(2)

        if self.rx1.get():
            logger.debug('RX1')
            self.rx_path_show.append('RX1')
            self.rx_path.append(1)

        if self.rx2.get():
            logger.debug('RX2')
            self.rx_path_show.append('RX2')
            self.rx_path.append(4)

        if self.rx3.get():
            logger.debug('RX3')
            self.rx_path_show.append('RX3')
            self.rx_path.append(8)

        if self.rx0_rx1.get():
            logger.debug('RX0+RX1')
            self.rx_path_show.append('RX0+RX1')
            self.rx_path.append(3)

        if self.rx2_rx3.get():
            logger.debug('RX2+RX3')
            self.rx_path_show.append('RX2+RX3')
            self.rx_path.append(12)

        if self.rx_all_path.get():
            logger.debug('all path')
            self.rx_path_show.append('ALL PATH')
            self.rx_path.append(15)

        if self.rx_path == []:
            logger.debug('Nothing to select for rx path')

        logger.info(f'RX path select: {self.rx_path_show}')
        logger.debug(f'RX path select: {self.rx_path}')

        return self.rx_path

    def select_rfout_anritsu(self, option):
        logger.info(f'RFOUT for Anritsu: {self.rfout_anritsu.get()}')

    def select_asw_path(self, option):
        logger.info(f'select AS path {self.asw_path.get()}')

    def select_sync_path(self, option):
        logger.info(f'select sync path {self.sync_path.get()}')

    def select_srs_path(self, option):
        logger.info(f'select SRS path {self.srs_path.get()}')

    def select_tx_level(self, option):
        logger.info(f'select TX Level {self.tx_level.get()}')

    def select_tx_level_endc(self, option):
        logger.info(f'select TX Level ENDC LTE: {self.tx_level_endc_lte.get()}, FR1: {self.tx_level_endc_fr1.get()}')

    def select_wait_time(self, option):
        logger.info(f'select Wait Time {self.wait_time.get()}')

    def count_select(self, option):
        logger.info(f'select Count Number: {self.count.get()}')

    def rx_quick_select(self):
        logger.info(f'Rx quick setting enable: {self.rx_quick_enable.get()}')

    def srs_enable(self):
        # logger.info(f'SRS status: {self.srs_path_enable.get()}')
        if self.srs_path_enable.get():
            logger.info('SRS is enabled')
        else:
            logger.info('SRS is disabled')

    def asw_enable(self):
        # logger.info(f'AS status: {self.asw_path_enable.get()}')
        if self.asw_path_enable.get():
            logger.info('AS is enabled')
        else:
            logger.info('AS is disabled')

    def pt_enable(self):
        if self.port_table_enable.get():
            logger.info('Port table enabled')
        else:
            logger.info('Port table disabled')

    def wanted_ftm_rb_lte(self):
        self.ftm_rb_lte = []
        if self.prb_lte.get():
            logger.debug('PRB')
            self.ftm_rb_lte.append('PRB')

        if self.frb_lte.get():
            logger.debug('FRB')
            self.ftm_rb_lte.append('FRB')

        if self.one_rb0_lte.get():
            logger.debug('1RB_0')
            self.ftm_rb_lte.append('1RB_0')

        if self.ftm_rb_lte == []:
            logger.debug('Nothing to select on RB setting for LTE')

        logger.info(f'RB setting for LTE to select: {self.ftm_rb_lte}')
        return self.ftm_rb_lte

    def wanted_ftm_rb_ulca_lte(self):
        self.ftm_rb_ulca_lte = []
        if self.one_rb0_null.get():
            logger.debug('1RB0_NULL')
            self.ftm_rb_ulca_lte.append('1RB_N')

        if self.prb_null.get():
            logger.debug('PRB_NULL')
            self.ftm_rb_ulca_lte.append('PRB_N')

        if self.frb_null.get():
            logger.debug('FRB_NULL')
            self.ftm_rb_ulca_lte.append('FRB_N')

        if self.frb_frb.get():
            logger.debug('FRB_FRB')
            self.ftm_rb_ulca_lte.append('FRB_FRB')

        if self.one_rb0_one_rbmax.get():
            logger.debug('1RB0_1RBmax')
            self.ftm_rb_ulca_lte.append('1RB0_1RBmax')

        if self.one_rbmax_one_rb0.get():
            logger.debug('1RBmax_1RB0')
            self.ftm_rb_ulca_lte.append('1RBmax_1RB0')

        if self.ftm_rb_ulca_lte == []:
            logger.debug('Nothing to select on RB setting for ULCA LTE')

        logger.info(f'RB setting for ULCA LTE to select: {self.ftm_rb_ulca_lte}')
        return self.ftm_rb_ulca_lte

    def wanted_ftm_rb_fr1(self):
        self.ftm_rb_fr1 = []
        if self.inner_full_fr1.get():
            logger.debug('INNER_FULL')
            self.ftm_rb_fr1.append('INNER_FULL')

        if self.outer_full_fr1.get():
            logger.debug('OUTER_FULL')
            self.ftm_rb_fr1.append('OUTER_FULL')

        if self.inner_1rb_left_fr1.get():
            logger.debug('INNER_1RB_LEFT')
            self.ftm_rb_fr1.append('INNER_1RB_LEFT')

        if self.inner_1rb_right_fr1.get():
            logger.debug('INNER_1RB_RIGHT')
            self.ftm_rb_fr1.append('INNER_1RB_RIGHT')

        if self.edge_1rb_left_fr1.get():
            logger.debug('EDGE_1RB_LEFT')
            self.ftm_rb_fr1.append('EDGE_1RB_LEFT')

        if self.edge_1rb_right_fr1.get():
            logger.debug('EDGE_1RB_RIGHT')
            self.ftm_rb_fr1.append('EDGE_1RB_RIGHT')

        if self.edge_full_left_fr1.get():
            logger.debug('EDGE_FULL_LEFT')
            self.ftm_rb_fr1.append('EDGE_FULL_LEFT')

        if self.edge_full_right_fr1.get():
            logger.debug('EDGE_FULL_RIGHT')
            self.ftm_rb_fr1.append('EDGE_FULL_RIGHT')

        if self.ftm_rb_fr1 == []:
            logger.debug('Nothing to select on RB setting for FR1')

        logger.info(f'RB setting for FR1 to select: {self.ftm_rb_fr1}')
        return self.ftm_rb_fr1

    def rx_auto_check_ue_pwr(self, event=None):
        self.TxMax.set(True)
        self.TxLow.set(True)
        self.rx_freq_sweep.set(False)
        self.wanted_ue_pwr()

    def sweep_auto_check_ue_pwr(self, event=None):
        self.TxMax.set(True)
        self.TxLow.set(False)
        self.rx.set(False)
        self.wanted_ue_pwr()

    def measure(self):
        import utils.parameters.external_paramters as ext_pmt

        # try:
        # to make the button to disabled state
        for button_run in self.button_run_list:
            button_run['state'] = tkinter.DISABLED

        self.export_ui_setting_yaml()
        # list-like
        ext_pmt.devices_serial = get_serial_devices()
        ext_pmt.tech = self.wanted_tech()
        ext_pmt.endc_bands = self.wanted_band_ENDC()
        ext_pmt.fr1_bands = self.wanted_band_FR1()
        ext_pmt.lte_bands = self.wanted_band_LTE()
        ext_pmt.lte_ca_bands = self.wanted_band_ca_LTE()
        ext_pmt.wcdma_bands = self.wanted_band_WCDMA()
        ext_pmt.gsm_bands = self.wanted_band_GSM()
        ext_pmt.hsupa_bands = self.wanted_band_HSUPA()
        ext_pmt.hsdpa_bands = self.wanted_band_HSDPA()
        ext_pmt.lte_bandwidths = self.wanted_bw()
        ext_pmt.lte_bandwidths_ca_combo = self.wanted_bw_ca()
        ext_pmt.fr1_bandwidths = self.wanted_bw_fr1()
        ext_pmt.channel = self.wanted_chan()
        ext_pmt.tx_max_pwr_sensitivity = self.wanted_ue_pwr()
        ext_pmt.rb_ftm_lte = self.wanted_ftm_rb_lte()
        ext_pmt.rb_ftm_ulca_lte = self.wanted_ftm_rb_ulca_lte()
        ext_pmt.rb_ftm_fr1 = self.wanted_ftm_rb_fr1()
        ext_pmt.tx_paths = self.wanted_tx_path()
        ext_pmt.tx_path_endc_lte = self.wanted_endc_tx_path_lte()
        ext_pmt.tx_path_endc_fr1 = self.wanted_endc_tx_path_fr1()
        ext_pmt.rx_paths = self.wanted_rx_path()
        ext_pmt.rx_paths_endc_lte = self.wanted_endc_rx_path_lte()
        ext_pmt.rx_paths_endc_fr1 = self.wanted_endc_rx_path_fr1()
        ext_pmt.mcs_lte = self.wanted_mcs_lte()
        ext_pmt.mcs_fr1 = self.wanted_mcs_fr1()
        ext_pmt.type_fr1 = self.wanted_type()
        ext_pmt.scripts = self.wanted_scripts()
        # non list-lke
        ext_pmt.port_tx = self.port_tx.get()
        ext_pmt.port_tx_lte = self.port_tx_lte.get()
        ext_pmt.port_tx_fr1 = self.port_tx_fr1.get()
        ext_pmt.band_segment = self.band_segment.get()
        ext_pmt.band_segment_fr1 = self.band_segment_fr1.get()
        ext_pmt.rfout_anritsu = self.rfout_anritsu.get()
        ext_pmt.asw_path = self.asw_path.get()
        ext_pmt.srs_path = self.srs_path.get()
        ext_pmt.srs_path_enable = self.srs_path_enable.get()
        ext_pmt.asw_path_enable = self.asw_path_enable.get()
        ext_pmt.port_table_en = self.port_table_enable.get()
        ext_pmt.rx_fast_test_enable = self.rx_quick_enable.get()
        ext_pmt.sync_path = self.sync_path.get()
        ext_pmt.sa_nsa = self.sa_nsa.get()
        ext_pmt.criteria_ulca_lte = self.criteria_ulca_lte.get()
        ext_pmt.mod_gsm = self.mod_gsm.get()
        ext_pmt.tx_pcl_lb = self.pcl_lb.get()
        ext_pmt.tx_pcl_mb = self.pcl_mb.get()
        ext_pmt.tx_level = self.tx_level.get()
        ext_pmt.tx_level_endc_lte = self.tx_level_endc_lte.get()
        ext_pmt.tx_level_endc_fr1 = self.tx_level_endc_fr1.get()
        # ext_pmt.wait_time = self.wait_time.get()  # obsolete
        ext_pmt.current_count = self.count.get()
        ext_pmt.psu_enable = self.psu_enable.get()
        ext_pmt.odpm_enable = self.odpm_enable.get()
        ext_pmt.volt_mipi_en = self.volt_mipi_en.get()
        ext_pmt.record_current_enable = self.record_current_enable.get()
        ext_pmt.condition = self.condition
        ext_pmt.part_number = self.part_number.get()
        ext_pmt.freq_sweep_step = self.freq_sweep_step.get()
        ext_pmt.freq_sweep_start = self.freq_sweep_start.get()
        ext_pmt.freq_sweep_stop = self.freq_sweep_stop.get()
        ext_pmt.vol_typ = self.vol_typ
        ext_pmt.tx_level_range_list[0] = self.tx_level_start.get()
        ext_pmt.tx_level_range_list[1] = self.tx_level_stop.get()

        if self.instrument.get() == 'Anritsu8820':
            from test_scripts.anritsu_items.mt8820_tx_lmh import TxTestGenre
            from test_scripts.anritsu_items.mt8820_rx import RxTestGenre
            from test_scripts.anritsu_items.mt8820_rx_freq_sweep import RxTestFreqSweep

            excel_folder_create()
            if self.wanted_test['tx']:
                inst = TxTestGenre()
                inst.run()

            if self.wanted_test['rx']:
                inst = RxTestGenre()
                inst.run()
                inst.ser.com_close()

            if self.wanted_test['rx_freq_sweep']:
                inst = RxTestFreqSweep()
                inst.run()

        elif self.instrument.get() == 'Anritsu8821':
            from test_scripts.anritsu_items.mt8821_tx_lmh import TxTestGenre
            from test_scripts.anritsu_items.mt8821_rx import RxTestGenre
            from test_scripts.anritsu_items.mt8821_rx_freq_sweep import RxTestFreqSweep

            excel_folder_create()
            if self.wanted_test['tx']:
                inst = TxTestGenre()
                inst.run()

            if self.wanted_test['rx']:
                inst = RxTestGenre()
                inst.run()
                inst.ser.com_close()  # because this might have multiple Rx controller by AT command to choose Rx path

            if self.wanted_test['rx_freq_sweep']:
                inst = RxTestFreqSweep()
                inst.run()

        elif self.instrument.get() == 'Agilent8960':
            pass

        elif self.instrument.get() == 'Cmw100':
            from test_scripts.cmw100_items.tx_lmh import TxTestGenre
            from test_scripts.cmw100_items.rx_lmh import RxTestGenre
            from test_scripts.cmw100_items.tx_level_sweep import TxTestLevelSweep
            from test_scripts.cmw100_items.tx_freq_sweep import TxTestFreqSweep
            from test_scripts.cmw100_items.tx_1rb_sweep import TxTest1RbSweep
            from test_scripts.cmw100_items.tx_power_fcc_ce import TxTestFccCe
            from test_scripts.cmw100_items.tx_ulca_combo import TxTestCa

            excel_folder_create()
            # self.test_pipeline(inst_class_dict)
            if self.wanted_test['tx'] and ext_pmt.sa_nsa == 0:
                for script in ext_pmt.scripts:
                    if script == 'GENERAL':
                        inst = TxTestGenre()
                        inst.run()
                        inst.ser.com_close()
                    elif script in ['FCC', 'CE']:
                        inst = TxTestFccCe()
                        inst.run(script)
                        inst.ser.com_close()

            if self.wanted_test['rx']:
                inst = RxTestGenre()
                inst.run()
                inst.ser.com_close()

            if self.wanted_test['tx_level_sweep'] and ext_pmt.sa_nsa == 0 and 'GENERAL' in ext_pmt.scripts:
                inst = TxTestLevelSweep()
                inst.run()
                inst.ser.com_close()

            if self.wanted_test['tx_freq_sweep'] and ext_pmt.sa_nsa == 0 and 'GENERAL' in ext_pmt.scripts:
                inst = TxTestFreqSweep()
                inst.run()
                inst.ser.com_close()

            if self.wanted_test['tx_1rb_sweep'] and ext_pmt.sa_nsa == 0 and 'GENERAL' in ext_pmt.scripts:
                inst = TxTest1RbSweep()
                inst.run()
                inst.ser.com_close()

            if self.wanted_test['tx_ca'] and ext_pmt.sa_nsa == 0 and 'ULCA' in ext_pmt.scripts:
                # for script in ext_pmt.scripts:
                # if script == 'ULCA':
                if self.ulca.get():
                    inst = TxTestCa()
                    inst.run()
                    inst.ser.com_close()


        elif self.instrument.get() == 'Cmw+Fsw':
            from test_scripts.harmonics.tx_harmonics import TxHarmonics
            # this is placeholder for tx_ca_cbe import from
            # this is placeholder for tx_ca_cbe import from

            excel_folder_create()
            # self.test_pipeline(inst_class_dict)
            for script in ext_pmt.scripts:
                if script == 'CSE':
                    if self.wanted_test['tx_harmonics'] and ext_pmt.sa_nsa == 0:
                        inst = TxHarmonics()
                        inst.run()
                        inst.ser.com_close()
                    elif self.wanted_test['tx_cbe'] and ext_pmt.sa_nsa == 0:
                        pass
                elif script == 'CA':
                    if slef.wanted_test['tx_ca_cbe'] and ext_pmt.sa_nsa == 0:
                        pass
                else:
                    pass

        # to make the button to normal state
        for button_run in self.button_run_list:
            button_run['state'] = tkinter.NORMAL

        # except Exception as err:
        #     logger.info(err)
        #     # to make the button to normal state
        #     for button_run in self.button_run_list:
        #         button_run['state'] = tkinter.NORMAL


if __name__ == "__main__":
    app = MainApp()
    app.run()
