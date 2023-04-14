from pathlib import Path
from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
from equipments.cmw100 import CMW100
from utils.log_init import log_set
import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
from utils.loss_handler import get_loss
from utils.adb_handler import get_odpm_current, RecordCurrent
from equipments.power_supply import Psu
from utils.excel_handler import txp_aclr_evm_current_plot_ftm, tx_power_relative_test_export_excel_ftm
from utils.channel_handler import channel_freq_select
import utils.parameters.rb_parameters as rb_pmt
from utils.ca_combo_handler import ca_combo_load_excel
from utils.parameters.rb_parameters import ULCA_3GPP_LTE
from utils.parameters.rb_parameters import ulca_fcc_lte
from utils.excel_handler import tx_ulca_power_relative_test_export_excel_ftm

logger = log_set('tx_ulca_lmh')


class TxTestCa(AtCmd, CMW100):
    def __init__(self):
        AtCmd.__init__(self)
        CMW100.__init__(self)
        self.band_cc1_channel_lte = None
        self.band_cc2_channel_lte = None
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
    @staticmethod
    def debug_ulca():
        if ext_pmt.debug_enable:
            input(f'Stop, and press "Enter" key in CLI and keep going')
        else:
            pass

    def get_temperature(self):
        """
        for P22, AT+GOOGTHERMISTOR=1,1 for MHB LPAMid/ MHB Rx1 LFEM, AT+GOOGTHERMISTOR=0,1
        for LB LPAMid, MHB ENDC LPAMid, UHB(n77/n79 LPAF)
        :return:
        """
        res0 = self.query_thermister0()
        res1 = self.query_thermister1()
        res_list = [res0, res1]
        therm_list = []
        for res in res_list:
            for r in res:
                if 'TEMPERATURE' in r.decode().strip():
                    try:
                        temp = eval(r.decode().strip().split(':')[1]) / 1000
                        therm_list.append(temp)
                    except Exception as err:
                        logger.debug(err)
                        therm_list.append(None)
        logger.info(f'thermistor0 get temp: {therm_list[0]}')
        logger.info(f'thermistor1 get temp: {therm_list[1]}')
        return therm_list

    def set_rb_allocation(self, cc1, cc2):
        self.rb_size_cc1_lte, self.rb_start_cc1_lte = cc1
        self.rb_size_cc2_lte, self.rb_start_cc2_lte = cc2

    def criteria_rb_selector_ulca_lte(self, combo_rb, mcs, allocation):
        if ext_pmt.criteria_ulca_lte == 0:
            cc1, cc2 = ULCA_3GPP_LTE[combo_rb][mcs][allocation]
            return cc1, cc2
        elif ext_pmt.criteria_ulca_lte == 1:
            cc1, cc2 = ulca_fcc_lte(self.bw_cc1, self.bw_cc2, allocation)
            return cc1, cc2

    def set_center_freq_tx_rx_loss(self):
        # this steps are to set on CMW100 and get center freq and then to give the parameter to AT CMD
        self.select_mode_fdd_tdd(self.band_lte)
        self.set_ca_mode('INTRaband')
        self.set_band_lte(self.band_lte)
        self.set_cc_bw_lte(1, self.bw_cc1)
        self.set_cc_bw_lte(2, self.bw_cc2)
        self.set_cc_channel_lte(1, self.band_cc1_channel_lte)
        self.set_cc_channel_lte(2, self.band_cc2_channel_lte)
        self.set_ca_spacing()
        # self.get_cc2_freq_query()
        # self.get_ca_freq_low_query()
        # self.get_ca_freq_high_query()
        self.tx_freq_lte = self.get_ca_freq_center_query()
        self.rx_freq_lte = cm_pmt_ftm.transfer_freq_tx2rx_lte(self.band_lte, self.tx_freq_lte)
        self.rx_freq_lte = int(self.rx_freq_lte / 100) * 100  # this is for sync use due to problem with detailed freq
        self.loss_tx = get_loss(self.tx_freq_lte)
        self.loss_rx = get_loss(self.rx_freq_lte)

    def tx_set_ulca_lte(self):
        # this is at command, real to tx set
        self.set_ulca_combo_lte()

    def tx_power_aclr_ulca_process_lte(self):
        self.set_test_mode_lte()  # modem open by band
        self.antenna_switch_v2()
        self.set_center_freq_tx_rx_loss()  # this is to set basic tx/rx/loss
        self.sig_gen_lte()
        self.sync_lte()
        self.tx_set_ulca_lte()

        # ulca combo info
        ulca_combo = [
            self.band_ulca_lte, self.chan_lmh,
            self.bw_cc1, self.bw_cc2, self.band_cc1_channel_lte, self.band_cc2_channel_lte,
            ]

        # ulca rb setting info
        ulca_rb_setting = [
            self.rb_size_cc1_lte, self.rb_start_cc1_lte,
            self.rb_size_cc2_lte, self.rb_start_cc2_lte,
        ]

        # mcs and path setting info
        mcs_path_setting = [self.mcs_cc1_lte, self.tx_path, self.sync_path, self.asw_srs_path]

        # [6 items] + [OBW, sem_pwr] + [U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2] + [Power, EVM, Freq_Err, IQ]*2 + \
        # [4 items] + path_setting(4 items)
        # total 29 information
        ulca_results = ulca_combo + self.tx_measure_ulca_lte() + ulca_rb_setting + mcs_path_setting
        logger.debug(ulca_results)

        # measure temp
        therm_list = self.get_temperature()

        # sub-information
        sub_info = {
            'cc1_alloc': self.alloc_cc[0],
            'cc2_alloc': self.alloc_cc[1],
            'temp0': therm_list[0],
            'temp1': therm_list[1],
        }


        # export to excel
        tx_ulca_power_relative_test_export_excel_ftm(self.tech, ulca_results, sub_info)

        logger.debug(ulca_results)

        # debug use
        self.debug_ulca()

        self.set_test_end_lte()

    def tx_power_aclr_ulca_pipline_lte(self):
        self.preset_instrument()
        self.set_test_end_lte()
        self.port_tx = ext_pmt.port_tx
        self.chan = ext_pmt.channel
        self.rx_level = -70

        # this is for now only 'LTE'
        if ext_pmt.tech:
            tech_list = ['LTE']
        else:
            tech_list = []

        for tech in tech_list:
            # this is for now only 'TX1'
            if 'TX2' in ext_pmt.tx_paths:
                tx_path_list = ext_pmt.tx_paths
                tx_path_list.remove('TX2')
            else:
                tx_path_list = ext_pmt.tx_paths

            for tx_path in tx_path_list:
                for band in ext_pmt.lte_ca_bands:  # '7C'
                    self.tech = tech
                    self.tx_path = tx_path
                    self.band_ulca_lte = band  # '7C'
                    self.band_lte = int(band[:-1])  # '7C' -> 7, '41C' -> 41
                    self.bw_lte = 10  # for sync
                    allocation = None
                    # self.rx_freq_lte = cm_pmt_ftm.dl_freq_selected('LTE', self.band_lte, self.bw_lte)[1]  # for sync use
                    # self.loss_rx = get_loss(self.rx_freq_lte)  # for sync use

                    # {chan: combo_rb: (cc1_rb_size, cc2_rb_size, cc1_chan, cc2_chan), ...}
                    self.combo_dict = ca_combo_load_excel(band)

                    for chan in self.chan:  # L, M, H
                        self.chan_lmh = chan
                        for combo_bw in ext_pmt.lte_bandwidths_ca_combo:  # bw '20+20'
                            self.bw_combo_lte = combo_bw
                            self.bw_cc1, self.bw_cc2 = combo_bw.split('+')  # '20', '20'
                            combo_rb = f'{int(self.bw_cc1) * 5}+{int(self.bw_cc2) * 5}'  # rb_combo '100+100'
                            for mcs in ext_pmt.mcs_lte:
                                self.mcs_cc1_lte = self.mcs_cc2_lte = mcs
                                bw_rb_cc1, bw_rb_cc2, chan_cc1, chan_cc2 = self.combo_dict[chan][combo_rb]
                                self.bw_rb_cc1 = bw_rb_cc1
                                self.bw_rb_cc2 = bw_rb_cc2
                                self.band_cc1_channel_lte = chan_cc1
                                self.band_cc2_channel_lte = chan_cc2

                                for allocation in ext_pmt.rb_ftm_ulca_lte:
                                    try:
                                        self.alloc_cc = allocation.split('_')
                                        # this is return rb allocation to cc1 and cc2
                                        cc1, cc2 = self.criteria_rb_selector_ulca_lte(combo_rb, mcs, allocation)

                                        self.set_rb_allocation(cc1, cc2)
                                        self.tx_power_aclr_ulca_process_lte()
                                    except Exception as err:
                                        logger.info(f'Exception message: {err}')
                                        logger.info(f"It might {band} doesn't have this combo {combo_rb}, {mcs}, "
                                                    f"{allocation}")

    def run(self):
        for tech in ext_pmt.tech:
            if tech == 'LTE':
                self.tx_power_aclr_ulca_pipline_lte()

def main():
    test = TxTestCa()
    test.run()



if __name__ == '__main__':
    main()