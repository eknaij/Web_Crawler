import requests #导入requests 模块
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import pygal
from pygal.style import LightColorizedStyle as LCS,LightenStyle as LS

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        #r.endcodding = r.apparent_endconding
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
    html = get_html(url)

    soup = BeautifulSoup(html, 'lxml')
    liTags = soup.find_all('div', attrs={'class': 't_con cleafix'})
    for li in liTags:
        # 初始化一个字典来存储文章信息
        comment = {}
        try:
            # 开始筛选信息，并保存到字典中
            comment['title'] = li.find(
                'a', class_='j_th_tit').text.strip()
            comment['link'] = "http://tieba.baidu.com" + \
                li.find('a', attrs={'class': 'j_th_tit'})['href']
            comment['name'] = li.find(
                'span', attrs={'class': 'tb_icon_author'})['title']
            comment['replyNum'] = li.find(
                'span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()
            comment['ctime']= li.find(
                'span',class_='pull-right is_show_create_time').text.strip()
            #print('标题： {} \t 链接：{} \t 发帖人：{}  \t 回复数量： {} \t 发帖时间： {}\n'.format(
                #comment['title'], comment['link'], comment['name'],  comment['replyNum'],comment['ctime']))
            comments.append(comment)
        except:
           print('出现异常')

    return comments


def Out2File(dict,i):
    '''
    将爬取到的文件写入到本地
    保存到当前目录的 TTBT.txt文件中。
    '''
    with open('Onepiece.txt', 'a',errors='ignore') as f:
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
    lines = {}
    with open('Onepiece.txt','r') as f:
        lines = f.readlines()
    names,replynums=[],[]
    for line in lines:
        name_t = line.index('标题： ')+3
        name_w = line.index(' 	 链接：')
        name = line[name_t:name_w]
        names.append(name)
        rps = int(line[line.index('回复数量：') + 5: line.index(' 	 发帖时间')])
        replynums.append(rps)
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
    my_config.width = 1200
    chart = pygal.Bar(my_config,style=my_style)
    chart.title = '海贼王贴吧帖子与回帖数目'
    chart.add('',replynums)
    chart.x_labels = names
    chart.render_to_file('show_replynums.svg')


base_url = 'https://tieba.baidu.com/f?kw=海贼王&ie=utf-8'
# 设置需要爬取的页码数量
deep = 1

if __name__ == '__main__':
    main(base_url, deep)

    