from pathlib import Path
import logging
import sys
from logging.config import fileConfig

def log_set_old():
    config_file = Path('logging.ini')
    fileConfig(config_file)
    logger = logging.getLogger()
    return logger

def log_set(name=__name__):
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    handler_stream = logging.StreamHandler(stream=sys.stdout)
    handler_stream.setLevel(logging.INFO)
    handler_console = logging.FileHandler('log.txt', mode='w')
    handler_console.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('[%(asctime)s %(name)-8s - %(levelname)-8s] %(message)s', datefmt='%Y%m%d %H:%M:%S')


    # add formatter to handlers
    handler_stream.setFormatter(formatter)
    handler_console.setFormatter(formatter)

    # add handlers to logger
    logger.addHandler(handler_stream)
    logger.addHandler(handler_console)

    return logger

def main():
    log_set()
    logging.info('test123')

if __name__ == '__main__':
    main()