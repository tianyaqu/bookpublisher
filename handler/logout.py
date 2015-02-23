#!/usr/bin/env python 
# coding=utf-8

from basic import alive,BaseHandler

class LogoutHandler(BaseHandler):
    @alive
    def get(self):
        self.del_current_sess()
        self.redirect('/')

    @alive
    def post(self):
        self.del_current_sess()
        self.redirect('/')

