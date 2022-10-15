import pathlib
import logging
from logging.config import fileConfig

def log_set():
    config_file = pathlib.Path('./utils/logging.ini')
    fileConfig(config_file)
    logger = logging.getLogger()
    return logger

def main():
    pass

if __name__ == '__main__':
    main()