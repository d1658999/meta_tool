import openpyxl
from openpyxl.chart import LineChart, Reference, BarChart, Series
from pathlib import Path

from utils.log_init import log_set
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
import utils.parameters.common_parameters_anritsu as cm_pmt_anritsu
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


def select_file_name_genre_tx(bw, tech, test_item='lmh'):
    """
    select:
        level_sweep
        lmh
        freq_sweep
        1rb_sweep
    """
    if test_item == 'level_sweep':
        return f'Tx_level_sweep_{bw}MHZ_{tech}.xlsx'
    elif test_item == 'lmh':
        return f'Tx_Pwr_ACLR_EVM_{bw}MHZ_{tech}_LMH.xlsx'
    elif test_item == 'freq_sweep':
        return f'Tx_freq_sweep_{bw}MHZ_{tech}.xlsx'
    elif test_item == '1rb_sweep':
        return f'Tx_1RB_sweep_{bw}MHZ_{tech}.xlsx'


def excel_folder_create():
    file_dir = excel_folder_path()
    file_dir.mkdir(parents=True, exist_ok=True)
    logger.info('----------folder create ----------')
    logger.info(file_dir)


def excel_folder_path():
    return Path('output') / Path(ext_pmt.devices_serial)


def tx_power_fcc_ce_export_excel_ftm(data, parameters_dict):
    script = parameters_dict['script']
    tech = parameters_dict['tech']
    band = parameters_dict['band']
    bw = parameters_dict['bw']
    rb_size = parameters_dict['rb_size']
    rb_start = parameters_dict['rb_start']
    tx_level = parameters_dict['tx_level']
    mcs = parameters_dict['mcs']
    tx_path = parameters_dict['tx_path']
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


