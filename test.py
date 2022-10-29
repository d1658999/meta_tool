from equipments.series_basis.cmw_series import CMW
from utils.log_init import log_set

logger = log_set('test_top')


class CMW100(CMW):
    def __init__(self):
        super().__init__('cmw100')
        logger.info('good')

def main():
    tt = ['GMSK'] * 8
    print(tt)



if __name__ == '__main__':
    main()
