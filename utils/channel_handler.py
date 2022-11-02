import utils.parameters.common_parameters_ftm as cm_pmt_ftm


def channel_freq_select(want_chan, freq_list):
    chan_freq_select_list = []
    for ch in want_chan:
        if ch == 'L':
            chan_freq_select_list.append(freq_list[0])
        elif ch == 'M':
            chan_freq_select_list.append(freq_list[1])
        elif ch == 'H':
            chan_freq_select_list.append(freq_list[2])
    return chan_freq_select_list


def chan_judge_gsm(band_gsm, rx_freq_gsm):
    if rx_freq_gsm < cm_pmt_ftm.dl_freq_selected('GSM', band_gsm, 0)[1]:
        return 'ch0'
    elif rx_freq_gsm == cm_pmt_ftm.dl_freq_selected('GSM', band_gsm, 0)[1]:
        return 'ch1'
    elif rx_freq_gsm > cm_pmt_ftm.dl_freq_selected('GSM', band_gsm, 0)[1]:
        return 'ch2'


def chan_judge_wcdma(band_wcdma, tx_freq_wcdma):
    rx_freq_wcdma = cm_pmt_ftm.transfer_freq_tx2rx_wcdma(band_wcdma, tx_freq_wcdma)
    if rx_freq_wcdma < cm_pmt_ftm.dl_freq_selected('WCDMA', band_wcdma, 5)[1]:
        return 'ch0'
    elif rx_freq_wcdma == cm_pmt_ftm.dl_freq_selected('WCDMA', band_wcdma, 5)[1]:
        return 'ch1'
    elif rx_freq_wcdma > cm_pmt_ftm.dl_freq_selected('WCDMA', band_wcdma, 5)[1]:
        return 'ch2'


def chan_judge_lte(band_lte, bw_lte, tx_freq_lte):
    rx_freq_lte = cm_pmt_ftm.transfer_freq_tx2rx_lte(band_lte, tx_freq_lte)
    if rx_freq_lte < cm_pmt_ftm.dl_freq_selected('LTE', band_lte, bw_lte)[1]:
        return 'ch0'
    elif rx_freq_lte == cm_pmt_ftm.dl_freq_selected('LTE', band_lte, bw_lte)[1]:
        return 'ch1'
    elif rx_freq_lte > cm_pmt_ftm.dl_freq_selected('LTE', band_lte, bw_lte)[1]:
        return 'ch2'


def chan_judge_fr1(band_fr1, bw_fr1, tx_freq_fr1):
    rx_freq_fr1 = cm_pmt_ftm.transfer_freq_tx2rx_fr1(band_fr1, tx_freq_fr1)
    if rx_freq_fr1 < cm_pmt_ftm.dl_freq_selected('FR1', band_fr1, bw_fr1)[1]:
        return 'ch0'
    elif rx_freq_fr1 == cm_pmt_ftm.dl_freq_selected('FR1', band_fr1, bw_fr1)[1]:
        return 'ch1'
    elif rx_freq_fr1 > cm_pmt_ftm.dl_freq_selected('FR1', band_fr1, bw_fr1)[1]:
        return 'ch2'


def main():
    pass


if __name__ == '__main__':
    main()
