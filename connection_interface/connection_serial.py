import serial
import serial.tools.list_ports

from utils.log_init import log_set

logger = log_set('Serial')


class ModemComport:
    def __init__(self):
        pass
        self.ser = None
        self.begin_serial()

    @staticmethod
    def get_comport_wanted():
        comports = serial.tools.list_ports.comports()
        comport_waned = None
        for comport in comports:
            if 'Modem' in comport.description:
                comport_waned = comport.name
                logger.info(f'Modem comport is: {comport_waned}')
                logger.debug(f'Serial number is: {comport.serial_number}')

        return comport_waned

    def com_open(self):
        try:
            self.ser.open()
        except Exception as err:
            logger.info('check the comport is locked or drop comport')
            logger.debug(err)
        else:
            logger.info('open modem comport')

    def com_close(self):
        self.ser.close()

    def begin_serial(self):
        self.ser = serial.Serial()
        self.ser.baudrate = 230400
        self.ser.timeout = 0.2
        self.ser.port = self.get_comport_wanted()
        self.com_open()

    def write(self, command):
        self.ser.write(command)

    def readlines(self):
        return self.ser.readlines()


def test():
    logger.info('test')


def main():
    test()


if __name__ == '__main__':
    main()
