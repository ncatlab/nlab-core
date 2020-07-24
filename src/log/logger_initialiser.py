#!/usr/bin/python3

import logging
import os
import sys
import time

def initialise(identifier, log_file_name):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logging.Formatter.converter = time.gmtime
    logging_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s")
    log_directory = os.environ["NLAB_LOG_DIRECTORY"]
    logging_file_handler = logging.FileHandler(
        os.path.join(log_directory, log_file_name + ".log"))
    logging_file_handler.setFormatter(logging_formatter)
    logger.addHandler(logging_file_handler)
    return logger
