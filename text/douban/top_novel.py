import requests
from bs4 import BeautifulSoup
import time
import os
class Top_Novel():
    def __init__(self):
        #给请求指定一个请求头来模拟chrome浏览器
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}  
        self.web_url = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4'
    def url_get(self):
        print('开始网页get请求')
        r = requests.get(self.web_url,headers=self.headers)
        print('开始获取小说界面的全部div标签')
        all_div = BeautifulSoup(r.text,'lxml').find_all('div',class_='info')
        print('所有小说的div标签获取完毕')
        # ~ 创建一个字典存储小说的信息
        dict_info = {}
        # ~ 循环获取小说的内容
        for msg in all_div:
            dict_info['title'] = msg.find('a')['title']
            print(dict_info['title'])
            dict_info['autor'] = msg.find('div',class_='pub').text.strip()
            dict_info['pf'] = msg.find('span',class_='rating_nums').text.strip()
            dict_info['pj'] = msg.find('span',class_='pl').text.strip()
            self.save_info(dict_info)
    def save_info(self,dict_info):
        print('开始保存小说的信息')
        with open('novel_msg.text','a+') as f:
            f.write('\n标题：{} \t 出版信息：{} \t 豆瓣评分：{} \t 评价数：{} \n'
                    .format(dict_info['title'],dict_info['autor'],
                    dict_info['pf'],dict_info['pj']))
        print('小说信息保存完成')

novel= Top_Novel()
novel.url_get()
        
