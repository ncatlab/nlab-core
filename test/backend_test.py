#!/usr/bin/python3

import argparse
import os
import subprocess
import sys

import tools.testing
from tools.testing import TestFailedException

def test_render_for_viewing_200():
    tools.testing.launch_backend_server()
    backend_port = os.environ["NLAB_BACKEND_PORT"]
    curl_backend_subprocess = subprocess.run(
        "docker exec -i " + \
             os.environ["NLAB_DOCKER_PYTHON_IMAGE_NAME"] + \
             " curl http://localhost:" + \
             backend_port + \
             "/nlab/show/title+of+test+page",
        shell = True,
        capture_output = True,
        text = True)
    with open("resources/rendered_page_without_nforum_discussion.html") as \
            rendered_page_file:
        expected_rendered_page = rendered_page_file.read()
    actual_rendered_page = curl_backend_subprocess.stdout
    if actual_rendered_page != expected_rendered_page:
        raise TestFailedException(
            "render_for_viewing_200",
            "Expected page for backend rendering different from actual page",
             expected_rendered_page,
             actual_rendered_page)
    curl_nginx_subprocess = subprocess.run(
        [
             "curl",
             "http://localhost:8000/nlab/show/title+of+test+page"
        ],
        capture_output = True,
        text = True)
    actual_nginx_page = curl_nginx_subprocess.stdout
    if actual_nginx_page != expected_rendered_page:
        raise TestFailedException(
            "render_for_viewing_200",
            "Expected page for nginx different from actual page",
             expected_rendered_page,
             actual_nginx_page)

def test_render_for_viewing_404():
    tools.testing.launch_backend_server()
    backend_port = os.environ["NLAB_BACKEND_PORT"]
    curl_subprocess = subprocess.run(
        "docker exec -i " + \
             os.environ["NLAB_DOCKER_PYTHON_IMAGE_NAME"] + \
             " curl -s -o /dev/null -w %{http_code} " + \
             "http://localhost:" + \
             backend_port + \
             "/render-for-viewing/nlab/non-existent+page",
        shell = True,
        capture_output = True,
        text = True)
    if curl_subprocess.stdout != "404":
        raise TestFailedException(
            "render_for_viewing_404",
            "Status code not 404 in response to backend request",
            "404",
            curl_subprocess.stdout)

def _run_and_clean_up(test, clean_up_static_root_directory = False):
    try:
        test()
    finally:
        tools.testing.shutdown_backend_server_if_running()
        if clean_up_static_root_directory:
            tools.testing.clean_up_static_root_directory()

def run_tests():
    _run_and_clean_up(test_render_for_viewing_200, True)
    _run_and_clean_up(test_render_for_viewing_404)

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
