import csv
from pathlib import Path
import utils.parameters.external_paramters as ext_pmt


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


def mipi_settings_dict(tx_path, tech, band):
    try:
        if ext_pmt.mipi_read_en:
            mipi_dicts = read_mipi_setting()
            return mipi_dicts[f'{tx_path}_{tech}_{band}']
    except Exception as e:
        logger.info(f'There is not mipi setting for {e}, please check the mipi setting')
        return None


def main():
    mipi = read_mipi_setting()
    print(mipi)
    print(mipi['TX1_FR1_77'].split(':'))


if __name__ == '__main__':
    main()
