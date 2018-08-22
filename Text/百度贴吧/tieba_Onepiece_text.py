import requests #导入requests 模块
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import time
import os  #导入os模块
import pygal
from pygal.style import LightColorizedStyle as LCS,LightenStyle as LS

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        # 这里我们知道百度贴吧的编码是utf-8，所以手动设置的。爬去其他的页面时建议使用：
        # r.endcodding = r.apparent_endconding
        r.encoding = 'utf-8'
        return r.text
    except:
        return " ERROR "


def get_content(url):
    '''
    分析贴吧的网页文件，整理信息，保存在列表变量中
    '''

    # 初始化一个列表来保存所有的帖子信息：
    comments = []
    # 首先，我们把需要爬取信息的网页下载到本地
    html = get_html(url)

    # 我们来做一锅汤
    soup = BeautifulSoup(html, 'lxml')

    # 按照之前的分析，我们找到所有具有‘ j_thread_list clearfix’属性的li标签。返回一个列表类型。
    liTags = soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})

    # 通过循环找到每个帖子里的我们需要的信息：
    for li in liTags:
        # 初始化一个字典来存储文章信息
        comment = {}
        #.text是获取标签下的text文本  有些标签下可能文本为空 所以会报错 歪了避免选择用try except
        try:
            # 开始筛选信息，并保存到字典中
            comment['title'] = li.find(
                'a', class_='j_th_tit ').text.strip() 
            comment['link'] = "http://tieba.baidu.com" + \
                li.find('a', attrs={'class': 'j_th_tit '})['href']
            comment['name'] = li.find(
                'span', attrs={'class': 'tb_icon_author '}).text.strip()
            comment['replyNum'] = li.find(
                'span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()
            comment['ctime']= li.find(
                'span',class_='pull-right is_show_create_time').text.strip()
            comments.append(comment)
        except:
           print('')

    return comments


def Out2File(dict,i):
    '''
    将爬取到的文件写入到本地
    保存到当前目录的 TTBT.txt文件中。

    '''
    with open('Onepiece.txt', 'a') as f:
        for comment in dict:
            f.write('标题： {} \t 链接：{} \t 发帖人：{}  \t 回复数量： {} \t 发帖时间： {}\n'.format(
                comment['title'], comment['link'], comment['name'],  comment['replyNum'],comment['ctime']))
        
        print('第'+str(i)+'页爬取完成')


def main(base_url, deep):
    url_list = []
    # 将所有需要爬去的url存入列表
    for i in range(0, deep):
        url_list.append(base_url + '&pn=' + str(50 * i))
    print('所有的网页已经下载到本地！共'+str(deep)+'页  开始筛选信息。。。。')
    i = 0
    #循环写入所有的数据
    for url in url_list:
        i= i+1
        content = get_content(url)
        Out2File(content,i)
    print('所有的信息都已经保存完毕！')
    #打开文件
    """lines = {}
    with open('Onepiece.txt',r) as f:
        lines = f.readlines()
    name,replynums=[],[]
    for line in lines:
        name = 
    #数据可视化
    my_style = LS('#333366',base_style=LCS)
    my_config = pygal.Config()
    my_config.x_label_rotation = 45
    my_config.show_legend =False
    my_config.title_font_size = 24
    my_config.label_font_size = 14
    my_config.major_label_font_size = 18
    my_config.truncate_label = 15
    my_config.show_y_guides = False
    my_config.width = 800

    chart = pygal.Bar(my_config,style=my_style)
    chart.title = '前20页中回复数最多的帖子排行'
    chart.x_labels = names"""


base_url = 'https://tieba.baidu.com/f?kw=海贼王&ie=utf-8'
# 设置需要爬取的页码数量
deep = 20

if __name__ == '__main__':
    main(base_url, deep)

    
