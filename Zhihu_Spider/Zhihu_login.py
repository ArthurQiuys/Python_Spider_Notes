#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Arthur Qiu on 2017/6/13

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path
try:
    from PIL import Image
except:
    pass

agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) ' \
        'Chrome/56.0.2924.87 Mobile Safari/537.36'
headers = {
    "Host": "www.zhihu.com",
    "Referer": "http://www.zhihu.com/",
    "User-Agent": agent
}
# 构造Requests headers


session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print "未能加载cookie"


def get_csrf():
    """
    是一个动态的参数
    csrf指的是Cross-site request forgery等价于session riding 也就是跨网站申请伪造
    :return:
    """
    index_url = 'http://www.zhihu.com'
    # 获取登录时需要用到的csrf
    index_page = session.get(index_url, headers=headers)
    html = index_page.text
    pattern = r'name="_csrf" value="(.*?)"'
    # 此处的_csrf返回的是一个list
    _csrf = re.findall(pattern, html)
    return _csrf[0]


def get_captcha():
    t = str(int(time.time()*1000))
    # 将时间从int强制转化为str
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha_url.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow的image显示验证码
    # 如果没有使用pillow 就需要到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg')
    captcha = input("please input the captcha\n")
    return captcha


def is_login():
    """
    查看用户个人信息来查看是否已经登陆
    :return: True or False
    """
    url = "http://www.zhihu.com/settings/profile"
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False


def login(secret, account):
    """
    登陆的主函数
    :param secret:密码
    :param account:账号
    :return:
    """
    _csrf = get_csrf()
    headers["X-Xsrftoken"] = _csrf
    headers["X-Requested-With"] = "XMLHttpRequest"
    if re.match(r"^1\d{10}$]", account):
        print "手机号登陆 \n"
        post_url = 'http://www.zhihu.com/login/phone_num'
        postdata = {
            '_csrf': _csrf,
            'password': secret,
            'phone_num': account
        }
    else:
        if "@" in account:
            print "邮箱登陆 \n"
        else:
            print "你的账号输入有问题，请宠幸登陆"
            return 0
    post_url = 'https://www.zhihu.com/login/email'
    postdata = {
        '_csrf': _csrf,
        'password': secret,
        'email': account
    }
    login_page = session.post(post_url, data=postdata, headers=headers)
    login_code = login_page.json()
    # 不需要输入验证码登陆成功
    if login_code['r'] == 1:
        postdata["captcha"] = get_captcha()
        login_page = session.post(post_url, daa=postdata, headers=headers)
        login_code = login_page.json()
        print login_code['msg']
        # 不需要验证码登陆失败
        # 使用需要输入验证码的方式进行登陆
    # 保存 cookies 到文件，
    # 下次可以使用 cookies 直接登陆，不需要输入账号和密码
    session.cookies.save()


try:
    input = raw_input
except:
    pass


if __name__ == '__main__':
    pass
if is_login():
    print "已经登陆"
else:
    account = raw_input('请输入你的用户名\n>   ')
    secret = raw_input("请输入你的木马\n>    ")
    login(secret, account)
