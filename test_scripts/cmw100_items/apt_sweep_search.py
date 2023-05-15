import traceback
from pathlib import Path
from utils.log_init import log_set
from test_scripts.cmw100_items.tx_level_sweep import TxTestLevelSweep
from utils.loss_handler import get_loss
import utils.parameters.external_paramters as ext_pmt
from utils.excel_handler import txp_aclr_evm_current_plot_ftm, tx_power_relative_test_export_excel_ftm
from utils.excel_handler import select_file_name_genre_tx_ftm, excel_folder_path
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
from utils.channel_handler import channel_freq_select
import utils.parameters.rb_parameters as rb_pmt

import datetime

logger = log_set('apt_sweep')
# TX_LEVEL_LIST = [24, 23]
VCC_START = 500
VCC_STOP = 60
VCC_STEP = 10
BIAS0_START = 255
BIAS0_STOP = 32
BIAS0_STEP = 4
BIAS1_START = 255
BIAS1_STOP = 32
BIAS1_STEP = 4
ACLR_LIMIT_USL = -37
ACLR_MARGIN = 15
EVM_LIMIT_USL = 2.0
EVM_LIMIT_ABS = 2.5
COUNT_BIAS1 = 16
COUNT_BIAS0 = 8
COUNT_VCC = 4


