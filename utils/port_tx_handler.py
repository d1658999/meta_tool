from pathlib import Path


def port_tx_table_transfer(txas_select):  # txas_select = 0/1
    # to determine the txas path
    file_path = Path('utils') / Path(f'port_table_txas_{txas_select}.txt')  # formal
    # file_path =  Path().cwd().parents[1] / Path('utils') / Path(f'port_table_txas_{txas_select}.txt')  # test

    # Create an empty dictionary to hold the port mappings
    port_table = {
        'TX1': {},
        'TX2': {},
        'MIMO_TX1': {},
        'MIMO_TX2': {},
    }
    # Open the txt file for reading
    with open(file_path, 'r') as f:
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
    port_table = port_tx_table_transfer(0)
    print(port_table)
            
if __name__ == '__main__':
    main()

