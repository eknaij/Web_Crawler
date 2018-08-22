#!-*- coding:utf-8 -*-
import requests #导入requests 模块
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import os  #导入os模块

# ~ http://www.mzitu.com/
# ~ http://www.mmjpg.com/
class Mmjpg():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36','Referer':'http://i.meizitu.net'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'http://www.mzitu.com/'  #要访问的网页地址
        self.folder_path = 'MmjpglPicture'  #设置图片要存放的文件目录
    def get_pic(self):
        print('开始网页get请求')
        r = self.request(self.web_url)
        print('开始获取所有li标签')
        all_li = BeautifulSoup(r.text, 'lxml').find_all('img',class_='lazy')  #获取网页中所有li标签
        print('开始创建文件夹')
        self.mkdir(self.folder_path)  #创建文件夹
        print('开始切换文件夹')
        os.chdir(self.folder_path)   #切换路径至上面创建的文件夹
        for li in all_li: #循环每个标签，获取标签中图片的url并且进行网络请求，最后保存图片
            img_str = li['data-original']
            print('img标签的src内容是：', img_str)
            img_name = li['alt']
            self.save_img(img_str, img_name) #调用save_img方法来保存图片
            
    def save_img(self, url, name): ##保存图片
        print('开始请求图片地址，过程会有点长...')
        img = self.request(url)
        file_name = name + '.jpg'
        print('开始保存图片')
        with open(file_name, 'ab') as f:
            f.write(img.content)
        print(file_name,'图片保存成功！')
    def request(self, url):  #返回网页的response
        r = requests.get(url, headers=self.headers)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        return r

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
        else:
            print(path, '文件夹已经存在了，不再创建')

beauty = Mmjpg()  #创建类的实例
beauty.get_pic()  #执行类中的方法
