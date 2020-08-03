#!/usr/bin/python3

import argparse
import datetime
import json
import string
import sys
import urllib.parse

import database.query_executor
import log.logger_initialiser

"""
Initialises logging. Logs to

page_renderer.log
"""
logger = log.logger_initialiser.initialise(__name__, "source_renderer")

class _NoDiscussionIDException(Exception):
    pass

class _NoCommentException (Exception):
    pass

def _page_metadata(page_id):
    return database.query_executor.execute_single_with_parameters(
        "SELECT name, web_id, updated_at FROM pages WHERE id=%s",
        [ page_id ])[0]

def _sub_wiki_metadata(sub_wiki_id):
    return database.query_executor.execute_single_with_parameters(
         "SELECT name, address FROM webs WHERE id=%s",
         [ sub_wiki_id ])[0]

def _page_content(page_id):
    return database.query_executor.execute_single_with_parameters(
        "SELECT content FROM revisions " +
        "WHERE page_id = %s " +
        "ORDER BY id DESC LIMIT 1",
        [ page_id ])[0][0]

"""
Finds the DiscussionID of the last active nForum discussion with the same
name as a given nLab page. If no discussion can be found with the same name,
a NoDiscussionIDException is raised.
"""
def _nforum_discussion_id(nlab_page_name):
    query_results = database.query_executor.execute_single_with_parameters(
        "SELECT DiscussionID FROM mathforge_nforum_Discussion " +
        "WHERE Name = %s " +
        "ORDER BY DateLastActive DESC LIMIT 1",
        [ nlab_page_name ])
    try:
        discussion_id = query_results[0][0]
        logger.info(
            "Successfully found last active nForum discussion ID for nLab " +
            "page " +
            nlab_page_name +
            " to be: " +
            str(discussion_id))
        return discussion_id
    except IndexError:
        logger.info(
            "No nForum discussion found for nLab page " +
            nlab_page_name)
        raise _NoDiscussionIDException()

"""
Finds the number of the last comment, or equivalently the total number of
comments, in a discussion with a particular DiscussionID. Raises a
NoCommentException if the discussion has no comment (this should never occur
under ordinary circumstances).
"""
def _last_comment_number(discussion_id):
    query_results = database.query_executor.execute_single_with_parameters(
        "SELECT COUNT(CommentID) FROM mathforge_nforum_Comment " +
        "WHERE DiscussionID = %s",
        [discussion_id])
    try:
        last_comment_number = query_results[0][0]
        logger.info(
            "Successfully last comment number in nForum discussion " +
            "with ID " +
            str(discussion_id) +
            " to be: " +
            str(last_comment_number))
        return last_comment_number
    except IndexError:
        logger.warning(
            "No comment found in discussion with ID: " +
            str(discussion_id))
        raise _NoCommentException()

"""
Returns a link to the last active nForum discussion with the same
name as a given nLab page. If not found, returns link to nForum Latest Changes
category page.
"""
def _nforum_discussion_link(nlab_page_title):
    try:
        discussion_id = _nforum_discussion_id(nlab_page_title)
        comment_number = _last_comment_number(discussion_id)
    except (_NoDiscussionIDException, _NoCommentException):
        logger.info(
            "Could not construct link to nForum discussion corresponding " +
            "to nLab page with name " +
            nlab_page_title)
        return "https://nforum.ncatlab.org/5"
    return (
        "https://nforum.ncatlab.org/discussion/" +
        str(discussion_id) +
        "/#Item_" +
        str(comment_number))

def _link_creator(page_title, sub_wiki_address):
    url_encoded_page_title = urllib.parse.quote_plus(page_title)
    return lambda link_type: (
        "https://ncatlab.org/" +
        sub_wiki_address +
        "/" +
        link_type +
        "/" +
        url_encoded_page_title)

