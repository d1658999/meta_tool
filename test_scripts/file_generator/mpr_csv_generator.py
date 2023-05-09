import csv
from pathlib import Path
from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
from utils.adb_handler import get_serial_devices

FOLDER_PATH = Path('output') / Path(get_serial_devices())
FILE_MPR_LTE = Path(FOLDER_PATH) / Path('mpr_lte.csv')
FILE_MPR_LTE_CA = Path(FOLDER_PATH) / Path('mpr_lte_ca.csv')
FILE_MPR_FR1_PC3 = Path(FOLDER_PATH) / Path('mpr_fr1_pc3.csv')
FILE_MPR_FR1_PC2 = Path(FOLDER_PATH) / Path('mpr_fr1_pc2.csv')
FILE_MPR_FR1_PC1p5 = Path(FOLDER_PATH) / Path('mpr_fr1_pc1p5.csv')


def check_csv_file_exists(file_path, want_type):
    """
    want_type:
        'mpr_fr1_pc3'
        'mpr_fr1_pc2'
        'mpr_fr1_pc1p5'
        'mpr_lte'
        'mpr_lte_ca'
    """

    if Path(file_path).exists():
        pass
    else:
        header_gen(want_type)


def header_gen(want_type):
    """
    want_type:
        'mpr_fr1_pc3'
        'mpr_fr1_pc2'
        'mpr_fr1_pc1p5'
        'mpr_lte'
        'mpr_lte_ca'
    """

    header_fr1 = [
        'Band', 'Tx_Path', 'ENABLE/DISABLE', 'BPSK_edge_dfts', 'BPSK_inner_dfts', 'BPSK_outer_dfts',
        'QPSK_edge_dfts', 'QPSK_inner_dfts', 'QPSK_outer_dfts',
        'Q16_edge_dfts', 'Q16_inner_dfts', 'Q16_outer_dfts',
        'Q64_edge_dfts', 'Q64_inner_dfts', 'Q64_outer_dfts',
        'Q256_edge_dfts', 'Q256_inner_dfts', 'Q256_outer_dfts',
        'reserved', 'reserved', 'reserved', 'reserved', 'reserved', 'reserved', 'reserved', 'reserved', 'reserved',
        'QPSK_edge_cp', 'QPSK_inner_cp', 'QPSK_outer_cp',
        'Q16_edge_cp', 'Q16_inner_cp', 'Q16_outer_cp',
        'Q64_edge_cp', 'Q64_inner_cp', 'Q64_outer_cp',
        'Q256_edge_cp', 'Q256_inner_cp', 'Q256_outer_cp',
        'reserved', 'reserved', 'reserved', 'reserved', 'reserved', 'reserved', 'reserved', 'reserved',
        'reserved', 'reserved', 'reserved', 'reserved', 'reserved',

    ]

    header_lte = [
        'Band', 'Tx_Path', 'ENABLE/DISABLE', 'QPSK_PRB', 'QPSK_FRB', 'Q16_PRB', 'Q16_FRB', 'Q64_PRB',
        'Q64_FRB', 'Q256_PRB', 'Q256_FRB', '1.4MHz_offset', '3MHz_offset', '5MHz_offset', '10MHz_offset',
        '15MHz_offset', '20MHz_offset',
    ]

    header_lte_ca = [
        'Band', 'Tx_Path', 'ENABLE/DISABLE', 'QPSK_le_8', 'QPSK_le_12', 'QPSK_le_16', 'QPSK_le_18',
        'QPSK_g_8_le_25', 'QPSK_g_12_le_50', 'QPSK_g_16_le_75', 'QPSK_g_18_le_100',
        'QPSK_g_25', 'QPSK_g_50', 'QPSK_g_75', 'QPSK_g_100',
        'Q16_le_8', 'Q16_le_12', 'Q16_le_16', 'Q16_le_18',
        'Q16_g_8_le_25', 'Q16_g_12_le_50', 'Q16_g_16_le_75', 'Q16_g_18_le_100',
        'Q16_g_25', 'Q16_g_50', 'Q16_g_75', 'Q16_g_100',
        'Q64_le_8_A', 'Q64_le_12_A', 'Q64_le_16_A', 'Q64_le_18_A',
        'Q64_g_8_B', 'Q64_g_12_B', 'Q64_g_16_B', 'Q64_g_18_B',
        'Q256_ge_1', 'Q256_ge_1', 'Q256_ge_1', 'Q256_ge_1',
        'QPSK_1RB_1RB', 'Q16_1RB_1RB', 'Q64_1RB_1RB', 'Q256_1RB_1RB',
        'reserved', 'reserved', 'reserved', 'reserved', 'reserved', 'reserved', 'reserved', 'reserved', 'reserved',
    ]

    if 'mpr_fr1' in want_type:
        file_path = Path(FOLDER_PATH) / Path(f'{want_type}.csv')
        with open(file_path, 'w', newline='') as csvfile:
            # Write the header row
            writer = csv.writer(csvfile)
            writer.writerow(header_fr1)

    elif want_type == 'mpr_lte':
        with open(FILE_MPR_LTE, 'w', newline='') as csvfile:
            # Write the header row
            writer = csv.writer(csvfile)
            writer.writerow(header_lte)

    elif want_type == 'mpr_lte_ca':
        with open(FILE_MPR_LTE_CA, 'w', newline='') as csvfile:
            # Write the header row
            writer = csv.writer(csvfile)
            writer.writerow(header_lte_ca)


