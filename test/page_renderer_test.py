#!/usr/bin/python3

import argparse
import json
import os
import subprocess
import sys

from tools.testing import TestFailedException

def _compare(test_name, expected_rendered_page_json, actual_rendered_page_json):
    actual_page_title = actual_rendered_page_json["page_title"]
    expected_page_title = expected_rendered_page_json["page_title"]
    if actual_page_title != expected_page_title:
        raise TestFailedException(
            test_name,
            "Expected page title different from actual page title",
            expected_page_title,
            actual_page_title)
    actual_sub_wiki_address = actual_rendered_page_json["sub_wiki_address"]
    expected_sub_wiki_address = expected_rendered_page_json["sub_wiki_address"]
    if actual_sub_wiki_address != expected_sub_wiki_address:
        raise TestFailedException(
            test_name,
            "Expected sub wiki address different from actual sub wiki address",
            expected_sub_wiki_address,
            actual_sub_wiki_address)
    expected_rendered_page = expected_rendered_page_json["rendered_html"]
    actual_rendered_page = actual_rendered_page_json["rendered_html"]
    if expected_rendered_page != actual_rendered_page:
        raise TestFailedException(
            test_name,
            "Expected different from actual rendering.",
            expected_rendered_page,
            actual_rendered_page)

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
    expected_rendered_page_json = {
        "page_title": "title of test page",
        "rendered_html": expected_rendered_page,
        "sub_wiki_address": "nlab"
    }
    actual_rendered_page_json = json.loads(render_page_subprocess.stdout)
    _compare(
        "page_renderer_without_nforum_discussion",
        expected_rendered_page_json,
        actual_rendered_page_json)

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
    expected_rendered_page_json = {
        "page_title": "title of other test page",
        "rendered_html": expected_rendered_page,
        "sub_wiki_address": "some-sub-wiki"
    }
    actual_rendered_page_json = json.loads(render_page_subprocess.stdout)
    _compare(
        "page_renderer_without_nforum_discussion_with_sub_wiki",
        expected_rendered_page_json,
        actual_rendered_page_json)

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
    expected_rendered_page_json = {
        "page_title": "title of third test page",
        "rendered_html": expected_rendered_page,
        "sub_wiki_address": "nlab"
    }
    actual_rendered_page_json = json.loads(render_page_subprocess.stdout)
    _compare(
        "page_renderer_with_nforum_discussion",
        expected_rendered_page_json,
        actual_rendered_page_json)

def run_tests():
    test_page_renderer_without_nforum_discussion()
    test_page_renderer_without_nforum_discussion_with_sub_wiki()
    test_page_renderer_with_nforum_discussion()

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
        run_tests()
    except TestFailedException as testFailedException:
        sys.exit(str(testFailedException))
    print("All tests passed")

if __name__ == "__main__":
     main()
