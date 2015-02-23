#!/usr/bin/env python
# coding=utf-8

class ConfModel():
    def get(self,db,name):
        return db.get('db',name)