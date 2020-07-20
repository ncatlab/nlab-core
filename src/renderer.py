#!/usr/bin/python3

import argparse
import logging
import mistletoe
import os
import sys
import time

"""
Initialises logging. Logs to

renderer.log
"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.Formatter.converter = time.gmtime
logging_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s")
log_directory = os.environ["NLAB_LOG_DIRECTORY"]
logging_file_handler = logging.FileHandler(
    os.path.join(log_directory, "renderer.log"))
logging_file_handler.setFormatter(logging_formatter)
logger.addHandler(logging_file_handler)

def render(page_id, page_content):
    return mistletoe.markdown(page_content)

"""
Sets up the command line argument parsing
"""
def argument_parser():
    parser = argparse.ArgumentParser(
        description = (
            "Renders the content of an nLab page, which should be passed on " +
            "stdin"))
    parser.add_argument(
        "page_id",
        help = "Id of nLab page")
    return parser

def main():
    parser = argument_parser()
    arguments = parser.parse_args()
    page_id = arguments.page_id
    page_content = sys.stdin.read()
    logger.info("Beginning rendering page with id: " + str(page_id))
    try:
        print(render(page_id, page_content))
    except Exception as exception:
        logger.warning(
            "An unexpected error occurred when rendering page with id: " +
            str(page_id) +
            ". Error: " +
            str(exception))
        sys.exit("An unexpected error occurred")

if __name__ == "__main__":
    main()
