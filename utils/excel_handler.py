import openpyxl
from openpyxl.chart import LineChart, Reference, BarChart, Series
from pathlib import Path

from utils.log_init import log_set
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
import utils.parameters.external_paramters as ext_pmt
from utils.channel_handler import chan_judge_fr1, chan_judge_lte, chan_judge_wcdma, chan_judge_gsm

logger = log_set('excel_hdl')


rx_path_gsm_dict = {
            2: 'RX0',
            1: 'RX1',
            4: 'RX2',
            8: 'RX3',
            3: 'RX0+RX1',
            12: 'RX2+RX3',
            15: 'ALL PATH',
        }
rx_path_wcdma_dict = {
    2: 'RX0',
    1: 'RX1',
    4: 'RX2',
    8: 'RX3',
    3: 'RX0+RX1',
    12: 'RX2+RX3',
    15: 'ALL PATH',
}
rx_path_lte_dict = {
    2: 'RX0',
    1: 'RX1',
    4: 'RX2',
    8: 'RX3',
    3: 'RX0+RX1',
    12: 'RX2+RX3',
    15: 'ALL PATH',
}
rx_path_fr1_dict = {
    2: 'RX0',
    1: 'RX1',
    4: 'RX2',
    8: 'RX3',
    3: 'RX0+RX1',
    12: 'RX2+RX3',
    15: 'ALL PATH',
}

def excel_folder_create():
    file_dir = excel_folder_path()
    file_dir.mkdir(parents=True, exist_ok=True)
    logger.info('----------folder create ----------')


def excel_folder_path():
    return Path('output') / Path(ext_pmt.devices_serial)


def endc_relative_power_senstivity_export_excel(data):
    """
    :param data:  data = [int(self.band_lte), int(self.band_fr1), self.power_monitor_endc_lte, self.power_endc_fr1, self.rx_level, self.bw_lte, self.bw_fr1, self.tx_freq_lte, self.tx_freq_fr1, self.tx_level_endc_lte, self.tx_level_endc_fr1, self.rb_size_lte, self.rb_start_lte, self.rb_size_fr1, self.rb_start_fr1]
    :return:
    """
    logger.info('----------save to excel----------')
    filename = f'Sensitivty_ENDC.xlsx'

    file_path = Path(excel_folder_path()) / Path(filename)

    if Path(file_path).exists() is False:
        logger.info('----------file does not exist, so create a new one----------')
        wb = openpyxl.Workbook()
        wb.remove(wb['Sheet'])

        # create the title and sheet for TxManx and -10dBm
        wb.create_sheet(f'Raw_Data_ENDC_FR1_TxMax')
        wb.create_sheet(f'Raw_Data_ENDC_FR1_-10dBm')
        for sheetname in wb.sheetnames:
            ws = wb[sheetname]
            ws['A1'] = 'Band_LTE'
            ws['B1'] = 'Band_FR1'
            ws['C1'] = 'Power_LTE_measured'
            ws['D1'] = 'Power_FR1_measured'
            ws['E1'] = 'Sensitivity_FR1'
            ws['F1'] = 'BW_LTE'
            ws['G1'] = 'BW_FR1'
            ws['H1'] = 'Freq_tx_LTE'
            ws['I1'] = 'Freq_tx_FR1'
            ws['J1'] = 'Tx_level_LTE'
            ws['K1'] = 'Tx_level_FR1'
            ws['L1'] = 'rb_size_LTE'
            ws['M1'] = 'rb_start_LTE'
            ws['N1'] = 'rb_size_FR1'
            ws['O1'] = 'rb_start_FR1'

        # create the title and sheet for Desense
        wb.create_sheet(f'Desens_ENDC')
        ws = wb[f'Desens_ENDC']
        ws['A1'] = 'Band_LTE'
        ws['B1'] = 'Band_FR1'
        ws['C1'] = 'BW_LTE'
        ws['D1'] = 'BW_FR1'
        ws['E1'] = 'Freq_tx_LTE'
        ws['F1'] = 'Freq_tx_FR1'
        ws['G1'] = 'Diff'

        # create dashboard
        wb.create_sheet(f'Dashboard')

        wb.save(file_path)
        wb.close()

    logger.info('----------file exist----------')
    wb = openpyxl.load_workbook(file_path)

    for d in data:
        sheetname = f'Raw_Data_ENDC_FR1_TxMax' if d[2] > 0 else f'Raw_Data_ENDC_FR1_-10dBm'
        ws = wb[sheetname]
        max_row = ws.max_row
        max_col = ws.max_column
        row = max_row + 1
        for col in range(max_col):
            ws.cell(row, col + 1).value = d[col]

    wb.save(file_path)
    wb.close()

    return file_path


def rx_power_relative_test_export_excel(data, parameters_dict):
    """
    data is dict like:
    rx_level: [ Power, Rx_level, [RSRP0-3], [CINR0-3], [AFC0-3]]
    """
    script = parameters_dict['script']
    tech = parameters_dict['tech']
    band = parameters_dict['band']
    bw = parameters_dict['bw']
    tx_level = parameters_dict['tx_level']
    mcs = parameters_dict['mcs']
    tx_path = parameters_dict['tx_path']
    rx_path = parameters_dict['rx_path']
    logger.info('----------save to excel----------')
    if script == 'GENERAL':
        filename = f'Sensitivty_{bw}MHZ_{tech}_LMH.xlsx'
        file_path = Path(excel_folder_path()) / Path(filename)

        if Path(file_path).exists() is False:  # if the file does not exist
            logger.info('----------file does not exist----------')
            wb = openpyxl.Workbook()
            wb.remove(wb['Sheet'])
            # to create sheet
            if tech == 'LTE':
                # create the title and sheet for TxManx and -10dBm
                wb.create_sheet(f'Raw_Data_{mcs}_TxMax')
                wb.create_sheet(f'Raw_Data_{mcs}_-10dBm')
                for sheetname in wb.sheetnames:
                    ws = wb[sheetname]
                    ws['A1'] = 'Band'
                    ws['B1'] = 'RX_Path'
                    ws['C1'] = 'Chan'
                    ws['D1'] = 'Tx_Freq'
                    ws['E1'] = 'Tx_level'
                    ws['F1'] = 'Power'
                    ws['G1'] = 'Rx_Level'
                    ws['H1'] = 'RSRP_RX0'
                    ws['I1'] = 'RSRP_RX1'
                    ws['J1'] = 'RSRP_RX2'
                    ws['K1'] = 'RSRP_RX3'
                    ws['L1'] = 'CINR_RX0'
                    ws['M1'] = 'CINR_RX1'
                    ws['N1'] = 'CINR_RX2'
                    ws['O1'] = 'CINR_RX3'
                    ws['P1'] = 'AGC_RX0'
                    ws['Q1'] = 'AGC_RX1'
                    ws['R1'] = 'AGC_RX2'
                    ws['S1'] = 'AGC_RX3'
                    ws['T1'] = 'TX_Path'

                # create the title and sheet for Desense
                wb.create_sheet(f'Desens_{mcs}')
                ws = wb[f'Desens_{mcs}']
                ws['A1'] = 'Band'
                ws['B1'] = 'Rx_Path'
                ws['C1'] = 'Chan'
                ws['D1'] = 'Diff'
                ws['E1'] = 'TX_Path'

            elif tech == 'FR1':
                # create the title and sheet for TxManx and -10dBm
                wb.create_sheet(f'Raw_Data_{mcs}_TxMax')
                wb.create_sheet(f'Raw_Data_{mcs}_-10dBm')
                for sheetname in wb.sheetnames:
                    ws = wb[sheetname]
                    ws['A1'] = 'Band'
                    ws['B1'] = 'RX_Path'
                    ws['C1'] = 'Chan'
                    ws['D1'] = 'Tx_Freq'
                    ws['E1'] = 'Tx_level'
                    ws['F1'] = 'Power'
                    ws['G1'] = 'Rx_Level'
                    ws['H1'] = 'RSRP_RX0'
                    ws['I1'] = 'RSRP_RX1'
                    ws['J1'] = 'RSRP_RX2'
                    ws['K1'] = 'RSRP_RX3'
                    ws['L1'] = 'CINR_RX0'
                    ws['M1'] = 'CINR_RX1'
                    ws['N1'] = 'CINR_RX2'
                    ws['O1'] = 'CINR_RX3'
                    ws['P1'] = 'AGC_RX0'
                    ws['Q1'] = 'AGC_RX1'
                    ws['R1'] = 'AGC_RX2'
                    ws['S1'] = 'AGC_RX3'
                    ws['T1'] = 'TX_Path'

                # create the title and sheet for Desense
                wb.create_sheet(f'Desens_{mcs}')
                ws = wb[f'Desens_{mcs}']
                ws['A1'] = 'Band'
                ws['B1'] = 'Rx_Path'
                ws['C1'] = 'Chan'
                ws['D1'] = 'Diff'
                ws['E1'] = 'TX_Path'

            elif tech == 'WCDMA':
                # create the title and sheet for TxManx and -10dBm
                wb.create_sheet(f'Raw_Data')
                for sheetname in wb.sheetnames:
                    ws = wb[sheetname]
                    ws['A1'] = 'Band'
                    ws['B1'] = 'RX_Path'
                    ws['C1'] = 'Chan'
                    ws['D1'] = 'Channel'
                    ws['E1'] = 'Tx_Freq'
                    ws['F1'] = 'Rx_Level'

                # create the title and sheet for Desense
                wb.create_sheet(f'Desens_{mcs}')
                ws = wb[f'Desens_{mcs}']
                ws['A1'] = 'Band'
                ws['B1'] = 'Rx_Path'
                ws['C1'] = 'Chan'
                ws['D1'] = 'Diff'

            elif tech == 'GSM':
                wb.create_sheet(f'Raw_Data')
                for sheetname in wb.sheetnames:
                    # create the title and sheet for TxManx and -10dBm
                    ws = wb[sheetname]
                    ws['A1'] = 'Band'
                    ws['B1'] = 'RX_Path'
                    ws['C1'] = 'Chan'
                    ws['D1'] = 'Channel'
                    ws['E1'] = 'Rx_Freq'
                    ws['F1'] = 'Rx_Level'
                    ws['G1'] = 'RSSI'

            # create dashboard
            wb.create_sheet(f'Dashboard')

            # save and close file
            wb.save(file_path)
            wb.close()

        # if the file exist
        logger.info('----------file exist----------')
        wb = openpyxl.load_workbook(file_path)
        ws = None
        # to fetch the sheet name
        if tech == 'LTE':
            sheetname = f'Raw_Data_{mcs}_TxMax' if tx_level > 0 else f'Raw_Data_{mcs}_-10dBm'
            ws = wb[sheetname]
        elif tech == 'FR1':
            sheetname = f'Raw_Data_{mcs}_TxMax' if tx_level > 0 else f'Raw_Data_{mcs}_-10dBm'
            ws = wb[sheetname]
        elif tech == 'WCDMA':
            sheetname = 'Raw_Data'
            ws = wb[sheetname]
        elif tech == 'GSM':
            sheetname = 'Raw_Data'
            ws = wb[sheetname]

        if tech == 'LTE':
            max_row = ws.max_row
            row = max_row + 1  # skip title
            for tx_freq, measured_data in data.items():
                chan = chan_judge_lte(band, bw, tx_freq)
                ws.cell(row, 1).value = band
                ws.cell(row, 2).value = rx_path_lte_dict[rx_path]
                ws.cell(row, 3).value = chan  # LMH
                ws.cell(row, 4).value = tx_freq
                ws.cell(row, 5).value = tx_level         # this tx level
                ws.cell(row, 6).value = measured_data[0]      # measured power
                ws.cell(row, 7).value = measured_data[1]      # RX level
                ws.cell(row, 8).value = measured_data[2][0]   # RSRP_RX0
                ws.cell(row, 9).value = measured_data[2][1]   # RSRP_RX1
                ws.cell(row, 10).value = measured_data[2][2]  # RSRP_RX2
                ws.cell(row, 11).value = measured_data[2][3]  # RSRP_RX3
                ws.cell(row, 12).value = measured_data[3][0]  # CINR_RX0
                ws.cell(row, 13).value = measured_data[3][1]  # CINR_RX1
                ws.cell(row, 14).value = measured_data[3][2]  # CINR_RX2
                ws.cell(row, 15).value = measured_data[3][3]  # CINR_RX3
                ws.cell(row, 16).value = measured_data[4][0]  # AGC_RX0
                ws.cell(row, 17).value = measured_data[4][1]  # AGC_RX1
                ws.cell(row, 18).value = measured_data[4][2]  # AGC_RX2
                ws.cell(row, 19).value = measured_data[4][3]  # AGC_RX3
                ws.cell(row, 20).value = tx_path
                row += 1
        elif tech == 'FR1':
            max_row = ws.max_row
            row = max_row + 1  # skip title
            for tx_freq, measured_data in data.items():
                chan = chan_judge_fr1(band, bw, tx_freq)
                ws.cell(row, 1).value = band
                ws.cell(row, 2).value = rx_path_fr1_dict[rx_path]
                ws.cell(row, 3).value = chan  # LMH
                ws.cell(row, 4).value = tx_freq
                ws.cell(row, 5).value = tx_level         # this tx level
                ws.cell(row, 6).value = measured_data[0]      # measured power
                ws.cell(row, 7).value = measured_data[1]      # RX level
                ws.cell(row, 8).value = measured_data[2][0]   # RSRP_RX0
                ws.cell(row, 9).value = measured_data[2][1]   # RSRP_RX1
                ws.cell(row, 10).value = measured_data[2][2]  # RSRP_RX2
                ws.cell(row, 11).value = measured_data[2][3]  # RSRP_RX3
                ws.cell(row, 12).value = measured_data[3][0]  # CINR_RX0
                ws.cell(row, 13).value = measured_data[3][1]  # CINR_RX1
                ws.cell(row, 14).value = measured_data[3][2]  # CINR_RX2
                ws.cell(row, 15).value = measured_data[3][3]  # CINR_RX3
                ws.cell(row, 16).value = measured_data[4][0]  # AGC_RX0
                ws.cell(row, 17).value = measured_data[4][1]  # AGC_RX1
                ws.cell(row, 18).value = measured_data[4][2]  # AGC_RX2
                ws.cell(row, 19).value = measured_data[4][3]  # AGC_RX3
                ws.cell(row, 20).value = tx_path
                row += 1

        elif tech == 'WCDMA':
            max_row = ws.max_row
            row = max_row + 1  # skip title
            for tx_chan, rx_level in data.items():
                chan = chan_judge_wcdma(band, cm_pmt_ftm.transfer_chan2freq_wcdma(band, tx_chan))
                ws.cell(row, 1).value = band
                ws.cell(row, 2).value = rx_path_wcdma_dict[rx_path]
                ws.cell(row, 3).value = chan  # LMH
                ws.cell(row, 4).value = tx_chan  # channel
                ws.cell(row, 5).value = cm_pmt_ftm.transfer_chan2freq_wcdma(band, tx_chan, 'tx')  # freq_tx
                ws.cell(row, 6).value = rx_level
                row += 1

        elif tech == 'GSM':
            max_row = ws.max_row
            row = max_row + 1
            for rx_chan, rx_level_rssi in data.items():
                chan = chan_judge_gsm(band, cm_pmt_ftm.transfer_chan2freq_gsm(band, rx_chan))
                ws.cell(row, 1).value = band
                ws.cell(row, 2).value = rx_path_gsm_dict[rx_path]
                ws.cell(row, 3).value = chan  # LMH
                ws.cell(row, 4).value = rx_chan  # channel
                ws.cell(row, 5).value = cm_pmt_ftm.transfer_chan2freq_gsm(band, rx_chan, 'rx')  # freq_rx
                ws.cell(row, 6).value = rx_level_rssi[0]
                ws.cell(row, 7).value = rx_level_rssi[1]
                row += 1

        wb.save(file_path)
        wb.close()

        return file_path


