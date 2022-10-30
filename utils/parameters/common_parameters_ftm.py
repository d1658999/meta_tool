# bandwidth index
def bandwidths_selected_fr1(band):
    band = int(band)
    bandwidths = {
        'N1': [5, 10, 15, 20, 25, 40, 50, ],  # remove 30
        'N2': [5, 10, 15, 20, ],
        'N3': [5, 10, 15, 20, 25, 40, ],  # remove 30
        'N5': [5, 10, 15, 20, ],
        'N7': [5, 10, 15, 20, 25, 40, 50, ],  # remove 30
        'N8': [5, 10, 15, 20, ],
        'N12': [5, 10, 15, ],
        'N13': [5, 10, ],
        'N14': [5, 10, ],
        'N18': [5, 10, 15],
        'N20': [5, 10, 15, 20, ],
        'N24': [5, 10, ],
        'N25': [5, 10, 15, 20, ],
        'N26': [5, 10, 15, 20],
        'N28': [5, 10, 15, 20],
        'N29': [5, 10],
        'N30': [5, 10],
        'N34': [5, 10, 15, ],
        'N38': [10, 15, 20, 25, 40, ],
        'N39': [10, 15, 20, 25, 40, ],
        'N40': [10, 15, 20, 25, 40, 50, 60, 80, ],
        'N41': [10, 15, 20, 40, 50, 60, 80, 100, ],
        'N48': [10, 15, 20, 40, 50, 60, 70, 80, 90, 100, ],
        'N66': [5, 10, 15, 20, 25, 30, 40, ],
        'N70': [5, 10, 15, 20, 25, ],
        'N71': [5, 10, 15, 20, ],
        'N75': [5, 10, 15, 20, 25, 30, 40, 50, ],
        'N76': [5, 10, ],
        'N77': [10, 15, 20, 25, 40, 50, 60, 70, 80, 90, 100, ],
        'N78': [10, 15, 20, 25, 40, 50, 60, 70, 80, 90, 100, ],
        'N79': [10, 20, 40, 50, 60, 80, 90, 100, ],
    }

    return bandwidths[f'N{band}']


def bandwidths_selected_lte(band):
    band = int(band)
    bandwidths = {
        'B1': [5, 10, 15, 20],
        'B2': [1.4, 3, 5, 10, 15, 20],
        'B3': [1.4, 3, 5, 10, 15, 20],
        'B4': [1.4, 3, 5, 10, 15, 20],
        'B5': [1.4, 3, 5, 10],
        'B7': [5, 10, 15, 20],
        'B8': [1.4, 3, 5, 10],
        'B12': [1.4, 3, 5, 10],
        'B13': [5, 10],
        'B14': [5, 10],
        'B17': [5, 10],
        'B18': [5, 10, 15],
        'B19': [5, 10, 15],
        'B20': [5, 10, 15, 20],
        'B21': [5, 10, 15],
        'B25': [1.4, 3, 5, 10, 15, 20],
        'B26': [1.4, 3, 5, 10, 15],
        'B28': [3, 5, 10, 15],
        'B29': [3, 5, 10],
        'B30': [5, 10],
        'B32': [5, 10, 15, 20],
        'B38': [5, 10, 15, 20],
        'B39': [5, 10, 15, 20],
        'B40': [5, 10, 15, 20],
        'B41': [5, 10, 15, 20],
        'B42': [5, 10, 15, 20],
        'B46': [10, 20],
        'B48': [5, 10, 15, 20],
        'B66': [1.4, 3, 5, 10, 15, 20],
        'B70': [5, 10, 15, 20],
        'B71': [5, 10, 15, 20],
        'B75': [5, 10, 15, 20],
    }

    return bandwidths[f'B{band}']


