#!/usr/bin/python3

import argparse
import os
import subprocess
import sys

import tools.testing
from tools.testing import TestFailedException

_static_page = "<html><p>Test</p></html>"

def _create_static_page():
    static_page_directory = os.path.join(
        os.environ["NLAB_DEPLOYED_STATIC_ROOT_DIRECTORY"],
        "nlab",
        "show")
    subprocess.run(
        "docker exec -it nlab-nginx /bin/bash -c " +
            "'mkdir -p " +
            static_page_directory +
            "; echo -n \"" +
            _static_page +
            "\" > " +
            os.path.join(static_page_directory, "title+of+test+page") +
            "'",
        shell = True)

def test_view_static_page_if_already_rendered():
    _create_static_page()
    curl_subprocess = subprocess.run(
        [
             "curl",
             "http://localhost:8000/nlab/show/title+of+test+page"
        ],
        capture_output = True,
        text = True)
    actual_page = curl_subprocess.stdout
    if actual_page != _static_page:
        raise TestFailedException(
            "view_static_page_if_already_rendered",
            "Expected page for nginx different from actual page",
             _static_page,
             actual_page)

def test_view_static_page_if_not_already_rendered():
    tools.testing.launch_backend_server()
    curl_subprocess = subprocess.run(
        [
             "curl",
             "http://localhost:8000/nlab/show/title+of+test+page"
        ],
        capture_output = True,
        text = True)
    actual_page = curl_subprocess.stdout
    with open("resources/rendered_page_without_nforum_discussion.html") as \
            rendered_page_file:
        expected_page = rendered_page_file.read()
    if actual_page != expected_page:
        raise TestFailedException(
            "view_static_page_if_not_already_rendered",
            "Expected page for nginx different from actual page",
             expected_page,
             actual_page)

def _run_and_clean_up(test):
    try:
        test()
    finally:
        tools.testing.shutdown_backend_server_if_running()
        tools.testing.clean_up_static_root_directory()

def run_tests():
    _run_and_clean_up(test_view_static_page_if_already_rendered)
    _run_and_clean_up(test_view_static_page_if_not_already_rendered)

"""
Sets up the command line argument parsing
"""
def argument_parser():
    parser = argparse.ArgumentParser(
        description = (
            "Tests for backend.py"))
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
        run_tests()
    except TestFailedException as testFailedException:
        sys.exit(str(testFailedException))
    print("All tests passed")

if __name__ == "__main__":
    main()
