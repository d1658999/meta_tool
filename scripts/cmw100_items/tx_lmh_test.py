from equipments.series_basis.serial_series import AtCmd
from equipments.cmw100_test import CMW100
from utils.log_init import log_set

logger = log_set('tx_lmh')


class Tx_lmh_test(AtCmd, CMW100):
    def __init__(self):
        AtCmd.__init__(self)
        CMW100.__init__(self)
        self.system_base_option_version_query('CMW_NRSub6G_Meas')
        self.band_fr1 = 2
        self.tech = 'FR1'
        self.select_mode_fdd_tdd(self.band_fr1)
        self.select_scs_fr1(self.band_fr1)
        self.set_band_fr1(self.band_fr1)






def main():
    test = Tx_lmh_test()


if __name__ == '__main__':
    main()


