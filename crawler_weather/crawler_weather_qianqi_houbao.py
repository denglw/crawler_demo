#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2019/4/10 17:39
# @Author  : Denglw
# @Email   : 892253193@qq.com
# @File    : crawler_qianqi_houbao.py
# @desc: 爬取天气后报网的历史天气数据 http://www.tianqihoubao.com/



# 参考 https://blog.csdn.net/weixin_43327576/article/details/86514093
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import csv
import time
import codecs

import sys
reload(sys)
sys.setdefaultencoding('utf-8') # utf-8编码设置

def get_one_page(url):
    '''
    获取网页
    '''
    print('正在加载'+url)
    headers={'User-Agent':'User-Agent:Mozilla/5.0'}
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.content.decode('gbk')
        return None
    except RequestException:
        return None

def parse_one_page(html):
    #对网页内容进行解析
    soup = BeautifulSoup(html,  "lxml")
    info = soup.find('div',  class_='wdetail')
    rows=[]
    tr_list = info.find_all('tr')[1:]       # 使用从第二个tr开始取
    for index,  tr in enumerate(tr_list):     # enumerate可以返回元素的位置及内容
        td_list = tr.find_all('td')
        date = td_list[0].text.strip().replace("\n", "")  # 取每个标签的text信息，并使用replace()函数将换行符删除
        weather = td_list[1].text.strip().replace("\n", "").split("/")[0].strip()
        temperature_high = td_list[2].text.strip().replace("\n",  "").split("/")[0].strip()
        temperature_low = td_list[2].text.strip().replace("\n",  "").split("/")[1].strip()

        rows.append((date,weather,temperature_high,temperature_low))
    return rows





cities = ['chengdu','leshan']
years = ['2018','2019']
months = ['01','02','03','04','05','06', '07', '08','09','10','11','12']

if __name__ == '__main__':
    # os.chdir()  # 设置工作路径
    for city in cities:
        with open(city + '_weather.csv','wb') as f:
            writer = csv.writer(f)
            f.write(codecs.BOM_UTF8)
            writer.writerow(['date','weather','temperature_high','temperature_low'])
            for year in years:
                for month in months:
                    url = 'http://www.tianqihoubao.com/lishi/'+city+'/month/'+year+month+'.html'
                    html = get_one_page(url)
                    time.sleep(3) #休眠3秒用于加载数据
                    content=parse_one_page(html)
                    writer.writerows(content)
                    print(city+year+month+' is OK!')
                    time.sleep(2)