def render_header(page_title, sub_wiki_name):
    with open("templates/header.html") as header_template_file:
        header_template = string.Template(header_template_file.read())
    if sub_wiki_name == "nLab":
        name_of_wiki = "nLab"
    else:
        name_of_wiki = "nLab - " + sub_wiki_name
    return header_template.substitute(
        name_of_wiki = name_of_wiki,
        page_title = page_title)

def render_upper_menu(page_title, sub_wiki_address):
    if sub_wiki_address != "nlab":
        with open("templates/upper_menu_without_discussion_link.html") as \
                upper_menu_template_file:
            upper_menu_template = string.Template(
                upper_menu_template_file.read())
        return upper_menu_template.substitute(
            sub_wiki_address = sub_wiki_address)
    with open("templates/upper_menu.html") as upper_menu_template_file:
        upper_menu_template = string.Template(upper_menu_template_file.read())
    return upper_menu_template.substitute(
        sub_wiki_address = sub_wiki_address,
        nforum_discussion_thread_link = _nforum_discussion_link(page_title))

def render_last_revision_info(last_revision, history_page_link):
    with open("templates/last_revision_info.html") as \
            last_revision_info_template_file:
        last_revision_info_template = string.Template(
            last_revision_info_template_file.read())
    human_readable_last_revision_date = datetime.datetime.strftime(
        last_revision,
        "%B %d, %Y")
    human_readable_last_revision_time = datetime.datetime.strftime(
        last_revision,
        "%H:%M:%S")
    return last_revision_info_template.substitute(
        last_revision_date = human_readable_last_revision_date,
        last_revision_time = human_readable_last_revision_time,
        history_page_link = history_page_link)

def render_bottom_menu(link_creator):
    with open("templates/bottom_menu.html") as bottom_menu_template_file:
        bottom_menu_template = string.Template(bottom_menu_template_file.read())
    return bottom_menu_template.substitute(
        edit_page_link = link_creator("edit"),
        page_history_link = link_creator("history"),
        page_cite_link = link_creator("show") + "/cite",
        page_source_link = link_creator("source"))

def render(page_metadata, page_content):
    page_title = page_metadata[0]
    sub_wiki_name = page_metadata[1]
    sub_wiki_address = page_metadata[2]
    last_revision = page_metadata[3]
    link_creator = _link_creator(page_title, sub_wiki_address)
    with open("templates/nlab_page.html") as nlab_page_template_file:
        nlab_page_template = string.Template(nlab_page_template_file.read())
    if sub_wiki_name == "nLab":
        browser_page_title = "nLab - " + page_title
    else:
        browser_page_title = "nLab - " + sub_wiki_name + " - " + page_title
    return nlab_page_template.substitute(
        page_title = browser_page_title,
        header = render_header(page_title, sub_wiki_name),
        upper_menu = render_upper_menu(page_title, sub_wiki_address),
        rendered_content = page_content,
        last_revision_info = render_last_revision_info(
            last_revision,
            "<a href=\"" + link_creator("history") + "\">history</a>"),
        bottom_menu = render_bottom_menu(link_creator))

"""
Sets up the command line argument parsing
"""
def argument_parser():
    parser = argparse.ArgumentParser(
        description = (
            "Renders an nLab page from the database"))
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
        page_title, sub_wiki_id, last_revision = _page_metadata(page_id)
        sub_wiki_name, sub_wiki_address = _sub_wiki_metadata(sub_wiki_id)
        page_metadata = (
            page_title,
            sub_wiki_name,
            sub_wiki_address,
            last_revision)
        print(json.dumps(
            {
                "page_title": page_title,
                "rendered_html": render(page_metadata, _page_content(page_id)),
                "sub_wiki_address": sub_wiki_address
            },
            indent = 2))
    except Exception as exception:
        logger.warning(
            "An unexpected error occurred when rendering page with id: " +
            str(page_id) +
            ". Error: " +
            str(exception))
        sys.exit("An unexpected error occurred")
    logger.info("Successfully rendered page with id: " + str(page_id))

if __name__ == "__main__":
    main()
