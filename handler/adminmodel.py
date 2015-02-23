#!/usr/bin/env python
# coding = utf-8

class AdminModel():
    def get_user_by_usid(self,db,usid):
        list = db.items(usid)
        return self.list2dict(list)

    def list2dict(self,ls):
        return {x:y for x,y in ls}

    def generate_pass(self,passwd,salt):
        return passwd+salt