def tx_power_fcc_ce_export_excel(self, data):
    logger.info('----------save to excel----------')
    filename = f'Power_{script}_{tech}.xlsx'
    file_path = Path(excel_folder_path()) / Path(filename)
    if Path(file_path).exists() is False:
        logger.info('----------file does not exist----------')
        wb = openpyxl.Workbook()
        wb.remove(wb['Sheet'])
        # to create sheet
        sheetname = script
        ws = wb.create_sheet(sheetname)
        ws['A1'] = 'Band'
        ws['B1'] = 'BW'
        ws['C1'] = 'MCS'
        ws['D1'] = 'RB_size'
        ws['E1'] = 'RB_start'
        ws['F1'] = 'Tx_path'
        ws['G1'] = 'Chan'
        ws['H1'] = 'Tx_Freq'
        ws['I1'] = 'Tx_level'
        ws['J1'] = 'Power_measured'

        wb.save(file_path)
        wb.close()

    logger.info('----------file exist----------')
    wb = openpyxl.load_workbook(file_path)
    ws = wb[script]
    band = None
    bw = None
    mcs = None
    rb_size = None
    rb_start = None

    if tech == 'LTE':
        band = band_lte
        bw = bw_lte
        mcs = mcs_lte
        rb_size = rb_size_lte
        rb_start = rb_start_lte

    elif tech == 'FR1':
        band = band_fr1
        bw = bw_fr1
        mcs = mcs_fr1
        rb_size = rb_size_fr1
        rb_start = rb_start_fr1

    for tx_freq, measured_data in data.items():
        max_row = ws.max_row
        row = max_row + 1
        ws.cell(row, 1).value = band
        ws.cell(row, 2).value = bw
        ws.cell(row, 3).value = mcs
        ws.cell(row, 4).value = rb_size
        ws.cell(row, 5).value = rb_start
        ws.cell(row, 6).value = tx_path
        ws.cell(row, 7).value = measured_data[0]
        ws.cell(row, 8).value = tx_freq
        ws.cell(row, 9).value = tx_level
        ws.cell(row, 10).value = measured_data[1]

    wb.save(file_path)
    wb.close()
    return file_path


