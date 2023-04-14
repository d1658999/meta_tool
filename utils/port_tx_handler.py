from pathlib import Path

FILE_PATH = Path('utils') / Path('port_table.txt')  # formal
# FILE_PATH = Path('port_table.txt')  # test

def port_tx_table_transfer():
    # Create an empty dictionary to hold the port mappings
    port_table = {
        'TX1': {},
        'TX2': {},
        'MIMO_TX1': {},
        'MIMO_TX2': {},
    }
    # Open the txt file for reading
    with open(FILE_PATH, 'r') as f:
        rows = f.readlines()
    
        # Loop over each row in the file
        for row in rows:
            # Split the row into port and band_list
            tx_path = row.split('=')[0].strip().split('_port_')[0]
            port = row.split('=')[0].strip().split('_port_')[1]
            bands_list = [b.strip() for b in row.split('=')[1].strip().split(',')]  # remove extra space if having

            # Add each key-value pair to the port_select dictionary
            if bands_list == ['']:
                continue
            else:
                for band in bands_list:
                    port_table[tx_path][band] = port


    return port_table  # {'TX1': {'1': '1', '5': '2', '48': '4'}, 'TX2': {'1': '3', , '78': '5',}}
            

def main():
    port_table = port_tx_table_transfer()
    print(port_table)
            
if __name__ == '__main__':
    main()

