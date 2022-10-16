import pyvisa

from utils.log_init import log_set


logger = log_set()


class VisaComport:
    def __init__(self, equipment_name):
        self.inst = None
        self.begin_visa(equipment_name)

    def begin_visa(self, equipment_name):
        if equipment_name in ['CMW100', 'Cmw100', 'cmw100']:
            try:
                cmw100 = pyvisa.ResourceManager().open_resource('TCPIP0::127.0.0.1::INSTR')
                cmw100.timeout = 5000
                logger.info('Connect to CMW100')
                logger.info('TCPIP0::127.0.0.1::INSTR')
                return cmw100

            except Exception as err:
                logger.info('Please check if connecting to CMW100 or the comport is occupied')

        elif '8820' in equipment_name or '8821' in equipment_name:
            gpib_wanted = None
            for gpib in self.get_gpib():  # this is to search GPIB for 8820/8821
                inst = pyvisa.ResourceManager().open_resource(gpib)
                inst_res = inst.query('*IDN?').strip()
                if '8820' in inst or '8821' in inst_res:
                    gpib_wanted = gpib

            self.inst = pyvisa.ResourceManager().open_resource(gpib_wanted)  # to build object of 'inst'
            self.inst.timeout = 5000
            logger.info(f"Connect to {self.inst.query('*IDN?').strip()}")

    @staticmethod
    def get_gpib():
        resources = []
        for resource in pyvisa.ResourceManager().list_resources():
            if 'GPIB' in resource:
                resources.append(resource)
                logger.debug(resource)
        return resources

    def write(self, command):
        self.inst.write(command)

    def query(self, command):
        return self.inst.query(command)