def tx_power_relative_test_export_excel(self, data, band, bw, tx_freq_level, mode=0):  # mode general: 0,  mode LMH: 1
    """
    data is dict like:
    tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET]
    """
    logger.info('----------save to excel----------')
    filename = None
    file_path = Path(excel_folder_path()) / Path(filename)
    if script == 'GENERAL':
        if mode == 1:
            if tx_freq_level >= 100:
                filename = f'relative power_{bw}MHZ_{tech}_LMH.xlsx'
            elif tx_freq_level <= 100:
                filename = f'TxP_ACLR_EVM_{bw}MHZ_{tech}_LMH.xlsx'

            if Path(file_path).exists() is False:
                logger.info('----------file does not exist----------')
                wb = openpyxl.Workbook()
                wb.remove(wb['Sheet'])
                # to create sheet
                if tech == 'LTE':
                    for mcs in ['QPSK', 'Q16', 'Q64', 'Q256']:  # some cmw10 might not have licesnse of Q256
                        wb.create_sheet(f'Raw_Data_{mcs}_PRB')
                        wb.create_sheet(f'Raw_Data_{mcs}_FRB')

                        for sheetname in wb.sheetnames:
                            ws = wb[sheetname]
                            ws['A1'] = 'Band'
                            ws['B1'] = 'Chan'
                            ws['C1'] = 'Tx_Freq'
                            ws['D1'] = 'Tx_level'
                            ws['E1'] = 'Measured_Power'
                            ws['F1'] = 'E_-1'
                            ws['G1'] = 'E_+1'
                            ws['H1'] = 'U_-1'
                            ws['I1'] = 'U_+1'
                            ws['J1'] = 'U_-2'
                            ws['K1'] = 'U_+2'
                            ws['L1'] = 'EVM'
                            ws['M1'] = 'Freq_Err'
                            ws['N1'] = 'IQ_OFFSET'
                            ws['O1'] = 'RB_num'
                            ws['P1'] = 'RB_start'
                            ws['Q1'] = 'MCS'
                            ws['R1'] = 'Tx_Path'
                            ws['S1'] = 'Sync_Path'
                            ws['T1'] = 'AS_Path'
                            ws['U1'] = 'Current(mA)'
                            ws['V1'] = 'Condition'
                            ws['W1'] = 'Temp0'
                            ws['X1'] = 'Temp1'

                elif tech == 'FR1':
                    for mcs in ['QPSK', 'Q16', 'Q64', 'Q256', 'BPSK']:  # some cmw10 might not have licesnse of Q256
                        wb.create_sheet(f'Raw_Data_{mcs}')

                        for sheetname in wb.sheetnames:
                            ws = wb[sheetname]
                            ws['A1'] = 'Band'
                            ws['B1'] = 'Chan'
                            ws['C1'] = 'Tx_Freq'
                            ws['D1'] = 'Tx_level'
                            ws['E1'] = 'Measured_Power'
                            ws['F1'] = 'E_-1'
                            ws['G1'] = 'E_+1'
                            ws['H1'] = 'U_-1'
                            ws['I1'] = 'U_+1'
                            ws['J1'] = 'U_-2'
                            ws['K1'] = 'U_+2'
                            ws['L1'] = 'EVM'
                            ws['M1'] = 'Freq_Err'
                            ws['N1'] = 'IQ_OFFSET'
                            ws['O1'] = 'RB_num'
                            ws['P1'] = 'RB_start'
                            ws['Q1'] = 'Type'
                            ws['R1'] = 'Tx_Path'
                            ws['S1'] = 'SCS(KHz)'
                            ws['T1'] = 'RB_STATE'
                            ws['U1'] = 'Sync_Path'
                            ws['V1'] = 'SRS_Path'
                            ws['W1'] = 'Current(mA)'
                            ws['X1'] = 'Condition'
                            ws['Y1'] = 'Temp0'
                            ws['Z1'] = 'Temp1'

                elif tech == 'WCDMA':

                    wb.create_sheet(f'Raw_Data')

                    for sheetname in wb.sheetnames:
                        ws = wb[sheetname]
                        ws['A1'] = 'Band'
                        ws['B1'] = 'Chan'
                        ws['C1'] = 'Channel'
                        ws['D1'] = 'Tx_Freq'
                        ws['E1'] = 'Tx_level'
                        ws['F1'] = 'Measured_Power'
                        ws['G1'] = 'U_-1'
                        ws['H1'] = 'U_+1'
                        ws['I1'] = 'U_-2'
                        ws['J1'] = 'U_+2'
                        ws['K1'] = 'OBW'
                        ws['L1'] = 'EVM'
                        ws['M1'] = 'Freq_Err'
                        ws['N1'] = 'IQ_OFFSET'
                        ws['O1'] = 'Tx_Path'
                        ws['P1'] = 'AS_Path'
                        ws['Q1'] = 'Current(mA)'
                        ws['R1'] = 'Condition'
                        ws['S1'] = 'Temp0'
                        ws['T1'] = 'Temp1'

                elif tech == 'GSM':

                    wb.create_sheet(f'Raw_Data_GMSK')
                    wb.create_sheet(f'Raw_Data_EPSK')

                    for sheetname in wb.sheetnames:
                        ws = wb[sheetname]
                        ws['A1'] = 'Band'
                        ws['B1'] = 'Chan'
                        ws['C1'] = 'Channel'
                        ws['D1'] = 'Rx_Freq'
                        ws['E1'] = 'Tx_PCL'
                        ws['F1'] = 'Measured_Power'
                        ws['G1'] = 'Phase_rms'
                        ws['H1'] = 'EVM_rms'
                        ws['I1'] = 'Ferr'
                        ws['J1'] = 'ORFS_MOD_-200'
                        ws['K1'] = 'ORFS_MOD_+200'
                        ws['L1'] = 'ORFS_MOD_-400'
                        ws['M1'] = 'ORFS_MOD_+400'
                        ws['N1'] = 'ORFS_MOD_-600'
                        ws['O1'] = 'ORFS_MOD_+600'
                        ws['P1'] = 'ORFS_SW_-400'
                        ws['Q1'] = 'ORFS_SW_+400'
                        ws['R1'] = 'ORFS_SW_-600'
                        ws['S1'] = 'ORFS_SW_+600'
                        ws['T1'] = 'ORFS_SW_-1200'
                        ws['U1'] = 'ORFS_SW_+1200'
                        ws['V1'] = 'AS_Path'
                        ws['W1'] = 'Current(mA)'
                        ws['X1'] = 'Condition'
                        ws['Y1'] = 'Temp0'
                        ws['Z1'] = 'Temp1'

                wb.save(file_path)
                wb.close()

            logger.info('----------file exist----------')
            wb = openpyxl.load_workbook(file_path)
            ws = None
            if tech == 'LTE':
                ws = wb[f'Raw_Data_{mcs_lte}_{rb_state}']
            elif tech == 'FR1':
                ws = wb[f'Raw_Data_{mcs_fr1}']
            elif tech == 'WCDMA':
                ws = wb[f'Raw_Data']
            elif tech == 'GSM':
                ws = wb[f'Raw_Data_{mod_gsm}']

            if tech == 'LTE':
                max_row = ws.max_row
                row = max_row + 1
                if tx_freq_level >= 100:
                    for tx_level, measured_data in data.items():
                        chan = chan_judge_lte(band, bw, tx_freq_level)
                        ws.cell(row, 1).value = band
                        ws.cell(row, 2).value = chan  # LMH
                        ws.cell(row, 3).value = tx_freq_level  # this tx_freq_lte
                        ws.cell(row, 4).value = tx_level
                        ws.cell(row, 5).value = measured_data[3]
                        ws.cell(row, 6).value = measured_data[2]
                        ws.cell(row, 7).value = measured_data[4]
                        ws.cell(row, 8).value = measured_data[1]
                        ws.cell(row, 9).value = measured_data[5]
                        ws.cell(row, 10).value = measured_data[0]
                        ws.cell(row, 11).value = measured_data[6]
                        ws.cell(row, 12).value = measured_data[7]
                        ws.cell(row, 13).value = measured_data[8]
                        ws.cell(row, 14).value = measured_data[9]
                        ws.cell(row, 15).value = rb_size_lte
                        ws.cell(row, 16).value = rb_start_lte
                        ws.cell(row, 17).value = mcs_lte
                        ws.cell(row, 18).value = tx_path
                        ws.cell(row, 19).value = sync_path
                        ws.cell(row, 20).value = asw_path
                        row += 1

                elif tx_freq_level <= 100:
                    for tx_freq, measured_data in data.items():
                        chan = chan_judge_lte(band, bw, tx_freq)
                        ws.cell(row, 1).value = band
                        ws.cell(row, 2).value = chan  # # LMH
                        ws.cell(row, 3).value = tx_freq
                        ws.cell(row, 4).value = tx_freq_level  # this tx_level
                        ws.cell(row, 5).value = measured_data[3]
                        ws.cell(row, 6).value = measured_data[2]
                        ws.cell(row, 7).value = measured_data[4]
                        ws.cell(row, 8).value = measured_data[1]
                        ws.cell(row, 9).value = measured_data[5]
                        ws.cell(row, 10).value = measured_data[0]
                        ws.cell(row, 11).value = measured_data[6]
                        ws.cell(row, 12).value = measured_data[7]
                        ws.cell(row, 13).value = measured_data[8]
                        ws.cell(row, 14).value = measured_data[9]
                        ws.cell(row, 15).value = rb_size_lte
                        ws.cell(row, 16).value = rb_start_lte
                        ws.cell(row, 17).value = mcs_lte
                        ws.cell(row, 18).value = tx_path
                        ws.cell(row, 19).value = sync_path
                        ws.cell(row, 20).value = asw_path
                        ws.cell(row, 21).value = measured_data[10]
                        ws.cell(row, 22).value = wt.condition
                        ws.cell(row, 23).value = measured_data[11]
                        ws.cell(row, 24).value = measured_data[12]

                        row += 1

            elif tech == 'FR1':
                max_row = ws.max_row
                row = max_row + 1
                if tx_freq_level >= 100:
                    for tx_level, measured_data in data.items():
                        chan = chan_judge_fr1(band, bw, tx_freq_level)
                        ws.cell(row, 1).value = band
                        ws.cell(row, 2).value = chan  # LMH
                        ws.cell(row, 3).value = tx_freq_level  # this tx_freq_lte
                        ws.cell(row, 4).value = tx_level
                        ws.cell(row, 5).value = measured_data[3]
                        ws.cell(row, 6).value = measured_data[2]
                        ws.cell(row, 7).value = measured_data[4]
                        ws.cell(row, 8).value = measured_data[1]
                        ws.cell(row, 9).value = measured_data[5]
                        ws.cell(row, 10).value = measured_data[0]
                        ws.cell(row, 11).value = measured_data[6]
                        ws.cell(row, 12).value = measured_data[7]
                        ws.cell(row, 13).value = measured_data[8]
                        ws.cell(row, 14).value = measured_data[9]
                        ws.cell(row, 15).value = rb_size_fr1
                        ws.cell(row, 16).value = rb_start_fr1
                        ws.cell(row, 17).value = type_fr1
                        ws.cell(row, 18).value = tx_path
                        ws.cell(row, 19).value = scs
                        ws.cell(row, 20).value = rb_state
                        ws.cell(row, 21).value = sync_path
                        ws.cell(row, 22).value = srs_path

                        row += 1

                elif tx_freq_level <= 100:
                    for tx_freq, measured_data in data.items():
                        chan = chan_judge_fr1(band, bw, tx_freq)
                        ws.cell(row, 1).value = band
                        ws.cell(row, 2).value = chan  # LMH
                        ws.cell(row, 3).value = tx_freq
                        ws.cell(row, 4).value = tx_freq_level  # this tx_level
                        ws.cell(row, 5).value = measured_data[3]
                        ws.cell(row, 6).value = measured_data[2]
                        ws.cell(row, 7).value = measured_data[4]
                        ws.cell(row, 8).value = measured_data[1]
                        ws.cell(row, 9).value = measured_data[5]
                        ws.cell(row, 10).value = measured_data[0]
                        ws.cell(row, 11).value = measured_data[6]
                        ws.cell(row, 12).value = measured_data[7]
                        ws.cell(row, 13).value = measured_data[8]
                        ws.cell(row, 14).value = measured_data[9]
                        ws.cell(row, 15).value = rb_size_fr1
                        ws.cell(row, 16).value = rb_start_fr1
                        ws.cell(row, 17).value = type_fr1
                        ws.cell(row, 18).value = tx_path
                        ws.cell(row, 19).value = scs
                        ws.cell(row, 20).value = rb_state
                        ws.cell(row, 21).value = sync_path
                        ws.cell(row, 22).value = srs_path
                        ws.cell(row, 23).value = measured_data[10]
                        ws.cell(row, 24).value = wt.condition
                        ws.cell(row, 25).value = measured_data[11]
                        ws.cell(row, 26).value = measured_data[12]

                        row += 1

            elif tech == 'WCDMA':
                max_row = ws.max_row
                row = max_row + 1
                if tx_freq_level >= 100:
                    for tx_level, measured_data in data.items():
                        chan = chan_judge_wcdma(band, tx_freq_level)
                        ws.cell(row, 1).value = band
                        ws.cell(row, 2).value = chan  # LMH
                        ws.cell(row, 3).value = cm_pmt_ftm.trandfer_freq2chan_wcdma(band_wcdma, tx_freq_level,
                                                                                    'tx')  # this channel
                        ws.cell(row, 4).value = tx_freq_level  # this tx_freq_wcdma
                        ws.cell(row, 5).value = tx_level
                        ws.cell(row, 6).value = measured_data[0]
                        ws.cell(row, 7).value = measured_data[1]
                        ws.cell(row, 8).value = measured_data[2]
                        ws.cell(row, 9).value = measured_data[3]
                        ws.cell(row, 10).value = measured_data[4]
                        ws.cell(row, 11).value = measured_data[5]
                        ws.cell(row, 12).value = measured_data[6]
                        ws.cell(row, 13).value = measured_data[7]
                        ws.cell(row, 14).value = measured_data[8]
                        ws.cell(row, 15).value = tx_path
                        ws.cell(row, 16).value = asw_path
                        row += 1

                elif tx_freq_level <= 100:
                    for tx_freq, measured_data in data.items():
                        chan = chan_judge_wcdma(band, tx_freq)
                        ws.cell(row, 1).value = band
                        ws.cell(row, 2).value = chan  # # LMH
                        ws.cell(row, 3).value = cm_pmt_ftm.trandfer_freq2chan_wcdma(band_wcdma, tx_freq,
                                                                                    'tx')  # this channel
                        ws.cell(row, 4).value = tx_freq
                        ws.cell(row, 5).value = tx_freq_level  # this tx_level
                        ws.cell(row, 6).value = measured_data[0]
                        ws.cell(row, 7).value = measured_data[1]
                        ws.cell(row, 8).value = measured_data[2]
                        ws.cell(row, 9).value = measured_data[3]
                        ws.cell(row, 10).value = measured_data[4]
                        ws.cell(row, 11).value = measured_data[5]
                        ws.cell(row, 12).value = measured_data[6]
                        ws.cell(row, 13).value = measured_data[7]
                        ws.cell(row, 14).value = measured_data[8]
                        ws.cell(row, 15).value = tx_path
                        ws.cell(row, 16).value = asw_path
                        ws.cell(row, 17).value = measured_data[9]
                        ws.cell(row, 18).value = wt.condition
                        ws.cell(row, 19).value = measured_data[10]
                        ws.cell(row, 20).value = measured_data[11]
                        row += 1

            elif tech == 'GSM':
                max_row = ws.max_row
                row = max_row + 1
                if tx_freq_level >= 100:
                    for tx_pcl, measured_data in data.items():
                        chan = chan_judge_gsm(band, tx_freq_level)
                        ws.cell(row, 1).value = band
                        ws.cell(row, 2).value = chan  # LMH
                        ws.cell(row, 3).value = cm_pmt_ftm.transfer_freq2chan_gsm(band_gsm, tx_freq_level)
                        ws.cell(row, 4).value = tx_freq_level  # this rx_freq_gsm
                        ws.cell(row, 5).value = tx_pcl
                        ws.cell(row, 6).value = measured_data[0]
                        ws.cell(row, 7).value = measured_data[1]
                        ws.cell(row, 8).value = measured_data[2]
                        ws.cell(row, 9).value = measured_data[3]
                        ws.cell(row, 10).value = measured_data[4]
                        ws.cell(row, 11).value = measured_data[5]
                        ws.cell(row, 12).value = measured_data[6]
                        ws.cell(row, 13).value = measured_data[7]
                        ws.cell(row, 14).value = measured_data[8]
                        ws.cell(row, 15).value = measured_data[9]
                        ws.cell(row, 16).value = measured_data[10]
                        ws.cell(row, 17).value = measured_data[11]
                        ws.cell(row, 18).value = measured_data[12]
                        ws.cell(row, 19).value = measured_data[13]
                        ws.cell(row, 20).value = measured_data[14]
                        ws.cell(row, 21).value = measured_data[15]
                        ws.cell(row, 22).value = asw_path

                        row += 1

                elif tx_freq_level <= 100:
                    for rx_freq, measured_data in data.items():
                        chan = chan_judge_gsm(band, rx_freq)
                        ws.cell(row, 1).value = band
                        ws.cell(row, 2).value = chan  # LMH
                        ws.cell(row, 3).value = cm_pmt_ftm.transfer_freq2chan_gsm(band_gsm, rx_freq)
                        ws.cell(row, 4).value = rx_freq  # this rx_freq_gsm
                        ws.cell(row, 5).value = tx_freq_level  # this pcl
                        ws.cell(row, 6).value = measured_data[0]
                        ws.cell(row, 7).value = measured_data[1]
                        ws.cell(row, 8).value = measured_data[2]
                        ws.cell(row, 9).value = measured_data[3]
                        ws.cell(row, 10).value = measured_data[4]
                        ws.cell(row, 11).value = measured_data[5]
                        ws.cell(row, 12).value = measured_data[6]
                        ws.cell(row, 13).value = measured_data[7]
                        ws.cell(row, 14).value = measured_data[8]
                        ws.cell(row, 15).value = measured_data[9]
                        ws.cell(row, 16).value = measured_data[10]
                        ws.cell(row, 17).value = measured_data[11]
                        ws.cell(row, 18).value = measured_data[12]
                        ws.cell(row, 19).value = measured_data[13]
                        ws.cell(row, 20).value = measured_data[14]
                        ws.cell(row, 21).value = measured_data[15]
                        ws.cell(row, 22).value = asw_path
                        ws.cell(row, 23).value = measured_data[16]
                        ws.cell(row, 24).value = wt.condition
                        ws.cell(row, 25).value = measured_data[17]
                        ws.cell(row, 26).value = measured_data[18]

                        row += 1

            wb.save(file_path)
            wb.close()

            return file_path
        else:  # mode = 0
            if tx_freq_level >= 100:
                filename = f'Tx_level_sweep_{bw}MHZ_{tech}.xlsx'
            elif tx_freq_level <= 100:
                if tx_1rb_filename_judge:
                    filename = f'Tx_1RB_sweep_{bw}MHZ_{tech}.xlsx'
                else:
                    filename = f'Freq_sweep_{bw}MHZ_{tech}.xlsx'
            file_path = Path(excel_folder_path()) / Path(filename)
            if Path(file_path).exists() is False:
                logger.info('----------file does not exist----------')
                wb = openpyxl.Workbook()
                wb.remove(wb['Sheet'])
                # to create sheet
                if tech == 'LTE':
                    for mcs in ['QPSK', 'Q16', 'Q64', 'Q256']:  # some cmw10 might not have licesnse of Q256
                        wb.create_sheet(f'Raw_Data_{mcs}_PRB')
                        wb.create_sheet(f'Raw_Data_{mcs}_FRB')

                    for sheetname in wb.sheetnames:
                        ws = wb[sheetname]
                        ws['A1'] = 'Band'
                        ws['B1'] = 'Tx_Freq'
                        ws['C1'] = 'Tx_level'
                        ws['D1'] = 'Measured_Power'
                        ws['E1'] = 'E_-1'
                        ws['F1'] = 'E_+1'
                        ws['G1'] = 'U_-1'
                        ws['H1'] = 'U_+1'
                        ws['I1'] = 'U_-2'
                        ws['J1'] = 'U_+2'
                        ws['K1'] = 'EVM'
                        ws['L1'] = 'Freq_Err'
                        ws['M1'] = 'IQ_OFFSET'
                        ws['N1'] = 'RB_num'
                        ws['O1'] = 'RB_start'
                        ws['P1'] = 'MCS'
                        ws['Q1'] = 'Tx_Path'
                        ws['R1'] = 'Sync_Path'
                        ws['S1'] = 'AS_Path'
                        ws['T1'] = 'Current(mA)'
                        ws['U1'] = 'Condition'

                elif tech == 'FR1':
                    for mcs in ['QPSK', 'Q16', 'Q64', 'Q256', 'BPSK']:  # some cmw10 might not have licesnse of Q256
                        wb.create_sheet(f'Raw_Data_{mcs}')

                        for sheetname in wb.sheetnames:
                            ws = wb[sheetname]
                            ws['A1'] = 'Band'
                            ws['B1'] = 'Tx_Freq'
                            ws['C1'] = 'Tx_level'
                            ws['D1'] = 'Measured_Power'
                            ws['E1'] = 'E_-1'
                            ws['F1'] = 'E_+1'
                            ws['G1'] = 'U_-1'
                            ws['H1'] = 'U_+1'
                            ws['I1'] = 'U_-2'
                            ws['J1'] = 'U_+2'
                            ws['K1'] = 'EVM'
                            ws['L1'] = 'Freq_Err'
                            ws['M1'] = 'IQ_OFFSET'
                            ws['N1'] = 'RB_num'
                            ws['O1'] = 'RB_start'
                            ws['P1'] = 'Type'
                            ws['Q1'] = 'Tx_Path'
                            ws['R1'] = 'SCS(KHz)'
                            ws['S1'] = 'RB_STATE'
                            ws['T1'] = 'Sync_Path'
                            ws['U1'] = 'SRS_Path'
                            ws['V1'] = 'Current(mA)'
                            ws['W1'] = 'Condition'

                elif tech == 'WCDMA':
                    wb.create_sheet(f'Raw_Data')
                    for sheetname in wb.sheetnames:
                        ws = wb[sheetname]
                        ws['A1'] = 'Band'
                        ws['B1'] = 'Channel'
                        ws['C1'] = 'Tx_Freq'
                        ws['D1'] = 'Tx_level'
                        ws['E1'] = 'Measured_Power'
                        ws['F1'] = 'U_-1'
                        ws['G1'] = 'U_+1'
                        ws['H1'] = 'U_-2'
                        ws['I1'] = 'U_+2'
                        ws['J1'] = 'OBW'
                        ws['K1'] = 'EVM'
                        ws['L1'] = 'Freq_Err'
                        ws['M1'] = 'IQ_OFFSET'
                        ws['N1'] = 'Tx_Path'
                        ws['O1'] = 'AS_Path'
                        ws['P1'] = 'Current(mA)'
                        ws['Q1'] = 'Condition'

                elif tech == 'GSM':
                    wb.create_sheet(f'Raw_Data_GMSK')
                    wb.create_sheet(f'Raw_Data_EPSK')

                    for sheetname in wb.sheetnames:
                        ws = wb[sheetname]
                        ws['A1'] = 'Band'
                        ws['B1'] = 'Channel'
                        ws['C1'] = 'Rx_Freq'
                        ws['D1'] = 'Tx_PCL'
                        ws['E1'] = 'Measured_Power'
                        ws['F1'] = 'Phase_rms'
                        ws['G1'] = 'EVM_rms'
                        ws['H1'] = 'Ferr'
                        ws['I1'] = 'ORFS_MOD_-200'
                        ws['J1'] = 'ORFS_MOD_+200'
                        ws['K1'] = 'ORFS_MOD_-400'
                        ws['L1'] = 'ORFS_MOD_+400'
                        ws['M1'] = 'ORFS_MOD_-600'
                        ws['N1'] = 'ORFS_MOD_+600'
                        ws['O1'] = 'ORFS_SW_-400'
                        ws['P1'] = 'ORFS_SW_+400'
                        ws['Q1'] = 'ORFS_SW_-600'
                        ws['R1'] = 'ORFS_SW_+600'
                        ws['S1'] = 'ORFS_SW_-1200'
                        ws['T1'] = 'ORFS_SW_+1200'
                        ws['U1'] = 'AS_Path'
                        ws['V1'] = 'Current(mA)'
                        ws['W1'] = 'Condition'

                wb.save(file_path)
                wb.close()

            logger.info('----------file exist----------')
            wb = openpyxl.load_workbook(file_path)
            ws = None
            if tech == 'LTE':
                ws = wb[f'Raw_Data_{mcs_lte}_{rb_state}']
            elif tech == 'FR1':
                ws = wb[f'Raw_Data_{mcs_fr1}']
            elif tech == 'WCDMA':
                ws = wb[f'Raw_Data']
            elif tech == 'GSM':
                ws = wb[f'Raw_Data_{mod_gsm}']

            if tech == 'LTE':
                max_row = ws.max_row
                row = max_row + 1
                if tx_freq_level >= 100:
                    for tx_level, measured_data in data.items():
                        ws.cell(row, 1).value = band
                        ws.cell(row, 2).value = tx_freq_level  # this tx_freq
                        ws.cell(row, 3).value = tx_level
                        ws.cell(row, 4).value = measured_data[3]
                        ws.cell(row, 5).value = measured_data[2]
                        ws.cell(row, 6).value = measured_data[4]
                        ws.cell(row, 7).value = measured_data[1]
                        ws.cell(row, 8).value = measured_data[5]
                        ws.cell(row, 9).value = measured_data[0]
                        ws.cell(row, 10).value = measured_data[6]
                        ws.cell(row, 11).value = measured_data[7]
                        ws.cell(row, 12).value = measured_data[8]
                        ws.cell(row, 13).value = measured_data[9]
                        ws.cell(row, 14).value = rb_size_lte
                        ws.cell(row, 15).value = rb_start_lte
                        ws.cell(row, 16).value = mcs_lte
                        ws.cell(row, 17).value = tx_path
                        ws.cell(row, 18).value = sync_path
                        ws.cell(row, 19).value = asw_path
                        ws.cell(row, 20).value = measured_data[10]
                        ws.cell(row, 21).value = wt.condition
                        row += 1

                elif tx_freq_level <= 100:
                    for tx_freq, measured_data in data.items():
                        ws.cell(row, 1).value = band
                        ws.cell(row, 2).value = tx_freq
                        ws.cell(row, 3).value = tx_freq_level  # this tx_level
                        ws.cell(row, 4).value = measured_data[3]
                        ws.cell(row, 5).value = measured_data[2]
                        ws.cell(row, 6).value = measured_data[4]
                        ws.cell(row, 7).value = measured_data[1]
                        ws.cell(row, 8).value = measured_data[5]
                        ws.cell(row, 9).value = measured_data[0]
                        ws.cell(row, 10).value = measured_data[6]
                        ws.cell(row, 11).value = measured_data[7]
                        ws.cell(row, 12).value = measured_data[8]
                        ws.cell(row, 13).value = measured_data[9]
                        ws.cell(row, 14).value = rb_size_lte
                        ws.cell(row, 15).value = rb_start_lte
                        ws.cell(row, 16).value = mcs_lte
                        ws.cell(row, 17).value = tx_path
                        ws.cell(row, 18).value = sync_path
                        ws.cell(row, 19).value = asw_path
                        row += 1

            elif tech == 'FR1':
                max_row = ws.max_row
                row = max_row + 1
                if tx_freq_level >= 100:
                    for tx_level, measured_data in data.items():
                        ws.cell(row, 1).value = band
                        ws.cell(row, 2).value = tx_freq_level  # this tx_freq
                        ws.cell(row, 3).value = tx_level
                        ws.cell(row, 4).value = measured_data[3]
                        ws.cell(row, 5).value = measured_data[2]
                        ws.cell(row, 6).value = measured_data[4]
                        ws.cell(row, 7).value = measured_data[1]
                        ws.cell(row, 8).value = measured_data[5]
                        ws.cell(row, 9).value = measured_data[0]
                        ws.cell(row, 10).value = measured_data[6]
                        ws.cell(row, 11).value = measured_data[7]
                        ws.cell(row, 12).value = measured_data[8]
                        ws.cell(row, 13).value = measured_data[9]
                        ws.cell(row, 14).value = rb_size_fr1
                        ws.cell(row, 15).value = rb_start_fr1
                        ws.cell(row, 16).value = type_fr1
                        ws.cell(row, 17).value = tx_path
                        ws.cell(row, 18).value = scs
                        ws.cell(row, 19).value = rb_state
                        ws.cell(row, 20).value = sync_path
                        ws.cell(row, 21).value = srs_path
                        ws.cell(row, 22).value = measured_data[10]
                        ws.cell(row, 23).value = wt.condition
                        row += 1

                elif tx_freq_level <= 100:
                    for tx_freq, measured_data in data.items():
                        ws.cell(row, 1).value = band
                        ws.cell(row, 2).value = tx_freq
                        ws.cell(row, 3).value = tx_freq_level  # this tx_level
                        ws.cell(row, 4).value = measured_data[3]
                        ws.cell(row, 5).value = measured_data[2]
                        ws.cell(row, 6).value = measured_data[4]
                        ws.cell(row, 7).value = measured_data[1]
                        ws.cell(row, 8).value = measured_data[5]
                        ws.cell(row, 9).value = measured_data[0]
                        ws.cell(row, 10).value = measured_data[6]
                        ws.cell(row, 11).value = measured_data[7]
                        ws.cell(row, 12).value = measured_data[8]
                        ws.cell(row, 13).value = measured_data[9]
                        ws.cell(row, 14).value = rb_size_fr1
                        ws.cell(row, 15).value = rb_start_fr1
                        ws.cell(row, 16).value = type_fr1
                        ws.cell(row, 17).value = tx_path
                        ws.cell(row, 18).value = scs
                        ws.cell(row, 19).value = rb_state
                        ws.cell(row, 20).value = sync_path
                        ws.cell(row, 21).value = srs_path
                        row += 1

            elif tech == 'WCDMA':
                max_row = ws.max_row
                row = max_row + 1
                if tx_freq_level >= 100:
                    for tx_level, measured_data in data.items():
                        ws.cell(row, 1).value = band
                        ws.cell(row, 2).value = cm_pmt_ftm.trandfer_freq2chan_wcdma(band_wcdma, tx_freq_level,
                                                                                    'tx')  # this channel
                        ws.cell(row, 3).value = tx_freq_level  # this tx_freq_wcdma
                        ws.cell(row, 4).value = tx_level
                        ws.cell(row, 5).value = measured_data[0]
                        ws.cell(row, 6).value = measured_data[1]
                        ws.cell(row, 7).value = measured_data[2]
                        ws.cell(row, 8).value = measured_data[3]
                        ws.cell(row, 9).value = measured_data[4]
                        ws.cell(row, 10).value = measured_data[5]
                        ws.cell(row, 11).value = measured_data[6]
                        ws.cell(row, 12).value = measured_data[7]
                        ws.cell(row, 13).value = measured_data[8]
                        ws.cell(row, 14).value = tx_path
                        ws.cell(row, 15).value = asw_path
                        ws.cell(row, 16).value = measured_data[9]
                        ws.cell(row, 17).value = wt.condition
                        row += 1

                elif tx_freq_level <= 100:
                    for tx_freq, measured_data in data.items():
                        ws.cell(row, 1).value = band
                        ws.cell(row, 2).value = tx_freq  # this channel
                        ws.cell(row, 3).value = cm_pmt_ftm.transfer_chan2freq_wcdma(band_wcdma, tx_freq, 'tx')
                        ws.cell(row, 4).value = tx_freq_level  # this tx_level
                        ws.cell(row, 5).value = measured_data[0]
                        ws.cell(row, 6).value = measured_data[1]
                        ws.cell(row, 7).value = measured_data[2]
                        ws.cell(row, 8).value = measured_data[3]
                        ws.cell(row, 9).value = measured_data[4]
                        ws.cell(row, 10).value = measured_data[5]
                        ws.cell(row, 11).value = measured_data[6]
                        ws.cell(row, 12).value = measured_data[7]
                        ws.cell(row, 13).value = measured_data[8]
                        ws.cell(row, 14).value = tx_path
                        ws.cell(row, 15).value = asw_path
                        row += 1

            elif tech == 'GSM':
                max_row = ws.max_row
                row = max_row + 1
                if tx_freq_level >= 100:
                    for tx_pcl, measured_data in data.items():
                        ws.cell(row, 1).value = band
                        ws.cell(row, 2).value = cm_pmt_ftm.transfer_freq2chan_gsm(band_gsm, tx_freq_level)
                        ws.cell(row, 3).value = tx_freq_level  # this rx_freq_gsm
                        ws.cell(row, 4).value = tx_pcl
                        ws.cell(row, 5).value = measured_data[0]
                        ws.cell(row, 6).value = measured_data[1]
                        ws.cell(row, 7).value = measured_data[2]
                        ws.cell(row, 8).value = measured_data[3]
                        ws.cell(row, 9).value = measured_data[4]
                        ws.cell(row, 10).value = measured_data[5]
                        ws.cell(row, 11).value = measured_data[6]
                        ws.cell(row, 12).value = measured_data[7]
                        ws.cell(row, 13).value = measured_data[8]
                        ws.cell(row, 14).value = measured_data[9]
                        ws.cell(row, 15).value = measured_data[10]
                        ws.cell(row, 16).value = measured_data[11]
                        ws.cell(row, 17).value = measured_data[12]
                        ws.cell(row, 18).value = measured_data[13]
                        ws.cell(row, 19).value = measured_data[14]
                        ws.cell(row, 20).value = measured_data[15]
                        ws.cell(row, 21).value = asw_path
                        ws.cell(row, 22).value = measured_data[16]
                        ws.cell(row, 23).value = wt.condition

                        row += 1

                elif tx_freq_level <= 100:
                    for rx_freq, measured_data in data.items():
                        ws.cell(row, 1).value = band
                        ws.cell(row, 2).value = cm_pmt_ftm.transfer_freq2chan_gsm(band_gsm, rx_freq)
                        ws.cell(row, 3).value = rx_freq  # this rx_freq_gsm
                        ws.cell(row, 4).value = tx_freq_level  # this pcl
                        ws.cell(row, 5).value = measured_data[0]
                        ws.cell(row, 6).value = measured_data[1]
                        ws.cell(row, 7).value = measured_data[2]
                        ws.cell(row, 8).value = measured_data[3]
                        ws.cell(row, 9).value = measured_data[4]
                        ws.cell(row, 10).value = measured_data[5]
                        ws.cell(row, 11).value = measured_data[6]
                        ws.cell(row, 12).value = measured_data[7]
                        ws.cell(row, 13).value = measured_data[8]
                        ws.cell(row, 14).value = measured_data[9]
                        ws.cell(row, 15).value = measured_data[10]
                        ws.cell(row, 16).value = measured_data[11]
                        ws.cell(row, 17).value = measured_data[12]
                        ws.cell(row, 18).value = measured_data[13]
                        ws.cell(row, 19).value = measured_data[14]
                        ws.cell(row, 20).value = measured_data[15]
                        ws.cell(row, 21).value = asw_path

                        row += 1

            wb.save(file_path)
            wb.close()

            return file_path