# DL Freq
def dl_freq_selected(standard, band, bw=5):
    band = int(band)
    band_dl_freq_fr1 = {
        'N1': [2110 + bw / 2, 2140, 2170 - bw / 2],
        'N2': [1930 + bw / 2, 1960, 1990 - bw / 2],
        'N3': [1805 + bw / 2, 1842.5, 1880 - bw / 2],
        'N5': [869 + bw / 2, 881.5, 894 - bw / 2],
        'N7': [2620 + bw / 2, 2655, 2690 - bw / 2],
        'N8': [925 + bw / 2, 942.5, 960 - bw / 2],
        'N12': [729 + bw / 2, 737.5, 746 - bw / 2],
        'N13': [746 + bw / 2, 751, 756 - bw / 2],
        'N14': [758 + bw / 2, 763, 768 - bw / 2],
        'N18': [860 + bw / 2, 867.5, 875 - bw / 2],
        'N20': [791 + bw / 2, 806, 821 - bw / 2],
        'N24': [1525 + bw / 2, 1542, 1559 - bw / 2],
        'N25': [1930 + bw / 2, 1962.5, 1995 - bw / 2],
        'N26': [859 + bw / 2, 876.5, 894 - bw / 2],
        'N28': [758 + bw / 2, 780.5, 803 - bw / 2],
        'N28A': [758 + bw / 2, 773, 788 - bw / 2],
        'N28B': [773 + bw / 2, 788, 803 - bw / 2],
        'N30': [2350 + bw / 2, 2355, 2360 - bw / 2],
        'N34': [2010 + bw / 2, 2017.5, 2025 - bw / 2],
        'N38': [2570 + bw / 2, 2595, 2620 - bw / 2],
        'N39': [1880 + bw / 2, 1900, 1920 - bw / 2],
        'N40': [2300 + bw / 2, 2350, 2400 - bw / 2],
        'N41': [2496 + bw / 2, 2593, 2690 - bw / 2],
        'N48': [3550 + bw / 2, 3625, 3700 - bw / 2],
        'N66': [2110 + bw / 2, 2145, 2180 - bw / 2],
        'N70': [1995 + bw / 2, 2007.5, 2020 - bw / 2],
        'N71': [617 + bw / 2, 634.5, 652 - bw / 2],
        'N75': [1432 + bw / 2, 1474.5, 1517 - bw / 2],
        'N76': [1427 + bw / 2, 1429.5, 1432 - bw / 2],
        'N77': [3300 + bw / 2, 3750, 4200 - bw / 2],
        'N78': [3300 + bw / 2, 3550, 3800 - bw / 2],
        'N79': [4400 + bw / 2, 4700, 5000 - bw / 2],
        # 'N78': [3350.01, 3549.99, 3750],
        # 'N77': [3350.01, 3750, 4149.99],

    }

    band_dl_freq_lte = {
        'B1': [2110 + bw / 2, 2140, 2170 - bw / 2],
        'B2': [1930 + bw / 2, 1960, 1990 - bw / 2],
        'B3': [1805 + bw / 2, 1842.5, 1880 - bw / 2],
        'B4': [2110 + bw / 2, 2132.5, 2155 - bw / 2],
        'B5': [869 + bw / 2, 881.5, 894 - bw / 2],
        'B7': [2620 + bw / 2, 2655, 2690 - bw / 2],
        'B8': [925 + bw / 2, 942.5, 960 - bw / 2],
        'B12': [729 + bw / 2, 737.5, 746 - bw / 2],
        'B13': [746 + bw / 2, 751, 756 - bw / 2],
        'B14': [758 + bw / 2, 763, 768 - bw / 2],
        'B17': [734 + bw / 2, 740, 746 - bw / 2],
        'B18': [860 + bw / 2, 867.5, 875 - bw / 2],
        'B19': [875 + bw / 2, 882.5, 890 - bw / 2],
        'B20': [791 + bw / 2, 806, 821 - bw / 2],
        'B21': [1495.9 + bw / 2, 1503.5, 1510.9 - bw / 2],
        'B25': [1930 + bw / 2, 1962.5, 1995 - bw / 2],
        'B26': [859 + bw / 2, 876.5, 894 - bw / 2],
        'B28': [758 + bw / 2, 780.5, 803 - bw / 2],
        # [758 + bw / 2, 780.5, 803 - bw / 2] for 28, [758 + bw / 2, 773, 788 - bw / 2] for 28A, [773 + bw / 2, 788,  - 803/ 2] for 28B
        'B28A': [758 + bw / 2, 773, 788 - bw / 2],
        'B28B': [773 + bw / 2, 788, 803 - bw / 2],
        'B29': [717 + bw / 2, 722.5, 728 - bw / 2],
        'B30': [2350 + bw / 2, 2355, 2360 - bw / 2],
        'B32': [1452 + bw / 2, 1474, 1496 - bw / 2],
        'B38': [2570 + bw / 2, 2595, 2620 - bw / 2],
        'B39': [1880 + bw / 2, 1900, 1920 - bw / 2],
        'B40': [2300 + bw / 2, 2350, 2400 - bw / 2],
        'B41': [2496 + bw / 2, 2593, 2690 - bw / 2],
        'B42': [3400 + bw / 2, 3500, 3600 - bw / 2],
        'B46': [5150 + bw / 2, 5537.5, 5925 - bw / 2],
        'B48': [3550 + bw / 2, 3625, 3700 - bw / 2],
        'B66': [2110 + bw / 2, 2145, 2180 - bw / 2],
        'B71': [617 + bw / 2, 634.5, 652 - bw / 2],
        'B75': [1432 + bw / 2, 1474.5, 1517 - bw / 2],

    }

    band_dl_freq_wcdma = {
        'B1': [2110, 2140, 2170],
        'B2': [1930, 1960, 1990],
        'B4': [2110, 2132.6, 2155],
        'B5': [860, 880, 891.6],
        'B8': [925, 942.6, 960],
        'B6': [875, 880, 885],
        'B9': [1845, 1862.4, 1879.8],
        'B19': [875, 882.6, 890],

    }

    band_dl_freq_gsm = {
        850: [869.2, 881.4, 893.8],
        900: [925.2, 942.4, 959.8],
        1800: [1805.2, 1842.4, 1879.8],
        1900: [1930.2, 1960, 1989.8],

    }

    if standard == 'LTE':
        if band == 28:
            from external_paramters import band_segment
            return [int(freq * 1000) for freq in band_dl_freq_lte[f'B{band}{band_segment}']]
        else:
            return [int(freq * 1000) for freq in band_dl_freq_lte[f'B{band}']]
    elif standard == 'WCDMA':
        return [int(freq * 1000) for freq in band_dl_freq_wcdma[f'B{band}']]
    elif standard == 'GSM':
        return [int(freq * 1000) for freq in band_dl_freq_gsm[band]]
    elif standard == 'FR1':
        if band == 28:
            from external_paramters import band_segment_fr1
            return [int(freq * 1000) for freq in band_dl_freq_fr1[f'N{band}{band_segment_fr1}']]
        else:
            return [int(freq * 1000) for freq in band_dl_freq_fr1[f'N{band}']]
    elif 'GSM':
        pass


