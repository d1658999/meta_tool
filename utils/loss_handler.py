import csv
from pathlib import Path

loss_port = {
    1: 'loss_1.csv',
    2: 'loss_2.csv',
    3: 'loss_3.csv',
    4: 'loss_4.csv',
    5: 'loss_5.csv',
    6: 'loss_6.csv',
    7: 'loss_7.csv',
    8: 'loss_8.csv',
}


def read_loss_file(port):
    # file_path = Path('loss.csv')  # test use
    # file_path = Path.cwd().parents[1] / Path('utils') / Path('loss.csv')  # test use
    file_path = Path('utils') / Path(loss_port[port])
    with open(file_path, 'r') as csvfile:
        rows = csv.reader(csvfile)
        next(rows)  # skip the title
        loss_dict = {}
        for row in list(rows):
            loss_dict[int(row[0])] = float(row[1])
        return loss_dict


def get_loss(freq, port, port_table_en=False):
    if port_table_en:
        pass
    else:
        port = 1

    loss_table_dict = read_loss_file(port)
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
