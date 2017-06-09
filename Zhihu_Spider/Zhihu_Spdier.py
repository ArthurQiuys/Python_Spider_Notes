#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Arthur Qiu on 2017/6/9
import requests
import ConfigParser


def create_session():
    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')
    cookies = cf.items('cookies')
    cookies = dict(cookies)
    email = cf.get('info', 'email')
    password = cf.get('info', 'password')

    session = requests.session()
    login_date = {'email': email, 'password': password}
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows Nt 6.1; WOW64) AppleWebKit/537,36 (KHTML, like Gecko) '
                      'Chrome/43.0.2357.124 Safari/537.36',
        'Host': 'www.zhihu.com',
        'Referer': 'http://www.zhihu.com/'
    }
    r = session.post('http://www.zhihu.com/login/email', data=login_date, headers=header)
    if r.json()['r'] == 1:
        print 'Login Filed, reason is:',
        for m in r.json()['date']:
            print r.json()['date'][m]
        print 'So we use cookies to login in ...'
        has_cookies = False
        for key in cookies:
            if key != '__name__' and cookies[key] != '':
                has_cookies = True
                break
            if has_cookies is False:
                raise ValueError('请填写config.ini文件中的cookies项。')
            else:
                r = session.get('http://www.zhihu.com/login/email', cookies=cookies)

    with open('login.html', 'w') as ap:
        ap.write(r.content)

        return session, cookies


if __name__ == '__main__':
    pass
requests_session, requests_cookies = create_session()

url = 'http://www.zhihu.com/login/19552832'
content = requests_session.get(url, cookies=requests_cookies).content
with open('url.html', 'w') as fp:
    fp.write(content)