def dl_chan_select_gsm(band):
    band_dl_ch_gsm = {
        850: [128, 189, 251],
        900: [975, 37, 124],
        1800: [512, 698, 885],
        1900: [512, 661, 810],
    }
    return [int(ch) for ch in band_dl_ch_gsm[band]]


def dl_chan_select_wcdma(band):
    band_dl_ch_wcdma = {
        'B1': [10562, 10700, 10838],
        'B2': [9662, 9800, 9938],
        'B4': [1537, 1638, 1738],
        'B5': [4357, 4400, 4458],
        'B8': [2937, 3013, 3088],
        'B6': [4387, 4400, 4413],
        'B9': [9237, 9312, 9387],
        'B19': [712, 738, 763],
    }

    return [int(ch) for ch in band_dl_ch_wcdma[f'B{band}']]


def transfer_chan_tx2rx_wcdma(band_wcdma, chan):
    band_wcdma = int(band_wcdma)
    spacing_wcdma = {
        1: 950,
        2: 400,
        4: 225,
        5: 225,
        8: 225,
        6: 225,
        9: 475,
        19: 400,

    }

    return chan + spacing_wcdma[band_wcdma]


def transfer_chan_rx2tx_wcdma(band_wcdma, chan):
    band_wcdma = int(band_wcdma)
    band_wcdma = int(band_wcdma)
    spacing_wcdma = {
        1: -950,
        2: -400,
        4: -225,
        5: -225,
        8: -225,
        6: -225,
        9: -475,
        19: -400,

    }

    return chan + spacing_wcdma[band_wcdma]


def transfer_chan2freq_wcdma(band, chan, tx_rx='tx'):
    band = int(band)
    chan = int(chan)

    if band == 4:
        if tx_rx == 'tx':
            return (1450 + 0.2 * chan) * 1000
        elif tx_rx == 'rx':
            return (1805 + 0.2 * chan) * 1000
    elif band == 8:
        return (340 + 0.2 * chan) * 1000
    elif band == 19:
        if tx_rx == 'tx':
            return (770 + 0.2 * chan) * 1000
        elif tx_rx == 'rx':
            return (735 + 0.2 * chan) * 1000
    else:
        return 0.2 * chan * 1000


def trandfer_freq2chan_wcdma(band, freq, tx_rx='tx'):
    if band == 4:
        if tx_rx == 'tx':
            return 5 * (freq / 1000 - 1450)
        elif tx_rx == 'rx':
            return 5 * (freq / 1000 - 1805)
    elif band == 8:
        return 5 * (freq / 1000 - 340)
    elif band == 19:
        if tx_rx == 'tx':
            return 5 * (freq / 1000 - 770)
        elif tx_rx == 'rx':
            return 5 * (freq / 1000 - 735)
    else:
        return 5 * freq / 1000


def transfer_freq_rx2tx_wcdma(band_wcdma, freq):
    band_wcdma = int(band_wcdma)
    spacing_wdcma = {
        1: -190000,
        2: -80000,
        4: -400000,
        5: -45000,
        8: -45000,
        6: -45000,
        9: -95000,
        19: -45000,
    }

    return freq + spacing_wdcma[band_wcdma]


def transfer_freq_tx2rx_wcdma(band_wcdma, freq):
    band_wcdma = int(band_wcdma)
    spacing_wdcma = {
        1: 190000,
        2: 80000,
        4: 400000,
        5: 45000,
        8: 45000,
        6: 45000,
        9: 95000,
        19: 45000,
    }

    return freq + spacing_wdcma[band_wcdma]


def transfer_chan2freq_gsm(band_gsm, chan, tx_rx='rx'):
    if tx_rx == 'rx':
        chan = 1024 + chan if chan < 125 else chan
        return int(dl_freq_selected('GSM', band_gsm, 0)[0] + 1000 * 0.2 * (chan - dl_chan_select_gsm(band_gsm)[0]))
    else:
        chan = 1024 + chan if chan < 125 else chan
        if band_gsm == 850 or band_gsm == 900:
            return int(
                dl_freq_selected('GSM', band_gsm, 0)[0] + 1000 * 0.2 * (chan - dl_chan_select_gsm(band_gsm)[0])) - 45000
        elif band_gsm == 1800:
            return int(
                dl_freq_selected('GSM', band_gsm, 0)[0] + 1000 * 0.2 * (chan - dl_chan_select_gsm(band_gsm)[0])) - 95000
        elif band_gsm == 1900:
            return int(
                dl_freq_selected('GSM', band_gsm, 0)[0] + 1000 * 0.2 * (chan - dl_chan_select_gsm(band_gsm)[0])) - 80000


