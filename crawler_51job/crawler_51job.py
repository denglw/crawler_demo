#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2019/4/10 16:26
# @Author  : Denglw
# @Email   : 892253193@qq.com
# @File    : crawler_51job.py
# @desc:  使用python2.7做的爬虫  抓取51job上面的职位名，公司名，薪资，发布时间等等。

from bs4 import BeautifulSoup
import urllib
import urllib2
import codecs
import re
import time
import logging
import MySQLdb


class Jobs(object):
    # 初始化
    """docstring for Jobs"""

    def __init__(self):
        super(Jobs, self).__init__()

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        # 数据库的操作，没有mysql可以做屏蔽
        self.db = MySQLdb.connect('127.0.0.1', 'root', 'root', 'py_test', charset='utf8')
        self.cursor = self.db.cursor()

        # log日志的显示
        self.logger = logging.getLogger("sjk")

        self.logger.setLevel(level=logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.FileHandler('log.txt')
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

        self.logger.info('初始化完成')

        # 模拟请求数据

    def jobshtml(self, key, page='1'):
        try:
            self.logger.info('开始请求第' + page + '页')
            # 网页url
            searchurl = "https://search.51job.com/list/040000,000000,0000,00,9,99,{key},2,{page}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99°reefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="

            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'
            # 设置请求头
            header = {'User-Agent': user_agent, 'Host': 'search.51job.com',
                      'Referer': 'https://www.51job.com/'}
            # 拼接url
            finalUrl = searchurl.format(key=key, page=page)

            request = urllib2.Request(finalUrl, headers=header)

            response = urllib2.urlopen(request)
            # 等待网页加载完成
            time.sleep(3)
            # gbk格式解码
            info = response.read().decode('gbk')

            self.logger.info('请求网页网页')

            self.decodeHtml(info=info, key=key, page=page)

        except urllib2.HTTPError as e:
            print e.reason

            # 解析网页数据

    def decodeHtml(self, info, key, page):
        self.logger.info('开始解析网页数据')
        # BeautifulSoup 解析网页
        soup = BeautifulSoup(info, 'html.parser')
        # 找到class = t1 t2 t3 t4 t5 的标签数据
        ps = soup.find_all(attrs={"class": re.compile(r'^t[1-5].*')})
        # 打开txt文件 a+ 代表追加
        f = codecs.open(key + '.txt', 'a+', 'UTF-8')
        # 清除之前的数据信息
        f.truncate()

        f.write('\n------------' + page + '--------------\n')

        count = 1

        arr = []
        # 做一些字符串的处理，形成数据格式  iOS开发工程师 有限公司 深圳-南山区 0.9-1.6万/月 05-16
        for pi in ps:
            spe = " "
            finalstr = pi.getText().strip()
            arr.append(finalstr)
            if count % 5 == 0:
                # 每一条数据插入数据库，如果没有安装mysql 可以将当前行注释掉
                self.connectMySQL(arr=arr)
                arr = []
                spe = "\n"
            writestr = finalstr + spe
            count += 1
            f.write(writestr)
        f.close()

        self.logger.info('解析完成')

    # 数据库操作 没有安装mysql 可以屏蔽掉
    def connectMySQL(self, arr):
        work = arr[0]
        company = arr[1]
        place = arr[2]
        salary = arr[3]
        time = arr[4]

        query = "select * from Jobs_tab where \
        company_name='%s' and work_name='%s' and work_place='%s' \
                                                            and salary='%s' and time='%s'" % (
        company, work, place, salary, time)
        self.cursor.execute(query)

        queryresult = self.cursor.fetchall()

        # 数据库中不存在就插入数据 存在就可以更新数据 不过我这边没有写
        sql = ''
        if len(queryresult) <= 0:
            sql = "insert into Jobs_tab(work_name,company_name,work_place,salary\
            ,time) values('%s','%s','%s','%s','%s')" % (work, company, place, salary, time)

        try:
            self.cursor.execute(sql)
            self.db.commit()

        except Exception as e:
            self.logger.info('写入数据库失败')
            self.logger.info(e)
            self.logger.info(sql)


            # 模拟登陆


# def login(self):
#   data = {'action':'save','isread':'on','loginname':'18086514327','password':'kui4131sjk'}


    # 开始抓取 主函数
    def run(self, key):
        # 只要前5页的数据 key代表搜索工做类型 这边我是用的ios page是页数
        for x in xrange(1, 6):
            self.jobshtml(key=key, page=str(x))

        self.logger.info('写入数据库完成')

        self.db.close()


# 参考 https://www.jb51.net/article/140842.htm
if __name__ == '__main__':
    Jobs().run(key='IOS') # 关键字 ios



