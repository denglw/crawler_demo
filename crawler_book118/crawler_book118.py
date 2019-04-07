#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2019/4/2 15:19
# @Author  : Denglw
# @Email   : 892253193@qq.com
# @File    : crawler_book118.py

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from urllib import urlretrieve
from merge_img_pdf import MergeImgPdf

class CrawlerBook:
    docTitle = 'testTitle'
    folderImg = 'testFolder'

    def downLoad(self,browseUrl,crawlerUrl,pageNum):

        # browser = webdriver.Chrome()
        browser = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        wait = WebDriverWait(browser, 60)
        # 原始url地址 https://max.book118.com/html/2017/0904/131853902.shtm
        #browser.get('https://max.book118.com/html/2017/0904/131853902.shtm')
        browser.get(browseUrl)
        self.docTitle = browser.title  # 爬取的文档的名称

        # 这里的url是内嵌的html地址 如何获取内嵌url请查看博客内容
        #browser.get('https://view55.book118.com/?readpage=RLnvymE5HZjh9LUTM3lKqw==&furl=o4j9ZG7fK94kkYRv4gktA2rYw4NlKHsQOI0uhdd7J6rybHMmR67ar6iKMqokN@IiO2OHdTQx8qL8FQkiLmQ7IRPuoLdY3mrpisxEl1qgF_r8BhhNbOGopg==&n=1')
        browser.get(crawlerUrl)
        # 获取翻页按钮
        nextpage = browser.find_element_by_id('nextBtn')
        #for i in range(0, 136):
        for i in range(0, pageNum):
            try:
                # 获取相应页面
                item = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#p' + str(i)))
                )
                # 获取页面中的图片链接并打印
                img = item.find_element_by_tag_name('img')
                url = img.get_attribute('src')
                print(url)
                # python 中str format 格式化数字补0方法  "{0:03d}".format(1) --> '001'
                img_filename = 'images/' + "{0:03d}".format(i + 1) + '.jpg'
                urlretrieve(url=url, filename=img_filename)
                nextpage.click()  # 执行翻页
            except TimeoutException:
                print("加载出错")
                break

        browser.quit()  # 关闭浏览器。当出现异常时记得在任务浏览器中关闭PhantomJS，因为会有多个PhantomJS在运行状态，影响电脑性能

    def mkdir(self,folderImg):
        # 去除首位空格
        path = folderImg.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)

            print path + ' 创建成功'
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print path + ' 目录已存在'
            return False




'''
1)python 代码的执行不依赖于 main（） 函数;
2)python 代码从没有缩进的代码开始执行。
'''
if __name__=="__main__":
    # 当前工程目录下创建目录
    curPath = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(curPath,'images')
    crawlerBook = CrawlerBook()
    crawlerBook.mkdir(path)
    browseUrl = 'https://max.book118.com/html/2017/0904/131853902.shtm'
    crawlerUrl = 'https://view55.book118.com/?readpage=RLnvymE5HZjh9LUTM3lKqw==&furl=o4j9ZG7fK94kkYRv4gktA2rYw4NlKHsQOI0uhdd7J6rybHMmR67ar6iKMqokN@IiO2OHdTQx8qL8FQkiLmQ7IRPuoLdY3mrpisxEl1qgF_r8BhhNbOGopg==&n=1'
    pageNum = 5 #book总共多少页 136
    crawlerBook.downLoad(browseUrl,crawlerUrl,pageNum)
    mergeImgPdf = MergeImgPdf()
    fileName=crawlerBook.docTitle
    mergeImgPdf.merge_img_pdf(path,fileName+'.pdf')