def transfer_freq2chan_gsm(band_gsm, freq, tx_rx='rx'):
    if tx_rx == 'rx':
        if 935000 <= freq <= 959800:
            return int(
                (freq - dl_freq_selected('GSM', band_gsm, 0)[0]) / 1000 * 5 + dl_chan_select_gsm(band_gsm)[0] - 1024)
        else:
            return int((freq - dl_freq_selected('GSM', band_gsm, 0)[0]) / 1000 * 5 + dl_chan_select_gsm(band_gsm)[0])
    else:
        if band_gsm == 850 or band_gsm == 900:
            freq = freq + 45000
            if 935000 <= freq <= 959800:
                return int((freq - dl_freq_selected('GSM', band_gsm, 0)[0]) / 1000 * 5 + dl_chan_select_gsm(band_gsm)[
                    0] - 1024)
            else:
                return int(
                    (freq - dl_freq_selected('GSM', band_gsm, 0)[0]) / 1000 * 5 + dl_chan_select_gsm(band_gsm)[0])
        elif band_gsm == 1800:
            freq = freq + 95000
            return int((freq - dl_freq_selected('GSM', band_gsm, 0)[0]) / 1000 * 5 + dl_chan_select_gsm(band_gsm)[0])
        elif band_gsm == 1900:
            freq = freq + 80000
            return int((freq - dl_freq_selected('GSM', band_gsm, 0)[0]) / 1000 * 5 + dl_chan_select_gsm(band_gsm)[0])


def transfer_freq_rx2tx_gsm(band_gsm, freq):
    band_gsm = int(band_gsm)
    spacing_gsm = {
        850: -45000,
        900: -45000,
        1800: -95000,
        1900: -80000,
    }

    return freq + spacing_gsm[band_gsm]


def transfer_freq_tx2rx_gsm(band_gsm, freq):
    band_gsm = int(band_gsm)
    spacing_gsm = {
        850: 45000,
        900: 45000,
        1800: 95000,
        1900: 80000,
    }

    return freq + spacing_gsm[band_gsm]


def transfer_freq_rx2tx_lte(band_lte, freq):
    band_lte = int(band_lte)
    if band_lte not in [38, 39, 40, 41, 42, 48]:
        spacing_lte = {
            1: -190000,
            2: -80000,
            3: -95000,
            4: -400000,
            5: -45000,
            7: -120000,
            8: -45000,
            12: -30000,
            13: 31000,
            14: 30000,
            17: -30000,
            18: -45000,
            19: -45000,
            20: 41000,
            21: -48000,
            25: -80000,
            26: -45000,
            28: -55000,
            30: -45000,
            66: -400000,
            71: 46000,

        }

        return freq + spacing_lte[band_lte]
    else:
        return freq


def transfer_freq_tx2rx_lte(band_lte, freq):
    band_lte = int(band_lte)
    if band_lte not in [38, 39, 40, 41, 42, 48]:
        spacing_lte = {
            1: 190000,
            2: 80000,
            3: 95000,
            4: 400000,
            5: 45000,
            7: 120000,
            8: 45000,
            12: 30000,
            13: -31000,
            14: -30000,
            17: 30000,
            18: 45000,
            19: 45000,
            20: -41000,
            21: 48000,
            25: 80000,
            26: 45000,
            28: 55000,
            30: 45000,
            66: 400000,
            71: -46000,

        }

        return freq + spacing_lte[band_lte]
    else:
        return freq


def transfer_freq_rx2tx_fr1(band_fr1, freq):
    band_fr1 = int(band_fr1)
    if band_fr1 not in [34, 38, 39, 40, 41, 42, 48, 75, 76, 77, 78, 79]:
        spacing_fr1 = {
            1: -190000,
            2: -80000,
            3: -95000,
            5: -45000,
            7: -120000,
            8: -45000,
            12: -30000,
            13: 31000,
            14: 30000,
            18: -45000,
            20: 41000,
            24: 101500,
            25: -80000,
            26: -45000,
            28: -55000,
            30: -45000,
            66: -400000,
            70: -300000,
            71: 46000,

        }

        return freq + spacing_fr1[band_fr1]
    else:
        return freq


def transfer_freq_tx2rx_fr1(band_fr1, freq):
    band_fr1 = int(band_fr1)
    if band_fr1 not in [34, 38, 39, 40, 41, 42, 48, 75, 76, 77, 78, 79]:
        spacing_fr1 = {
            1: 190000,
            2: 80000,
            3: 95000,
            5: 45000,
            7: 120000,
            8: 45000,
            12: 30000,
            13: -31000,
            14: -30000,
            18: 45000,
            20: -41000,
            24: -101500,
            25: 80000,
            26: 45000,
            28: 55000,
            30: 45000,
            66: 400000,
            70: 300000,
            71: -46000,
        }

        return freq + spacing_fr1[band_fr1]
    else:
        return freq


