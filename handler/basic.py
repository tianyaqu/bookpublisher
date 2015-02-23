#!/usr/bin/env python
# coding=utf-8

import tornado.web
from confmodel import ConfModel
from adminmodel import AdminModel
from ConfigParser import ConfigParser
import functools

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self._storage = {'model': {}, 'dbase': {}, }

    def on_finish(self):
        for dbase in self._storage['dbase']:
            # self._storage['dbase'][dbase].close()
            pass

    def get_from_conf(self, item):
        return self.model('conf').get(self.dbase('config'),item)

    def model(self,name):
        name = name.title() + 'Model'
        if name not in self._storage['model']:
            self._storage['model'][name] = globals()[name]()
        return self._storage['model'][name]

    def dbase(self,name):
        if name not in self._storage['dbase']:
            cf = ConfigParser()
            cf.read(name)
            self._storage['dbase'][name] = cf
        return self._storage['dbase'][name]

    def input(self, *args, **kwargs):
        return self.get_argument(*args, **kwargs)

    def get_current_user(self):
        usid = self.get_cookie('l_usid')
        auid = self.get_secure_cookie('l_auid')
        auth = self.get_secure_cookie('l_auth')
        if usid and auth:
            user = self.model('admin').get_user_by_usid(self.dbase('users'), usid)
            if user and user['auid'] == auid and self.model('admin').generate_pass(user['token'],user['salt']) == auth:
                return user
            self.del_current_sess()

    def del_current_sess(self):
        self.clear_cookie("l_auid")
        self.clear_cookie("l_auth")
        # self.clear_cookie("_usid")

    def merge_query(self, args, mask=[]):
        for k in self.request.arguments.keys():
            if k not in args:
                args[k] = self.get_argument(k)
        for k in mask:
            if k in args:
                del args[k]

        return args

    def makeurl(self, args, base=None):
        if base == None:
            base = self.request.path
        return tornado.httputil.url_concat(base, args)

def alive(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            self.redirect('/login')
            return
        return method(self,*args,**kwargs)
    return wrapper
