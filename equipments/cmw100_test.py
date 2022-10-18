from equipments.series_basis.cmw_series import CMW
from utils.log_init import log_set

logger = log_set()


class CMW100(CMW):
    def __init__(self, equipment='cmw100'):
        super().__init__(equipment)

    def set_gprf_measurement_fr1(self):
        logger.info('----------set GPRF Measurement----------')
        self.set_gprf_if_filter()
        self.set_gprf_bandpass_filter_bw(self.bw_fr1)
        self.set_gprf_rf_input_path(self.port_tx)
        self.set_gprf_power_count()
        self.set_gprf_power_repetition()
        self.set_gprf_power_list_mode()
        self.set_gprf_trigger_source()
        self.set_gprf_trigger_slope()
        self.set_gprf_trigger_step_length(5.0e-3)
        # self.set_gprf_trigger_step_length(8.0e-3)
        self.set_gprf_trigger_measure_length(5.0e-3)
        # self.command_cmw100_write(f'TRIGger:GPRF:MEAS:POWer:OFFSet 2.1E-3')
        # self.command_cmw100_write(f'TRIGger:GPRF:MEAS:POWer:OFFSet 5E-4')
        self.command_cmw100_write(f'TRIGger:GPRF:MEAS:POWer:OFFSet 0')
        self.command_cmw100_write(f'TRIG:GPRF:MEAS:POW:MODE ONCE')
        self.command_cmw100_write(f'CONF:GPRF:MEAS:RFS:ENP {self.tx_level}')
        self.command_cmw100_write(f'CONF:GPRF:MEAS:RFS:UMAR 10.000000')
        self.command_cmw100_write(f'CONF:GPRF:MEAS:RFS:EATT {self.loss_tx}')

def main():
    cmw100 = CMW100()
    cmw100.cmw_query('*IDN?')


if __name__ == '__main__':
    main()
