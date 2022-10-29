lte_bands = [5]       # 1,2,3,4,7,25,66,38,39,40,41,5,8,12,13,14,17,18,19,20,28,71,42,48
wcdma_bands = [5,8]
gsm_bands = [900, 850]  # 900, 1800, 1900, 850
hsupa_bands = [1]
hsdpa_bands = [1]
fr1_bands = [77, 78]
endc_bands = ["3_78"]  # "3_78", "2_77","66_77"
band_segment = 'A'  # 'A' | 'B' for B28A ,B28B
band_segment_fr1 = 'B'

lte_bandwidths = [10]     # 1.4, 3, 5, 10, 15, 20
fr1_bandwidths = [10]  # 10, 15, 20, 25, 30 , 40, 50, 60, 80, 90, 100, 70

tech = ['WCDMA']   # 'LTE' | 'WCDMA' | 'GSM' | 'HSUPA' | 'HSDPA' | 'FR1'
channel = 'LMH'  # 'LMH'

fdd_tdd_cross_test = 0     # this is only for 8821,  0: only measure one of FDD or TDD; 1: measure both FDD and TDD

tx_max_pwr_sensitivity = [1, 0]  # 1: Txmax power, 0: -10dBm

tx_level = 26
tx_level_endc_lte = 26
tx_level_endc_fr1 = 0
tx_pcl_lb = 5  # GMSK_MB: 0 ~ 15, EPSK_MB 2~15:
tx_pcl_mb = 0  # GMSK_MB: 0 ~ 15, EPSK_MB 2~15:
sa_nsa = 0
duty_cycle = 100  # 100 for NR TDD PC3, 50: for NR TDD PC2
init_rx_sync_level = -70

port_tx = 1
port_tx_lte = 1  # 1 ~ 8 default is  1
# port_rx_lte = 1  # 1 ~ 8 default is  1
port_tx_fr1 = 4  # 1 ~ 8 default is  1
# port_rx_fr1 = 1  # 1 ~ 8 default is  1
rfout_anritsu = 'MAIN'

asw_path = 0
srs_path = 0
odpm_enable = True
psu_enable = True
psu_voltage = 4.0
psu_current = 5.0
temp = 25
srs_path_enable = False
sync_path = 'Main'  # 'Main', 'CA#1', 'CA#2', 'CA#3'
tx_paths = ['TX1']   # 'TX1' | 'TX2' | 'MIMO
rx_paths = [15]  #  0: default(free run) | 1: DRX_ONLY | 2: PRX ONLY | 3: PRX+DRX | 4: 4RX_PRX(RX2) ONLY | 8: 4RX_DRX(RX3) ONLY | 12: 4RX_PRX(RX2) + 4RX_DRX(RX3) | 15: ALL PATH
condition = 'NV'

scripts = ['GENERAL']  # 'GENERAL' | 'FCC' | 'CE' | 'FACTORY'

mod_gsm = 'GMSK'  # 'GMSK' | 'EPSK'
type_fr1 = ['DFTS']  # 'DFTS' | 'CP'
mcs_lte = ['QPSK']   # 'QPSK' | 'Q16' | 'Q64' | 'Q256'
mcs_fr1 = ['QPSK', 'Q16', 'Q64', 'Q256']   # 'BPSK' | 'QPSK' | 'Q16' | 'Q64' | 'Q256'
rb_ftm_lte = ['FRB']  # 'PRB' | 'FRB'
rb_ftm_fr1 = ['OUTER_FULL']  #  'INNER_FULL' | 'OUTER_FULL' | 'INNER_1RB_LEFT' | 'INNER_1RB_RIGHT' | 'EDGE_1RB_LEFT' | 'EDGE_1RB_RIGHT' | 'EDGE_FULL_LEFT' | 'EDGE_FULL_RIGHT'
scs = [1]  # 0: 15KHz | 1: 30KHz | 2: 60KHz

tx_level_range_list = [-20, 26]  # tx_level_1, tx_level_2
tx_pcl_range_list_lb = [19, 5]  # tx_pcl_1, tx_pcl_2; GMSK_LB: 5 ~ 19, EPSK_LB: 8~19
tx_pcl_range_list_mb = [15, 0]  # tx_pcl_1, tx_pcl_2; GMSK_MB: 0 ~ 15, EPSK_MB: 2~15






def main():
    """
        test
    """
    print(wcdma_bands == [])

if __name__ == "__main__":
    main()
