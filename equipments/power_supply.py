import pyvisa
import logging
from logging.config import fileConfig
import time
import utils.parameters.external_paramters as ext_pmt


PSU_LIST = ['E3631A', 'E3642A', 'E36313A']
fileConfig('logging.ini')
logger = logging.getLogger()


class Psu:
    def __init__(self):
        self.build_object()
        # if psu_enable:
        #     self.build_object()
        # else:
        #     logger.info('----------Disable PSU----------')

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

    def get_current(self, n=5):
        logger.info('----------Get current value----------')
        current_measure = []
        count = 0
        while count < n:
            current = eval(self.psu.query('MEAS:CURR?')) * 1000
            logger.debug(current)
            current_measure.append(current)
            count += 1
            # time.sleep(0.1)
        return current_measure

    def current_average(self, n):
        logger.debug('calculation for currnet average')
        _n = n + 4
        current_list = self.get_current(_n)  # _n >= 5
        average = round(sum(current_list) / len(current_list), 2)
        logger.info(f'Average current: {average} mA')
        return average

    def build_object(self):
        logger.info('start to connect')
        gpib_usb_want = None
        for gpib_usb in self.get_gpib_psu():  # this is to search GPIB for PSU
            inst = pyvisa.ResourceManager().open_resource(gpib_usb)
            inst = inst.query('*IDN?').strip()
            logger.info('----------Search PSU we are using----------')
            for psu in PSU_LIST:
                if psu in inst:
                    gpib_usb_want = gpib_usb
                    self.psu_inst = psu
                    break

        self.psu = pyvisa.ResourceManager().open_resource(gpib_usb_want)  # to build inst object
        self.psu.timeout = 5000

    @staticmethod
    def get_gpib_psu():
        resources = []
        logger.info('----------Search GPIB----------')
        for resource in pyvisa.ResourceManager().list_resources():
            if 'GPIB' in resource or 'USB' in resource:
                resources.append(resource)
                logger.debug(resource)
        return resources



def main():
        psu = Psu()
        psu.psu_init()
        # rm = pyvisa.ResourceManager().list_resources()
        # print(rm)




if __name__ == '__main__':
    main()