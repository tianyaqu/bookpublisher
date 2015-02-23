#!/usr/bin/env python 
# coding=utf-8

from basic import BaseHandler


class LoginHandler(BaseHandler):
    def get(self):
        title = self.get_from_conf('site')
        self.render('login.html', args = title)

    def post(self):
        try:
            usid = self.input('email')
            passwd = self.input('password')
            remember = self.input('remember',None)
            if remember:
                remember = 1

            if self.validate(usid,passwd):
                user = self.model('admin').get_user_by_usid(self.dbase('users'), usid)
                if user and self.model('admin').generate_pass(passwd, user['salt']) == user['pass']:
                    self.set_cookie('l_usid',usid,expires_days=remember)

                    auid = user['auid']
                    self.set_secure_cookie("l_auid", auid, expires_days=remember)

                    token = user['token']
                    salt = user['salt']
                    auth = self.model('admin').generate_pass(token, salt)
                    self.set_secure_cookie("l_auth", auth, expires_days=remember)

                    self.redirect('/')
                # self.render('index.html',title='ok',text='fully wok')
            else:
                self.render('index.html',title='no',text = 'not work')
        except:
            self.render('index.html',title='sb',text='somthingwr')

    def validate(self,user,password):
        return True
        """
        if user == 'qusai@baidu.com' and password == '1234':
            return True
        return False
        """

