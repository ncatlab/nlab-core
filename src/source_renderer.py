#!/usr/bin/python3

import argparse
import mistletoe
import sys

import logging/logger_initialiser.py

"""
Initialises logging. Logs to

source_renderer.log
"""
logger = logger_initialiser.initialise(__name__, "source_renderer")

def render(page_id, page_content):
    return mistletoe.markdown(page_content)

"""
Sets up the command line argument parsing
"""
def argument_parser():
    parser = argparse.ArgumentParser(
        description = (
            "Renders the source of an nLab page, which should be passed on " +
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
    logger.info("Beginning rendering source of page with id: " + str(page_id))
    try:
        print(render(page_id, page_content))
    except Exception as exception:
        logger.warning(
            "An unexpected error occurred when rendering source of page with " +
            "id: " +
            str(page_id) +
            ". Error: " +
            str(exception))
        sys.exit("An unexpected error occurred")

if __name__ == "__main__":
    main()
