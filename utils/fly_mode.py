import time

from utils.log_init import log_set
from connection_interface.connection_serial import ModemComport

logger = log_set('FlyMode')


class FlyMode:
    def __init__(self):
        self.off = 'AT+CFUN=0\r'
        self.on = 'AT+CFUN=1\r'
        self.ser = None
        self.begin()

    def begin(self):
        self.ser = ModemComport()

    def com_open(self):
        self.ser.com_open()

    def com_close(self):
        self.ser.com_close()

    def fly_on(self):
        self.ser.write(self.off.encode())
        logger.info('flymode is on, 0')

    def fly_off(self):
        self.ser.write(self.on.encode())
        logger.info('flymode is off, 1')


def main():  # this is used for test some function
    s = FlyMode()
    s.com_open()
    s.fly_on()
    time.sleep(1)
    s.fly_off()
    s.com_close()


if __name__ == '__main__':
    main()
