from equipments.series_basis.cmw_series import CMW


class CMW100(CMW):
    def __init__(self):
        super().__init__('cmw100')
        print('good')

def main():
    cmw100 = CMW100()


if __name__ == '__main__':
    main()
