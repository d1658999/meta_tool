import csv
from pathlib import Path

fdc_loss_port = {
    1: 'fdc_loss_1.csv',
    2: 'fdc_loss_2.csv',
    3: 'fdc_loss_3.csv',
    4: 'fdc_loss_4.csv',
    5: 'fdc_loss_5.csv',
    6: 'fdc_loss_6.csv',
    7: 'fdc_loss_7.csv',
    8: 'fdc_loss_8.csv',
}


def read_loss_file():
    # file_path = Path('loss.csv')  # test use
    # file_path = Path.cwd().parents[1] / Path('utils') / Path('loss.csv')  # test use
    file_path = Path('utils') / Path('loss.csv')
    with open(file_path, 'r') as csvfile:
        rows = csv.reader(csvfile)
        next(rows)  # skip the title
        loss_dict = {}
        for row in list(rows):
            loss_dict[int(row[0])] = float(row[1])
        return loss_dict


def read_fdc_file(port):
    file_path = Path('utils') / Path('fdcorrection_loss') / Path(fdc_loss_port[port])
    with open(file_path, 'r') as csvfile:
        rows = csv.reader(csvfile)
        next(rows)  # skip the title
        loss_list = []
        for row in list(rows):
            loss_list.append(row[0] * 10 ** 6)
            loss_list.append(float(row[1]))
        return loss_list


def get_loss(freq):
    loss_table_dict = read_loss_file()
    want_loss = None
    for f in loss_table_dict:
        if freq >= int(f) * 1000:
            want_loss = float(loss_table_dict[f])
        elif int(f) * 1000 > freq:
            break
    return want_loss


def main():
    file = read_loss_file()
    file = sorted(file.keys())
    print(file)
    # for f in file:
    #     print(f, file[f], (type(f), type(file[f])))


if __name__ == '__main__':
    main()
