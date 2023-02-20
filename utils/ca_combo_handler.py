import openpyxl
from pathlib import Path


FILE_NAME = 'CA_36508.xlsx'
# FILE_PATH = Path.cwd() / Path('utils') / Path('parameters') / Path(FILE_NAME)  # formal use
FILE_PATH = Path.cwd() / Path('parameters') / Path(FILE_NAME)  # test use


def ca_combo_load_excel(band, file_path=FILE_PATH):
    """
    # return [(chan, combo_rb, cc1_rb_size, cc2_rb_size, cc1_chan, cc2_chan), ...]
    return [chan: (combo_rb, cc1_rb_size, cc2_rb_size, cc1_chan, cc2_chan), ...]
    """
    wb = openpyxl.load_workbook(file_path)
    ws = wb[f'{band}']
    max_row = ws.max_row
    # combo_ca_bw_chan = []
    # if band in [38, 39, 40, 41, 42, 48, 46, ]:
    #     for row in range(3, max_row):
    #         chan = ws.cell(row, 1).value
    #         combo = ws.cell(row, 2).value
    #         bw_cc1 = ws.cell(row, 3).value
    #         chan_ul_cc1 = ws.cell(row, 4).value
    #         bw_cc2 = ws.cell(row, 6).value
    #         chan_ul_cc2 = ws.cell(row, 7).value
    #         combo_ca_bw_chan.append((chan, combo, bw_cc1, bw_cc2, chan_ul_cc1, chan_ul_cc2))
    #     return combo_ca_bw_chan
    #
    # else:
    #     for row in range(3, max_row):
    #         chan = ws.cell(row, 1).value
    #         combo = ws.cell(row, 2).value
    #         bw_cc1 = ws.cell(row, 3).value
    #         chan_ul_cc1 = ws.cell(row, 4).value
    #         bw_cc2 = ws.cell(row, 8).value
    #         chan_ul_cc2 = ws.cell(row, 9).value
    #         combo_ca_bw_chan.append((chan, combo, bw_cc1, bw_cc2, chan_ul_cc1, chan_ul_cc2))
    #     return combo_ca_bw_chan
    chan_ca_combo_dict = {}
    combo_ca_bw_chan_list = []
    if band in [38, 39, 40, 41, 42, 48, 46, ]:
        for row in range(3, max_row):
            chan = ws.cell(row, 1).value
            combo = ws.cell(row, 2).value
            bw_cc1 = ws.cell(row, 3).value
            chan_ul_cc1 = ws.cell(row, 4).value
            bw_cc2 = ws.cell(row, 6).value
            chan_ul_cc2 = ws.cell(row, 7).value
            combo_ca_bw_chan_list.append((combo, bw_cc1, bw_cc2, chan_ul_cc1, chan_ul_cc2))
            chan_ca_combo_dict[chan] = combo_ca_bw_chan_list
    else:
        for row in range(3, max_row):
            chan = ws.cell(row, 1).value
            combo = ws.cell(row, 2).value
            bw_cc1 = ws.cell(row, 3).value
            chan_ul_cc1 = ws.cell(row, 4).value
            bw_cc2 = ws.cell(row, 8).value
            chan_ul_cc2 = ws.cell(row, 9).value
            combo_ca_bw_chan_list.append((combo, bw_cc1, bw_cc2, chan_ul_cc1, chan_ul_cc2))
            chan_ca_combo_dict[chan] = combo_ca_bw_chan_list

    return chan_ca_combo_dict



def main():
    test_list = ca_combo_load_excel('7C')
    print(test_list)



if __name__ == '__main__':
    main()
