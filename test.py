from equipments.series_basis.callbox.cmw_series import CMW
from utils.log_init import log_set

logger = log_set('test_top')


class CMW100(CMW):
    def __init__(self):
        super().__init__('cmw100')
        logger.info('good')

def main():
    # devices_serial = get_serial_devices()
    # output_devices_dir = Path('output') / Path('test_ser_num')
    # output_devices_dir.mkdir(parents=True, exist_ok=True)
    # print(pathlib.Path.cwd())
    print(123)



if __name__ == '__main__':
    main()
