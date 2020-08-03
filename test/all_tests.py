#!/usr/bin/python3

import argparse
import os
import subprocess

import backend_test
import nginx_test
import page_renderer_test
import render_nlab_page_for_viewing_test
from tools.testing import TestFailedException

"""
Sets up the command line argument parsing
"""
def argument_parser():
    parser = argparse.ArgumentParser(
        description = (
            "Runs all tests"))
    parser.add_argument(
        "-p",
        "--populate_database",
        action = "store_true",
        help = "Populate the database with test data. Default false, as " +
            "typically one will only need to do this once for each launching " +
            "of the MySQL container")
    return parser

def main():
    parser = argument_parser()
    arguments = parser.parse_args()
    if arguments.populate_database:
        subprocess.run(["tools/populate_database_with_test_data.sh"])
    try:
        page_renderer_test.run_tests()
        render_nlab_page_for_viewing_test.run_tests()
        backend_test.run_tests()
        nginx_test.run_tests()
    except TestFailedException as testFailedException:
        sys.exit(str(testFailedException))
    print("All tests passed")

if __name__ == "__main__":
     main()
