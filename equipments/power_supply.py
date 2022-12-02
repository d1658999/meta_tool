import time

from connection_interface.connection_visa import VisaComport
from utils.log_init import log_set
import utils.parameters.external_paramters as ext_pmt


logger = log_set('PSU')

class Psu:
    def __init__(self):
        self.psu_inst = None
        self.psu = VisaComport('psu')
        self.psu_select()

    def psu_select(self):
        psu_list = ['E3631A', 'E3642A', 'E36313A']
        psu_res = self.psu.query('*IDN?')
        for psu in psu_list:
            if psu in psu_res:
                self.psu_inst = psu

    def psu_init(self, voltage=ext_pmt.psu_voltage, current=ext_pmt.psu_current):
        volt_output_port = None
        if self.psu_inst == 'E3631A':
            volt_output_port = 'INST P6V'
        elif self.psu_inst == 'E3642A':
            volt_output_port = 'VOLT:RANG P8V'  # APPLY P8V is fine
        elif self.psu_inst == 'E36313A':
            volt_output_port = 'APPLY P6V'

        logger.info('----------Init PSU----------')
        logger.info(self.psu.query("*IDN?").strip())
        self.psu.write('*CLS')
        self.psu.write(volt_output_port)
        self.psu.write(f'VOLT {voltage}')
        self.psu.write(f'CURR {current}')
        logger.info(f'Now PSU limit is set to {voltage} V, {current} A')

    def get_psu_current(self, n=5):
        logger.info('----------Get psu current value----------')
        current_measure = []
        count = 0
        while count < n:
            current = eval(self.psu.query('MEAS:CURR?')) * 1000
            logger.debug(current)
            current_measure.append(current)
            count += 1
            time.sleep(0.1)
        return current_measure

    def psu_current_average(self, n):
        logger.debug('calculation for currnet average')
        current_list = self.get_psu_current(n)
        average = round(sum(current_list) / len(current_list), 2)
        logger.info(f'Average current: {average} mA')
        return average


def main():
    psu = Psu()
    psu.psu_init()
    # rm = pyvisa.ResourceManager().list_resources()
    # print(rm)


if __name__ == '__main__':
    main()
