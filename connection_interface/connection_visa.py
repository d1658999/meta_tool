import logging
import pyvisa


def get_resource(self):
    self.cmw100 = pyvisa.ResourceManager().open_resource('TCPIP0::127.0.0.1::INSTR')
    self.cmw100.timeout = 5000
    logger.info('Connect to CMW100')
    logger.info('TCPIP0::127.0.0.1::INSTR')