def tx_power_relative_test_export_excel_ftm(data, parameters_dict):
    """
    data is dict like:
    tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET]
    """
    script = parameters_dict['script']
    tech = parameters_dict['tech']
    band = parameters_dict['band']
    bw = parameters_dict['bw']
    tx_freq_level = parameters_dict['tx_freq_level']
    mcs = parameters_dict['mcs']
    tx_path = parameters_dict['tx_path']
    mod = parameters_dict['mod']
    rb_state = parameters_dict['rb_state']
    rb_size = parameters_dict['rb_size']
    rb_start = parameters_dict['rb_start']
    sync_path = parameters_dict['sync_path']
    asw_srs_path = parameters_dict['asw_srs_path']
    scs = parameters_dict['scs']
    type_ = parameters_dict['type']
    test_item = parameters_dict['test_item']
    logger.info('----------save to excel----------')
    filename = None
    if script == 'GENERAL':
        if tx_freq_level >= 100:
            filename = select_file_name_genre_tx(bw, tech, test_item)
        elif tx_freq_level <= 100:
            filename = select_file_name_genre_tx(bw, tech, test_item)

        file_path = Path(excel_folder_path()) / Path(filename)

        if Path(file_path).exists() is False:
            logger.info('----------file does not exist----------')
            wb = openpyxl.Workbook()
            wb.remove(wb['Sheet'])
            # to create sheet
            if tech == 'LTE':
                # create dashboard
                for _ in ['QPSK', 'Q16', 'Q64', 'Q256']:  # some cmw100 might not have licesnse of Q256
                    wb.create_sheet(f'Dashboard_{_}')
                    # wb.create_sheet(f'Dashboard_{_}_PRB')
                    # wb.create_sheet(f'Dashboard_{_}_FRB')

                # create the Raw data sheets
                for _ in ['QPSK', 'Q16', 'Q64', 'Q256']:  # some cmw100 might not have licesnse of Q256
                    wb.create_sheet(f'Raw_Data_{_}')
                    # wb.create_sheet(f'Raw_Data_{_}_PRB')
                    # wb.create_sheet(f'Raw_Data_{_}_FRB')

                # create the title for every sheets
                for sheetname in wb.sheetnames:
                    if 'Raw_Data' in sheetname:
                        ws = wb[sheetname]
                        ws['A1'] = 'Band'
                        ws['B1'] = 'BW'
                        ws['C1'] = 'Tx_Freq'
                        ws['D1'] = 'Chan'
                        ws['E1'] = 'Tx_level'
                        ws['F1'] = 'Measured_Power'
                        ws['G1'] = 'E_-1'
                        ws['H1'] = 'E_+1'
                        ws['I1'] = 'U_-1'
                        ws['J1'] = 'U_+1'
                        ws['K1'] = 'U_-2'
                        ws['L1'] = 'U_+2'
                        ws['M1'] = 'EVM'
                        ws['N1'] = 'Freq_Err'
                        ws['O1'] = 'IQ_OFFSET'
                        ws['P1'] = 'RB_num'
                        ws['Q1'] = 'RB_start'
                        ws['R1'] = 'MCS'
                        ws['S1'] = 'Tx_Path'
                        ws['T1'] = 'RB_STATE'
                        ws['U1'] = 'Sync_Path'
                        ws['V1'] = 'AS_Path'
                        ws['W1'] = 'Current(mA)'
                        ws['X1'] = 'Condition'
                        ws['Y1'] = 'Temp0'
                        ws['Z1'] = 'Temp1'
                    else:  # to pass the dashboard
                        pass

            elif tech == 'FR1':
                # create dashboard
                for _ in ['QPSK', 'Q16', 'Q64', 'Q256', 'BPSK']:  # some cmw100 might not have licesnse of Q256
                    wb.create_sheet(f'Dashboard_{_}')

                # create the Raw data sheets
                for _ in ['QPSK', 'Q16', 'Q64', 'Q256', 'BPSK']:  # some cmw100 might not have licesnse of Q256
                    wb.create_sheet(f'Raw_Data_{_}')

                # create the title for every sheets
                for sheetname in wb.sheetnames:
                    if 'Raw_Data' in sheetname:
                        ws = wb[sheetname]
                        ws['A1'] = 'Band'
                        ws['B1'] = 'BW'
                        ws['C1'] = 'Tx_Freq'
                        ws['D1'] = 'Chan'
                        ws['E1'] = 'Tx_level'
                        ws['F1'] = 'Measured_Power'
                        ws['G1'] = 'E_-1'
                        ws['H1'] = 'E_+1'
                        ws['I1'] = 'U_-1'
                        ws['J1'] = 'U_+1'
                        ws['K1'] = 'U_-2'
                        ws['L1'] = 'U_+2'
                        ws['M1'] = 'EVM'
                        ws['N1'] = 'Freq_Err'
                        ws['O1'] = 'IQ_OFFSET'
                        ws['P1'] = 'RB_num'
                        ws['Q1'] = 'RB_start'
                        ws['R1'] = 'Type'
                        ws['S1'] = 'Tx_Path'
                        ws['T1'] = 'SCS(KHz)'
                        ws['U1'] = 'RB_STATE'
                        ws['V1'] = 'Sync_Path'
                        ws['W1'] = 'AS_SRS_Path'
                        ws['X1'] = 'Current(mA)'
                        ws['Y1'] = 'Condition'
                        ws['Z1'] = 'Temp0'
                        ws['AA1'] = 'Temp1'
                    else:  # to pass the dashboard
                        pass

            elif tech == 'WCDMA':
                # create dashboard
                wb.create_sheet(f'Dashboard')

                # create the Raw data sheets
                wb.create_sheet(f'Raw_Data')

                # create the title for every sheets
                for sheetname in wb.sheetnames:
                    if 'Raw_Data' in sheetname:
                        ws = wb[sheetname]
                        ws['A1'] = 'Band'
                        ws['B1'] = 'Channel'
                        ws['C1'] = 'Chan'
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
                    else:  # to pass the dashboard
                        pass

            elif tech == 'GSM':
                # create dashboard
                wb.create_sheet(f'Dashboard_GMSK')
                wb.create_sheet(f'Dashboard_EPSK')

                # create the Raw data sheets
                wb.create_sheet(f'Raw_Data_GMSK')
                wb.create_sheet(f'Raw_Data_EPSK')

                # creat the title for every sheets
                for sheetname in wb.sheetnames:
                    if 'Raw_Data' in sheetname:
                        ws = wb[sheetname]
                        ws['A1'] = 'Band'
                        ws['B1'] = 'Channel'
                        ws['C1'] = 'Chan'
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
                    else:  # to pass the dashboard
                        pass

            # save and close file
            wb.save(file_path)
            wb.close()

        logger.info('----------file exist----------')
        wb = openpyxl.load_workbook(file_path)
        ws = None
        if tech == 'LTE':
            ws = wb[f'Raw_Data_{mcs}']
        elif tech == 'FR1':
            ws = wb[f'Raw_Data_{mcs}']
        elif tech == 'WCDMA':
            ws = wb[f'Raw_Data']
        elif tech == 'GSM':
            ws = wb[f'Raw_Data_{mod}']

        if tech == 'LTE':
            max_row = ws.max_row
            row = max_row + 1
            if tx_freq_level >= 100:  # level_sweep
                for tx_level, measured_data in data.items():
                    chan = chan_judge_lte(band, bw, tx_freq_level)
                    ws.cell(row, 1).value = band
                    ws.cell(row, 2).value = bw
                    ws.cell(row, 3).value = tx_freq_level  # this freq_lte
                    ws.cell(row, 4).value = chan  # LMH
                    ws.cell(row, 5).value = tx_level
                    ws.cell(row, 6).value = measured_data[3]
                    ws.cell(row, 7).value = measured_data[2]
                    ws.cell(row, 8).value = measured_data[4]
                    ws.cell(row, 9).value = measured_data[1]
                    ws.cell(row, 10).value = measured_data[5]
                    ws.cell(row, 11).value = measured_data[0]
                    ws.cell(row, 12).value = measured_data[6]
                    ws.cell(row, 13).value = measured_data[7]
                    ws.cell(row, 14).value = measured_data[8]
                    ws.cell(row, 15).value = measured_data[9]
                    ws.cell(row, 16).value = rb_size
                    ws.cell(row, 17).value = rb_start
                    ws.cell(row, 18).value = mcs
                    ws.cell(row, 19).value = tx_path
                    ws.cell(row, 20).value = rb_state
                    ws.cell(row, 21).value = sync_path
                    ws.cell(row, 22).value = asw_srs_path
                    ws.cell(row, 23).value = measured_data[10]
                    ws.cell(row, 24).value = ext_pmt.condition
                    row += 1

            elif tx_freq_level <= 100:  # 1rb_sweep, lmh, freq_sweep
                for tx_freq, measured_data in data.items():
                    chan = chan_judge_lte(band, bw, tx_freq) if test_item != 'freq_sweep' else None
                    ws.cell(row, 1).value = band
                    ws.cell(row, 2).value = bw
                    ws.cell(row, 3).value = tx_freq
                    ws.cell(row, 4).value = chan  # LMH
                    ws.cell(row, 5).value = tx_freq_level  # this tx_level
                    ws.cell(row, 6).value = measured_data[3]
                    ws.cell(row, 7).value = measured_data[2]
                    ws.cell(row, 8).value = measured_data[4]
                    ws.cell(row, 9).value = measured_data[1]
                    ws.cell(row, 10).value = measured_data[5]
                    ws.cell(row, 11).value = measured_data[0]
                    ws.cell(row, 12).value = measured_data[6]
                    ws.cell(row, 13).value = measured_data[7]
                    ws.cell(row, 14).value = measured_data[8]
                    ws.cell(row, 15).value = measured_data[9]
                    ws.cell(row, 16).value = rb_size
                    ws.cell(row, 17).value = rb_start
                    ws.cell(row, 18).value = mcs
                    ws.cell(row, 19).value = tx_path
                    ws.cell(row, 20).value = rb_state
                    ws.cell(row, 21).value = sync_path
                    ws.cell(row, 22).value = asw_srs_path
                    ws.cell(row, 23).value = measured_data[10] if test_item == 'lmh' else None
                    ws.cell(row, 24).value = ext_pmt.condition if test_item == 'lmh' else None
                    ws.cell(row, 25).value = measured_data[11] if test_item == 'lmh' else None
                    ws.cell(row, 26).value = measured_data[12] if test_item == 'lmh' else None
                    row += 1

        elif tech == 'FR1':
            max_row = ws.max_row
            row = max_row + 1
            if tx_freq_level >= 100:  # level_sweep
                for tx_level, measured_data in data.items():
                    chan = chan_judge_fr1(band, bw, tx_freq_level)
                    ws.cell(row, 1).value = band
                    ws.cell(row, 2).value = bw
                    ws.cell(row, 3).value = tx_freq_level  # this freq_fr1
                    ws.cell(row, 4).value = chan  # LMH
                    ws.cell(row, 5).value = tx_level
                    ws.cell(row, 6).value = measured_data[3]
                    ws.cell(row, 7).value = measured_data[2]
                    ws.cell(row, 8).value = measured_data[4]
                    ws.cell(row, 9).value = measured_data[1]
                    ws.cell(row, 10).value = measured_data[5]
                    ws.cell(row, 11).value = measured_data[0]
                    ws.cell(row, 12).value = measured_data[6]
                    ws.cell(row, 13).value = measured_data[7]
                    ws.cell(row, 14).value = measured_data[8]
                    ws.cell(row, 15).value = measured_data[9]
                    ws.cell(row, 16).value = rb_size
                    ws.cell(row, 17).value = rb_start
                    ws.cell(row, 18).value = type_
                    ws.cell(row, 19).value = tx_path
                    ws.cell(row, 20).value = scs
                    ws.cell(row, 21).value = rb_state
                    ws.cell(row, 22).value = sync_path
                    ws.cell(row, 23).value = asw_srs_path
                    ws.cell(row, 24).value = measured_data[10]
                    ws.cell(row, 25).value = ext_pmt.condition
                    row += 1

            elif tx_freq_level <= 100:  # 1rb_sweep, lmh, freq_sweep
                for tx_freq, measured_data in data.items():
                    chan = chan_judge_fr1(band, bw, tx_freq) if test_item != 'freq_sweep' else None
                    ws.cell(row, 1).value = band
                    ws.cell(row, 2).value = bw
                    ws.cell(row, 3).value = tx_freq
                    ws.cell(row, 4).value = chan  # LMH
                    ws.cell(row, 5).value = tx_freq_level  # this tx_level
                    ws.cell(row, 6).value = measured_data[3]
                    ws.cell(row, 7).value = measured_data[2]
                    ws.cell(row, 8).value = measured_data[4]
                    ws.cell(row, 9).value = measured_data[1]
                    ws.cell(row, 10).value = measured_data[5]
                    ws.cell(row, 11).value = measured_data[0]
                    ws.cell(row, 12).value = measured_data[6]
                    ws.cell(row, 13).value = measured_data[7]
                    ws.cell(row, 14).value = measured_data[8]
                    ws.cell(row, 15).value = measured_data[9]
                    ws.cell(row, 16).value = rb_size
                    ws.cell(row, 17).value = rb_start
                    ws.cell(row, 18).value = type_
                    ws.cell(row, 19).value = tx_path
                    ws.cell(row, 20).value = scs
                    ws.cell(row, 21).value = rb_state
                    ws.cell(row, 22).value = sync_path
                    ws.cell(row, 23).value = asw_srs_path
                    ws.cell(row, 24).value = measured_data[10] if test_item == 'lmh' else None
                    ws.cell(row, 25).value = ext_pmt.condition if test_item == 'lmh' else None
                    ws.cell(row, 26).value = measured_data[11] if test_item == 'lmh' else None
                    ws.cell(row, 27).value = measured_data[12] if test_item == 'lmh' else None
                    row += 1

        elif tech == 'WCDMA':
            max_row = ws.max_row
            row = max_row + 1
            if tx_freq_level >= 100:  # level_sweep
                for tx_level, measured_data in data.items():
                    chan = chan_judge_wcdma(band, tx_freq_level)
                    ws.cell(row, 1).value = band
                    # this channel
                    ws.cell(row, 2).value = cm_pmt_ftm.trandfer_freq2chan_wcdma(band, tx_freq_level, 'tx')
                    ws.cell(row, 3).value = chan  # LMH
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
                    ws.cell(row, 16).value = asw_srs_path
                    ws.cell(row, 17).value = measured_data[9]
                    ws.cell(row, 18).value = ext_pmt.condition
                    row += 1

            elif tx_freq_level <= 100:  # 1rb_sweep, lmh, freq_sweep
                for tx_freq, measured_data in data.items():
                    chan = chan_judge_wcdma(band, tx_freq) if test_item != 'freq_sweep' else None
                    ws.cell(row, 1).value = band
                    ws.cell(row, 2).value = cm_pmt_ftm.trandfer_freq2chan_wcdma(band, tx_freq, 'tx')  # this channel
                    ws.cell(row, 3).value = chan  # LMH
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
                    ws.cell(row, 16).value = asw_srs_path
                    ws.cell(row, 17).value = measured_data[9] if test_item == 'lmh' else None
                    ws.cell(row, 18).value = ext_pmt.condition if test_item == 'lmh' else None
                    ws.cell(row, 19).value = measured_data[10] if test_item == 'lmh' else None
                    ws.cell(row, 20).value = measured_data[11] if test_item == 'lmh' else None
                    row += 1

        elif tech == 'GSM':
            max_row = ws.max_row
            row = max_row + 1
            if tx_freq_level >= 100:  # level_sweep
                for tx_pcl, measured_data in data.items():
                    chan = chan_judge_gsm(band, tx_freq_level)
                    ws.cell(row, 1).value = band
                    ws.cell(row, 2).value = cm_pmt_ftm.transfer_freq2chan_gsm(band, tx_freq_level)  # channel
                    ws.cell(row, 3).value = chan  # LMH
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
                    ws.cell(row, 22).value = asw_srs_path
                    ws.cell(row, 23).value = measured_data[10]
                    ws.cell(row, 24).value = ext_pmt.condition

                    row += 1

            elif tx_freq_level <= 100:  # 1rb_sweep, lmh, freq_sweep
                for rx_freq, measured_data in data.items():
                    chan = chan_judge_gsm(band, rx_freq) if test_item != 'freq_sweep' else None
                    ws.cell(row, 1).value = band
                    ws.cell(row, 2).value = cm_pmt_ftm.transfer_freq2chan_gsm(band, rx_freq)
                    ws.cell(row, 3).value = chan  # LMH
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
                    ws.cell(row, 22).value = asw_srs_path
                    ws.cell(row, 23).value = measured_data[16] if test_item == 'lmh' else None
                    ws.cell(row, 24).value = ext_pmt.condition if test_item == 'lmh' else None
                    ws.cell(row, 25).value = measured_data[17] if test_item == 'lmh' else None
                    ws.cell(row, 26).value = measured_data[18] if test_item == 'lmh' else None
                    row += 1

        wb.save(file_path)
        wb.close()

        return file_path


