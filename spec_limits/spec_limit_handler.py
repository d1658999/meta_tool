import yaml
import csv
from pathlib import Path
from utils.log_init import log_set

logger = log_set('spec_limits')


CSV_PWR_FILE_FR1 = 'power_limits_fr1.csv'
CSV_PWR_FILE_LTE = 'power_limits_lte.csv'
CSV_PWR_FILE_WCDMA = 'power_limits_wcdma.csv'
CSV_PWR_FILE_GSM = 'power_limits_gsm.csv'
PWR_LIMITS_YAML_NAME = 'power_limits.yaml'
ACLR_LIMITS_YAML_NAME = 'aclr_color_code.yaml'
EVM_LIMITS_YAML_NAME = 'evm_limits.yaml'

CSV_PWR_PATH_FR1 = Path('spec_limits') / Path(CSV_PWR_FILE_FR1)
CSV_PWR_PATH_LTE = Path('spec_limits') / Path(CSV_PWR_FILE_LTE)
CSV_PWR_PATH_WCDMA = Path('spec_limits') / Path(CSV_PWR_FILE_WCDMA)
CSV_PWR_PATH_GSM = Path('spec_limits') / Path(CSV_PWR_FILE_GSM)
PWR_LIMITS_YAML_PATH = Path('spec_limits') / PWR_LIMITS_YAML_NAME
ACLR_LIMITS_YAML_PATH = Path('spec_limits') / ACLR_LIMITS_YAML_NAME
EVM_LIMITS_YAML_PATH = Path('spec_limits') / PWR_LIMITS_YAML_NAME

TECHs = ['FR1', 'LTE', 'WCDMA', 'GSM']

def power_limits_csv2yaml():
    """
    tech -> modultation -> band -> rb_state
    """
    logger.info('tranfer spec_limits csv file to yaml')
    with open(PWR_LIMITS_YAML_PATH, 'w', encoding='utf-8') as outfile:
        contents = {}
        for tech in TECHs:  # FR1, LTE, WCDMA, GSM
            if tech == 'FR1':
                with open(CSV_PWR_PATH_FR1, 'r') as csvfile:
                    rows = csv.reader(csvfile)
                    next(rows)  # skip the title
                    for row in list(rows):
                        contents.setdefault(row[0], {})
                        contents[row[0]].setdefault(row[10], {})
                        contents[row[0]][row[10]].setdefault(int(row[1]), dict())
                        contents[row[0]][row[10]][int(row[1])] = {
                            'INNER_FULL': float(row[2]),
                            'OUTER_FULL': float(row[3]),
                            'INNER_1RB_LEFT': float(row[4]),
                            'INNER_1RB_RIGHT': float(row[5]),
                            'EDGE_1RB_LEFT': float(row[6]),
                            'EDGE_1RB_RIGHT': float(row[7]),
                            'EDGE_FULL_LEFT': float(row[8]),
                            'EDGE_FULL_RIGHT': float(row[9]),
                        }

            elif tech == 'LTE':
                with open(CSV_PWR_PATH_LTE, 'r') as csvfile:
                    rows = csv.reader(csvfile)
                    next(rows)  # skip the title
                    for row in list(rows):
                        contents.setdefault(row[0], {})
                        contents[row[0]].setdefault(row[4], {})
                        contents[row[0]][row[4]].setdefault(int(row[1]), dict())
                        contents[row[0]][row[4]][int(row[1])] = {
                            'PRB': float(row[2]),
                            'FRB': float(row[3]),
                        }

            elif tech == 'WCDMA':
                with open(CSV_PWR_PATH_WCDMA, 'r') as csvfile:
                    rows = csv.reader(csvfile)
                    next(rows)  # skip the title
                    for row in list(rows):
                        contents.setdefault(row[0], {})
                        contents[row[0]].setdefault(row[3], {})
                        contents[row[0]][row[3]].setdefault(int(row[1]), dict())
                        contents[row[0]][row[3]][int(row[1])] = {
                            'Genre': float(row[2]),
                        }

            elif tech == 'GSM':
                with open(CSV_PWR_PATH_GSM, 'r') as csvfile:
                    rows = csv.reader(csvfile)
                    next(rows)  # skip the title
                    for row in list(rows):
                        contents.setdefault(row[0], {})
                        contents[row[0]].setdefault(row[3], {})
                        contents[row[0]][row[3]].setdefault(int(row[1]), dict())
                        contents[row[0]][row[3]][int(row[1])] = {
                            'Genre': float(row[2]),
                        }
        yaml.dump(contents, outfile, default_flow_style=False, encoding='utf-8', allow_unicode=True)


def import_power_limits():
    logger.info('import power yaml file ')
    with open(PWR_LIMITS_YAML_PATH, 'r') as s:
        spec_power_limits = yaml.safe_load(s)
        return spec_power_limits


def import_aclr_limits():
    logger.info('import aclr yaml file ')
    with open(ACLR_LIMITS_YAML_PATH, 'r') as s:
        spec_aclr_limits = yaml.safe_load(s)
        return spec_aclr_limits


def import_evm_limits():
    logger.info('import evm yaml file ')
    with open(PWR_LIMITS_YAML_PATH, 'r') as s:
        spec_evm_limits = yaml.safe_load(s)
        return spec_evm_limits


def main():  # test use
    power_limits_csv2yaml()
    # power_limits_csv2yaml('LTE')


if __name__ == '__main__':
    main()
