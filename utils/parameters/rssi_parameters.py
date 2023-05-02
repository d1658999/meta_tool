RAT = {
    'GSM': 0,
    'WCDMA': 1,
    'LTE': 2,
    'LTE_Diff': 3,
    'NR': 6,
}

BANDS_GSM = {
    '380': 1,
    '410': 2,
    '450': 3,
    '480': 4,
    '710': 5,
    '750': 6,
    '810': 7,
    '850': 8,
    '900': 10,
    '1800': 12,
    '1900': 13,
}

RX_BW = {
    'GSM': {
        '0.2': 0,
    },
    'WCDMA': {
        '3.84': 0,
    },
    'LTE': {
        '0.1': 1,
        '1.4': 2,
        '5': 3,
        '10': 4,
        '15': 5,
        '20': 6,
    },
    'NR': {
        '0.1': 1,
        '1.4': 2,
        '5': 3,
        '10': 4,
        '15': 5,
        '20': 6,
        '25': 7,
        '30': 8,
        '40': 9,
        '50': 10,
        '60': 11,
        '70': 15,
        '80': 12,
        '90': 13,
        '100': 14,
        '502': 16,
        '1002': 17,
        '2002': 18,
    }
}

TX_BW = {
    'GSM': {
        '0.2': 0,
    },
    'WCDMA': {
        '3.84': 0,
    },
    'LTE': {
        '0.1': 0,
        '1.4': 1,
        '5': 2,
        '10': 3,
        '15': 4,
        '20': 5,
    },
    'NR': {
        '5': 0,
        '10': 1,
        '15': 2,
        '20': 3,
        '25': 4,
        '30': 5,
        '40': 6,
        '50': 7,
        '60': 8,
        '70': 12,
        '80': 9,
        '90': 10,
        '100': 11,
        '502': 13,
        '1002': 14,
        '2002': 15,
    }
}

SCAN_MODE = {
    'FULL': 0,
    'PART': 1,
}

STEP_FREQ = {
    'GSM': {
        '0.2': 1,
        '0.4': 2,
        '0.6': 3,
        '0.8': 4,
        '1.0': 5,
        '1.2': 6,
        '1.4': 7,
        '1.6': 8,
        '1.8': 9,
        '2.0': 10,
        '2.2': 11,
        '2.4': 12,
        '2.6': 13,
        '2.8': 14,
        '3.0': 15,
        '3.2': 16,
    },
    'WCDMA': {
        '0.2': 1,
        '0.4': 2,
        '0.6': 3,
        '0.8': 4,
        '1.0': 5,
        '1.2': 6,
        '1.4': 7,
        '1.6': 8,
        '1.8': 9,
        '2.0': 10,
        '2.2': 11,
        '2.4': 12,
        '2.6': 13,
        '2.8': 14,
        '3.0': 15,
        '3.2': 16,

    },
    'LTE': {
        '0.015': 1,
        '0.1': 2,
        '0.2': 3,
        '0.3': 4,
        '0.4': 5,
        '0.5': 6,
        '0.6': 7,
        '0.7': 8,
        '0.8': 9,
        '0.9': 10,
        '1.0': 11,
        '1.1': 12,
        '1.2': 13,
        '1.3': 14,
        '1.4': 15,
        '1.5': 16,
        '1.6': 17,
    },

    'NR': {
        '0.015': 1,
        '0.1': 2,
        '0.2': 3,
        '0.3': 4,
        '0.4': 5,
        '0.5': 6,
        '0.6': 7,
        '0.7': 8,
        '0.8': 9,
        '0.9': 10,
        '1.0': 11,
        '1.1': 12,
        '1.2': 13,
        '1.3': 14,
        '1.4': 15,
        '1.5': 16,
        '1.6': 17,
    },
}

