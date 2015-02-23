#!/usr/bin/env python
# coding=utf-8

import re
from pymongo import MongoClient
from basic import BaseHandler

class HomeHandler(BaseHandler):
    def get(self):
        self.render('home.html',title='HomePage')
