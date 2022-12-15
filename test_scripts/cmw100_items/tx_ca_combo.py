from pathlib import Path
from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
from equipments.cmw100 import CMW100
from utils.log_init import log_set
import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
from utils.loss_handler import get_loss
from utils.adb_handler import get_odpm_current, record_current
from equipments.power_supply import Psu
from utils.excel_handler import txp_aclr_evm_current_plot_ftm, tx_power_relative_test_export_excel_ftm
from utils.channel_handler import channel_freq_select
import utils.parameters.rb_parameters as rb_pmt
from utils.ca_combo_handler import ca_combo_load_excel

logger = log_set('tx_lmh')


class TxTestCa(AtCmd, CMW100):
    def __init__(self):
        AtCmd.__init__(self)
        CMW100.__init__(self)
        self.band_cc1_channel_lte = None
        self.bw_cc2 = None
        self.bw_cc1 = None
        self.combo_list = None
        self.bw_combo = None
        self.bw_cc2_lte = None
        self.bw_cc1_lte = None
        self.psu = None
        self.tx_freq_wcdma = None
        self.file_path = None
        self.parameters = None
        self.rb_state = None
        self.script = None
        self.chan = None
        self.tx_level = ext_pmt.tx_level

    # def ca_bw_combo_seperate_lte(self, bw_cc1, bw_cc2):
    #     self.bw_cc1_lte = int(bw_cc1)
    #     self.bw_cc2_lte = int(bw_cc2)

    def set_rb_location(self, cc1_rb_size, cc2_rb_size):
        self.rb_size_cc1_lte = cc1_rb_size
        self.rb_size_cc2_lte = cc2_rb_size
        self.rb_start_cc1_lte = 0
        self.rb_start_cc2_lte = 0

    def tx_power_aclr_ca_process_lte(self):
        self.select_mode_fdd_tdd(self.band_lte)
        self.set_ca_mode('INTRaband')
        self.set_band_lte(self.band_lte)
        self.set_cc_bw_lte_cmw(1, self.bw_cc1)
        self.set_cc_bw_lte_cmw(2, self.bw_cc2)
        self.set_cc_channel_lte(1, self.band_cc1_channel_lte)
        self.set_ca_spacing()
        self.get_cc2_freq_query()
        self.get_ca_freq_low_query()
        self.tx_freq_lte = self.get_ca_freq_center_query()
        self.loss_tx = get_loss(self.tx_freq_lte)
        self.set_rf_setting_external_tx_port_attenuation_lte(self.loss_tx)
        self.get_ca_freq_high_query()
        self.set_expect_power_lte(self.tx_level)
        self.set_rf_setting_user_margin_lte(10)
        self.set_ca_no_sync_lte()  # this is at command
        self.set_select_carrier('CC1')
        self.get_modulation_avgerage_lte()
        self.set_select_carrier('CC2')
        self.get_modulation_avgerage_lte()
        self.set_measure_start_on_lte()
        self.cmw_query('*OPC?')
        self.get_aclr_average_lte()
        self.set_test_end_lte()

    def tx_power_aclr_ca_pipline_lte(self):
        self.port_tx = ext_pmt.port_tx
        self.chan = ext_pmt.channel
        self.rx_level = -70
        # items = [
        #     (tech, tx_path, band, bw_combo, mcs)
        #     for tech in ext_pmt.tech
        #     for tx_path in ext_pmt.tx_paths
        #     for band in ext_pmt.lte_bands
        #     for bw_combo in ext_pmt.lte_bandwidths_ca_combo
        #     for mcs in ext_pmt.mcs_lte
        # ]
        # self.tech = item[0]
        # self.tx_path = item[1]
        # self.band_lte = item[2]
        # self.bw_combo_lte = item[3]
        # self.mcs_cc1_lte = self.mcs_cc2_lte = item[4]
        # self.ca_bw_combo_seperate_lte(self.bw_combo_lte)  # to separate bw for cc1 and cc2

        for tech in ext_pmt.tech:
            for tx_path in ext_pmt.tx_paths:
                for band in ext_pmt.lte_bands:
                    self.tech = tech
                    self.tx_path = tx_path
                    self.band_lte = band
                    self.bw_lte = 10  # for sync
                    self.rx_freq_lte = cm_pmt_ftm.dl_freq_selected('LTE', self.band_lte, self.bw_lte)[1]  # for sync use
                    self.loss_rx = get_loss(self.rx_freq_lte)  # for sync use
                    # [(chan, combo_rb, cc1_rb_size, cc2_rb_size, cc1_chan, cc2_chan), ...]
                    self.combo_list = ca_combo_load_excel(band)

                    for chan in self.chan:  # L, M, H
                        for combo_bw in ext_pmt.lte_bandwidths_ca_combo:  # bw '20+20'
                            self.bw_cc1, self.bw_cc2 = combo_bw.split('+')  # '100+100'
                            combo_rb = f'{int(eval(self.bw_cc1)) * 5}+{int(eval(self.bw_cc2)) * 5}'
                            for mcs in ext_pmt.mcs_lte:
                                self.mcs_cc1_lte = self.mcs_cc2_lte = mcs
                                for d in self.combo_list:  # 'LOW', 'MID', 'HIGH' in combo_list
                                    if d[0][0] == chan and d[1] == combo_rb:  # this is for judge the combo_rb group
                                        # self.ca_bw_combo_seperate_lte(d[2], d[3])
                                        self.set_rb_location(d[2], d[3])  # for set rb_size_cc1/cc2_lte
                                        self.band_cc1_channel_lte = d[4]
                                        self.bw_combo_lte = f'{int(d[2] / 5)}+{int(d[3] / 5)}'
                                        self.set_test_mode_lte()  # modem open by band
                                        self.sig_gen_lte()
                                        self.sync_lte()
                                        self.tx_power_aclr_ca_process_lte()
                                    else:
                                        continue

    def run(self):
        self.tx_power_aclr_ca_pipline_lte()


def main():
    test = TxTestCa()
    test.run()



if __name__ == '__main__':
    main()