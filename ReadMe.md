# Python 爬虫学习的记录
===
## python网络爬虫主要分3个板块
1.抓取
2.分析
3.储存

下面是我自己对爬虫学习的一些记录
## OS X上安装一些python Spider的库
1.Requests
    $ pip install requests
  或者可以直接克隆版本库
    git clone git://github.com/kennethreitz/requests.git
  也可以下载tarball
    $ curl -OL https://github.com/kennethreitz/requests/tarball/master
  获取到代码之后就可以安装到python的包中
    $ python setup.py install
值得注意的是在直接pip安装的时候可能会出现一些错误，大多数是因为对特定文件的写入权限问题，所以需要sudo超级权限