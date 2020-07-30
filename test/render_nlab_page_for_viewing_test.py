#!/usr/bin/python3

import argparse
import os
import subprocess
import sys

from tools.testing import TestFailedException

def test_render_and_place_for_viewing():
    render_and_place_for_viewing_subprocess = subprocess.run(
        [
            "docker",
            "exec",
            "-it",
            os.environ["NLAB_DOCKER_PYTHON_IMAGE_NAME"],
            "python3",
            "render_nlab_page_for_viewing.py",
            "1"
        ])
    render_and_place_for_viewing_subprocess.check_returncode()
    curl_subprocess = subprocess.run(
        [
             "curl",
             "http://localhost:8000/nlab/show/title+of+test+page"
        ],
        capture_output = True,
        text = True)
    with open("resources/rendered_page_without_nforum_discussion.html") as \
            rendered_page_file:
        expected_rendered_page = rendered_page_file.read()
    actual_rendered_page = curl_subprocess.stdout
    if actual_rendered_page != expected_rendered_page:
        raise TestFailedException(
            "render_and_place_for_viewing",
            "Expected different from actual page",
             expected_rendered_page,
             actual_rendered_page)

def run_tests():
    test_render_and_place_for_viewing()

"""
Sets up the command line argument parsing
"""
def argument_parser():
    parser = argparse.ArgumentParser(
        description = (
            "Tests for render_nlab_page_for_viewing.py"))
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
