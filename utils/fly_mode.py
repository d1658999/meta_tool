import time

from utils.log_init import log_set
from connection_interface.connection_serial import ModemComport

logger = log_set()


class FlyMode:
    def __init__(self, comport):
        self.on = None
        self.off = None
        self.ser = None
        self.begin(comport)

    def begin(self, comport):
        self.ser = ModemComport()
        self.ser.baudrate = 230400
        self.ser.port = comport
        self.off = 'AT+CFUN=0\r'
        self.on = 'AT+CFUN=1\r'

    def com_open(self):
        self.ser.open()

    def com_close(self):
        self.ser.close()

    def fly_on(self):
        self.ser.write(self.off.encode())
        logger.info('flymode is on, 0')

    def fly_off(self):
        self.ser.write(self.on.encode())
        logger.info('flymode is off, 1')


def main():  # this is used for test some function
    port = ModemComport().get_comport_wanted()
    s = FlyMode(port)
    s.com_open()
    s.fly_on()
    time.sleep(1)
    s.fly_off()
    s.com_close()


if __name__ == '__main__':
    main()