def txp_aclr_evm_plot(self, file_path, mode=0):  # mode 0: general, mode 1: LMH
    logger.info('----------Plot Chart---------')
    wb = openpyxl.load_workbook(file_path)
    if script == 'GENERAL':
        if tech == 'LTE':
            if mode == 1:
                for ws_name in wb.sheetnames:
                    logger.info(f'========={ws_name}==========')
                    ws = wb[ws_name]

                    if ws._charts != []:  # if there is charts, delete it
                        ws._charts.clear()

                    logger.info('----------Power---------')
                    chart = LineChart()
                    chart.title = 'Power'
                    chart.y_axis.title = 'Power(dBm)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=5, min_row=1, max_col=5, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "Y1")

                    logger.info('----------ACLR---------')
                    chart = LineChart()
                    chart.title = 'ACLR'
                    chart.y_axis.title = 'ACLR(dB)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'
                    chart.y_axis.scaling.min = -60
                    chart.y_axis.scaling.max = -20

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=6, min_row=1, max_col=11, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'triangle'  # for EUTRA_-1
                    chart.series[0].marker.size = 10
                    chart.series[1].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[1].marker.size = 10
                    chart.series[2].graphicalProperties.line.width = 50000  # for UTRA_-1
                    chart.series[3].graphicalProperties.line.width = 50000  # for UTRA_+1
                    chart.series[4].graphicalProperties.line.dashStyle = 'dash'  # for UTRA_-2
                    chart.series[5].graphicalProperties.line.dashStyle = 'dash'  # for UTRA_+2

                    ws.add_chart(chart, "Y39")

                    logger.info('----------EVM---------')
                    chart = LineChart()
                    chart.title = 'EVM'
                    chart.y_axis.title = 'EVM(%)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=12, min_row=1, max_col=12, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "Y77")

                    logger.info('----------Current---------')
                    chart = LineChart()
                    chart.title = 'Current'
                    chart.y_axis.title = 'Current(mA)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=21, min_row=1, max_col=21, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "Y115")

                wb.save(file_path)
                wb.close()
            else:  # mode 0
                for ws_name in wb.sheetnames:
                    logger.info(f'========={ws_name}==========')
                    ws = wb[ws_name]

                    if ws._charts != []:  # if there is charts, delete it
                        ws._charts.clear()

                    logger.info('----------Power---------')
                    chart = LineChart()
                    chart.title = 'Power'
                    chart.y_axis.title = 'Power(dBm)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=4, min_row=1, max_col=4, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "V1")

                    logger.info('----------ACLR---------')
                    chart = LineChart()
                    chart.title = 'ACLR'
                    chart.y_axis.title = 'ACLR(dB)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'
                    chart.y_axis.scaling.min = -60
                    chart.y_axis.scaling.max = -20

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=5, min_row=1, max_col=10, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'triangle'  # for EUTRA_-1
                    chart.series[0].marker.size = 10
                    chart.series[1].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[1].marker.size = 10
                    chart.series[2].graphicalProperties.line.width = 50000  # for UTRA_-1
                    chart.series[3].graphicalProperties.line.width = 50000  # for UTRA_+1
                    chart.series[4].graphicalProperties.line.dashStyle = 'dash'  # for UTRA_-2
                    chart.series[5].graphicalProperties.line.dashStyle = 'dash'  # for UTRA_+2

                    ws.add_chart(chart, "V39")

                    logger.info('----------EVM---------')
                    chart = LineChart()
                    chart.title = 'EVM'
                    chart.y_axis.title = 'EVM(%)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=11, min_row=1, max_col=11, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "V77")

                    logger.info('----------Current---------')
                    chart = LineChart()
                    chart.title = 'Current'
                    chart.y_axis.title = 'Current(mA)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=20, min_row=1, max_col=20, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "V115")

                wb.save(file_path)
                wb.close()
        elif tech == 'FR1':
            if mode == 1:
                for ws_name in wb.sheetnames:
                    logger.info(f'========={ws_name}==========')
                    ws = wb[ws_name]

                    if ws._charts != []:  # if there is charts, delete it
                        ws._charts.clear()

                    logger.info('----------Power---------')
                    chart = LineChart()
                    chart.title = 'Power'
                    chart.y_axis.title = 'Power(dBm)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=5, min_row=1, max_col=5, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "AA1")

                    logger.info('----------ACLR---------')
                    chart = LineChart()
                    chart.title = 'ACLR'
                    chart.y_axis.title = 'ACLR(dB)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'
                    chart.y_axis.scaling.min = -60
                    chart.y_axis.scaling.max = -20

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=6, min_row=1, max_col=11, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'triangle'  # for EUTRA_-1
                    chart.series[0].marker.size = 10
                    chart.series[1].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[1].marker.size = 10
                    chart.series[2].graphicalProperties.line.width = 50000  # for UTRA_-1
                    chart.series[3].graphicalProperties.line.width = 50000  # for UTRA_+1
                    chart.series[4].graphicalProperties.line.dashStyle = 'dash'  # for UTRA_-2
                    chart.series[5].graphicalProperties.line.dashStyle = 'dash'  # for UTRA_+2

                    ws.add_chart(chart, "AA39")

                    logger.info('----------EVM---------')
                    chart = LineChart()
                    chart.title = 'EVM'
                    chart.y_axis.title = 'EVM(%)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=12, min_row=1, max_col=12, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "AA77")

                    logger.info('----------Current---------')
                    chart = LineChart()
                    chart.title = 'Current'
                    chart.y_axis.title = 'Current(mA)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=23, min_row=1, max_col=23, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "AA115")

                wb.save(file_path)
                wb.close()
            else:
                for ws_name in wb.sheetnames:
                    logger.info(f'========={ws_name}==========')
                    ws = wb[ws_name]

                    if ws._charts != []:  # if there is charts, delete it
                        ws._charts.clear()

                    logger.info('----------Power---------')
                    chart = LineChart()
                    chart.title = 'Power'
                    chart.y_axis.title = 'Power(dBm)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=4, min_row=1, max_col=4, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "X1")

                    logger.info('----------ACLR---------')
                    chart = LineChart()
                    chart.title = 'ACLR'
                    chart.y_axis.title = 'ACLR(dB)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'
                    chart.y_axis.scaling.min = -60
                    chart.y_axis.scaling.max = -20

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=5, min_row=1, max_col=10, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'triangle'  # for EUTRA_-1
                    chart.series[0].marker.size = 10
                    chart.series[1].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[1].marker.size = 10
                    chart.series[2].graphicalProperties.line.width = 50000  # for UTRA_-1
                    chart.series[3].graphicalProperties.line.width = 50000  # for UTRA_+1
                    chart.series[4].graphicalProperties.line.dashStyle = 'dash'  # for UTRA_-2
                    chart.series[5].graphicalProperties.line.dashStyle = 'dash'  # for UTRA_+2

                    ws.add_chart(chart, "X39")

                    logger.info('----------EVM---------')
                    chart = LineChart()
                    chart.title = 'EVM'
                    chart.y_axis.title = 'EVM(%)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=11, min_row=1, max_col=11, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "X77")

                    logger.info('----------Current---------')
                    chart = LineChart()
                    chart.title = 'Current'
                    chart.y_axis.title = 'Current(mA)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=22, min_row=1, max_col=22, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "X115")
                wb.save(file_path)
                wb.close()
        elif tech == 'WCDMA':
            if mode == 1:  # for LMH use
                for ws_name in wb.sheetnames:
                    logger.info(f'========={ws_name}==========')
                    ws = wb[ws_name]

                    if ws._charts != []:  # if there is charts, delete it
                        ws._charts.clear()

                    logger.info('----------Power---------')
                    chart = LineChart()
                    chart.title = 'Power'
                    chart.y_axis.title = 'Power(dBm)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=6, min_row=1, max_col=6, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "U1")

                    logger.info('----------ACLR---------')
                    chart = LineChart()
                    chart.title = 'ACLR'
                    chart.y_axis.title = 'ACLR(dB)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'
                    chart.y_axis.scaling.min = -60
                    chart.y_axis.scaling.max = -20

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=7, min_row=1, max_col=10, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'triangle'  # for UTRA_-1
                    chart.series[0].marker.size = 10
                    chart.series[1].marker.symbol = 'circle'  # for UTRA_+1
                    chart.series[1].marker.size = 10
                    chart.series[2].graphicalProperties.line.width = 50000  # for UTRA_-2
                    chart.series[3].graphicalProperties.line.width = 50000  # for UTRA_+2

                    ws.add_chart(chart, "U39")

                    logger.info('----------EVM---------')
                    chart = LineChart()
                    chart.title = 'EVM'
                    chart.y_axis.title = 'EVM(%)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=12, min_row=1, max_col=12, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "U77")

                    logger.info('----------Current---------')
                    chart = LineChart()
                    chart.title = 'Current'
                    chart.y_axis.title = 'Current(mA)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=17, min_row=1, max_col=17, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "U115")

                wb.save(file_path)
                wb.close()
            else:  # for non LMH such as sweep
                for ws_name in wb.sheetnames:
                    logger.info(f'========={ws_name}==========')
                    ws = wb[ws_name]

                    if ws._charts != []:  # if there is charts, delete it
                        ws._charts.clear()

                    logger.info('----------Power---------')
                    chart = LineChart()
                    chart.title = 'Power'
                    chart.y_axis.title = 'Power(dBm)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=5, min_row=1, max_col=5, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "S1")

                    logger.info('----------ACLR---------')
                    chart = LineChart()
                    chart.title = 'ACLR'
                    chart.y_axis.title = 'ACLR(dB)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'
                    chart.y_axis.scaling.min = -60
                    chart.y_axis.scaling.max = -20

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=6, min_row=1, max_col=9, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'triangle'  # for UTRA_-1
                    chart.series[0].marker.size = 10
                    chart.series[1].marker.symbol = 'circle'  # for UTRA_+1
                    chart.series[1].marker.size = 10
                    chart.series[2].graphicalProperties.line.width = 50000  # for UTRA_-2
                    chart.series[3].graphicalProperties.line.width = 50000  # for UTRA_+2

                    ws.add_chart(chart, "S39")

                    logger.info('----------EVM---------')
                    chart = LineChart()
                    chart.title = 'EVM'
                    chart.y_axis.title = 'EVM(%)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=11, min_row=1, max_col=11, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "S77")

                    logger.info('----------Current---------')
                    chart = LineChart()
                    chart.title = 'Current'
                    chart.y_axis.title = 'Current(mA)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=16, min_row=1, max_col=16, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "S115")

                wb.save(file_path)
                wb.close()
        elif tech == 'GSM':
            if mode == 1:
                for ws_name in wb.sheetnames:
                    logger.info(f'========={ws_name}==========')
                    ws = wb[ws_name]

                    if ws._charts != []:  # if there is charts, delete it
                        ws._charts.clear()

                    logger.info('----------Power---------')
                    chart = LineChart()
                    chart.title = 'Power'
                    chart.y_axis.title = 'Power(dBm)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=6, min_row=1, max_col=6, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "AA1")

                    logger.info('----------ORFS_MOD---------')
                    chart = LineChart()
                    chart.title = 'ORFS_MOD'
                    chart.y_axis.title = 'ORFS_MOD(dB)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'
                    chart.y_axis.scaling.min = -80
                    chart.y_axis.scaling.max = -20

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=10, min_row=1, max_col=15, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[2].marker.symbol = 'triangle'  # for ORFS_-400
                    chart.series[2].marker.size = 10
                    chart.series[3].marker.symbol = 'circle'  # for ORFS_+400
                    chart.series[3].marker.size = 10
                    chart.series[0].graphicalProperties.line.width = 50000  # for ORFS_-200
                    chart.series[1].graphicalProperties.line.width = 50000  # for ORFS_+200
                    chart.series[4].graphicalProperties.line.dashStyle = 'dash'  # for ORFS_-600
                    chart.series[5].graphicalProperties.line.dashStyle = 'dash'  # for ORFS_+600

                    ws.add_chart(chart, "AA39")

                    logger.info('----------ORFS_SW---------')
                    chart = LineChart()
                    chart.title = 'ORFS_SW'
                    chart.y_axis.title = 'ORFS_SW(dBm)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'
                    chart.y_axis.scaling.min = -80
                    chart.y_axis.scaling.max = -20

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=16, min_row=1, max_col=21, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[2].marker.symbol = 'triangle'  # for ORFS_-400
                    chart.series[2].marker.size = 10
                    chart.series[3].marker.symbol = 'circle'  # for ORFS_+400
                    chart.series[3].marker.size = 10
                    chart.series[0].graphicalProperties.line.width = 50000  # for ORFS_-600
                    chart.series[1].graphicalProperties.line.width = 50000  # for ORFS_+600
                    chart.series[4].graphicalProperties.line.dashStyle = 'dash'  # for ORFS_-1200
                    chart.series[5].graphicalProperties.line.dashStyle = 'dash'  # for ORFS_+1200

                    ws.add_chart(chart, "AA77")

                    if 'GMSK' in ws_name:
                        logger.info('----------PHASE_RMS---------')
                        chart = LineChart()
                        chart.title = 'PHASE'
                        chart.y_axis.title = 'PHASE(degree)'
                        chart.x_axis.title = 'Band'
                        chart.x_axis.tickLblPos = 'low'

                        chart.height = 20
                        chart.width = 32

                        y_data = Reference(ws, min_col=7, min_row=1, max_col=7, max_row=ws.max_row)
                        x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                        chart.add_data(y_data, titles_from_data=True)
                        chart.set_categories(x_data)

                        chart.series[0].marker.symbol = 'circle'
                        chart.series[0].marker.size = 10

                        ws.add_chart(chart, "AA115")

                    elif 'EPSK' in ws_name:
                        logger.info('----------EVM_RMS---------')
                        chart = LineChart()
                        chart.title = 'EVM'
                        chart.y_axis.title = 'EVM(%)'
                        chart.x_axis.title = 'Band'
                        chart.x_axis.tickLblPos = 'low'

                        chart.height = 20
                        chart.width = 32

                        y_data = Reference(ws, min_col=8, min_row=1, max_col=8, max_row=ws.max_row)
                        x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                        chart.add_data(y_data, titles_from_data=True)
                        chart.set_categories(x_data)

                        chart.series[0].marker.symbol = 'circle'
                        chart.series[0].marker.size = 10

                        ws.add_chart(chart, "AA115")

                    logger.info('----------Current---------')
                    chart = LineChart()
                    chart.title = 'Current'
                    chart.y_axis.title = 'Current(mA)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=23, min_row=1, max_col=23, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "AA153")

                wb.save(file_path)
                wb.close()
            else:  # mode = 0
                for ws_name in wb.sheetnames:
                    ws = wb[ws_name]

                    if ws._charts != []:  # if there is charts, delete it
                        ws._charts.clear()

                    logger.info('----------Power---------')
                    chart = LineChart()
                    chart.title = 'Power'
                    chart.y_axis.title = 'Power(dBm)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=5, min_row=1, max_col=5, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "X1")

                    logger.info('----------ORFS_MOD---------')
                    chart = LineChart()
                    chart.title = 'ORFS_MOD'
                    chart.y_axis.title = 'ORFS_MOD(dB)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'
                    chart.y_axis.scaling.min = -80
                    chart.y_axis.scaling.max = -20

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=9, min_row=1, max_col=14, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[2].marker.symbol = 'triangle'  # for ORFS_-400
                    chart.series[2].marker.size = 10
                    chart.series[3].marker.symbol = 'circle'  # for ORFS_+400
                    chart.series[3].marker.size = 10
                    chart.series[0].graphicalProperties.line.width = 50000  # for ORFS_-200
                    chart.series[1].graphicalProperties.line.width = 50000  # for ORFS_+200
                    chart.series[4].graphicalProperties.line.dashStyle = 'dash'  # for ORFS_-600
                    chart.series[5].graphicalProperties.line.dashStyle = 'dash'  # for ORFS_+600

                    ws.add_chart(chart, "X39")

                    logger.info('----------ORFS_SW---------')
                    chart = LineChart()
                    chart.title = 'ORFS_SW'
                    chart.y_axis.title = 'ORFS_SW(dBm)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'
                    chart.y_axis.scaling.min = -80
                    chart.y_axis.scaling.max = -20

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=15, min_row=1, max_col=20, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[2].marker.symbol = 'triangle'  # for ORFS_-400
                    chart.series[2].marker.size = 10
                    chart.series[3].marker.symbol = 'circle'  # for ORFS_+400
                    chart.series[3].marker.size = 10
                    chart.series[0].graphicalProperties.line.width = 50000  # for ORFS_-600
                    chart.series[1].graphicalProperties.line.width = 50000  # for ORFS_+600
                    chart.series[4].graphicalProperties.line.dashStyle = 'dash'  # for ORFS_-1200
                    chart.series[5].graphicalProperties.line.dashStyle = 'dash'  # for ORFS_+1200

                    ws.add_chart(chart, "X77")

                    if 'GMSK' in ws_name:
                        logger.info('----------PHASE_RMS---------')
                        chart = LineChart()
                        chart.title = 'PHASE'
                        chart.y_axis.title = 'PHASE(degree)'
                        chart.x_axis.title = 'Band'
                        chart.x_axis.tickLblPos = 'low'

                        chart.height = 20
                        chart.width = 32

                        y_data = Reference(ws, min_col=6, min_row=1, max_col=6, max_row=ws.max_row)
                        x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                        chart.add_data(y_data, titles_from_data=True)
                        chart.set_categories(x_data)

                        chart.series[0].marker.symbol = 'circle'
                        chart.series[0].marker.size = 10

                        ws.add_chart(chart, "X115")

                    elif 'EPSK' in ws_name:
                        logger.info('----------EVM_RMS---------')
                        chart = LineChart()
                        chart.title = 'EVM'
                        chart.y_axis.title = 'EVM(%)'
                        chart.x_axis.title = 'Band'
                        chart.x_axis.tickLblPos = 'low'

                        chart.height = 20
                        chart.width = 32

                        y_data = Reference(ws, min_col=7, min_row=1, max_col=7, max_row=ws.max_row)
                        x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                        chart.add_data(y_data, titles_from_data=True)
                        chart.set_categories(x_data)

                        chart.series[0].marker.symbol = 'circle'
                        chart.series[0].marker.size = 10

                        ws.add_chart(chart, "X115")

                    logger.info('----------Current---------')
                    chart = LineChart()
                    chart.title = 'Current'
                    chart.y_axis.title = 'Current(mA)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=22, min_row=1, max_col=22, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws.add_chart(chart, "X153")

                wb.save(file_path)
                wb.close()


