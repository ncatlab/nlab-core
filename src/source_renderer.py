#!/usr/bin/python3

import argparse
import mistletoe
import os
import sys

import log.logger_initialiser
import renderer.latex_renderer

from renderer.exception import SourceRendererException

"""
Initialises logging. Logs to

source_renderer.log
"""
logger = log.logger_initialiser.initialise(__name__, "source_renderer")

class nLabRenderer(mistletoe.html_renderer.HTMLRenderer):
    def __init__(self):
        token_classes = nLabRenderer.token_classes_to_use()
        super().__init__(*token_classes)

    def render_inline_latex_token(self, token):
        return token.render()

    @staticmethod
    def latex_compiler_token_class_if_to_be_used():
        if os.environ["NLAB_DEPLOYED_RUN_COMMAND_FOR_LATEX_COMPILER"]:
            return renderer.latex_renderer.InlineLatexToken

    @staticmethod
    def token_classes_to_use():
        token_classes = []
        latex_compiler_token_class = \
            nLabRenderer.latex_compiler_token_class_if_to_be_used()
        if latex_compiler_token_class is not None:
            token_classes.append(latex_compiler_token_class)
        return token_classes

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
        with nLabRenderer() as renderer:
            print(renderer.render(mistletoe.Document(page_content)))
    except SourceRendererException as sourceRendererException:
        logger.info(
            "An error occurred when rendering source of page with id: " +
            str(page_id) +
            ". Error: " +
            str(sourceRendererException))
        sys.exit(str(sourceRendererException))
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