def txp_aclr_evm_current_plot_ftm(file_path, parameters_dict):
    script = parameters_dict['script']
    tech = parameters_dict['tech']
    band = parameters_dict['band']
    bw = parameters_dict['bw']
    tx_freq_level = parameters_dict['tx_freq_level']
    mcs = parameters_dict['mcs']
    tx_path = parameters_dict['tx_path']
    mod = parameters_dict['mod']
    rb_state = parameters_dict['rb_state']
    rb_size = parameters_dict['rb_size']
    rb_start = parameters_dict['rb_start']
    sync_path = parameters_dict['sync_path']
    asw_srs_path = parameters_dict['asw_srs_path']
    scs = parameters_dict['scs']
    type_ = parameters_dict['type']
    logger.info('----------Plot Chart---------')
    wb = openpyxl.load_workbook(file_path)
    if script == 'GENERAL':
        if tech == 'LTE':
            for ws_name in wb.sheetnames:
                if 'Raw_Data' in ws_name:
                    logger.info(f'========={ws_name}==========')
                    ws = wb[ws_name]
                    ws_dashboard = wb['Dashboard_' + ws_name[9:]]

                    if ws_dashboard._charts:  # if there is charts, delete it
                        ws_dashboard._charts.clear()

                    logger.info('----------Power---------')
                    chart = LineChart()
                    chart.title = 'Power'
                    chart.y_axis.title = 'Power(dBm)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=6, min_row=1, max_col=6, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=3, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'
                    chart.series[0].marker.size = 10

                    ws_dashboard.add_chart(chart, "A1")

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

                    y_data = Reference(ws, min_col=7, min_row=1, max_col=12, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=3, max_row=ws.max_row)
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

                    ws_dashboard.add_chart(chart, "A41")

                    logger.info('----------EVM---------')
                    chart = LineChart()
                    chart.title = 'EVM'
                    chart.y_axis.title = 'EVM(%)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=13, min_row=1, max_col=13, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=3, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws_dashboard.add_chart(chart, "A81")

                    logger.info('----------Current---------')
                    chart = LineChart()
                    chart.title = 'Current'
                    chart.y_axis.title = 'Current(mA)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=23, min_row=1, max_col=23, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=3, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'
                    chart.series[0].marker.size = 10

                    ws_dashboard.add_chart(chart, "A121")
                else:
                    pass

            wb.save(file_path)
            wb.close()

        elif tech == 'FR1':
            for ws_name in wb.sheetnames:
                if 'Raw_Data' in ws_name:
                    logger.info(f'========={ws_name}==========')
                    ws = wb[ws_name]
                    ws_dashboard = wb['Dashboard_' + ws_name[9:]]

                    if ws_dashboard._charts:  # if there is charts, delete it
                        ws_dashboard._charts.clear()

                    logger.info('----------Power---------')
                    chart = LineChart()
                    chart.title = 'Power'
                    chart.y_axis.title = 'Power(dBm)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=6, min_row=1, max_col=6, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=3, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws_dashboard.add_chart(chart, "A1")

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

                    y_data = Reference(ws, min_col=7, min_row=1, max_col=12, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=3, max_row=ws.max_row)
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

                    ws_dashboard.add_chart(chart, "A41")

                    logger.info('----------EVM---------')
                    chart = LineChart()
                    chart.title = 'EVM'
                    chart.y_axis.title = 'EVM(%)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=13, min_row=1, max_col=13, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=3, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                    chart.series[0].marker.size = 10

                    ws_dashboard.add_chart(chart, "A81")

                    logger.info('----------Current---------')
                    chart = LineChart()
                    chart.title = 'Current'
                    chart.y_axis.title = 'Current(mA)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=24, min_row=1, max_col=24, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=3, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].marker.symbol = 'circle'
                    chart.series[0].marker.size = 10

                    ws_dashboard.add_chart(chart, "A121")

            wb.save(file_path)
            wb.close()

        elif tech == 'WCDMA':
            for ws_name in wb.sheetnames:
                if 'Raw_Data' in ws_name:
                    logger.info(f'========={ws_name}==========')
                    ws = wb[ws_name]
                    ws_dashboard = wb['Dashboard']

                    if ws_dashboard._charts:  # if there is charts, delete it
                        ws_dashboard._charts.clear()

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

                    ws_dashboard.add_chart(chart, "A1")

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

                    ws_dashboard.add_chart(chart, "A41")

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

                    ws_dashboard.add_chart(chart, "A81")

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

                    ws_dashboard.add_chart(chart, "A121")

            wb.save(file_path)
            wb.close()
        elif tech == 'GSM':
            for ws_name in wb.sheetnames:
                if 'Raw_Data' in ws_name:
                    logger.info(f'========={ws_name}==========')
                    ws = wb[ws_name]
                    ws_dashboard = wb['Dashboard_' + ws_name[9:]]

                    if ws_dashboard._charts:  # if there is charts, delete it
                        ws_dashboard._charts.clear()

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

                    ws_dashboard.add_chart(chart, "A1")

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

                    ws_dashboard.add_chart(chart, "A41")

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

                    ws_dashboard.add_chart(chart, "A81")

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

                        ws_dashboard.add_chart(chart, "A115")

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

                        ws_dashboard.add_chart(chart, "A121")

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

                    ws_dashboard.add_chart(chart, "A161")

            wb.save(file_path)
            wb.close()


def rx_power_relative_test_export_excel_ftm(data, parameters_dict):
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
            # create dashboard
            wb.create_sheet(f'Dashboard')

            # to create sheet
            if tech == 'LTE':
                # create the title and sheet for TxManx and -10dBm
                wb.create_sheet(f'Raw_Data_{mcs}_TxMax')
                wb.create_sheet(f'Raw_Data_{mcs}_-10dBm')
                for sheetname in wb.sheetnames:
                    if 'Raw_Data' in sheetname:
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
                    else:
                        pass

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
                    if 'Raw_Data' in sheetname:
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
                    else:
                        pass

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
                ws.cell(row, 5).value = tx_level  # this tx level
                ws.cell(row, 6).value = measured_data[0]  # measured power
                ws.cell(row, 7).value = measured_data[1]  # RX level
                ws.cell(row, 8).value = measured_data[2][0]  # RSRP_RX0
                ws.cell(row, 9).value = measured_data[2][1]  # RSRP_RX1
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
                ws.cell(row, 5).value = tx_level  # this tx level
                ws.cell(row, 6).value = measured_data[0]  # measured power
                ws.cell(row, 7).value = measured_data[1]  # RX level
                ws.cell(row, 8).value = measured_data[2][0]  # RSRP_RX0
                ws.cell(row, 9).value = measured_data[2][1]  # RSRP_RX1
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


def rx_power_endc_test_export_excel_ftm(data):
    """
    :param data:  data = [int(band_lte), int(band_fr1), power_monitor_endc_lte, power_endc_fr1,
    rx_level, bw_lte, bw_fr1, tx_freq_lte, tx_freq_fr1, tx_level_endc_lte,
    tx_level_endc_fr1, rb_size_lte, rb_start_lte, rb_size_fr1, rb_start_fr1]
    :return:
    """
    logger.info('----------save to excel----------')
    filename = f'Sensitivty_ENDC.xlsx'

    file_path = Path(excel_folder_path()) / Path(filename)

    if Path(file_path).exists() is False:
        logger.info('----------file does not exist, so create a new one----------')
        wb = openpyxl.Workbook()
        wb.remove(wb['Sheet'])
        # create dashboard
        wb.create_sheet(f'Dashboard')

        # create the title and sheet for TxManx and -10dBm
        wb.create_sheet(f'Raw_Data_ENDC_FR1_TxMax')
        wb.create_sheet(f'Raw_Data_ENDC_FR1_-10dBm')
        for sheetname in wb.sheetnames:
            if 'Raw_Data' in sheetname:
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
            else:
                pass

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


def rx_desense_process_ftm(file_path, mcs):
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


def rx_desense_endc_process_ftm(file_path):
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


def rxs_relative_plot_ftm(file_path, parameters_dict):
    logger.info('----------Plot Chart---------')
    # tech ='LTE'
    # mcs_lte = 'QPSK'
    script = parameters_dict['script']
    tech = parameters_dict['tech']
    mcs = parameters_dict['mcs']

    wb = openpyxl.load_workbook(file_path)
    if script == 'GENERAL':
        if tech == 'LTE':
            ws_dashboard = wb[f'Dashboard']
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
            ws_dashboard = wb[f'Dashboard']
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
            ws_dashboard = wb[f'Dashboard']
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
            ws_dashboard = wb[f'Dashboard']
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


def rxs_endc_plot_ftm(file_path):
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


