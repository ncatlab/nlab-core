#!/usr/bin/python3

import argparse
import os
import re
import subprocess
import sys

from tools.testing import TestFailedException

def test_source_renderer_markdown_only():
    source_renderer_subprocess = subprocess.run(
        "docker exec -it " +
            os.environ["NLAB_DOCKER_PYTHON_IMAGE_NAME"] +
            " /bin/bash -c 'echo -n \"Test\n\nSecond _test_\" | " +
            "python3 source_renderer.py 1'",
        capture_output = True,
        text = True,
        shell = True)
    actual_rendered_source = source_renderer_subprocess.stdout.rstrip()
    expected_rendered_source = "<p>Test</p>\n<p>Second <em>test</em></p>"
    if actual_rendered_source != expected_rendered_source:
        raise TestFailedException(
            "source_renderer_markdown_only",
            "Expected rendered source different from actual",
            expected_rendered_source,
            actual_rendered_source)

def test_inline_latex_token():
    source_renderer_subprocess = subprocess.run(
        "docker exec -it " +
            os.environ["NLAB_DOCKER_PYTHON_IMAGE_NAME"] +
            " /bin/bash -c 'echo -n \"Test \$a^{2}\$ test \$\\frac{b}{c}\$\" " +
            "| python3 source_renderer.py 1'",
        capture_output = True,
        text = True,
        shell = True)
    actual_rendered_source = source_renderer_subprocess.stdout.rstrip()
    expected_rendered_source = (
        "<p>Test <math xmlns='http://www.w3.org/1998/Math/MathML' " +
        "display='inline'><msup><mi>a</mi> <mn>2</mn></msup></math> test " +
        "<math xmlns='http://www.w3.org/1998/Math/MathML' display='inline'>" +
        "<mfrac><mi>b</mi><mi>c</mi></mfrac></math></p>")
    if actual_rendered_source != expected_rendered_source:
        raise TestFailedException(
            "inline_latex_token",
            "Expected rendering different from actual",
            expected_rendered_source,
            actual_rendered_source)

def test_inline_latex_token_invalid_syntax():
    source_renderer_subprocess = subprocess.run(
        "docker exec -it " +
            os.environ["NLAB_DOCKER_PYTHON_IMAGE_NAME"] +
            " /bin/bash -c 'echo -n \"Test \$a^{2}\$ test \$\\frac{b{c}\$\" " +
            "| python3 source_renderer.py 1'",
        capture_output = True,
        text = True,
        shell = True)
    try:
        source_renderer_subprocess.check_returncode()
    except subprocess.CalledProcessError as called_process_error:
        exit_code = called_process_error.returncode
        if exit_code != 1:
            raise TestFailedException(
                "inline_latex_token_invalid_syntax",
                "Unexpected exit code",
                1,
                exit_code)
        if not "LaTeX syntax error" in called_process_error.stdout:
            raise TestFailedException(
                "inline_latex_token_invalid_syntax",
                 "Unexpected stderr",
                 "LaTeX syntax error",
                 source_renderer_subprocess.stderr)
        return
    raise TestFailedException(
        "inline_latex_token_invalid_syntax",
        "Unexpected exit code",
        1,
        0)

def run_tests():
    test_source_renderer_markdown_only()
    test_inline_latex_token()
    test_inline_latex_token_invalid_syntax()

"""
Sets up the command line argument parsing
"""
def argument_parser():
    parser = argparse.ArgumentParser(
        description = (
            "Tests for source_renderer.py"))
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
