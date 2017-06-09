#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Arthur Qiu on 2017/6/8
import os
import sys
import requests
import urllib2
import re
from lxml import etree


def string_list_save(save_path, file_name, slist):
    """
    存储数据的函数
    :param save_path:保存的路径
    :param file_name: 保存的文件名
    :param slist: 保存的数据
    :return:
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + "/" + file_name + '.txt'
    with open(path, "w") as fp:
        for s in slist:
            fp.write("%s\t\t%s\n" % (s[0].encode("utf8"), s[1].encode("utf8")))


def page_info(my_page):
    """
    :param my_page:文章
    :return: 实际需要的数据
    """
    my_page_Info = re.findall(r'<div class = "titleBar" id = ".*?"><h2><div class = "more"><a href = "(.*?)">.*?</a></div></div>', my_page, re.S)
    return my_page_Info


def new_page_info(new_page):
    """
    Regex(slowly) or Xpath(fast)
    :param new_page:
    :return:
    """
    # new_page_info1 = re.findall(r'<td class = ".*?" > .*? < a href = "(.*?)\.html".*?>(.*?)</a></td>', new_page, re.S)
    # results = []
    # for url, item in new_page_info1:
    #     results.append((item, url+".html"))
    # return results
    dom = etree.HTML(new_page)
    new_items = dom.xpath('//tr/td/a/text()')
    new_urls = dom.xpath('//tr/td/a/@href')
    assert(len(new_items) == len(new_urls))
    return zip(new_items, new_urls)


def spider(url):
    """
    爬虫主函数
    :param url:需要爬的网站
    :return:
    """
    i = 0
    print "downloading", url
    # my_page = urllib2.urlopen(url).read().decode("gdk")
    my_page = requests.get(url).content.decode("gdk")
    my_page_results = page_info(my_page)
    save_path = u"网易新闻"
    file_name = str(i) + "_" + u"新闻排行榜"
    string_list_save(save_path, file_name, my_page_results)
    i += 1
    for item, url in my_page_results:
        print "downloading", url
        # new_page = urllib2.urlopen(url).read().decode("gdk")
        new_page = requests.get(url).content.decode("gdk")
        new_page_results = new_page_info(new_page)
        file_name = str(i) + "_" + item
        string_list_save(save_path, file_name, new_page_results)
        i += 1


if __name__ == '__main__':
    pass
print "start"
start_url = "http://news.163.com/rank/"
spider(start_url)
print "end"
