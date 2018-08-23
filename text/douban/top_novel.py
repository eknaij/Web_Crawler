import requests
from bs4 import BeautifulSoup
import time
import os
import pygal
from pygal.style import LightColorizedStyle as LCS,LightenStyle as LS

class Top_Novel():
    def __init__(self):
        #给请求指定一个请求头来模拟chrome浏览器
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}  
        self.web_url = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?'
        self.filename = 'novel_msg.text'
    def url_get(self,web_url):
        # ~ print('开始网页get请求')
        r = requests.get(web_url,headers=self.headers)
        # ~ print('开始获取小说界面的全部div标签')
        all_div = BeautifulSoup(r.text,'lxml').find_all('div',class_='info')
        # ~ print('所有小说的div标签获取完毕')
        # ~ 创建一个字典存储小说的信息
        self.dict_info = {}
        # ~ 循环获取小说的内容
        for msg in all_div:
            self.dict_info['title'] = msg.find('a')['title']
            self.dict_info['autor'] = msg.find('div',class_='pub').text.strip()
            self.dict_info['pf'] = msg.find('span',class_='rating_nums').text.strip()
            self.dict_info['pj'] = msg.find('span',class_='pl').text.strip()
            self.save_info()
    def save_info(self):
        # ~ print('开始保存小说的信息')
        with open(self.filename,'a+') as f:
            f.write('标题： {} \t 出版信息：{} \t 豆瓣评分：{} \t 评价数：{} \n'
                    .format(self.dict_info['title'],self.dict_info['autor'],
                    self.dict_info['pf'],self.dict_info['pj']))
        # ~ print('小说信息保存完成')
    def geturl_list(self):
        self.deep = input('请输入爬取的页数：')
        url_list = []
        for i in range(0,int(self.deep)):
            url_list.append(self.web_url+'start='+str(20*i)+'&type=T')
        print('页面信息保存完毕')
        i = 0
        for url in url_list:
            self.url_get(url)
            i = i +1
            print('已完成'+str(i)+'/'+self.deep+'页')
    #将数据进行可视化
    def show_msg(self):
        names,ples = [],[]
        with open(self.filename,'r') as f:
            lines = f.readlines()
            for line in lines:
                name_t = line.index(' ')
                name_w = line.index(' 	 出版信息：')
                name = line[name_t:name_w]
                names.append(name)
                pls = int(line[line.index('评价数：(')+5 : line.index('人评价')])
                ples.append(pls)
            
        my_style = LS('#333366',base_style=LCS)
        my_config = pygal.Config()
        my_config.x_label_rotation = 60
        my_config.show_legend =False
        my_config.title_font_size = 24
        my_config.label_font_size = 14 
        my_config.major_label_font_size = 18
        my_config.truncate_label = 15
        my_config.show_y_guides = False
        my_config.width = 1500

        chart = pygal.Bar(my_config,style=my_style)
        chart.title = '豆瓣读书前'+self.deep+'页小说的评论数情况'
        chart.x_labels = names
        chart.add('',ples)
        chart.render_to_file('show_pls.svg')

novel= Top_Novel()
novel.geturl_list()
novel.show_msg()
        
