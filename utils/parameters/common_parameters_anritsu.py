IMSI = '001010123456789'

ANRITSU_OFF = 0  # Call processing function set to Off
ANRITSU_IDLE = 1  # Idle state
ANRITSU_IDLE_REGIST = 2  # Idle( Regist ) Idle state (location registered)
ANRITSU_REGIST = 3			# Under location registration
ANRITSU_CONNECTED = 6  # Under communication or connected for LTE
ANRITSU_LOOP_MODE_1 = 7  # Loopback mode 1 for WCDMA
ANRITSU_LOOP_MODE_1_OPEN = 8  # Loop mode(open)
ANRITSU_LOOP_MODE_1_CLOSE = 9  # loop mode(close)

MESUREMENT_GOOD = 0  # if the measurement status is good
MESUREMENT_BAD = 5  # if the measurement status is bad, it might be low reference signal
MESUREMENT_TIMEOUT = 13
MESUREMENT_X = 7

HSUPA_ETFCI_SUBTEST1 = 75
HSUPA_ETFCI_SUBTEST2 = 67
HSUPA_ETFCI_SUBTEST3 = 92
HSUPA_ETFCI_SUBTEST4 = 71
HSUPA_ETFCI_SUBTEST5 = 81  # this is for old versionm before v8.7.0, now not used

SWEEP_STEP = 2  # this is step when sensitivity all channel sweep
CHAN_LIST = []  # if wanting to measure single channel when RX sweep by special resason, use it. Or let it empty

# bandwidth index
def bandwidths_selected(band):
    bandwidths = {
        'B1': [5, 10 , 15, 20],
        'B2': [1.4, 3, 5, 10 , 15, 20],
        'B3': [1.4, 3, 5, 10 , 15, 20],
        'B4': [1.4, 3, 5, 10 , 15, 20],
        'B5': [1.4, 3, 5, 10],
        'B7': [5, 10 , 15, 20],
        'B8': [1.4, 3, 5, 10],
        'B12': [1.4, 3, 5, 10],
        'B13': [5, 10],
        'B14': [5, 10],
        'B17': [5, 10],
        'B18': [5, 10, 15],
        'B19': [5, 10, 15],
        'B20': [5, 10 , 15, 20],
        'B21': [5, 10, 15],
        'B25': [1.4, 3, 5, 10, 15, 20],
        'B26': [1.4, 3, 5, 10, 15],
        'B28': [3, 5, 10, 15, 20],
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
        'B66': [1.4, 3, 5, 10 , 15, 20],
        'B70': [5, 10, 15, 20],
        'B71': [5, 10, 15, 20],
        'B75': [5, 10, 15, 20],
    }

    return bandwidths[f'B{band}']