ANTENNA_SELECTION = {
    'RX0+RX1_avg': 0,
    'RX0_avg': 1,
    'RX1_avg': 2,
    'RX0+RX1_max_avg': 3,
    'RX0_max_avg': 4,
    'RX1_max_avg': 5,
    '4RX_avg': 6,
    'RX0+RX1_samples': 10,
    'RX0_samples': 11,
    'RX1_samples': 12,
    '4RX_samples': 16,
    'RX0+RX1_TX_avg_tx': 20,
    'RX0_TX_avg_tx': 21,
    'RX1_TX_avg_tx': 22,
    'RX0+RX1_TX_max_avg_tx': 23,
    'RX0_TX_max_avg_tx': 24,
    'RX1_TX_max_avg_tx': 25,
    '4RX_TX_avg_tx': 26,
}

TX1_ENABLE = {
    'OFF': 0,
    'ON_DFTS': 1,
    'ON_CP': 2,
}

TX2_ENABLE = {
    'OFF': 0,
    'ON_LTE_CA': 1,
    'ON_DFTS': 2,
    'ON_CP_LTE': 3,
}

MCS = {
    'SCS15_BPSK': 0,
    'SCS15_QPSK': 1,
    'SCS15_Q16': 2,
    'SCS15_Q64': 3,
    'SCS15_Q256': 4,
    'SCS15_Q1024': 5,
    'SCS30_BPSK': 10,
    'SCS30_QPSK': 11,
    'SCS30_Q16': 12,
    'SCS30_Q64': 13,
    'SCS30_Q256': 14,
    'SCS30_Q1024': 15,
    'SCS60_BPSK': 20,
    'SCS60_QPSK': 21,
    'SCS60_Q16': 22,
    'SCS60_Q64': 23,
    'SCS60_Q256': 24,
    'SCS60_Q1024': 25,
    'SCS120_BPSK': 30,
    'SCS120_QPSK': 31,
    'SCS120_Q16': 32,
    'SCS120_Q64': 33,
    'SCS120_Q256': 34,
    'SCS120_Q1024': 35,

}

Start_Rx_Freq = 1960000  # KHz
Stop_Rx_Freq = 1960000  # KHz
TX1_Band = 2
TX1_Freq = 1880000  # KHz
TX1_PWR = 200  # x10
TX1_rb_num = 50
TX1_rb_start = 0
TX2_Band = 2
TX2_Freq = 1880000  # KHz
TX2_PWR = 200  # x10
TX2_rb_num = 50
TX2_rb_start = 0

Sampling_Count = 20


def rx_bands_collection(tech, band):
    if tech == 'GSM':
        return BANDS_GSM
    else:
        return band


def main():
    command_line = f'AT+RSSISCAN=' \
                   f'{RAT["LTE"]},' \
                   f'{rx_bands_collection("LTE", 2)}' \
                   f'{RX_BW["LTE"][10]},' \
                   f'{SCAN_MODE["PART"]},' \
                   f'{Start_Rx_Freq},' \
                   f'{Stop_Rx_Freq},' \
                   f'{STEP_FREQ["LTE"][0.015]},' \
                   f'{ANTENNA_SELECTION["4RX_avg"]},' \
                   f'{Sampling_Count},' \
                   f'0,' \
                   f'{TX1_ENABLE["ON_DFTS"]},' \
                   f'{TX1_Band},' \
                   f'{TX_BW["LTE"][10]},' \
                   f'{TX1_Freq},' \
                   f'{TX1_PWR},' \
                   f'{TX1_rb_num},' \
                   f'{TX1_rb_start},' \
                   f'{MCS["SCS15_QPSK"]},' \
                   f'{TX2_ENABLE["ON_DFTS"]},' \
                   f'{TX2_Band},' \
                   f'{TX_BW["LTE"][10]},' \
                   f'{TX2_Freq},' \
                   f'{TX2_PWR},' \
                   f'{TX2_rb_num},' \
                   f'{TX2_rb_start},' \
                   f'{MCS["SCS15_QPSK"]},' \
                   f''
    print(command_line)


if __name__ == "__main__":
    main()
