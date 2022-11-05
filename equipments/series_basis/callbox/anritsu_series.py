from connection_interface.connection_visa import VisaComport
from utils.log_init import log_set

logger = log_set('Anritsu_series')


class CMW:
    def __init__(self, equipment):
        self.cmw = VisaComport(equipment)

    def cmw_query(self, command):
        response = self.cmw.query(command).strip()
        logger.info(f'Visa::<<{command}')
        logger.info(f'Visa::>>{response}')
        return response

    def cmw_write(self, command):
        self.cmw.write(command)
        logger.info(f'Visa::<<{command}')