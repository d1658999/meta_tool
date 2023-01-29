import pyvisa
import time
import utils.parameters.external_paramters as ext_pmt
from connection_interface.connection_visa import VisaComport
from utils.log_init import log_set

logger = log_set('temp_chamber')


class TempChamber:
    def __init__(self):
        self.tpchb = VisaComport('temp_chamber')

    def tpchb_init(self, target_temp, wait):
        logger.info('----------Init Temp----------')
        logger.info(self.tpchb.query("*IDN?").strip())
        logger.info(f'Start to go to temp {target_temp} C')
        self.power_on()
        self.set_temperature(target_temp)
        time.sleep(0.2)
        temp_state = None
        try:
            temp_state = float(self.tpchb.query('TEMP?').strip().split(',')[0])
        except Exception as err:
            logger.info(err)
            temp_state = float(self.tpchb.query('TEMP?').strip().split(',')[0])
        finally:
            while True:
                if target_temp - 1 < temp_state < target_temp + 1:
                    break
                else:
                    time.sleep(10)
                    temp_state = float(self.tpchb.query('TEMP?').strip().split(',')[0])
                    logger.info(f'Now the room temp is {temp_state}C')
            logger.info(f'Achieve to the target temp {target_temp}, and need to wait {wait} seconds')
            time.sleep(wait)

    def power_off(self):
        """
        power off the temop chamber
        """
        logger.into('Power off the temp-chamber')
        self.tpchb.write(f'POWER,OFF')

    def power_on(self):
        """
        power on the temop chamber
        """
        logger.info('Power on the temp-chamber')
        self.tpchb.write(f'POWER,ON')

    def set_temperature(self, target_temp=25.0):
        """
        set the target temp
        """
        self.tpchb.write(f'TEMP,S{target_temp} H80 L-40')

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
    pass


if __name__ == '__main__':
    main()
