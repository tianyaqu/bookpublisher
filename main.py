#!/usr/bin/env python
# coding=utf-8

import re
import os.path
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options

from handler.home import HomeHandler
from handler.follow import FollowHandler
from handler.publish import PublishHandler
from handler.login import LoginHandler
from handler.logout import LogoutHandler

define("port",default=8888,help="run on a given port",type=int)

class APP(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/",HomeHandler),
            (r"/follow",FollowHandler),
            (r"/publish",PublishHandler),
            (r"/login",LoginHandler),
            (r"/logout",LogoutHandler),
            # (r"/search",CategoryHandler),
        ]

        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__),"templates"),
            static_path = os.path.join(os.path.dirname(__file__),"static"),
            debug = True,
            cookie_secret = 'Yoursecretcookie',
        )

        tornado.web.Application.__init__(self,handlers,**settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(APP())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
