def query_rsrp_cinr_wcdma(self):
    res = self.command(f'AT+LRXMEAS={self.rx_path_lte},20')
    for line in res:
        if '+LRXMEAS:' in line.decode():
            self.rsrp_list = line.decode().split(':')[1].strip().split(',')[:4]
            self.cinr_list = line.decode().split(':')[1].strip().split(',')[4:]
            self.rsrp_list = [eval(rsrp) / 100 for rsrp in self.rsrp_list]
            self.cinr_list = [eval(cinr) / 100 for cinr in self.cinr_list]
            logger.info(f'**** RSRP: {self.rsrp_list} ****')
            logger.info(f'**** CINR: {self.cinr_list} ****')


def query_rsrp_cinr_lte(self):
    res = self.command(f'AT+LRXMEAS={self.rx_path_lte},20')
    for line in res:
        if '+LRXMEAS:' in line.decode():
            self.rsrp_list = line.decode().split(':')[1].strip().split(',')[:4]
            self.cinr_list = line.decode().split(':')[1].strip().split(',')[4:]
            self.rsrp_list = [eval(rsrp) / 100 for rsrp in self.rsrp_list]
            self.cinr_list = [eval(cinr) / 100 for cinr in self.cinr_list]
            logger.info(f'**** RSRP: {self.rsrp_list} ****')
            logger.info(f'**** CINR: {self.cinr_list} ****')


def query_rsrp_cinr_fr1(self):
    res = self.command(f'AT+NRXMEAS={self.rx_path_fr1},20')
    for line in res:
        if '+NRXMEAS:' in line.decode():
            self.rsrp_list = line.decode().split(':')[1].strip().split(',')[:4]
            self.cinr_list = line.decode().split(':')[1].strip().split(',')[4:]
            self.rsrp_list = [eval(rsrp) / 100 for rsrp in self.rsrp_list]
            self.cinr_list = [eval(cinr) / 100 for cinr in self.cinr_list]
            logger.info(f'**** RSRP: {self.rsrp_list} ****')
            logger.info(f'**** CINR: {self.cinr_list} ****')


def query_agc_wcdma(self):
    res = self.command(f'AT+LRX1RX2AGCIDXRD')
    for line in res:
        if '+LRX1RX2AGCIDXRD:' in line.decode():
            self.agc_list = line.decode().split(':')[1].strip().split(',')
            self.agc_list = [eval(agc) for agc in self.agc_list]
            logger.info(f'**** AGC: {self.agc_list} ****')


def query_agc_lte(self):
    res = self.command(f'AT+LRX1RX2AGCIDXRD')
    for line in res:
        if '+LRX1RX2AGCIDXRD:' in line.decode():
            self.agc_list = line.decode().split(':')[1].strip().split(',')
            self.agc_list = [eval(agc) for agc in self.agc_list]
            logger.info(f'**** AGC: {self.agc_list} ****')


def query_agc_fr1(self):
    res = self.command(f'AT+NAGCIDXRD')
    for line in res:
        if '+NRX1RX2AGCIDXRD:' in line.decode():
            self.agc_list = line.decode().split(':')[1].strip().split(',')
            self.agc_list = [eval(agc) for agc in self.agc_list]
            logger.info(f'**** AGC: {self.agc_list} ****')


def get_esens_wcdma(self):
    self.esens_list = [round(self.rx_level - c - 1, 2) for c in self.cinr_list]
    logger.info(f'**** ESENS: {self.esens_list} ****')


def get_esens_lte(self):
    self.esens_list = [round(self.rx_level - c - 1, 2) for c in self.cinr_list]
    logger.info(f'**** ESENS: {self.esens_list} ****')


def get_esens_fr1(self):
    self.esens_list = [round(self.rx_level - c - 1, 2) for c in self.cinr_list]
    logger.info(f'**** ESENS: {self.esens_list} ****')


def query_rx_measure_wcdma(self):
    self.query_rsrp_cinr_wcdma()
    self.query_agc_wcdma()
    self.get_esens_wcdma()


def query_rx_measure_lte(self):
    self.query_rsrp_cinr_lte()
    self.query_agc_lte()
    self.get_esens_lte()


def query_rx_measure_fr1(self):
    self.query_rsrp_cinr_fr1()
    self.query_agc_fr1()
    self.get_esens_fr1()


def query_fer_measure_gsm(self):
    logger.info('========== FER measure ==========')
    self.sig_gen_gsm()
    self.sync_gsm()
    res = self.command(f'AT+TESTBER={self.band_tx_set_dict_gsm[self.band_gsm]},{self.mod_dict_gsm[self.mod_gsm]},'
                       f'0,1,{self.rx_chan_gsm},{-1 * int(round(self.rx_level, 0))},7,2', delay=0.5)
    for line in res:
        if '+TESTBER: ' in line.decode():
            results = eval(line.decode().split(': ')[1])
            self.rssi, self.fer = [round(r / 100, 2) for r in results]
            logger.info(f'****RSSI: {self.rssi} ****')
            logger.info(f'****FER: {self.fer} %****')


def query_fer_measure_wcdma(self):
    logger.info('========== FER measure ==========')
    res = self.command('AT+HGETSENSE=100', delay=2)
    for line in res:
        if '+GETSENSE:' in line.decode():
            self.fer = eval(line.decode().split(':')[1])
            logger.info(f'****FER: {self.fer / 1000} %****')


def query_fer_measure_lte(self):
    logger.info('========== FER measure ==========')
    res = self.command('AT+LFERMEASURE=500', delay=0.5)
    for line in res:
        if '+LFERMEASURE:' in line.decode():
            self.fer = eval(line.decode().split(':')[1])
            logger.info(f'****FER: {self.fer / 100} %****')


def query_fer_measure_fr1(self):
    logger.info('========== FER measure ==========')
    res = self.command('AT+NFERMEASURE=500', delay=0.5)
    for line in res:
        if '+NFERMEASURE:' in line.decode():
            self.fer = eval(line.decode().split(':')[1])
            logger.info(f'****FER: {self.fer / 100} %****')


def search_window_gsm(self):
    rssi = None
    self.query_fer_measure_gsm()
    while self.fer < 2:
        rssi = self.rssi
        self.rx_level = round(self.rx_level - self.window, 1)  # to reduce a unit
        # self.set_rx_level()
        self.query_fer_measure_gsm()
    return rssi
    # self.command_cmw100_query('*OPC?')


def search_window_wcdma(self):
    self.query_fer_measure_wcdma()
    while self.fer < 100:
        self.rx_level = round(self.rx_level - self.window, 1)  # to reduce a unit
        self.set_rx_level()
        self.query_fer_measure_wcdma()
        # self.command_cmw100_query('*OPC?')


def search_window_lte(self):
    self.query_fer_measure_lte()
    while self.fer < 500:
        self.rx_level = round(self.rx_level - self.window, 1)  # to reduce a unit
        self.set_rx_level()
        self.query_fer_measure_lte()
        # self.command_cmw100_query('*OPC?')


def search_window_fr1(self):
    self.query_fer_measure_fr1()
    while self.fer < 500:
        self.rx_level = round(self.rx_level - self.window, 1)  # to reduce a unit
        self.set_rx_level()
        self.query_fer_measure_fr1()
        # self.command_cmw100_query('*OPC?')