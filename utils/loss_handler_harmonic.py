import csv
from pathlib import Path


def read_loss_file_cmw100():
    # file_path = Path('loss.csv')  # test use
    file_path = Path('utils') / Path('harmonic_CMW100_C.csv')
    with open(file_path, 'r') as csvfile:
        rows = csv.reader(csvfile)
        next(rows)  # skip the title
        loss_dict = {}
        for row in list(rows):
            loss_dict[float(row[0])] = float(row[1])
        return loss_dict


def read_loss_file_spectrum():
    # file_path = Path('loss.csv')  # test use
    file_path = Path('utils') / Path('harmonic_SPECTRUM_D.csv')
    with open(file_path, 'r') as csvfile:
        rows = csv.reader(csvfile)
        next(rows)  # skip the title
        loss_dict = {}
        for row in list(rows):
            loss_dict[float(row[0])] = float(row[1])
        return loss_dict


# def read_loss_file_spectrum_lb():
#     # file_path = Path('loss.csv')  # test use
#     file_path = Path('utils') / Path('harmonic_SPECTRUM_D_LB.csv')
#     with open(file_path, 'r') as csvfile:
#         rows = csv.reader(csvfile)
#         next(rows)  # skip the title
#         loss_dict = {}
#         for row in list(rows):
#             loss_dict[int(row[0])] = float(row[1])
#         return loss_dict
#
#
# def read_loss_file_spectrum_mhb():
#     # file_path = Path('loss.csv')  # test use
#     file_path = Path('utils') / Path('harmonic_SPECTRUM_D_MHB.csv')
#     with open(file_path, 'r') as csvfile:
#         rows = csv.reader(csvfile)
#         next(rows)  # skip the title
#         loss_dict = {}
#         for row in list(rows):
#             loss_dict[int(row[0])] = float(row[1])
#         return loss_dict
#
#
# def read_loss_file_spectrum_uhb():
#     # file_path = Path('loss.csv')  # test use
#     file_path = Path('utils') / Path('harmonic_SPECTRUM_D_UHB.csv')
#     with open(file_path, 'r') as csvfile:
#         rows = csv.reader(csvfile)
#         next(rows)  # skip the title
#         loss_dict = {}
#         for row in list(rows):
#             loss_dict[int(row[0])] = float(row[1])
#         return loss_dict


def get_loss_cmw100(freq):
    loss_table_dict = read_loss_file_cmw100()
    want_loss = None
    for f in loss_table_dict:
        if freq >= f * 1000:
            want_loss = float(loss_table_dict[f])
        elif f * 1000 > freq:
            break
    return -want_loss


def get_loss_spectrum(freq):
    loss_table_dict = read_loss_file_spectrum()
    want_loss = None
    for f in loss_table_dict:
        if freq >= int(f) * 1000:
            want_loss = float(loss_table_dict[f])
        elif int(f) * 1000 > freq:
            break
    return -want_loss


# def get_loss_lb(freq):
#     loss_table_dict = read_loss_file_spectrum_lb()
#     want_loss = None
#     for f in loss_table_dict:
#         if freq >= int(f) * 1000:
#             want_loss = float(loss_table_dict[f])
#         elif int(f) * 1000 > freq:
#             break
#     return want_loss
#
#
# def get_loss_mhb(freq):
#     loss_table_dict = read_loss_file_spectrum_mhb()
#     want_loss = None
#     for f in loss_table_dict:
#         if freq >= int(f) * 1000:
#             want_loss = float(loss_table_dict[f])
#         elif int(f) * 1000 > freq:
#             break
#     return want_loss
#
#
# def get_loss_uhb(freq):
#     loss_table_dict = read_loss_file_spectrum_uhb()
#     want_loss = None
#     for f in loss_table_dict:
#         if freq >= int(f) * 1000:
#             want_loss = float(loss_table_dict[f])
#         elif int(f) * 1000 > freq:
#             break
#     return want_loss


def main():
    file = read_loss_file()
    file = sorted(file.keys())
    print(file)
    # for f in file:
    #     print(f, file[f], (type(f), type(file[f])))


if __name__ == '__main__':
    main()