# =================== below is for anritsu ===================

def create_sheet_title_rx_freq_sweep(sheet):
    sh = sheet
    sh['A1'] = 'Band'
    sh['B1'] = 'DL_chan'
    sh['C1'] = 'Sensitivity'
    sh['D1'] = 'Tx_power'


def create_excel_rx_freq_sweep(standard, band, power_selected, bw=5):
    wb = openpyxl.Workbook()
    wb.remove(wb['Sheet'])

    if power_selected == 1:
        sheet = f'Band{band}_TxMax'
        wb.create_sheet(sheet)
    else:
        sheet = f'Band{band}_TxMin'
        wb.create_sheet(sheet)

    # create titile for first row
    create_sheet_title_rx_freq_sweep(sheet)

    # save file
    excel_path = f'Rx_Freq_Sweep_{bw}MHZ_{standard}.xlsx' if ext_pmt.condition is None \
        else f'Rx_Freq_Sweep_{bw}MHZ_{standard}_{ext_pmt.condition}.xlsx'
    wb.save(excel_path)
    wb.close()


def create_excel_rx_lmh(standard, bw=5):
    if standard == 'LTE':
        wb = openpyxl.Workbook()
        wb.remove(wb['Sheet'])
        wb.create_sheet('Sensitivity_TxMax')
        wb.create_sheet('Sensitivity_TxMin')
        wb.create_sheet('Desens')
        wb.create_sheet('PWR_TxMax')
        wb.create_sheet('PWR_TxMin')

        for sheet in wb.sheetnames:
            sh = wb[sheet]
            sh['A1'] = 'Band'
            sh['B1'] = 'ch0'
            sh['C1'] = 'ch1'
            sh['D1'] = 'ch2'

        excel_path = f'Sens_sig_{bw}MHZ_{standard}.xlsx' if ext_pmt.condition is None \
            else f'Sens_sig_{bw}MHZ_LTE_{ext_pmt.condition}.xlsx'
        wb.save(excel_path)
        wb.close()


def create_excel_tx_lmh(standard, bw=5, chcoding=None):
    excel_file = None
    if standard == 'LTE':
        excel_file = f'Tx_sig_{bw}MHZ_{standard}.xlsx' if ext_pmt.condition is None \
            else f'Tx_sig_{bw}MHZ_{standard}_{ext_pmt.condition}.xlsx'
    elif standard == 'WCDMA' and chcoding == 'REFMEASCH':  # WCDMA
        excel_file = f'Tx_sig_WCDMA.xlsx' if ext_pmt.condition is None else f'Tx_sig_WCDMA_{ext_pmt.condition}.xlsx'
    elif standard == 'WCDMA' and chcoding == 'EDCHTEST':  # HSUPA
        excel_file = f'Tx_sig_HSUPA.xlsx' if ext_pmt.condition is None else f'Tx_sig_HSUPA_{ext_pmt.condition}.xlsx'
    elif standard == 'WCDMA' and chcoding == 'FIXREFCH':  # HSDPA
        excel_file = f'Tx_sig_HSDPA.xlsx' if ext_pmt.condition is None else f'Tx_sig_HSDPA_{ext_pmt.condition}.xlsx'

    excel_path = excel_folder_path() / excel_file
    wb = None
    if standard == 'LTE':
        wb = openpyxl.Workbook()
        wb.remove(wb['Sheet'])
        wb.create_sheet('PWR_Q_1')
        wb.create_sheet('PWR_Q_P')
        wb.create_sheet('PWR_Q_F')
        wb.create_sheet('PWR_16_P')
        wb.create_sheet('PWR_16_F')
        wb.create_sheet('PWR_64_P')
        wb.create_sheet('PWR_64_F')
        wb.create_sheet('PWR_256_F')
        wb.create_sheet('ACLR_Q_P')
        wb.create_sheet('ACLR_Q_F')
        wb.create_sheet('ACLR_16_P')
        wb.create_sheet('ACLR_16_F')
        wb.create_sheet('ACLR_64_P')
        wb.create_sheet('ACLR_64_F')
        wb.create_sheet('ACLR_256_F')
        wb.create_sheet('EVM_Q_P')
        wb.create_sheet('EVM_Q_F')
        wb.create_sheet('EVM_16_P')
        wb.create_sheet('EVM_16_F')
        wb.create_sheet('EVM_64_P')
        wb.create_sheet('EVM_64_F')
        wb.create_sheet('EVM_256_F')

        for sheet in wb.sheetnames:
            if 'ACLR' in sheet:
                sh = wb[sheet]
                sh['A1'] = 'Band'
                sh['B1'] = 'Channel'
                sh['C1'] = 'EUTRA_-1'
                sh['D1'] = 'EUTRA_+1'
                sh['E1'] = 'UTRA_-1'
                sh['F1'] = 'UTRA_+1'
                sh['G1'] = 'UTRA_-2'
                sh['H1'] = 'UTRA_+2'

            else:
                sh = wb[sheet]
                sh['A1'] = 'Band'
                sh['B1'] = 'ch0'
                sh['C1'] = 'ch1'
                sh['D1'] = 'ch2'

    elif standard == 'WCDMA' and chcoding == 'REFMEASCH':  # this is WCDMA
        wb = openpyxl.Workbook()
        wb.remove(wb['Sheet'])
        wb.create_sheet('PWR')
        wb.create_sheet('ACLR')
        wb.create_sheet('EVM')

        for sheet in wb.sheetnames:
            if 'ACLR' in sheet:
                sh = wb[sheet]
                sh['A1'] = 'Band'
                sh['B1'] = 'Channel'
                sh['C1'] = 'UTRA_-1'
                sh['D1'] = 'UTRA_+1'
                sh['E1'] = 'UTRA_-2'
                sh['F1'] = 'UTRA_+2'
            else:
                sh = wb[sheet]
                sh['A1'] = 'Band'
                sh['B1'] = 'ch01'
                sh['C1'] = 'ch02'
                sh['D1'] = 'ch03'

    elif standard == 'WCDMA' and chcoding == 'EDCHTEST':  # this is HSUPA
        wb = openpyxl.Workbook()
        wb.remove(wb['Sheet'])
        wb.create_sheet('PWR')
        wb.create_sheet('ACLR')

        for sheet in wb.sheetnames:
            if 'ACLR' in sheet:
                sh = wb[sheet]
                sh['A1'] = 'Band'
                sh['B1'] = 'Channel'
                sh['C1'] = 'UTRA_-1'
                sh['D1'] = 'UTRA_+1'
                sh['E1'] = 'UTRA_-2'
                sh['F1'] = 'UTRA_+2'
                sh['G1'] = 'subtest_number'
            else:
                sh = wb[sheet]
                sh['A1'] = 'Band'
                sh['B1'] = 'ch01'
                sh['C1'] = 'ch02'
                sh['D1'] = 'ch03'
                sh['E1'] = 'subtest_number'

    elif standard == 'WCDMA' and chcoding == 'FIXREFCH':  # this is HSDPA
        wb = openpyxl.Workbook()
        wb.remove(wb['Sheet'])
        wb.create_sheet('PWR')
        wb.create_sheet('ACLR')
        wb.create_sheet('EVM')

        for sheet in wb.sheetnames:
            if 'ACLR' in sheet:
                sh = wb[sheet]
                sh['A1'] = 'Band'
                sh['B1'] = 'Channel'
                sh['C1'] = 'UTRA_-1'
                sh['D1'] = 'UTRA_+1'
                sh['E1'] = 'UTRA_-2'
                sh['F1'] = 'UTRA_+2'
                sh['G1'] = 'subtest_number'
            else:
                sh = wb[sheet]
                sh['A1'] = 'Band'
                sh['B1'] = 'ch01'
                sh['C1'] = 'ch02'
                sh['D1'] = 'ch03'
                sh['E1'] = 'subtest_number'

    wb.save(excel_path)
    wb.close()

    return excel_path


def fill_desens(excel_path):
    wb = openpyxl.load_workbook(excel_path)

    ws = wb['Desens']
    ws_s_txmax = wb['Sensitivity_TxMax']
    ws_s_txmin = wb['Sensitivity_TxMin']
    max_row = max(ws_s_txmax.max_row, ws_s_txmin.max_row)
    for row in range(2, max_row + 1):
        for col in range(1, ws.max_column + 1):
            if col == 1:
                ws.cell(row, col).value = ws_s_txmax.cell(row, col).value
            else:
                try:
                    logger.debug(ws_s_txmax.cell(row, col).value)
                    logger.debug(ws_s_txmin.cell(row, col).value)
                    ws.cell(row, col).value = round(ws_s_txmax.cell(row, col).value -
                                                    ws_s_txmin.cell(row, col).value, 1)
                except TypeError:
                    if ws_s_txmax.cell(row, col).value is None and ws_s_txmin.cell(row, col).value is not None:
                        logger.debug('Sensitivity_TxMax is None')
                        ws.cell(row, col).value = - round(ws_s_txmin.cell(row, col).value, 1)
                    elif ws_s_txmin.cell(row, col).value is None and ws_s_txmax.cell(row, col).value is not None:
                        logger.debug('Sensitivity_TxMin is None')
                        ws.cell(row, col).value = round(ws_s_txmax.cell(row, col).value, 1)
                    else:
                        logger.debug('Sensitivity_TxMax and Sensitivity_TxMin are None')

    wb.save(excel_path)
    wb.close()


