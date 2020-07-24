#!/usr/bin/python3

import argparse
import difflib
import os
import subprocess
import sys

def _difference_between_strings(expected, actual):
    return '\n'.join(difflib.context_diff(
        expected.split("\n"),
        actual.split("\n"),
        fromfile = 'Expected',
        tofile = 'Actual'))

class TestFailedException(Exception):
    def __init__(self, test_name, message, expected, actual):
        super().__init__(
            "Test failed: " +
            test_name +
            ". " +
            message +
            "\n\n" +
            _difference_between_strings(expected, actual))

def test_page_renderer_without_nforum_discussion():
    render_page_subprocess = subprocess.run(
        [
            "docker",
            "exec",
            "-it",
            os.environ["NLAB_DOCKER_PYTHON_IMAGE_NAME"],
            "python3",
            "page_renderer.py",
            "1"
        ],
        capture_output = True,
        text = True)
    with open("resources/rendered_page_without_nforum_discussion.html") as \
            rendered_page_file:
        expected_rendered_page = rendered_page_file.read()
    actual_rendered_page = render_page_subprocess.stdout
    if actual_rendered_page != expected_rendered_page:
        raise TestFailedException(
            "page_renderer_without_nforum_discussion",
            "Expected different from actual rendering.",
            expected_rendered_page,
            actual_rendered_page)

def test_page_renderer_without_nforum_discussion_with_sub_wiki():
    render_page_subprocess = subprocess.run(
        [
            "docker",
            "exec",
            "-it",
            os.environ["NLAB_DOCKER_PYTHON_IMAGE_NAME"],
            "python3",
            "page_renderer.py",
            "2"
        ],
        capture_output = True,
        text = True)
    with open(
                "resources/" +
                "rendered_page_without_nforum_discussion_with_sub_wiki.html") \
            as rendered_page_file:
        expected_rendered_page = rendered_page_file.read()
    actual_rendered_page = render_page_subprocess.stdout
    if actual_rendered_page != expected_rendered_page:
        raise TestFailedException(
            "page_renderer_without_nforum_discussion_with_sub_wiki",
            "Expected different from actual rendering.",
            expected_rendered_page,
            actual_rendered_page)

def test_page_renderer_with_nforum_discussion():
    render_page_subprocess = subprocess.run(
        [
            "docker",
            "exec",
            "-it",
            os.environ["NLAB_DOCKER_PYTHON_IMAGE_NAME"],
            "python3",
            "page_renderer.py",
            "3"
        ],
        capture_output = True,
        text = True)
    with open("resources/rendered_page_with_nforum_discussion.html") as \
            rendered_page_file:
        expected_rendered_page = rendered_page_file.read()
    actual_rendered_page = render_page_subprocess.stdout
    if actual_rendered_page != expected_rendered_page:
        raise TestFailedException(
            "page_renderer_with_nforum_discussion",
            "Expected different from actual rendering.",
            expected_rendered_page,
            actual_rendered_page)


"""
Sets up the command line argument parsing
"""
def argument_parser():
    parser = argparse.ArgumentParser(
        description = (
            "Tests for page_renderer.py"))
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
        test_page_renderer_without_nforum_discussion()
        test_page_renderer_without_nforum_discussion_with_sub_wiki()
        test_page_renderer_with_nforum_discussion()
    except TestFailedException as testFailedException:
        sys.exit(str(testFailedException))
    print("All tests passed")

if __name__ == "__main__":
     main()