# DL channel
def dl_ch_selected(standard, band, bw=5):
    band_dl_ch_lte = {
        'B1': [int((0 + bw / 2 * 10)), 300, int(599 - (bw / 2) * 10 + 1)],
        'B2': [int((600 + bw / 2 * 10)), 900, int(1199 - (bw / 2) * 10 + 1 )],
        'B3': [int((1200 + bw / 2 * 10)), 1575, int(1949 - (bw / 2) * 10 + 1)],
        'B4': [int((1950 + bw / 2 * 10)), 2175, int(2399 - (bw / 2) * 10 + 1)],
        'B5': [int((2400 + bw / 2 * 10)), 2525, int(2649 - (bw / 2) * 10 + 1)],
        'B7': [int((2750 + bw / 2 * 10)), 3100, int(3449 - (bw / 2) * 10 + 1)],
        'B8': [int((3450 + bw / 2 * 10)), 3625, int(3799 - (bw / 2) * 10 + 1)],
        'B12': [int((5010 + bw / 2 * 10)), 5095, int(5179 - (bw / 2) * 10 + 1)],
        'B13': [int((5180 + bw / 2 * 10)), 5230, int(5279 - (bw / 2) * 10 + 1)],
        'B14': [int((5280 + bw / 2 * 10)), 5330, int(5379 - (bw / 2) * 10 + 1)],
        'B17': [int((5730 + bw / 2 * 10)), 5790, int(5849 - (bw / 2) * 10 + 1)],
        'B18': [int((5850 + bw / 2 * 10)), 5925, int(5999 - (bw / 2) * 10 + 1)],
        'B19': [int((6000 + bw / 2 * 10)), 6075, int(6149 - (bw / 2) * 10 + 1)],
        'B20': [int((6150 + bw / 2 * 10)), 6300, int(6449 - (bw / 2) * 10 + 1)],
        'B21': [int((6450 + bw / 2 * 10)), 6525, int(6599 - (bw / 2) * 10 + 1)],
        'B25': [int((8040 + bw / 2 * 10)), 8365, int(8689 - (bw / 2) * 10 + 1)],
        'B26': [int((8690 + bw / 2 * 10)), 8865, int(9039 - (bw / 2) * 10 + 1)],
        'B28': [int((9210 + bw / 2 * 10)), 9435, int(9659 - (bw / 2) * 10 + 1)],
        'B28A': [int((9210 + bw / 2 * 10)), 9360, int(9509 - (bw / 2) * 10 + 1)],
        'B28B': [int((9360 + bw / 2 * 10)), 9510, int(9659 - (bw / 2) * 10 + 1)],
        'B29': [int((9660 + bw / 2 * 10)), 9715, int(9769 - (bw / 2) * 10 + 1)],
        'B30': [int((9770 + bw / 2 * 10)), 9820, int(9869 - (bw / 2) * 10 + 1)],
        'B32': [int((9920 + bw / 2 * 10)), 10140, int(10359 - (bw / 2) * 10 + 1)],
        'B38': [int((37750 + bw / 2 * 10)), 38000, int(38249 - (bw / 2) * 10 + 1)],
        'B39': [int((38250 + bw / 2 * 10)), 38450, int(38649 - (bw / 2) * 10 + 1)],
        'B40': [int((38650 + bw / 2 * 10)), 39150, int(39649 - (bw / 2) * 10 + 1)],
        'B41': [int((39650 + bw / 2 * 10)), 40620, int(41589 - (bw / 2) * 10 + 1)],
        'B42': [int((41590 + bw / 2 * 10)), 42590, int(43589 - (bw / 2) * 10 + 1)],
        'B46': [int((46790 + bw / 2 * 10)), 50665, int(54539 - (bw / 2) * 10 + 1)],
        'B48': [int((55240 + bw / 2 * 10)), 55990, int(56739 - (bw / 2) * 10 + 1)],
        'B66': [int((66436 + bw / 2 * 10)), 66786, int(67135 - (bw / 2) * 10 + 1)],
        'B71': [int((68586 + bw / 2 * 10)), 68761, int(68935 - (bw / 2) * 10 + 1)],
        'B75': [int((69466 + bw / 2 * 10)), 69891, int(70315 - (bw / 2) * 10 + 1)],

    }

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

    if standard == 'LTE':
        if band == 28:
            from want_test_band import band_segment
            return band_dl_ch_lte[f'B{band}{band_segment}']
        else:
            return band_dl_ch_lte[f'B{band}']
    elif standard == 'WCDMA':
        return band_dl_ch_wcdma[f'B{band}']
    elif 'GSM':
        pass


def special_uplink_config_sensitivity(band, bw):
    if (int(band) in [2,3,25]) and int(bw) == 15:
        return 50, 25
    elif (int(band) in [2,3,25]) and int(bw) == 20:
        return 50, 50
    elif int(band) in [5,8,18,19,21,26,28,30]  and int(bw) == 10:
        return 25, 25
    elif int(band) == 7 and int(bw) == 20:
        return 75, 25
    elif int(band) == 7 and int(bw) == 20:
        return 75, 25
    elif int(band) in [12,17] and int(bw) == 5:
        return 20, 5
    elif int(band) == 12 and int(bw) == 10:
        return 20, 30
    elif int(band) == 13 and (int(bw) in [5,10]):
        return 20, 0
    elif int(band) == 14 and (int(bw) in [5,10]):
        return 15, 0
    elif int(band) == 17 and int(bw) == 10:
        return 20, 30
    elif (int(band) == 18 in [18,19,21,26,28]) and int(bw) == 15:
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





def main():
    """
    this main() function is used for testing some function
    """

    # print(dl_ch_selected('LTE', 1, 10))
    # print(dl_ch_selected('WCDMA', 5))
    # for _ in [1.4, 3, 5, 10]:
    #     if _ in bandwidths_selected(1):
    #         print(_)
    #     else:
    #         continue

    if CHAN_LIST:
        print(CHAN_LIST)
    else:
        print('others')


if __name__ == "__main__" :
    main()