def fill_sensitivity_freq_sweep(row, ws, band, dl_ch, data):
    # data[x]: 0 = power, 1 = sensitivity, 2 = PER
    ws.cell(row, 1).value = band
    ws.cell(row, 2).value = dl_ch
    logger.debug('sensitivity')
    ws.cell(row, 3).value = data[1]
    logger.debug('power')
    ws.cell(row, 4).value = data[0]


def fill_sensitivity_lmh(standard, row, ws, band, dl_ch, data, items_selected, bw=5):
    # items_selected: 0 = power, 1 = sensitivity, 2 = PER
    ws.cell(row, 1).value = band

    if dl_ch < cm_pmt_anritsu.dl_ch_selected(standard, band, bw)[1]:
        ws.cell(row, 2).value = data[items_selected]
        if items_selected == 0:
            logger.debug('power of L ch')
        elif items_selected == 1:
            logger.debug('sensitivity of L ch')
    elif dl_ch == cm_pmt_anritsu.dl_ch_selected(standard, band, bw)[1]:
        ws.cell(row, 3).value = data[items_selected]
        if items_selected == 0:
            logger.debug('power of M ch')
        elif items_selected == 1:
            logger.debug('sensitivity of M ch')
    elif dl_ch > cm_pmt_anritsu.dl_ch_selected(standard, band, bw)[1]:
        ws.cell(row, 4).value = data[items_selected]
        if items_selected == 0:
            logger.debug('power of H ch')
        elif items_selected == 1:
            logger.debug('sensitivity of H ch')


def fill_power_aclr_evm_hspa(standard, chcoding, row, ws, band, dl_ch, test_items, items_selected, subtest):
    if standard == 'WCDMA':
        if chcoding == 'EDCHTEST' or chcoding == 'FIXREFCH':  # this is for HSUPA pr HSDPA
            ws.cell(row, 1).value = band
            if items_selected == 0 or items_selected == 2:  # when select power or evm
                ws.cell(row, 5).value = subtest
                if dl_ch < cm_pmt_anritsu.dl_ch_selected(standard, band)[1]:
                    ws.cell(row, 2).value = test_items[items_selected]
                    if items_selected == 0:
                        logger.debug('the power of L ch')
                    elif items_selected == 2:
                        logger.debug('the evm of L ch')
                elif dl_ch == cm_pmt_anritsu.dl_ch_selected(standard, band)[1]:
                    ws.cell(row, 3).value = test_items[items_selected]
                    if items_selected == 0:
                        logger.debug('the power of M ch')
                    elif items_selected == 2:
                        logger.debug('the evm of M ch')
                elif dl_ch > cm_pmt_anritsu.dl_ch_selected(standard, band)[1]:
                    ws.cell(row, 4).value = test_items[items_selected]
                    if items_selected == 0:
                        logger.debug('the power of H ch')
                    elif items_selected == 2:
                        logger.debug('the evm of H ch')

            elif items_selected == 1:  # when select aclr
                ws.cell(row, 7).value = subtest
                if dl_ch < cm_pmt_anritsu.dl_ch_selected(standard, band)[1]:
                    ws.cell(row, 2).value = 'ch01'
                    for col, aclr_item in enumerate(test_items[items_selected]):
                        ws.cell(row, 3 + col).value = aclr_item
                    logger.debug('the ALCR of L ch')
                elif dl_ch == cm_pmt_anritsu.dl_ch_selected(standard, band)[1]:
                    ws.cell(row, 2).value = 'ch02'
                    for col, aclr_item in enumerate(test_items[items_selected]):
                        ws.cell(row, 3 + col).value = aclr_item
                    logger.debug('the ACLR of M ch')
                elif dl_ch > cm_pmt_anritsu.dl_ch_selected(standard, band)[1]:
                    ws.cell(row, 2).value = 'ch03'
                    for col, aclr_item in enumerate(test_items[items_selected]):
                        ws.cell(row, 3 + col).value = aclr_item
                    logger.debug('the ACLR of H ch')

    else:
        logger.info('It might be error to go here!!')


def fill_power_aclr_evm(standard, row, ws, band, dl_ch, test_items, items_selected,
                        bw=5):  # items_selected: 0 = POWER, 1 = ACLR, 2 = EVM
    ws.cell(row, 1).value = band
    if items_selected == 0 or items_selected == 2:  # when select power or evm
        if dl_ch < cm_pmt_anritsu.dl_ch_selected(standard, band, bw)[1]:
            ws.cell(row, 2).value = test_items[items_selected]
            if items_selected == 0:
                logger.debug('the power of L ch')
            elif items_selected == 2:
                logger.debug('the evm of L ch')
        elif dl_ch == cm_pmt_anritsu.dl_ch_selected(standard, band, bw)[1]:
            ws.cell(row, 3).value = test_items[items_selected]
            if items_selected == 0:
                logger.debug('the power of M ch')
            elif items_selected == 2:
                logger.debug('the evm of M ch')
        elif dl_ch > cm_pmt_anritsu.dl_ch_selected(standard, band, bw)[1]:
            ws.cell(row, 4).value = test_items[items_selected]
            if items_selected == 0:
                logger.debug('the power of H ch')
            elif items_selected == 2:
                logger.debug('the evm of H ch')

    elif items_selected == 1:  # when select aclr
        if dl_ch < cm_pmt_anritsu.dl_ch_selected(standard, band, bw)[1]:
            ws.cell(row, 2).value = 'ch01'
            for col, aclr_item in enumerate(test_items[items_selected]):
                ws.cell(row, 3 + col).value = aclr_item
            logger.debug('the ALCR of L ch')
        elif dl_ch == cm_pmt_anritsu.dl_ch_selected(standard, band, bw)[1]:
            ws.cell(row, 2).value = 'ch02'
            for col, aclr_item in enumerate(test_items[items_selected]):
                ws.cell(row, 3 + col).value = aclr_item
            logger.debug('the ACLR of M ch')
        elif dl_ch > cm_pmt_anritsu.dl_ch_selected(standard, band, bw)[1]:
            ws.cell(row, 2).value = 'ch03'
            for col, aclr_item in enumerate(test_items[items_selected]):
                ws.cell(row, 3 + col).value = aclr_item
            logger.debug('the ACLR of H ch')


def fill_progress_rx_sweep(standard, ws, band, dl_ch, data,
                           power_selected, bw=5):  # items_selected: 0 = power, 1 = sensitivity, 2 = PER
    if standard == 'LTE':
        if power_selected == 1:
            logger.debug(f'capture band: {band}, {bw}MHZ, {dl_ch}, TxMax, sensitivity')
        elif power_selected == 0:
            logger.debug(f'capture band: {band}, {bw}MHZ, {dl_ch}, TxMin, sensitivity')

        if ws.max_row == 1:  # only title
            fill_sensitivity_freq_sweep(2, ws, band, dl_ch, data)
            logger.debug('Only title')
        else:
            for row in range(2, ws.max_row + 1):  # not only title
                if ws.cell(row, 1).value == band and ws.cell(row, 2).value == dl_ch:  # if band is in the row
                    fill_sensitivity_freq_sweep(row, ws, band, dl_ch, data)
                    logger.debug('Band and dl_ch are found')
                    break

                elif row == ws.max_row:  # if band and dl_ch are found and final row
                    fill_sensitivity_freq_sweep(row + 1, ws, band, dl_ch, data)
                    logger.debug('Band and dl_ch are not found')
                    break
                else:
                    logger.debug('continue to search')
                    continue

    elif standard == 'WCDMA':
        if power_selected == 1:
            logger.debug(f'capture band: {band}, {dl_ch}, TxMax, sensitivity')
        elif power_selected == 0:
            logger.debug(f'capture band: {band}, {dl_ch}, TxMin, sensitivity')

        if ws.max_row == 1:  # only title
            fill_sensitivity_freq_sweep(2, ws, band, dl_ch, data)
            logger.debug('Only title')
        else:
            for row in range(2, ws.max_row + 1):  # not only title
                if ws.cell(row, 1).value == band and ws.cell(row, 2).value == dl_ch:  # if band is in the row
                    fill_sensitivity_freq_sweep(row, ws, band, dl_ch, data)
                    logger.debug('Band and dl_ch are found')
                    break

                elif row == ws.max_row:  # if band and dl_ch are found and final row
                    fill_sensitivity_freq_sweep(row + 1, ws, band, dl_ch, data)
                    logger.debug('Band and dl_ch are not found')
                    break
                else:
                    logger.debug('continue to search')
                    continue
    elif standard == 'GSM':
        pass


