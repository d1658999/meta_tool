import yaml
import csv
from pathlib import Path
from utils.log_init import log_set
import math

logger = log_set('spec_limits')

TDD_BAND = [42, 48, 38, 39, 40, 41, 75, 77, 78, 79]
CSV_PWR_FILE_FR1 = 'power_limits_fr1.csv'
CSV_PWR_FILE_LTE = 'power_limits_lte.csv'
CSV_PWR_FILE_WCDMA = 'power_limits_wcdma.csv'
CSV_PWR_FILE_GSM = 'power_limits_gsm.csv'
PWR_LIMITS_YAML_NAME = 'power_limits.yaml'
ACLR_LIMITS_YAML_NAME = 'aclr_color_code.yaml'
EVM_LIMITS_YAML_NAME = 'evm_color_code.yaml'

CSV_PWR_PATH_FR1 = Path('spec_limits') / Path(CSV_PWR_FILE_FR1)
CSV_PWR_PATH_LTE = Path('spec_limits') / Path(CSV_PWR_FILE_LTE)
CSV_PWR_PATH_WCDMA = Path('spec_limits') / Path(CSV_PWR_FILE_WCDMA)
CSV_PWR_PATH_GSM = Path('spec_limits') / Path(CSV_PWR_FILE_GSM)
PWR_LIMITS_YAML_PATH = Path('spec_limits') / PWR_LIMITS_YAML_NAME
ACLR_LIMITS_YAML_PATH = Path('spec_limits') / ACLR_LIMITS_YAML_NAME
EVM_LIMITS_YAML_PATH = Path('spec_limits') / EVM_LIMITS_YAML_NAME
SENS_FDD_FR1_PATH = Path('spec_limits') / 'Sens_fdd_fr1.csv'
SENS_LTE_PATH = Path('spec_limits') / 'Sens_lte.csv'
SENS_FDD_FR1_YAML = Path('spec_limits') / 'Sens_fdd_fr1.yaml'
SENS_TDD_FR1_YAML = Path('spec_limits') / 'Sens_tdd_fr1.yaml'
SENS_LTE_YAML = Path('spec_limits') / 'Sens_lte.yaml'

TECHs = ['FR1', 'LTE', 'WCDMA', 'GSM']

TDD_NRB = {
    15:
        {
            5: 25,
            10: 52,
            15: 79,
            20: 106,
            25: 133,
            30: 160,
            35: 188,
            40: 216,
            45: 242,
            50: 270,
        },
    30:
        {
            5: 11,
            10: 24,
            15: 38,
            20: 51,
            25: 65,
            30: 78,
            35: 92,
            40: 106,
            45: 119,
            50: 133,
            60: 162,
            70: 189,
            80: 217,
            90: 245,
            100: 273,
        },
    60:
        {
            10: 11,
            15: 18,
            20: 24,
            25: 31,
            30: 38,
            35: 44,
            40: 51,
            45: 58,
            50: 65,
            60: 79,
            70: 93,
            80: 107,
            90: 121,
            100: 135,
        },
}

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
    with open(EVM_LIMITS_YAML_PATH, 'r') as s:
        spec_evm_limits = yaml.safe_load(s)
        return spec_evm_limits


def csv_to_yaml_fr1(csv_file_path, yaml_file_path, has_header=True):  # generate fdd sensitivity criteria
    """
    Converts a CSV file to a YAML file:
    - First column becomes the first tier.
    - Second column becomes the second tier.
    - Remaining columns are handled using zip().
    """

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        data = list(csv_reader)

        if has_header:
            header = data[0]
            data = data[1:]
            yaml_dict = {}
            for row in data:
                if row[0] not in yaml_dict:  # new create
                    new_dict = {
                        row[0]: {  # First column as the first tier key
                            row[1]: dict(zip(header[2:], row[2:]))  # Second tier, zip remaining columns
                        }
                    }
                    yaml_dict.update(new_dict)

                else:
                    yaml_dict[row[0]][row[1]] = dict(zip(header[2:], row[2:]))

    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(yaml_dict, yaml_file, default_flow_style=False)


def csv_to_yaml_lte(csv_file_path, yaml_file_path, has_header=True):  # generate fdd sensitivity criteria
    """
    Converts a CSV file to a YAML file:
    - First column becomes the first tier.
    - Second column becomes the second tier.
    - Remaining columns are handled using zip().
    """

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        data = list(csv_reader)

        if has_header:
            header = data[0]
            data = data[1:]
            yaml_dict = {}
            for row in data:
                if row[0] not in yaml_dict:  # new create
                    new_dict = {
                        row[0]: dict(zip(header[2:], row[2:]))  # Second tier, zip remaining columns
                    }
                    yaml_dict.update(new_dict)

                else:
                    yaml_dict[row[0]] = dict(zip(header[2:], row[2:]))

    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(yaml_dict, yaml_file, default_flow_style=False)



def sensitivity_criteria_fr1(band, scs, bw):
    if band in TDD_BAND:
        with open(SENS_TDD_FR1_YAML, 'r') as s:
            sens = yaml.safe_load(s)

        formula = sens[str(band)][str(scs)].replace('N', str(TDD_NRB[scs][bw]))

        return eval(formula)

    else:
        with open(SENS_FDD_FR1_YAML, 'r') as s:
            sens = yaml.safe_load(s)

        return float(sens[str(band)][str(scs)][f'BW{bw}'])


def sensitivity_criteria_lte(band, bw):
    with open(SENS_LTE_YAML, 'r') as s:
        sens = yaml.safe_load(s)

    return float(sens[str(band)][f'BW{bw}'])


def main():  # test use
    power_limits_csv2yaml()
    # power_limits_csv2yaml('LTE')


if __name__ == '__main__':
    # main()
    # print(sensitivity_criteria_ftm(77, 30, 100))
    # csv_to_yaml(SENS_FDD_FR1_PATH, SENS_FDD_FR1_YAML)  # tranfer csv to yaml for fdd sens
    # csv_to_yaml_lte(SENS_LTE_PATH, SENS_LTE_YAML)
    pass