def special_uplink_config_sensitivity_lte(band, bw):
    if (int(band) in [2, 3, 25]) and int(bw) == 15:
        return 50, 25
    elif (int(band) in [2, 3, 25]) and int(bw) == 20:
        return 50, 50
    elif int(band) in [5, 8, 18, 19, 21, 26, 28, 30] and int(bw) == 10:
        return 25, 25
    elif int(band) == 7 and int(bw) == 20:
        return 75, 25
    elif int(band) == 7 and int(bw) == 20:
        return 75, 25
    elif int(band) in [12, 17] and int(bw) == 5:
        return 20, 5
    elif int(band) == 12 and int(bw) == 10:
        return 20, 30
    elif int(band) == 13 and (int(bw) in [5, 10]):
        return 20, 0
    elif int(band) == 14 and (int(bw) in [5, 10]):
        return 15, 0
    elif int(band) == 17 and int(bw) == 10:
        return 20, 30
    elif (int(band) == 18 in [18, 19, 21, 26, 28]) and int(bw) == 15:
        return 25, 50
    elif int(band) == 20 and int(bw) == 10:
        return 20, 0
    elif int(band) == 20 and int(bw) == 15:
        return 20, 11
    elif int(band) == 20 and int(bw) == 20:
        return 20, 16
    elif int(band) == 28 and int(bw) == 20:
        return 25, 75
    else:
        if int(bw) == 1.4:
            return 6, 0
        else:
            return int(bw) * 5, 0


