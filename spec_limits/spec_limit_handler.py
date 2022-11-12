import yaml
import csv

CSV_PATH_FR1 = 'power_limits_fr1.csv'
CSV_PATH_LTE = 'power_limits_lte.csv'
CSV_PATH_WCDMA = 'power_limits_wcdma.csv'
CSV_PATH_GSM = 'power_limits_gsm.csv'
PWR_LIMITS_YAML_PATH = 'power_limits.yaml'
TECHs = ['FR1', 'LTE', 'WCDMA', 'GSM']

def power_limits_csv2yaml():
    """
    tech -> modultation -> band -> rb_state
    """
    with open(PWR_LIMITS_YAML_PATH, 'w', encoding='utf-8') as outfile:
        contents = {}
        for tech in TECHs:  # FR1, LTE, WCDMA, GSM
            if tech == 'FR1':
                with open(CSV_PATH_FR1, 'r') as csvfile:
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
                with open(CSV_PATH_LTE, 'r') as csvfile:
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
                with open(CSV_PATH_WCDMA, 'r') as csvfile:
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
                with open(CSV_PATH_GSM, 'r') as csvfile:
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
    with open(PWR_LIMITS_YAML_PATH, 'r') as s:
        spec_power_limits = yaml.safe_load(s)
        return spec_power_limits


def main():  # test use
    power_limits_csv2yaml()
    # power_limits_csv2yaml('LTE')


if __name__ == '__main__':
    main()