def fill_progress_rx(standard, ws, band, dl_ch, data, items_selected, power_selected,
                     bw=None):  # items_selected: 0 = power, 1 = sensitivity, 2 = PER
    if standard == 'LTE':
        if power_selected == 1:
            logger.debug(f'capture band: {band}, {bw}MHZ, {dl_ch}, TxMax, sensitivity')
        elif power_selected == 0:
            logger.debug(f'capture band: {band}, {bw}MHZ, {dl_ch}, TxMin, sensitivity')

        if ws.max_row == 1:  # only title
            fill_sensitivity_lmh(standard, 2, ws, band, dl_ch, data, items_selected, bw)
            logger.debug('Only title')
        else:
            for row in range(2, ws.max_row + 1):  # not only title
                if ws.cell(row, 1).value == band:  # if band is in the row
                    # POWER and EVM
                    fill_sensitivity_lmh(standard, row, ws, band, dl_ch, data, items_selected, bw)
                    logger.debug('Band is found')
                    break

                elif ws.cell(row, 1).value != band and row == ws.max_row:  # if band is not in the row and final row
                    fill_sensitivity_lmh(standard, row + 1, ws, band, dl_ch, data, items_selected, bw)
                    logger.debug('Band is not found and the row is final and then to add new line')
                    break
                else:
                    logger.debug('continue to search')
                    continue

    elif standard == 'WCDMA':
        if power_selected == 1:
            logger.debug(f'capture band: {band}, {dl_ch}, TxMax, sensitivity')
        elif power_selected == 0:
            logger.debug(f'capture band: {band}, {dl_ch}, TxMin, sensitivity')

        if ws.max_row == 1:  # only title
            fill_sensitivity_lmh(standard, 2, ws, band, dl_ch, data, items_selected)
            logger.debug('Only title')
        else:
            for row in range(2, ws.max_row + 1):  # not only title
                if ws.cell(row, 1).value == band:  # if band is in the row
                    # POWER and EVM
                    fill_sensitivity_lmh(standard, row, ws, band, dl_ch, data, items_selected)
                    logger.debug('Band is found')
                    break

                elif ws.cell(row, 1).value != band and row == ws.max_row:  # if band is not in the row and final row
                    fill_sensitivity_lmh(standard, row + 1, ws, band, dl_ch, data, items_selected)
                    logger.debug('Band is not found and the row is final and then to add new line')
                    break
                else:
                    logger.debug('continue to search')
    elif standard == 'GSM':
        pass


def fill_progress_hspa_tx(standard, chcoding, ws, band, dl_ch, test_items, test_items_selected, subtest):
    aclr_ch = cm_pmt_anritsu.aclr_ch_judge(standard, band, dl_ch)  # this is for ACLR fill in ACLR_TAB

    logger.debug(f'capture band: {band}, {aclr_ch}')

    if ws.max_row == 1:  # only title
        fill_power_aclr_evm_hspa(standard, chcoding, 2, ws, band, dl_ch, test_items, test_items_selected, subtest)
        logger.debug('Only title')

    else:
        for row in range(2, ws.max_row + 1):  # not only title
            if ws.cell(row, 1).value == band and (
                    test_items_selected == 0 or test_items_selected == 2):  # if band is in the row
                # POWER and EVM
                if ws.cell(row, 5).value == subtest:
                    fill_power_aclr_evm_hspa(standard, chcoding, row, ws, band, dl_ch, test_items, test_items_selected,
                                             subtest)
                    logger.debug('Band is found')
                    break
                elif ws.cell(row, 5).value != subtest and row == ws.max_row:
                    fill_power_aclr_evm_hspa(standard, chcoding, row + 1, ws, band, dl_ch, test_items,
                                             test_items_selected, subtest)
                    logger.debug('Band is the same, but subtest in not the same')
                    break

            elif ws.cell(row, 1).value != band and row == ws.max_row:  # if band is not in the row and final row
                fill_power_aclr_evm_hspa(standard, chcoding, row + 1, ws, band, dl_ch, test_items, test_items_selected,
                                         subtest)
                logger.debug('Band is not found and the row is final and then to add new line')
                break

            elif ws.cell(row, 1).value == band and test_items_selected == 1 \
                    and ws.cell(row, 2).value == aclr_ch:

                if ws.cell(row, 7).value == subtest:
                    fill_power_aclr_evm_hspa(standard, chcoding, row, ws, band, dl_ch, test_items, test_items_selected,
                                             subtest)
                    logger.debug('ch is the same for ACLR and subtest is the same')
                    break
                elif ws.cell(row, 7).value != subtest and row == ws.max_row:
                    fill_power_aclr_evm_hspa(standard, chcoding, row + 1, ws, band, dl_ch, test_items,
                                             test_items_selected, subtest)
                    logger.debug('ch is the same for ACLR and subtest is not the same')
                    break

            elif ws.cell(row, 1).value == band and row == ws.max_row and test_items_selected == 1 and ws.cell(row,
                                                                                                              2).value != aclr_ch:
                if ws.cell(row, 7).value == subtest:
                    fill_power_aclr_evm_hspa(standard, chcoding, row + 1, ws, band, dl_ch, test_items,
                                             test_items_selected, subtest)
                    logger.debug('ch is not the same for ACLR and subtest is the same')
                    break
                elif ws.cell(row, 7).value != subtest:
                    fill_power_aclr_evm_hspa(standard, chcoding, row + 1, ws, band, dl_ch, test_items,
                                             test_items_selected, subtest)
                    logger.debug('ch is not the same for ACLR and subtest is not the same')
                    break
            else:
                logger.debug('continue to search')
                continue


def fill_progress_tx(standard, ws, band, dl_ch, test_items, test_items_selected,
                     bw=None):  # items_selected: 0 = POWER, 1 = ACLR, 2 = EVM
    aclr_ch = cm_pmt_anritsu.aclr_ch_judge(standard, band, dl_ch, bw)  # this is for ACLR fill in ACLR_TAB

    if standard == 'LTE':
        logger.debug(f'capture band: {band}, {bw}MHZ, {aclr_ch}')
        if ws.max_row == 1:  # only title
            fill_power_aclr_evm(standard, 2, ws, band, dl_ch, test_items, test_items_selected, bw)
            logger.debug('Only title')
        else:
            for row in range(2, ws.max_row + 1):  # not only title
                if ws.cell(row, 1).value == band and (
                        test_items_selected == 0 or test_items_selected == 2):  # if band is in the row
                    # POWER and EVM
                    fill_power_aclr_evm(standard, row, ws, band, dl_ch, test_items, test_items_selected, bw)
                    logger.debug('Band is found')
                    break
                elif ws.cell(row, 1).value == band and row == ws.max_row and test_items_selected == 1 and ws.cell(
                        row, 2).value != aclr_ch:
                    fill_power_aclr_evm(standard, row + 1, ws, band, dl_ch, test_items, test_items_selected,
                                        bw)
                    logger.debug('ch is not the same for ACLR')
                    break
                elif ws.cell(row, 1).value == band and test_items_selected == 1 and ws.cell(row,
                                                                                            2).value == aclr_ch:
                    fill_power_aclr_evm(standard, row, ws, band, dl_ch, test_items, test_items_selected, bw)
                    logger.debug('ch is the same for ACLR')
                    break
                elif ws.cell(row, 1).value != band and row == ws.max_row:  # if band is not in the row and final row
                    fill_power_aclr_evm(standard, row + 1, ws, band, dl_ch, test_items, test_items_selected,
                                        bw)
                    logger.debug('Band is not found and the row is final and then to add new line')
                    break
                else:
                    logger.debug('continue to search')
                    continue
    elif standard == 'WCDMA':
        logger.debug(f'capture band: {band}, {aclr_ch}')

        if ws.max_row == 1:  # only title
            fill_power_aclr_evm(standard, 2, ws, band, dl_ch, test_items, test_items_selected)
            logger.debug('Only title')
        else:
            for row in range(2, ws.max_row + 1):  # not only title
                if ws.cell(row, 1).value == band and (
                        test_items_selected == 0 or test_items_selected == 2):  # if band is in the row
                    # POWER and EVM
                    fill_power_aclr_evm(standard, row, ws, band, dl_ch, test_items, test_items_selected)
                    logger.debug('Band is found')
                    break
                elif ws.cell(row, 1).value == band and row == ws.max_row and test_items_selected == 1 and ws.cell(
                        row, 2).value != aclr_ch:
                    fill_power_aclr_evm(standard, row + 1, ws, band, dl_ch, test_items, test_items_selected)
                    logger.debug('ch is not the same for ACLR')
                    break
                elif ws.cell(row, 1).value == band and test_items_selected == 1 and ws.cell(row,
                                                                                            2).value == aclr_ch:
                    fill_power_aclr_evm(standard, row, ws, band, dl_ch, test_items, test_items_selected)
                    logger.debug('ch is the same for ACLR')
                    break
                elif ws.cell(row, 1).value != band and row == ws.max_row:  # if band is not in the row and final row
                    fill_power_aclr_evm(standard, row + 1, ws, band, dl_ch, test_items, test_items_selected)
                    logger.debug('Band is not found and the row is final and then to add new line')
                    break
                else:
                    logger.debug('continue to search')
                    continue


