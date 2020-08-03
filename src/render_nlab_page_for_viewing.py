#!/usr/bin/python3

import argparse
import json
import os
import pathlib
import subprocess
import sys
import urllib.parse

import log.logger_initialiser

"""
Initialises logging. Logs to

render_nlab_page_for_viewing.log
"""
logger = log.logger_initialiser.initialise(
    __name__,
    "render_nlab_page_for_viewing")

"""
Saves a rendered page as a HTML file in the correct place for viewing via
nginx
"""
def place_for_static_viewing(page_title, address_of_sub_wiki, rendered_html):
    root_directory_of_static_nlab = os.environ[
        "NLAB_DEPLOYED_STATIC_ROOT_DIRECTORY"]
    url_encoded_page_title = urllib.parse.quote_plus(page_title)
    directory_of_static_page = os.path.join(
        root_directory_of_static_nlab,
        address_of_sub_wiki,
        "show")
    path_of_static_page = os.path.join(
        directory_of_static_page,
        url_encoded_page_title)
    try:
        with open(path_of_static_page, "w") as static_page_file:
            static_page_file.write(rendered_html)
    except FileNotFoundError:
        pathlib.Path(directory_of_static_page).mkdir(
            parents = True,
            exist_ok = True)
        with open(path_of_static_page, "w") as static_page_file:
            static_page_file.write(rendered_html)


"""
Uses the deployed page renderer
"""
def render(page_id):
    render_page_subprocess = subprocess.run(
        [
            "python3",
            "page_renderer.py",
            str(page_id)
        ],
        capture_output = True,
        text = True)
    render_page_subprocess.check_returncode()
    return json.loads(render_page_subprocess.stdout)

def render_and_place_for_static_viewing(page_id):
    rendered_page_json = render(page_id)
    place_for_static_viewing(
        rendered_page_json["page_title"],
        rendered_page_json["sub_wiki_address"],
        rendered_page_json["rendered_html"])

"""
Sets up the command line argument parsing
"""
def argument_parser():
    parser = argparse.ArgumentParser(
        description = (
            "Renders an nLab page from the database, and places the " +
            "rendered page in the correct place for static viewing via nginx"))
    parser.add_argument(
        "page_id",
        help = "Id of nLab page")
    return parser

def main():
    parser = argument_parser()
    arguments = parser.parse_args()
    page_id = arguments.page_id
    logger.info("Beginning rendering page with id: " + str(page_id))
    try:
        render_and_place_for_static_viewing(page_id)
    except Exception as exception:
        raise exception
        logger.warning(
            "An unexpected error occurred when rendering page with id: " +
            str(page_id) +
            ". Error: " +
            str(exception))
        sys.exit("An unexpected error occurred")
    logger.info("Successfully rendered page with id: " + str(page_id))

if __name__ == "__main__":
    main()
