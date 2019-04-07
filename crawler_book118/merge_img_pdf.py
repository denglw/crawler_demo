#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2019/4/7 10:54
# @Author  : Denglw
# @Email   : 892253193@qq.com
# @File    : merge_img_pdf.py

from PIL import Image
import os
import sys
print sys.getdefaultencoding()
# https://www.2cto.com/kf/201803/733604.html
# https://blog.csdn.net/staHuri/article/details/81876310

class MergeImgPdf:
    from PIL import ImageFile
    ImageFile.LOAD_TRUNCATED_IMAGES = True #封装于class添加此语句解决异常
    def merge_img_pdf(self,path,pdf_name):
        #file_list = os.listdir('.')
        file_list = os.listdir(path)
        pic_name = []
        im_list = []
        for x in file_list:
            if "jpg" in x or 'png' in x or 'jpeg' in x:
                pic_name.append(x)

        pic_name.sort()
        new_pic = self.__add_path(path, pic_name)

        print("hec", new_pic)

        im1 = Image.open(new_pic[0])
        new_pic.pop(0)
        for i in new_pic:
            img = Image.open(i)
            # im_list.append(Image.open(i))
            if img.mode == "RGBA":
                img = img.convert('RGB')
                im_list.append(img)
            else:
                im_list.append(img)
        im1.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=im_list)
        tip = 'out put file name：'.decode('utf-8')
        print(tip, pdf_name)

    def __add_path(self,path,pic_name):
        new_pic = []
        path = path+'/'
        for x in pic_name:
            if "png" in x:
                new_pic.append(path+x)
        for x in pic_name:
            if "jpg" in x:
                new_pic.append(path+x)
        for x in pic_name:
            if "jpg" in x:
                new_pic.append(path+x)

        return new_pic

if __name__ == '__main__':
    test = """ 
  _____ _____ _____   _______ ____    _____  _____  ______ 
 |  __ \_   _/ ____| |__   __/ __ \  |  __ \|  __ \|  ____|
 | |__) || || |         | | | |  | | | |__) | |  | | |__   
 |  ___/ | || |         | | | |  | | |  ___/| |  | |  __|  
 | |    _| || |____     | | | |__| | | |    | |__| | |     
 |_|   |_____\_____|    |_|  \____/  |_|    |_____/|_|     


"""
    curPath = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(curPath, 'images')
    print 'path'+path
    mergeImgPdf = MergeImgPdf()
    mergeImgPdf.merge_img_pdf(path,'book118.pdf')