def fill_values_rx_sweep(excel_path, standard, data, band, dl_ch, power_selected, bw=None):
    """
    data format:[Tx Power, Sensitivity, PER]
    """
    band = band
    bw = bw
    excel_path = excel_path
    if standard == 'LTE':
        if Path(excel_path).exists() is False:
            create_excel_rx_freq_sweep(standard, power_selected, bw)
            logger.debug('Create Excel')

        wb = openpyxl.load_workbook(excel_path)
        logger.debug('Open Excel')

        if power_selected == 1:
            logger.debug(f'start to fill Sweep of Sensitivity and Power level')
            ws_name = f'Band{band}_Sweep_TxMax'
            # check sheet if it is in the workboook
            if ws_name not in wb.sheetnames:
                wb.create_sheet(ws_name)

            ws = wb[ws_name]
            # check if it has the title at first row
            if ws.cell(1, 1).value is None:
                create_sheet_title_rx_freq_sweep(ws)

            logger.debug('fill sensitivity and power')
            fill_progress_rx_sweep(standard, ws, band, dl_ch, data,
                                   power_selected)  # progress of filling sensitivity progress

        elif power_selected == 0:
            logger.debug(f'start to fill Sweep of Sensitivity and Power level')
            ws_name = f'Band{band}_Sweep_TxMin'

            # check sheet if it is in the workboook
            if ws_name not in wb.sheetnames:
                wb.create_sheet(f'Band{band}_Sweep_TxMin')

            ws = wb[ws_name]
            # check if it has the title at first row
            if ws.cell(1, 1).value is None:
                create_sheet_title_rx_freq_sweep(ws)

            logger.debug('fill sensitivity')
            fill_progress_rx_sweep(standard, ws, band, dl_ch, data,
                                   power_selected)  # progress of filling sensitivity progress

        wb.save(excel_path)
        wb.close()

        return excel_path

    elif standard == 'WCDMA':
        if Path(excel_path).exists() is False:
            create_excel_rx_freq_sweep(standard, power_selected, bw)
            logger.debug('Create Excel')

        wb = openpyxl.load_workbook(excel_path)
        logger.debug('Open Excel')

        if power_selected == 1:
            logger.debug(f'start to fill Sweep of  Sensitivity and Power level')
            ws_name = f'Band{band}_Sweep_TxMax'
            # check sheet if it is in the workboook
            if ws_name not in wb.sheetnames:
                wb.create_sheet(ws_name)

            ws = wb[ws_name]
            # check if it has the title at first row
            if ws.cell(1, 1).value is None:
                create_sheet_title_rx_freq_sweep(ws)

            logger.debug('fill sensitivity and power')
            fill_progress_rx_sweep(standard, ws, band, dl_ch, data,
                                   power_selected)  # progress of filling sensitivity progress

        elif power_selected == 0:
            logger.debug(f'start to fill Sweep of  Sensitivity and Power level')
            ws_name = f'Band{band}_Sweep_TxMin'
            # check sheet if it is in the workboook
            if ws_name not in wb.sheetnames:
                wb.create_sheet(ws_name)

            ws = wb[ws_name]
            # check if it has the title at first row
            if ws.cell(1, 1).value is None:
                create_sheet_title_rx_freq_sweep(ws)

            logger.debug('fill sensitivity')
            fill_progress_rx_sweep(standard, ws, band, dl_ch, data,
                                   power_selected)  # progress of filling sensitivity progress

        wb.save(excel_path)
        wb.close()

        return excel_path


def fill_values_rx(excel_path, standard, data, band, dl_ch, power_selected, bw=None):
    """
        data format:[Tx Power, Sensitivity, PER]
    """
    excel_path = excel_path
    if standard == 'LTE':
        if Path(excel_path).exists() is False:
            create_excel_rx_lmh(standard, bw)
            logger.debug('Create Excel')

        wb = openpyxl.load_workbook(excel_path)
        logger.debug('Open Excel')

        if power_selected == 1:
            logger.debug(f'start to fill Sensitivity and Tx Power and Desens')
            ws = wb['Sensitivity_TxMax']
            logger.debug('fill sensitivity')
            fill_progress_rx(standard, ws, band, dl_ch, data, 1, power_selected, bw)  # fill sensitivity
            ws = wb['PWR_TxMax']
            logger.debug('fill power')
            fill_progress_rx(standard, ws, band, dl_ch, data, 0, power_selected, bw)  # fill power

        elif power_selected == 0:
            logger.debug(f'start to fill Sensitivity and Tx Power and Desens')
            ws = wb['Sensitivity_TxMin']
            logger.debug('fill sensitivity')
            fill_progress_rx(standard, ws, band, dl_ch, data, 1, power_selected, bw)  # fill sensitivity
            ws = wb['PWR_TxMin']
            logger.debug('fill power')
            fill_progress_rx(standard, ws, band, dl_ch, data, 0, power_selected, bw)  # fill power

        wb.save(excel_path)
        wb.close()

        return excel_path

    elif standard == 'WCDMA':
        if Path(excel_path).exists() is False:
            create_excel_rx_lmh(standard, bw)
            logger.debug('Create Excel')

        wb = openpyxl.load_workbook(excel_path)
        logger.debug('Open Excel')

        if power_selected == 1:
            logger.debug(f'start to fill Sensitivity and Tx Power and Desens')
            ws = wb['Sensitivity_TxMax']
            logger.debug('fill sensitivity')
            fill_progress_rx(standard, ws, band, dl_ch, data, 1, power_selected)  # fill sensitivity
            ws = wb['PWR_TxMax']
            logger.debug('fill power')
            fill_progress_rx(standard, ws, band, dl_ch, data, 0, power_selected)  # fill power

        elif power_selected == 0:
            logger.debug(f'start to fill Sensitivity and Tx Power and Desens')
            ws = wb['Sensitivity_TxMin']
            logger.debug('fill sensitivity')
            fill_progress_rx(standard, ws, band, dl_ch, data, 1, power_selected)  # fill sensitivity
            ws = wb['PWR_TxMin']
            logger.debug('fill power')
            fill_progress_rx(standard, ws, band, dl_ch, data, 0, power_selected)  # fill power

        wb.save(excel_path)
        wb.close()

        return excel_path


def fill_values_tx(excel_path, standard, data, band, dl_ch, chcoding, bw=None):
    excel_path = excel_path
    if standard == 'LTE':
        """
            LTE format:{Q1:[power], Q_P:[power, ACLR, EVM], ...} and ACLR format is [L, M, H] 
        """
        if Path(excel_path).exists() is False:
            create_excel_tx_lmh(standard, bw)
            logger.debug('Create Excel')

        wb = openpyxl.load_workbook(excel_path)
        logger.debug('Open Excel')
        for mod, test_items in data.items():

            ws = wb[f'PWR_{mod}']  # POWER
            logger.debug('start to fill Power')
            fill_progress_tx(standard, ws, band, dl_ch, test_items, 0, bw)

            if mod != 'Q_1':
                ws = wb[f'ACLR_{mod}']  # ACLR
                logger.debug('start to fill ACLR')
                fill_progress_tx(standard, ws, band, dl_ch, test_items, 1, bw)

                ws = wb[f'EVM_{mod}']  # EVM
                logger.debug('start to fill EVM')
                fill_progress_tx(standard, ws, band, dl_ch, test_items, 2, bw)

        wb.save(excel_path)
        wb.close()

        return excel_path

    elif standard == 'WCDMA':
        """
            WCDMA format:[power, ACLR, EVM], ...} and ACLR format is list format like [L, M, H]  
        """
        if chcoding == 'REFMEASCH':  # this is WCDMA
            if Path(excel_path).exists() is False:
                create_excel_tx_lmh(standard)
                logger.debug('Create Excel')

            wb = openpyxl.load_workbook(excel_path)

            logger.debug('Open Excel')

            ws = wb[f'PWR']  # POWER
            logger.debug('start to fill Power')
            fill_progress_tx(standard, ws, band, dl_ch, data, 0)

            ws = wb[f'ACLR']  # ACLR
            logger.debug('start to fill ACLR')
            fill_progress_tx(standard, ws, band, dl_ch, data, 1)

            ws = wb[f'EVM']  # EVM
            logger.debug('start to fill EVM')
            fill_progress_tx(standard, ws, band, dl_ch, data, 2)

            wb.save(excel_path)
            wb.close()

            return excel_path

        elif chcoding == 'EDCHTEST':  # this is HSUPA
            """
                HSUPA format:{subtest_number: [power, ACLR], ...} and ACLR format is list format like [L, M, H]  
            """
            if Path(excel_path).exists() is False:
                create_excel_tx_lmh(standard, bw)
                logger.debug('Create Excel')

            wb = openpyxl.load_workbook(excel_path)
            logger.debug('Open Excel')

            for subtest, test_items in data.items():
                logger.info(f'start to fill subtest{subtest}')

                ws = wb[f'PWR']  # POWER
                logger.debug('start to fill Power')
                fill_progress_hspa_tx(standard, chcoding, ws, band, dl_ch, test_items, 0, subtest)

                ws = wb[f'ACLR']  # ACLR
                logger.debug('start to fill ACLR')
                fill_progress_hspa_tx(standard, chcoding, ws, band, dl_ch, test_items, 1, subtest)

                wb.save(excel_path)
                wb.close()

            return excel_path

        elif chcoding == 'FIXREFCH':  # this is HSDPA
            """
                HSDPA format:{subtest_number: [power, ACLR], ...} and ACLR format is list format like [L, M, H]  
                only subtest3 is for [power, ACLR, evm], evm to pickup the worst vaule from p0, p1, p2, p3
            """
            if Path(excel_path).exists() is False:
                create_excel_tx_lmh(standard, bw)
                logger.debug('Create Excel')

            wb = openpyxl.load_workbook(excel_path)
            logger.debug('Open Excel')
            for subtest, test_items in data.items():
                logger.info(f'start to fill subtest{subtest}')

                ws = wb[f'PWR']  # POWER
                logger.debug('start to fill Power')
                fill_progress_hspa_tx(standard, chcoding, ws, band, dl_ch, test_items, 0, subtest)

                ws = wb[f'ACLR']  # ACLR
                logger.debug('start to fill ACLR')
                fill_progress_hspa_tx(standard, chcoding, ws, band, dl_ch, test_items, 1, subtest)

                if subtest == 3:
                    ws = wb[f'EVM']  # EVM
                    logger.debug('start to fill EVM')
                    fill_progress_hspa_tx(standard, chcoding, ws, band, dl_ch, test_items, 2, subtest)

                wb.save(excel_path)
                wb.close()

            return excel_path


