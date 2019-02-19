import logging
import subprocess

from logging import DEBUG, INFO, WARNING, ERROR

from os.path import join, exists
from sys import stdout

path = 'logs'

def add_logger(name, level):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter('%(message)s')

        log_file = join(path, f'{name}.log')
        
        if not exists(path):
            subprocess.run(["mkdir", path])

        if not exists(log_file):
            subprocess.run(["touch", log_file])

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stdout_handler = logging.StreamHandler(stdout)
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)

    return logger
