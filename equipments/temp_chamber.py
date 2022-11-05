import pyvisa
import logging
from logging.config import fileConfig
import time
import want_test_band as wt

fileConfig('logging.ini')
logger = logging.getLogger()


class TempChamber:
    def __init__(self):
        self.build_object()

    def tpchb_init(self, target_temp=wt.temp):
        logger.info('----------Init Temp----------')
        logger.info(self.tpchb.query("*IDN?").strip())
        logger.info(f'Start to go to temp {target_temp} C')
        self.tpchb.write(f'POWER,ON')
        self.tpchb.write(f'TEMP,S{target_temp} H80 L-40')
        time.sleep(0.2)
        temp_state = float(self.tpchb.query('TEMP?').strip().split(',')[0])
        while True:
            if target_temp - 1 < temp_state < target_temp + 1:
                break
            else:
                time.sleep(10)
                temp_state = float(self.tpchb.query('TEMP?').strip().split(',')[0])
                logger.info(f'Now the room temp is {temp_state}C')
        logger.info(f'Acheieve to the target temp {target_temp}, and need to wait 2 min')
        time.sleep(120)

    def build_object(self):
        logger.info('start to connect')
        gpib_want = None
        for gpib in self.get_gpib_tpchb():  # this is to search GPIB for PSU
            inst = pyvisa.ResourceManager().open_resource(gpib)
            inst = inst.query('*IDN?').strip()
            logger.info('----------Search temp chamber we are using----------')
            if 'NA:CMD_ERR' in inst:
                gpib_want = gpib
                break

        self.tpchb = pyvisa.ResourceManager().open_resource(gpib_want)  # to build inst object
        self.tpchb.timeout = 5000

    @staticmethod
    def get_gpib_tpchb():
        resources = []
        logger.info('----------Search GPIB----------')
        for resource in pyvisa.ResourceManager().list_resources():
            if 'GPIB' in resource:
                resources.append(resource)
                logger.debug(resource)
        return resources


def main():
    psu = Psu(True)
    psu.psu_init()
    # rm = pyvisa.ResourceManager().list_resources()
    # print(rm)


if __name__ == '__main__':
    main()