def csv_file_lte(output_object, band):
    check_csv_file_exists(FILE_MPR_LTE, 'mpr_lte')
    with open(FILE_MPR_LTE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Iterate over the dictionary
        for key, value in output_object.items():
            # Write the key and value to the csv file
            if 'TX0' in key and 'LTE' in key:
                writer.writerow([band, 'TX1', *value.values()])
            elif 'TX1' in key and 'LTE' in key:
                writer.writerow([band, 'TX2', *value.values()])


def csv_file_lte_ca(output_object, band):
    check_csv_file_exists(FILE_MPR_LTE_CA, 'mpr_lte_ca')
    with open(FILE_MPR_LTE_CA, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Iterate over the dictionary
        for key, value in output_object.items():
            if 'INTRA_CA' in key:
                # Write the key and value to the csv file
                writer.writerow([band, 'TX1', *value.values()])


def csv_file_fr1_pc3(output_object, band):
    check_csv_file_exists(FILE_MPR_FR1_PC3, 'mpr_fr1_pc3')
    with open(FILE_MPR_FR1_PC3, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Iterate over the dictionary
        for key, value in output_object.items():
            # Write the key and value to the csv file
            if 'TX0' in key and 'NR_SUB6' in key:
                writer.writerow([band, 'TX1', *value.values()])
            elif 'TX1' in key and 'NR_SUB6' in key:
                writer.writerow([band, 'TX2', *value.values()])


def csv_file_fr1_pc2(output_object, band):
    check_csv_file_exists(FILE_MPR_FR1_PC2, 'mpr_fr1_pc2')
    with open(FILE_MPR_FR1_PC2, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Iterate over the dictionary
        for key, value in output_object.items():
            # Write the key and value to the csv file
            if 'TX0' in key and 'NR_SUB6' in key:
                writer.writerow([band, 'TX1', *value.values()])
            elif 'TX1' in key and 'NR_SUB6' in key:
                writer.writerow([band, 'TX2', *value.values()])


def csv_file_fr1_pc1p5(output_object, band):
    check_csv_file_exists(FILE_MPR_FR1_PC1p5, 'mpr_fr1_pc1p5')
    with open(FILE_MPR_FR1_PC1p5, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Iterate over the dictionary
        for key, value in output_object.items():
            # Write the key and value to the csv file
            if 'TX0' in key and 'NR_SUB6' in key:
                writer.writerow([band, 'TX1', *value.values()])
            elif 'TX1' in key and 'NR_SUB6' in key:
                writer.writerow([band, 'TX2', *value.values()])


def csv_file_generator(mpr_nv, band, tx_path_list=None):
    if tx_path_list is None:
        tx_path_list = ['TX1']

    command = AtCmd()

    if mpr_nv == '!LTERF.TX.USER DSP MPR OFFSET TX':
        for tx_path in tx_path_list:
            test_output = command.get_mpr_value('!LTERF.TX.USER DSP MPR OFFSET TX', band, tx_path)
            csv_file_lte(test_output, band)

    elif mpr_nv == '!LTERF.TX.USER DSP MPR INTRA_CA OFFSET TX':
        test_output = command.get_mpr_value('!LTERF.TX.USER DSP MPR INTRA_CA OFFSET TX', band, 'TX1')
        csv_file_lte_ca(test_output, band)

    elif mpr_nv == '!NR_SUB6RF.TX.USER MPR OFFSET TX':
        for tx_path in tx_path_list:
            test_output = command.get_mpr_value('!LTERF.TX.USER DSP MPR INTRA_CA OFFSET TX', band, tx_path)
            csv_file_fr1_pc3(test_output, band)

    elif mpr_nv == '!NR_SUB6RF.TX.USER MPR OFFSET PC2 TX':
        for tx_path in tx_path_list:
            test_output = command.get_mpr_value('!NR_SUB6RF.TX.USER MPR OFFSET PC2 TX', band, tx_path)
            csv_file_fr1_pc2(test_output, band)

    elif mpr_nv == '!NR_SUB6RF.TX.USER MPR OFFSET PC1p5 TX':
        for tx_path in tx_path_list:
            test_output = command.get_mpr_value('!NR_SUB6RF.TX.USER MPR OFFSET PC1p5 TX', band, tx_path)
            csv_file_fr1_pc1p5(test_output, band)

    elif mpr_nv == 'ALL':
        test_output = command.get_mpr_value_all(band)

        csv_file_lte(test_output, band)

        csv_file_lte_ca(test_output, band)

        csv_file_fr1_pc3(test_output, band)

        csv_file_fr1_pc2(test_output, band)

        csv_file_fr1_pc1p5(test_output, band)


def main():
    csv_file_generator('ALL', 41)


if __name__ == '__main__':
    main()