def rxs_relative_plot(file_path, parameters_dict):
    logger.info('----------Plot Chart---------')
    # tech ='LTE'
    # mcs_lte = 'QPSK'
    script = parameters_dict['script']
    tech = parameters_dict['tech']
    mcs = parameters_dict['mcs']

    wb = openpyxl.load_workbook(file_path)
    if script == 'GENERAL':
        if tech == 'LTE':
            ws_dashboard = wb[f'dashboard']
            ws_desens = wb[f'Desens_{mcs}']
            ws_txmax = wb[f'Raw_Data_{mcs}_TxMax']
            ws_txmin = wb[f'Raw_Data_{mcs}_-10dBm']

            if ws_dashboard._charts:  # if there is charts, delete it
                ws_dashboard._charts.clear()

            chart1 = LineChart()
            chart1.title = 'Sensitivity'
            chart1.y_axis.title = 'Rx_Level(dBm)'
            chart1.x_axis.title = 'Band'
            chart1.x_axis.tickLblPos = 'low'
            chart1.height = 20
            chart1.width = 32
            y_data_txmax = Reference(ws_txmax, min_col=7, min_row=2, max_col=7, max_row=ws_txmax.max_row)
            y_data_txmin = Reference(ws_txmin, min_col=7, min_row=2, max_col=7, max_row=ws_txmin.max_row)
            y_data_desens = Reference(ws_desens, min_col=4, min_row=1, max_col=4, max_row=ws_desens.max_row)
            x_data = Reference(ws_desens, min_col=1, min_row=2, max_col=3, max_row=ws_desens.max_row)

            series_txmax = Series(y_data_txmax, title="Tx_Max")
            series_txmin = Series(y_data_txmin, title="Tx_-10dBm")

            chart1.append(series_txmax)
            chart1.append(series_txmin)
            chart1.set_categories(x_data)
            chart1.y_axis.majorGridlines = None

            chart2 = BarChart()
            chart2.add_data(y_data_desens, titles_from_data=True)
            chart2.y_axis.axId = 200
            chart2.y_axis.title = 'Diff(dB)'

            chart1.y_axis.crosses = "max"
            chart1 += chart2
            # save at dashboard sheet
            ws_dashboard.add_chart(chart1, "A1")

            wb.save(file_path)
            wb.close()

        elif tech == 'FR1':
            ws_dashboard = wb[f'dashboard']
            ws_desens = wb[f'Desens_{mcs}']
            ws_txmax = wb[f'Raw_Data_{mcs}_TxMax']
            ws_txmin = wb[f'Raw_Data_{mcs}_-10dBm']

            if ws_dashboard._charts:  # if there is charts, delete it
                ws_dashboard._charts.clear()

            chart1 = LineChart()
            chart1.title = 'Sensitivity'
            chart1.y_axis.title = 'Rx_Level(dBm)'
            chart1.x_axis.title = 'Band'
            chart1.x_axis.tickLblPos = 'low'
            chart1.height = 20
            chart1.width = 32
            y_data_txmax = Reference(ws_txmax, min_col=7, min_row=2, max_col=7, max_row=ws_txmax.max_row)
            y_data_txmin = Reference(ws_txmin, min_col=7, min_row=2, max_col=7, max_row=ws_txmin.max_row)
            y_data_desens = Reference(ws_desens, min_col=4, min_row=1, max_col=4, max_row=ws_desens.max_row)
            x_data = Reference(ws_desens, min_col=1, min_row=2, max_col=3, max_row=ws_desens.max_row)

            series_txmax = Series(y_data_txmax, title="Tx_Max")
            series_txmin = Series(y_data_txmin, title="Tx_-10dBm")

            chart1.append(series_txmax)
            chart1.append(series_txmin)
            chart1.set_categories(x_data)
            chart1.y_axis.majorGridlines = None

            chart2 = BarChart()
            chart2.add_data(y_data_desens, titles_from_data=True)
            chart2.y_axis.axId = 200
            chart2.y_axis.title = 'Diff(dB)'

            chart1.y_axis.crosses = "max"
            chart1 += chart2
            # save at dashboard sheet
            ws_dashboard.add_chart(chart1, "A1")

            wb.save(file_path)
            wb.close()

        elif tech == 'WCDMA':
            ws_dashboard = wb[f'dashboard']
            ws = wb[f'Raw_Data']

            if ws_dashboard._charts:  # if there is charts, delete it
                ws_dashboard._charts.clear()

            chart1 = LineChart()
            chart1.title = 'Sensitivity'
            chart1.y_axis.title = 'Rx_Level(dBm)'
            chart1.x_axis.title = 'Band'
            chart1.x_axis.tickLblPos = 'low'
            chart1.height = 20
            chart1.width = 32
            y_data = Reference(ws, min_col=6, min_row=2, max_col=6, max_row=ws.max_row)
            x_data = Reference(ws, min_col=1, min_row=2, max_col=3, max_row=ws.max_row)
            # save at dashboard sheet
            series_pure_sens = Series(y_data, title="Pure_Sensititvity_FTM")

            chart1.append(series_pure_sens)
            chart1.set_categories(x_data)

            ws_dashboard.add_chart(chart1, "A1")

            wb.save(file_path)
            wb.close()

        elif tech == 'GSM':
            ws_dashboard = wb[f'dashboard']
            ws = wb[f'Raw_Data']

            if ws_dashboard._charts:  # if there is charts, delete it
                ws_dashboard._charts.clear()

            chart1 = LineChart()
            chart1.title = 'Sensitivity'
            chart1.y_axis.title = 'Rx_Level(dBm)'
            chart1.x_axis.title = 'Band'
            chart1.x_axis.tickLblPos = 'low'
            chart1.height = 20
            chart1.width = 32
            y_data = Reference(ws, min_col=6, min_row=1, max_col=7, max_row=ws.max_row)
            x_data = Reference(ws, min_col=1, min_row=2, max_col=3, max_row=ws.max_row)

            chart1.add_data(y_data, titles_from_data=True)

            chart1.set_categories(x_data)
            # save at dashboard sheet
            ws_dashboard.add_chart(chart1, "A1")

            wb.save(file_path)
            wb.close()