def special_uplink_config_sensitivity_fr1(band, scs, bw):
    if int(band) == 1:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 50, 2
            elif bw == 15:
                return 75, 4
            elif bw == 20:
                return 100, 6
            elif bw == 25:
                return 128, 5
            elif bw == 30:
                return 128, 32
            elif bw == 40:
                return 128, 88
            elif bw == 50:
                return 128, 142

        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 15:
                return 36, 2
            elif bw == 20:
                return 50, 1
            elif bw == 25:
                return 64, 1
            elif bw == 30:
                return 64, 14
            elif bw == 40:
                return 64, 42
            elif bw == 50:
                return 64, 69
        elif scs == 60:
            if bw == 10:
                return 10, 1
            elif bw == 15:
                return 18, 0
            elif bw == 20:
                return 24, 0
            elif bw == 25:
                return 30, 1
            elif bw == 30:
                return 30, 8
            elif bw == 40:
                return 30, 21
            elif bw == 50:
                return 30, 35
    elif int(band) == 2:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 50, 2
            elif bw == 15:
                return 50, 29
            elif bw == 20:
                return 50, 56
        elif scs == 30:
            if bw == 5:
                return 10, 1
            elif bw == 10:
                return 24, 0
            elif bw == 15:
                return 24, 14
            elif bw == 20:
                return 24, 27
        elif scs == 60:
            if bw == 10:
                return 10, 1
            elif bw == 15:
                return 10, 8
            elif bw == 20:
                return 10, 14
    elif int(band) == 3:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 50, 2
            elif bw == 15:
                return 50, 29
            elif bw == 20:
                return 50, 56
            elif bw == 25:
                return 50, 83
            elif bw == 30:
                return 50, 110
            elif bw == 40:
                return 50, 166
        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 15:
                return 24, 14
            elif bw == 20:
                return 24, 27
            elif bw == 25:
                return 24, 41
            elif bw == 30:
                return 24, 54
            elif bw == 40:
                return 24, 82
        elif scs == 60:
            if bw == 10:
                return 10, 1
            elif bw == 15:
                return 10, 8
            elif bw == 20:
                return 10, 14
            elif bw == 25:
                return 10, 21
            elif bw == 30:
                return 10, 28
            elif bw == 40:
                return 10, 41
    elif int(band) == 5:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 25, 27
            elif bw == 15:
                return 25, 54
            elif bw == 20:
                return 25, 81
        elif scs == 30:
            if bw == 10:
                return 10, 14
            elif bw == 15:
                return 10, 28
            elif bw == 20:
                return 10, 41
    elif int(band) == 7:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 50, 2
            elif bw == 15:
                return 75, 4
            elif bw == 20:
                return 75, 31
            elif bw == 25:
                return 64, 32
            elif bw == 40:
                return 108, 54
            elif bw == 50:
                return 135, 67
        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 15:
                return 36, 2
            elif bw == 20:
                return 36, 15
            elif bw == 25:
                return 32, 16
            elif bw == 40:
                return 50, 25
            elif bw == 50:
                return 64, 32
        elif scs == 60:
            if bw == 10:
                return 10, 1
            elif bw == 15:
                return 18, 0
            elif bw == 20:
                return 18, 6
            elif bw == 25:
                return 15, 7
            elif bw == 40:
                return 25, 12
            elif bw == 50:
                return 32, 16
    elif int(band) == 8:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 25, 27
            elif bw == 15:
                return 25, 54
            elif bw == 20:
                return 25, 81
        elif scs == 30:
            if bw == 10:
                return 10, 14
            elif bw == 15:
                return 10, 28
            elif bw == 20:
                return 10, 41
    elif int(band) == 12:
        if scs == 15:
            if bw == 5:
                return 20, 5
            elif bw == 10:
                return 20, 32
            elif bw == 15:
                return 20, 59
        elif scs == 30:
            if bw == 10:
                return 10, 14
            elif bw == 15:
                return 10, 28
    elif int(band) == 14:
        if scs == 15:
            if bw == 5:
                return 20, 5
            elif bw == 10:
                return 20, 32
        elif scs == 30:
            if bw == 10:
                return 10, 14
    elif int(band) == 18:
        if scs == 15:
            if bw == 5:
                return 20, 5
            elif bw == 10:
                return 20, 32
            elif bw == 15:
                return 20, 59
        elif scs == 30:
            if bw == 10:
                return 10, 14
            elif bw == 15:
                return 10, 28
    elif int(band) == 20:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 20, 0
            elif bw == 15:
                return 20, 11
            elif bw == 20:
                return 20, 16
        elif scs == 30:
            if bw == 10:
                return 10, 0
            elif bw == 15:
                return 10, 6
            elif bw == 20:
                return 10, 8
    elif int(band) == 24:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 50, 0
        elif scs == 30:
            if bw == 10:
                return 24, 0
        elif scs == 60:
            if bw == 10:
                return 10, 0
    elif int(band) == 25:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 50, 0
            elif bw == 15:
                return 50, 29
            elif bw == 20:
                return 50, 56
        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 15:
                return 24, 14
            elif bw == 20:
                return 24, 27
        elif scs == 60:
            if bw == 10:
                return 10, 0
            elif bw == 15:
                return 10, 8
            elif bw == 20:
                return 10, 14
    elif int(band) == 26:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 25, 27
            elif bw == 15:
                return 25, 54
            elif bw == 20:
                return 25, 81
        elif scs == 30:
            if bw == 5:
                return 12, 12
            elif bw == 10:
                return 12, 26
            elif bw == 15:
                return 12, 39
    elif int(band) == 28:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 25, 27
            elif bw == 15:
                return 25, 54
            elif bw == 20:
                return 25, 81
            elif bw == 30:
                return 25, 135
        elif scs == 30:
            if bw == 10:
                return 10, 14
            elif bw == 15:
                return 10, 28
            elif bw == 20:
                return 10, 41
            elif bw == 30:
                return 10, 68
    elif int(band) == 30:
        if scs == 15:
            if bw == 5:
                return 25, 5
            elif bw == 10:
                return 20, 32
        elif scs == 30:
            if bw == 10:
                return 10, 14
    elif int(band) == 34:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 50, 0
            elif bw == 15:
                return 75, 0
        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 15:
                return 36, 0
        elif scs == 60:
            if bw == 10:
                return 10, 0
            elif bw == 15:
                return 18, 0
    elif int(band) == 38:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 50, 0
            elif bw == 15:
                return 75, 0
            elif bw == 20:
                return 100, 0
            elif bw == 25:
                return 128, 0
            elif bw == 40:
                return 216, 0
        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 15:
                return 36, 0
            elif bw == 20:
                return 50, 0
            elif bw == 25:
                return 64, 0
            elif bw == 40:
                return 100, 0
        elif scs == 60:
            if bw == 10:
                return 10, 0
            elif bw == 15:
                return 18, 0
            elif bw == 20:
                return 24, 0
            elif bw == 25:
                return 30, 0
            elif bw == 40:
                return 50, 0
    elif int(band) == 39:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 50, 0
            elif bw == 15:
                return 75, 0
            elif bw == 20:
                return 100, 0
            elif bw == 25:
                return 128, 0
            elif bw == 30:
                return 160, 0
            elif bw == 40:
                return 216, 0
        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 15:
                return 36, 0
            elif bw == 20:
                return 50, 0
            elif bw == 25:
                return 64, 0
            elif bw == 30:
                return 75, 0
            elif bw == 40:
                return 100, 0
        elif scs == 60:
            if bw == 10:
                return 10, 0
            elif bw == 15:
                return 18, 0
            elif bw == 20:
                return 24, 0
            elif bw == 25:
                return 30, 0
            elif bw == 30:
                return 36, 0
            elif bw == 40:
                return 50, 0
    elif int(band) == 40:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 50, 0
            elif bw == 15:
                return 75, 0
            elif bw == 20:
                return 100, 0
            elif bw == 25:
                return 128, 0
            elif bw == 30:
                return 160, 0
            elif bw == 40:
                return 216, 0
            elif bw == 50:
                return 270, 0
        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 15:
                return 36, 0
            elif bw == 20:
                return 50, 0
            elif bw == 25:
                return 64, 0
            elif bw == 30:
                return 75, 0
            elif bw == 40:
                return 100, 0
            elif bw == 50:
                return 128, 0
            elif bw == 60:
                return 162, 0
            elif bw == 80:
                return 216, 0
        elif scs == 60:
            if bw == 10:
                return 10, 0
            elif bw == 15:
                return 18, 0
            elif bw == 20:
                return 24, 0
            elif bw == 25:
                return 30, 0
            elif bw == 30:
                return 36, 0
            elif bw == 40:
                return 50, 0
            elif bw == 50:
                return 64, 0
            elif bw == 60:
                return 75, 0
            elif bw == 80:
                return 100, 0
    elif int(band) == 41:
        if scs == 15:
            if bw == 10:
                return 50, 0
            elif bw == 15:
                return 75, 0
            elif bw == 20:
                return 100, 0
            elif bw == 30:
                return 160, 0
            elif bw == 40:
                return 216, 0
            elif bw == 50:
                return 270, 0
        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 15:
                return 36, 0
            elif bw == 20:
                return 50, 0
            elif bw == 30:
                return 75, 0
            elif bw == 40:
                return 100, 0
            elif bw == 50:
                return 128, 0
            elif bw == 60:
                return 162, 0
            elif bw == 80:
                return 216, 0
            elif bw == 90:
                return 243, 0
            elif bw == 100:
                return 270, 0
        elif scs == 60:
            if bw == 10:
                return 10, 0
            elif bw == 15:
                return 18, 0
            elif bw == 20:
                return 24, 0
            elif bw == 30:
                return 36, 0
            elif bw == 40:
                return 50, 0
            elif bw == 50:
                return 64, 0
            elif bw == 60:
                return 75, 0
            elif bw == 80:
                return 100, 0
            elif bw == 90:
                return 120, 0
            elif bw == 100:
                return 135, 0
    elif int(band) == 48:
        if scs == 15:
            if bw == 10:
                return 50, 0
            elif bw == 15:
                return 75, 0
            elif bw == 20:
                return 100, 0
            elif bw == 25:
                return 128, 0
            elif bw == 40:
                return 216, 0
            elif bw == 50:
                return 270, 0
        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 15:
                return 36, 0
            elif bw == 20:
                return 50, 0
            elif bw == 25:
                return 64, 0
            elif bw == 40:
                return 100, 0
            elif bw == 50:
                return 128, 0
            elif bw == 60:
                return 162, 0
            elif bw == 80:
                return 216, 0
            elif bw == 90:
                return 243, 0
            elif bw == 100:
                return 270, 0
        elif scs == 60:
            if bw == 10:
                return 10, 0
            elif bw == 15:
                return 18, 0
            elif bw == 20:
                return 24, 0
            elif bw == 25:
                return 30, 0
            elif bw == 40:
                return 50, 0
            elif bw == 50:
                return 64, 0
            elif bw == 60:
                return 75, 0
            elif bw == 80:
                return 100, 0
            elif bw == 90:
                return 120, 0
            elif bw == 100:
                return 135, 0
    elif int(band) == 50:
        if scs == 15:
            if bw == 10:
                return 50, 0
            elif bw == 15:
                return 75, 0
            elif bw == 20:
                return 100, 0
            elif bw == 40:
                return 216, 0
            elif bw == 50:
                return 270, 0
        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 15:
                return 36, 0
            elif bw == 20:
                return 50, 0
            elif bw == 40:
                return 100, 0
            elif bw == 50:
                return 128, 0
            elif bw == 60:
                return 162, 0
            elif bw == 80:  # note 3?
                return 216, 0
        elif scs == 60:
            if bw == 10:
                return 10, 0
            elif bw == 15:
                return 18, 0
            elif bw == 20:
                return 24, 0
            elif bw == 40:
                return 50, 0
            elif bw == 50:
                return 64, 0
            elif bw == 60:
                return 75, 0
            elif bw == 80:  # note 3?
                return 100, 0
    elif int(band) == 51:
        if scs == 15:
            if bw == 5:
                return 25, 0
    elif int(band) == 53:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 50, 0
        elif scs == 30:
            if bw == 10:
                return 24, 0
        elif scs == 60:
            if bw == 10:
                return 10, 0
    elif int(band) == 65:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 50, 2
            elif bw == 15:
                return 75, 4
            elif bw == 20:
                return 100, 6
        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 15:
                return 36, 2
            elif bw == 15:
                return 50, 1
        elif scs == 60:
            if bw == 10:
                return 10, 1
            elif bw == 15:
                return 18, 0
    elif int(band) == 66:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 50, 2
            elif bw == 15:
                return 75, 4
            elif bw == 20:
                return 100, 6
            elif bw == 25:
                return 128, 5
            elif bw == 30:
                return 160, 0
            elif bw == 40:
                return 216, 0
        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 15:
                return 36, 2
            elif bw == 20:
                return 50, 1
            elif bw == 25:
                return 64, 1
            elif bw == 30:
                return 75, 3
            elif bw == 40:
                return 100, 6
        elif scs == 60:
            if bw == 10:
                return 10, 1
            elif bw == 15:
                return 18, 0
            elif bw == 20:
                return 24, 0
            elif bw == 25:
                return 30, 1
            elif bw == 30:
                return 36, 2
            elif bw == 40:
                return 50, 1
    elif int(band) == 70:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 50, 2
            elif bw == 15:
                return 75, 4
            elif bw == 20:  # note 3?
                return 100, 6
            elif bw == 25:  # note 3?
                return 128, 5
        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 15:
                return 36, 2
            elif bw == 20:  # note 3?
                return 50, 1
            elif bw == 25:  # note 3?
                return 64, 1
        elif scs == 60:
            if bw == 10:
                return 10, 1
            elif bw == 15:
                return 18, 0
            elif bw == 20:
                return 24, 0  # note 3?
            elif bw == 25:
                return 30, 1  # note 3?
    elif int(band) == 71:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 25, 0
            elif bw == 15:
                return 20, 0
            elif bw == 20:
                return 20, 0
        elif scs == 30:
            if bw == 10:
                return 12, 0
            elif bw == 15:
                return 10, 0
            elif bw == 20:
                return 10, 0
    elif int(band) == 74:
        if scs == 15:
            if bw == 5:
                return 25, 0
            elif bw == 10:
                return 25, 27
            elif bw == 15:
                return 25, 54
            elif bw == 20:
                return 25, 81
        elif scs == 30:
            if bw == 10:
                return 10, 14
            elif bw == 15:
                return 10, 28
            elif bw == 20:
                return 10, 41
        elif scs == 60:
            if bw == 10:
                return 5, 6
            elif bw == 15:
                return 5, 13
            elif bw == 20:
                return 5, 19
    elif int(band) == 77:
        if scs == 15:
            if bw == 10:
                return 50, 0
            elif bw == 15:
                return 75, 0
            elif bw == 20:
                return 100, 0
            elif bw == 25:
                return 128, 0
            elif bw == 40:
                return 216, 0
            elif bw == 50:
                return 270, 0
        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 15:
                return 36, 0
            elif bw == 20:
                return 50, 0
            elif bw == 25:
                return 64, 0
            elif bw == 40:
                return 100, 0
            elif bw == 50:
                return 128, 0
            elif bw == 60:
                return 162, 0
            elif bw == 80:
                return 216, 0
            elif bw == 90:
                return 243, 0
            elif bw == 100:
                return 270, 0
        elif scs == 60:
            if bw == 10:
                return 10, 0
            elif bw == 15:
                return 18, 0
            elif bw == 20:
                return 24, 0
            elif bw == 25:
                return 30, 0
            elif bw == 40:
                return 50, 0
            elif bw == 50:
                return 64, 0
            elif bw == 60:
                return 75, 0
            elif bw == 80:
                return 100, 0
            elif bw == 90:
                return 120, 0
            elif bw == 100:
                return 135, 0
    elif int(band) == 78:
        if scs == 15:
            if bw == 10:
                return 50, 0
            elif bw == 15:
                return 75, 0
            elif bw == 20:
                return 100, 0
            elif bw == 25:
                return 128, 0
            elif bw == 40:
                return 216, 0
            elif bw == 50:
                return 270, 0
        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 15:
                return 36, 0
            elif bw == 20:
                return 50, 0
            elif bw == 25:
                return 64, 0
            elif bw == 40:
                return 100, 0
            elif bw == 50:
                return 128, 0
            elif bw == 60:
                return 162, 0
            elif bw == 80:
                return 216, 0
            elif bw == 90:
                return 243, 0
            elif bw == 100:
                return 270, 0
        elif scs == 60:
            if bw == 10:
                return 10, 0
            elif bw == 15:
                return 18, 0
            elif bw == 20:
                return 24, 0
            elif bw == 25:
                return 30, 0
            elif bw == 40:
                return 50, 0
            elif bw == 50:
                return 64, 0
            elif bw == 60:
                return 75, 0
            elif bw == 80:
                return 100, 0
            elif bw == 90:
                return 120, 0
            elif bw == 100:
                return 135, 0
    elif int(band) == 79:
        if scs == 15:
            if bw == 40:
                return 216, 0
            elif bw == 50:
                return 270, 0
        elif scs == 30:
            if bw == 10:
                return 24, 0
            elif bw == 20:
                return 50, 0
            elif bw == 40:
                return 100, 0
            elif bw == 50:
                return 128, 0
            elif bw == 60:
                return 162, 0
            elif bw == 80:
                return 216, 0
            elif bw == 90:
                return 243, 0
            elif bw == 100:
                return 270, 0
        elif scs == 60:
            if bw == 40:
                return 50, 0
            elif bw == 50:
                return 64, 0
            elif bw == 60:
                return 75, 0
            elif bw == 80:
                return 100, 0
            elif bw == 100:
                return 135, 0


def main():
    """
    this main() function is used for testing some function
    """

    print(transfer_freq2chan_gsm(1800, 1747500, 'tx'))


if __name__ == "__main__":
    main()
