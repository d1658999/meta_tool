import csv
from pathlib import Path


def read_mipi_setting():
    # file_path = Path('mipi_setting.csv')  # test use
    # file_path = Path.cwd().parents[1] / Path('utils') / Path('loss.csv')  # test use
    file_path = Path('utils') / Path('mipi_setting.csv')
    with open(file_path, 'r') as csvfile:
        rows = csv.reader(csvfile)
        next(rows)  # skip the title
        mipi_setting_dict = {}
        for row in list(rows):
            mipi_setting_dict[row[0]] = row[1]
        return mipi_setting_dict


def main():
    mipi = read_mipi_setting()
    print(mipi)
    print(mipi['TX1_FR1_77'].split(':'))


if __name__ == '__main__':
    main()