def rxs_endc_plot(file_path):
    logger.info('----------Plot Chart---------')
    wb = openpyxl.load_workbook(file_path)
    ws_dashboard = wb[f'dashboard']
    ws_desens = wb[f'Desens_ENDC']
    ws_txmax = wb[f'Raw_Data_ENDC_FR1_TxMax']
    ws_txmin = wb[f'Raw_Data_ENDC_FR1_-10dBm']

    if ws_dashboard._charts:  # if there is charts, delete it
        ws_dashboard._charts.clear()

    chart1 = LineChart()
    chart1.title = 'Sensitivity'
    chart1.y_axis.title = 'Rx_Level(dBm)'
    chart1.x_axis.title = 'Band'
    chart1.x_axis.tickLblPos = 'low'
    chart1.height = 20
    chart1.width = 32
    y_data_txmax = Reference(ws_txmax, min_col=5, min_row=2, max_col=5, max_row=ws_txmax.max_row)
    y_data_txmin = Reference(ws_txmin, min_col=5, min_row=2, max_col=5, max_row=ws_txmin.max_row)
    y_data_desens = Reference(ws_desens, min_col=7, min_row=1, max_col=7, max_row=ws_desens.max_row)
    x_data = Reference(ws_desens, min_col=1, min_row=2, max_col=6, max_row=ws_desens.max_row)

    series_txmax = Series(y_data_txmax, title="Tx_Max")
    series_txmin = Series(y_data_txmin, title="Tx_-10dBm")

    chart1.append(series_txmax)
    chart1.append(series_txmin)
    chart1.set_categories(x_data)
    chart1.y_axis.majorGridlines = None

    chart2 = BarChart()
    chart2.add_data(y_data_desens, titles_from_data=True)
    chart2.y_axis.axId = 200
    chart2.y_axis.title = 'Diff(dB)'

    chart1.y_axis.crosses = "max"
    chart1 += chart2

    ws_dashboard.add_chart(chart1, "A1")

    wb.save(file_path)
    wb.close()


