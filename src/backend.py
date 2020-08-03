#!/usr/bin/python3

"""
The starting point of the backend application server
"""

import cherrypy

import database.query_executor
import log.logger_initialiser
import render_nlab_page_for_viewing
import urllib.parse

"""
Initialises logging. Logs to

backend.log
"""
logger = log.logger_initialiser.initialise(__name__, "backend")

def _sub_wiki_id(sub_wiki_address):
    return database.query_executor.execute_single_with_parameters(
        "SELECT id FROM webs WHERE address = %s",
        [ sub_wiki_address ])[0][0]

def _page_id(sub_wiki_address, page_title):
    sub_wiki_id = _sub_wiki_id(sub_wiki_address)
    return database.query_executor.execute_single_with_parameters(
        "SELECT id FROM pages WHERE name = %s AND web_id = %s",
        [ page_title, sub_wiki_id ])[0][0]

@cherrypy.expose
@cherrypy.popargs("sub_wiki_address", "page_type", "page_title")
@cherrypy.tools.allow(methods = [ "GET" ])
class RenderForViewing(object):
    def GET(self, sub_wiki_address, page_type, page_title):
        logger.info(
            "Received GET request to render page. Title: " +
            page_title +
            ". Sub-wiki address: " +
            sub_wiki_address +
            ". Page type: " +
            page_type)
        url_decoded_page_title = urllib.parse.unquote_plus(page_title)
        try:
            rendered_page_json = render_nlab_page_for_viewing.render(
                _page_id(sub_wiki_address, url_decoded_page_title))
            rendered_html = rendered_page_json["rendered_html"]
            render_nlab_page_for_viewing.place_for_static_viewing(
                rendered_page_json["page_title"],
                rendered_page_json["sub_wiki_address"],
                rendered_html)
        except IndexError:
            logger.info(
                "No page found with title " +
                url_decoded_page_title +
                "for sub-wiki with address " +
                sub_wiki_address)
            raise cherrypy.HTTPError(status = 404)
        except Exception as exception:
            logger.warning(
                "An unexpected error occurred. Error: " +
                str(exception))
            raise cherrypy.HTTPError(status = 500)
        logger.info(
            "Successfully rendered page for viewing with title " +
            url_decoded_page_title +
            "for sub-wiki with address " +
            sub_wiki_address)
        return rendered_html

def main():
    cherrypy.config.update(
        {
            "server.socket_host": "0.0.0.0",
            "server.socket_port": 9000
        })
    config = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher()
        }
    }
    cherrypy.quickstart(
        RenderForViewing(),
        "/",
        config)

if __name__ == "__main__":
    main()
