#!/usr/bin/env python
import traceback

import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.web

from settings import Settings
from token_helper import TokenHelper
from oauthhandler import OauthHandler

from tornado.options import define, options, parse_command_line

define("debug", default=False, help="run in debug mode")

@tornado.gen.coroutine
def main():
    try:
        parse_command_line()
        app = tornado.web.Application([
                (r"/oauth", OauthHandler)
              ],
            cookie_secret="abcdefghijklmnopqrstuvwxyz",
            xsrf_cookies=False,
            debug=options.debug,
            )
        app.settings['token_helper'] = TokenHelper()
        server = tornado.httpserver.HTTPServer(app)
        server.bind(Settings.port)
        print("main - Serving... on port {0}".format(Settings.port))
        server.start()
        tornado.ioloop.IOLoop.instance().spawn_callback(app.settings['token_helper'].event_loop)
        tornado.ioloop.IOLoop.instance().start()
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()
