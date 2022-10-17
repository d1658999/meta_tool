from equipments.series_basis.cmw_series import CMW
from utils.log_init import log_set


logger = log_set()


class CMW100(CMW):
    def __init__(self, equipment='cmw100'):
        super().__init__(equipment)




def main():
    cmw100 = CMW100()
    cmw100.cmw_query('*IDN?')


if __name__ == '__main__':
    main()