def rx_desense_process(file_path, mcs):
    """
    cell column: Band	| Rx_Path | Chan | Diff | TX_Path
    """
    wb = openpyxl.load_workbook(file_path)
    ws_txmax = wb[f'Raw_Data_{mcs}_TxMax']
    ws_txmin = wb[f'Raw_Data_{mcs}_-10dBm']
    ws_desens = wb[f'Desens_{mcs}']
    for row in range(2, ws_txmax.max_row + 1):
        ws_desens.cell(row, 1).value = ws_txmax.cell(row, 1).value
        ws_desens.cell(row, 2).value = ws_txmax.cell(row, 2).value
        ws_desens.cell(row, 3).value = ws_txmax.cell(row, 3).value
        ws_desens.cell(row, 4).value = ws_txmax.cell(row, 7).value - ws_txmin.cell(row, 7).value
        ws_desens.cell(row, 5).value = ws_txmax.cell(row, 20).value

    wb.save(file_path)
    wb.close()


def rx_desense_endc_process(file_path):
    wb = openpyxl.load_workbook(file_path)
    ws_txmax = wb[f'Raw_Data_ENDC_FR1_TxMax']
    ws_txmin = wb[f'Raw_Data_ENDC_FR1_-10dBm']
    ws_desens = wb[f'Desens_ENDC']
    for row in range(2, ws_txmax.max_row + 1):
        ws_desens.cell(row, 1).value = ws_txmax.cell(row, 1).value
        ws_desens.cell(row, 2).value = ws_txmax.cell(row, 2).value
        ws_desens.cell(row, 3).value = ws_txmax.cell(row, 6).value
        ws_desens.cell(row, 4).value = ws_txmax.cell(row, 7).value
        ws_desens.cell(row, 5).value = ws_txmax.cell(row, 8).value
        ws_desens.cell(row, 6).value = ws_txmax.cell(row, 9).value
        ws_desens.cell(row, 7).value = ws_txmax.cell(row, 5).value - ws_txmin.cell(row, 5).value

    wb.save(file_path)
    wb.close()