class AptSweep(TxTestLevelSweep):
    def __init__(self):
        super().__init__()
        self.candidate = None

    def tx_apt_sweep_pipeline_fr1(self):
        self.rx_level = ext_pmt.init_rx_sync_level
        self.tx_level = ext_pmt.tx_level
        self.port_tx = ext_pmt.port_tx
        self.chan = ext_pmt.channel
        self.sa_nsa_mode = ext_pmt.sa_nsa
        items = [
            (tech, tx_path, bw, band, type_)
            for tech in ext_pmt.tech
            for tx_path in ext_pmt.tx_paths
            for bw in ext_pmt.fr1_bandwidths
            for band in ext_pmt.fr1_bands
            for type_ in ext_pmt.type_fr1
        ]

        for item in items:
            if item[0] == 'FR1' and ext_pmt.fr1_bands != []:
                self.tech = item[0]
                self.tx_path = item[1]
                self.bw_fr1 = item[2]
                self.band_fr1 = item[3]
                self.type_fr1 = item[4]
                try:
                    self.port_table_selector(self.band_fr1, self.tx_path)
                    if self.bw_fr1 in cm_pmt_ftm.bandwidths_selected_fr1(self.band_fr1):
                        # force to APT mode
                        self.set_apt_mode_force(1, 'TX1', 0)

                        self.tx_apt_sweep_process_fr1()

                        # recover to ET/SAPT mode
                        self.set_apt_mode_force(1, 'TX1', 1)
                    else:
                        logger.info(f'NR B{self.band_fr1} does not have BW {self.bw_fr1}MHZ')

                except KeyError as err:
                    logger.debug(f'Error {err}')
                    traceback.print_exc()
                    logger.info(f'NR Band {self.band_fr1} does not have this tx path {self.tx_path}')

        for bw in ext_pmt.fr1_bandwidths:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'FR1', 'apt_sweep')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'GENERAL', 'tech': 'FR1'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundError:
                logger.info(f'there is no file to plot BW{bw} ')

    def tx_apt_sweep_process_fr1(self):
        """
        band_fr1:
        bw_fr1:
        tx_freq_fr1:
        rb_num:
        rb_start:
        mcs:
        pwr:
        rf_port:
        loss:
        tx_path:
        data {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('FR1', self.band_fr1, self.bw_fr1)
        tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq) for rx_freq in rx_freq_list]
        self.rx_freq_fr1 = rx_freq_list[1]
        self.tx_freq_fr1 = tx_freq_list[1]
        self.loss_rx = get_loss(rx_freq_list[1])
        self.preset_instrument()
        self.set_test_end_fr1()
        self.set_test_mode_fr1()
        self.select_asw_srs_path()
        self.sig_gen_fr1()
        self.sync_fr1()

        tx_freq_lmh_list = [cm_pmt_ftm.transfer_freq_rx2tx_fr1(self.band_fr1, rx_freq) for rx_freq in rx_freq_list]
        tx_freq_select_list = sorted(set(channel_freq_select(self.chan, tx_freq_lmh_list)))

        for mcs in ext_pmt.mcs_fr1:
            self.mcs_fr1 = mcs
            for script in ext_pmt.scripts:
                if script == 'GENERAL':
                    self.script = script
                    for rb_ftm in ext_pmt.rb_ftm_fr1:  # INNER, OUTER
                        self.rb_size_fr1, self.rb_start_fr1 = rb_pmt.GENERAL_FR1[self.bw_fr1][self.scs][self.type_fr1][
                            self.rb_alloc_fr1_dict[rb_ftm]]  # INNER: 0, # OUTER: 1
                        self.rb_state = rb_ftm  # INNER, OUTER

                        #  initial all before tx level progress
                        for tx_freq_select in tx_freq_select_list:
                            self.tx_freq_fr1 = tx_freq_select
                            self.loss_tx = get_loss(self.tx_freq_fr1)
                            # self.tx_set_fr1()
                            # self.tx_power_relative_test_initial_fr1()

                            #  following is real change tx level progress
                            self.tx_apt_sweep_subprocess_fr1()

        self.set_test_end_fr1()

    def tx_apt_sweep_subprocess_fr1(self):
        tx_range_list = ext_pmt.tx_level_range_list  # [tx_level_1, tx_level_2]

        logger.info('----------TX Level Sweep progress---------')
        logger.info(f'----------from {tx_range_list[0]} dBm to {tx_range_list[1]} dBm----------')

        step = -1 if tx_range_list[0] > tx_range_list[1] else 1

        self.data = {}
        self.candidate = {}
        vcc_start, bias0_start, bias1_start = VCC_START, BIAS0_START, BIAS1_START
        if self.tx_path in ['TX1', 'TX2']:
            for tx_level in range(tx_range_list[0], tx_range_list[1] + step, step):
                self.tx_level = tx_level
                logger.info(f'========Now Tx level = {self.tx_level} dBm========')
                # self.set_level_fr1(self.tx_level)
                self.tx_set_fr1()
                self.set_apt_trymode_5()

                self.set_pa_range_mode('H')
                self.set_apt_trymode_5()


                # self.aclr_mod_current_results = self.tx_measure_fr1()

                # start to sweep vcc, bias0, bias1
                self.tx_apt_sweep_search(vcc_start, bias0_start, bias1_start)

                # this will use previous vcc,bias0, bias1 to start sweep
                vcc_start = self.candidate[self.tx_level][-3]
                bias0_start = self.candidate[self.tx_level][-2]
                bias1_start = self.candidate[self.tx_level][-1]
                logger.info(f'Adopt the best current consumption as {vcc_start}, {bias0_start}, {bias1_start} '
                            f'as next tx level start parameter')

        elif self.tx_path in ['MIMO']:
            logger.info("MIMO doesn't need this function")
            # for tx_level in range(tx_range_list[0], tx_range_list[1] + step, step):
            #     path_count = 1  # this is for mimo path to store tx_path
            #     for port_tx in [self.port_mimo_tx1, self.port_mimo_tx2]:
            #         self.port_tx = port_tx
            #         self.tx_path_mimo = self.tx_path + f'_{path_count}'
            #         self.tx_level = tx_level
            #         logger.info(f'========Now Tx level = {self.tx_level} dBm========')
            #         self.set_level_fr1(self.tx_level)
            #
            #         # start to sweep vcc, bias0, bias1
            #         self.tx_apt_sweep_search(vcc_start, bias0_start, bias1_start)
            #
            #         # this willuse previous vcc,bias0, bias1 to start sweep
            #         vcc_start = self.candidate[-3]
            #         bias0_start = self.candidate[-2]
            #         bias1_start = self.candidate[-1]

    def tx_apt_sweep_search(self, vcc_start, bias0_start, bias1_start):
        count_vcc = COUNT_VCC
        for vcc in range(vcc_start, VCC_STOP, -VCC_STEP):
            logger.info(f'Now VCC is {vcc} to run')
            # speed up sweep time for bias0
            if self.tx_level >= 18:
                count_bias0 = COUNT_BIAS0
            elif 18 > self.tx_level > 12:
                count_bias0 = 6
            elif 12 > self.tx_level > 7:
                count_bias0 = 4
            else:
                count_bias0 = 2

            for bias0 in range(bias0_start, BIAS0_STOP, -BIAS0_STEP):
                # speed up sweep time for bias1
                if self.tx_level >= 18:
                    count_bias1 = COUNT_BIAS1
                elif 18 > self.tx_level >= 12:
                    count_bias1 = 8
                elif 12 > self.tx_level > 7:
                    count_bias1 = 4
                else:
                    count_bias1 = 2

                for bias1 in range(bias1_start, BIAS1_STOP, -BIAS1_STEP):

                    self.set_level_fr1(self.tx_level)
                    self.set_apt_trymode()

                    self.set_apt_vcc_trymode('TX1', vcc)
                    self.set_apt_bias_trymode('TX1', bias0, bias1)

                    self.aclr_mod_current_results = self.tx_measure_fr1()
                    self.aclr_mod_current_results.append(self.measure_current(self.band_fr1))
                    self.aclr_mod_current_results.append(vcc)
                    self.aclr_mod_current_results.append(bias0)
                    self.aclr_mod_current_results.append(bias1)

                    logger.debug(f'Get the apt result{self.aclr_mod_current_results}, {vcc}, {bias0}, {bias1}')

                    aclr_m = self.aclr_mod_current_results[2]
                    aclr_p = self.aclr_mod_current_results[4]
                    evm = self.aclr_mod_current_results[7]

                    if ((ACLR_LIMIT_USL - ACLR_MARGIN) < aclr_m < ACLR_LIMIT_USL) and (
                            (ACLR_LIMIT_USL - ACLR_MARGIN) < aclr_p < ACLR_LIMIT_USL) and (evm < EVM_LIMIT_USL):

                        self.data[self.tx_level] = self.aclr_mod_current_results

                        # check the current if it is the smallest
                        try:
                            if not self.candidate:
                                self.candidate[self.tx_level] = self.aclr_mod_current_results

                            elif self.candidate[self.tx_level][-4] >= self.aclr_mod_current_results[-4]:
                                self.candidate[self.tx_level] = self.aclr_mod_current_results
                            else:
                                pass
                        except KeyError:
                            # this is for forward tx_level to continue
                            self.candidate[self.tx_level] = self.aclr_mod_current_results

                        if self.tx_path in ['TX1', 'TX2']:  # this is for TX1, TX2, not MIMO
                            self.parameters = {
                                'script': self.script,
                                'tech': self.tech,
                                'band': self.band_fr1,
                                'bw': self.bw_fr1,
                                'tx_freq_level': self.tx_freq_fr1,
                                'mcs': self.mcs_fr1,
                                'tx_path': self.tx_path,
                                'mod': None,
                                'rb_state': self.rb_state,
                                'rb_size': self.rb_size_fr1,
                                'rb_start': self.rb_start_fr1,
                                'sync_path': self.sync_path,
                                'asw_srs_path': self.asw_srs_path,
                                'scs': self.scs,
                                'type': self.type_fr1,
                                'test_item': 'apt_sweep',
                            }
                            self.file_path = tx_power_relative_test_export_excel_ftm(self.data, self.parameters)
                            self.data = {}
                    elif aclr_m > ACLR_LIMIT_USL or aclr_p > ACLR_LIMIT_USL or evm > EVM_LIMIT_ABS:
                        if count_bias1 > 1:
                            count_bias1 -= 1
                            logger.debug(f'activate the exception for bias1')
                        else:
                            logger.info(f'over {COUNT_BIAS1} times failed spec for bias1, so skip remains of bias1')
                            break
                if count_bias0 > 1 and count_bias1 == 1:
                    count_bias0 -= 1
                    logger.debug(f'activate the exception for bias0')
                elif count_bias0 > 1:
                    continue
                else:
                    logger.info(f'over {COUNT_BIAS0} times failed spec for bias0, so skip remains of bias0')
                    break
            if count_vcc > 1 and count_bias0 == 1:
                count_vcc -= 1
                logger.debug(f'activate the exception for vcc')
            elif count_vcc > 1:
                continue
            else:
                logger.info(f'over {COUNT_VCC} times failed spec for vcc, so skip remains of vcc')
                break

    def run(self):
        for tech in ext_pmt.tech:
            if tech == 'FR1':
                self.tx_apt_sweep_pipeline_fr1()

        self.cmw_close()


def main():
    start = datetime.datetime.now()

    apt_sweep = AptSweep()
    # apt_sweep.tx_apt_sweep_pipeline_fr1()
    apt_sweep.set_apt_internal_calibration_fr1('TX1', 1950000)
    stop = datetime.datetime.now()

    logger.info(f'Timer: {stop - start}')


if __name__ == '__main__':
    main()
