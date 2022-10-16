import csv
from pathlib import Path


def read_loss_file():
    file_path = Path('utils') / Path('loss.csv')
    with open(file_path, 'r') as csvfile:
        rows = csv.reader(csvfile)
        next(rows)  # skip the title
        loss_list = []
        for row in list(rows):
            loss_list.append((int(row[0]), float(row[1])))
        return loss_list


def get_loss(freq):
    loss_table = read_loss_file()
    want_loss = None
    for lt in loss_table:
        if freq > lt[0] * 1000:
            want_loss = lt[1]
        elif lt[0] * 1000 > freq:
            break
    return want_loss


def main():
    pass


if __name__ == '__main__':
    main()