def excel_plot_line(standard, chcoding, excel_path):
    logger.debug('Start to plot line chart in Excel')
    if standard == 'LTE':
        try:
            wb = openpyxl.load_workbook(excel_path)
            for ws_name in wb.sheetnames:
                ws = wb[ws_name]

                if ws._charts != []:  # if there is charts, delete it
                    del ws._charts[0]

                if 'PWR' in ws_name or 'EVM' in ws_name:
                    chart = LineChart()
                    chart.title = f'{ws_name[:3]}'
                    if 'PWR' in ws_name:
                        chart.y_axis.title = f'{ws_name[:3]}(dBm)'
                    elif 'EVM' in ws_name:
                        chart.y_axis.title = f'{ws_name[:3]}%'

                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=2, min_row=1, max_col=ws.max_column, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=1, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].graphicalProperties.line.dashStyle = 'dash'  # for L_ch
                    chart.series[1].graphicalProperties.line.width = 50000  # for M_ch
                    chart.series[2].marker.symbol = 'circle'  # for H_ch
                    chart.series[2].marker.size = 10

                    ws.add_chart(chart, "F1")

                    wb.save(excel_path)
                    wb.close()

                elif 'Sensitivity' in ws_name or 'Desens' in ws_name:
                    chart = LineChart()
                    chart.title = f'{ws_name[:11]}'

                    chart.y_axis.title = f'Sensitivity(dBm)'

                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'

                    chart.height = 20
                    chart.width = 32

                    y_data = Reference(ws, min_col=2, min_row=1, max_col=ws.max_column, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=1, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                    chart.series[0].graphicalProperties.line.dashStyle = 'dash'  # for L_ch
                    chart.series[1].graphicalProperties.line.width = 50000  # for M_ch
                    chart.series[2].marker.symbol = 'circle'  # for H_ch
                    chart.series[2].marker.size = 10

                    ws.add_chart(chart, "F1")

                    wb.save(excel_path)
                    wb.close()

                elif 'Sweep' in ws_name:
                    chart_sens = LineChart()
                    chart_sens.title = 'Sensitivity_Rx_Chan_Sweep'
                    chart_sens.y_axis.title = f'{ws_name[:11]}'
                    chart_sens.x_axis.title = 'Rx_chan'
                    chart_sens.x_axis.tickLblPos = 'low'
                    # chart_sens.y_axis.scaling.min = -60
                    # chart_sens.y_axis.scaling.max = -20

                    chart_sens.height = 20
                    chart_sens.width = 40

                    y_data_sens = Reference(ws, min_col=ws.max_column - 1, min_row=1, max_col=ws.max_column - 1,
                                            max_row=ws.max_row)

                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart_sens.add_data(y_data_sens, titles_from_data=True)
                    chart_sens.set_categories(x_data)

                    # chart_sens.y_axis.majorGridlines = None

                    chart_sens.series[0].marker.symbol = 'circle'  # for sensitivity
                    chart_sens.series[0].marker.size = 3

                    chart_pwr = LineChart()  # create a second chart

                    y_data_pwr = Reference(ws, min_col=ws.max_column, min_row=1, max_col=ws.max_column,
                                           max_row=ws.max_row)
                    chart_pwr.add_data(y_data_pwr, titles_from_data=True)

                    chart_pwr.series[0].graphicalProperties.line.dashStyle = 'dash'  # for power
                    chart_pwr.y_axis.title = 'Power(dBm)'
                    chart_pwr.y_axis.axId = 200
                    chart_pwr.y_axis.majorGridlines = None

                    chart_sens.y_axis.crosses = 'max'
                    chart_sens += chart_pwr

                    ws.add_chart(chart_sens, "J1")
                    # ws.add_chart(chart_sens, "J42")

                    wb.save(excel_path)
                    wb.close()


                elif 'ACLR' in ws_name:
                    chart = LineChart()
                    chart.title = 'ACLR'
                    chart.y_axis.title = 'ACLR(dB)'
                    chart.x_axis.title = 'Band'
                    chart.x_axis.tickLblPos = 'low'
                    chart.y_axis.scaling.min = -60
                    chart.y_axis.scaling.max = -20

                    chart.height = 20
                    chart.width = 40

                    y_data = Reference(ws, min_col=3, min_row=1, max_col=ws.max_column, max_row=ws.max_row)
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

                    ws.add_chart(chart, "J1")

                    wb.save(excel_path)
                    wb.close()
        except TypeError as err:
            logger.debug(err)
            logger.info(f"This Band doesn't have this BW")

    elif standard == 'WCDMA':
        wb = openpyxl.load_workbook(excel_path)
        for ws_name in wb.sheetnames:
            ws = wb[ws_name]

            if ws._charts != []:  # if there is charts, delete it
                del ws._charts[0]

            if 'PWR' in ws_name or 'EVM' in ws_name:
                chart = LineChart()
                chart.title = f'{ws_name[:3]}'
                if 'PWR' in ws_name:
                    chart.y_axis.title = f'{ws_name[:3]}(dBm)'
                elif 'EVM' in ws_name:
                    chart.y_axis.title = f'{ws_name[:3]}%'

                chart.x_axis.title = 'Band'
                chart.x_axis.tickLblPos = 'low'

                chart.height = 20
                chart.width = 32

                if chcoding == 'REFMEASCH':  # this is WCDMA:
                    y_data = Reference(ws, min_col=2, min_row=1, max_col=ws.max_column, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=1, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                else:  # HSUPA, HSDPA
                    y_data = Reference(ws, min_col=2, min_row=1, max_col=ws.max_column - 1, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=1, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                chart.series[0].graphicalProperties.line.dashStyle = 'dash'  # for L_ch
                chart.series[1].graphicalProperties.line.width = 50000  # for M_ch
                chart.series[2].marker.symbol = 'circle'  # for H_ch
                chart.series[2].marker.size = 10

                ws.add_chart(chart, "F1")

                wb.save(excel_path)
                wb.close()

            elif 'ACLR' in ws_name:
                chart = LineChart()
                chart.title = 'ACLR'
                chart.y_axis.title = 'ACLR(dB)'
                chart.x_axis.title = 'Band'
                chart.x_axis.tickLblPos = 'low'
                chart.y_axis.scaling.min = -60
                chart.y_axis.scaling.max = -20

                chart.height = 20
                chart.width = 40

                if chcoding == 'REFMEASCH':  # this is WCDMA:
                    y_data = Reference(ws, min_col=3, min_row=1, max_col=ws.max_column, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                else:
                    y_data = Reference(ws, min_col=3, min_row=1, max_col=ws.max_column - 1, max_row=ws.max_row)
                    x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                    chart.add_data(y_data, titles_from_data=True)
                    chart.set_categories(x_data)

                chart.series[0].graphicalProperties.line.width = 50000  # for UTRA_-1
                chart.series[1].graphicalProperties.line.width = 50000  # for UTRA_+1
                chart.series[2].graphicalProperties.line.dashStyle = 'dash'  # for UTRA_-2
                chart.series[3].graphicalProperties.line.dashStyle = 'dash'  # for UTRA_+2

                ws.add_chart(chart, "J1")

                wb.save(excel_path)
                wb.close()

            elif 'Sensitivity' in ws_name or 'Desens' in ws_name:
                chart = LineChart()
                chart.title = f'{ws_name[:11]}'

                chart.y_axis.title = f'Sensitivity(dBm)'

                chart.x_axis.title = 'Band'
                chart.x_axis.tickLblPos = 'low'

                chart.height = 20
                chart.width = 32

                y_data = Reference(ws, min_col=2, min_row=1, max_col=ws.max_column, max_row=ws.max_row)
                x_data = Reference(ws, min_col=1, min_row=2, max_col=1, max_row=ws.max_row)
                chart.add_data(y_data, titles_from_data=True)
                chart.set_categories(x_data)

                chart.series[0].graphicalProperties.line.dashStyle = 'dash'  # for L_ch
                chart.series[1].graphicalProperties.line.width = 50000  # for M_ch
                chart.series[2].marker.symbol = 'circle'  # for H_ch
                chart.series[2].marker.size = 10

                ws.add_chart(chart, "F1")

                wb.save(excel_path)
                wb.close()

    elif standard == 'GSM':
        pass
