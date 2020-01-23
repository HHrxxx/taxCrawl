# 国家税务总局
# 税收政策---最新文件

import requests
from bs4 import BeautifulSoup
import pymysql
import datetime

# 建立数据库连接
db_conn = pymysql.connect(host="localhost", user="root", password="root", db="taxspider", charset="utf8")
# 创建游标对象
cur = db_conn.cursor();

hdrs = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 '
}

# for i in range(2, 50):
# url = "http://www.chinatax.gov.cn/chinatax/manuscriptList/n8107" \
#       "24?_isAgg=0&_pageSize=20&_template=index&_channelName=%E7%A8%8E%E5%8A%A1%E6%96%B0%E9%97%BB&_keyWH=wenhao&page={}".format(i)
# url = "http://www.chinatax.gov.cn/chinatax/whmanuscriptList/n810755?_isAgg=0&_pageSize=20&_template=index&_channelName=%E6%9C%80%E6%96%B0%E6%96%87%E4%BB%B6&_keyWH=wenhao&page={}".format(
#     i)
url = "http://www.chinatax.gov.cn/chinatax/whmanuscriptList/n810755?_isAgg=0&_pageSize=20&_template=index&_channelName=%E6%9C%80%E6%96%B0%E6%96%87%E4%BB%B6&_keyWH=wenhao&page=3"
r = requests.get(url, headers=hdrs)
soup = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'html.parser')
# 获取指定class下的ul
ul_list = soup.find('ul', class_='list')
if (ul_list is None):
    print("None")
# 获取所有的li标签
li_list = ul_list.find_all('li')
print(url)
for item in li_list:
    k = item.find_all('a')[0]  # 获取a标签
    # hre = ur+k.get('href')  # 链接
    hre = k.get('href')  # 链接
    title = k.contents[0]  # 标题
    source = item.find_all('span')[0].contents[0]
    # source = "国家税务总局"
    # 获取content
    r = requests.get(hre, headers=hdrs)
    soup2 = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'html.parser')
    div_list2 = soup2.find_all('div', class_='text')
    content = ""
    postTime = ""
    if (len(div_list2) != 0):
        contentAll = div_list2[1]  # fontzoom
        p_list = contentAll.find_all('p')

        cnt = 0
        for i in p_list:
            content += i.text
            if (cnt == (len(p_list) - 2)):
                postTime = i.text  # 只有在文章内容中才有时间，不一定能爬取到，每个文章排版位置都不一样。

    data = (title, hre, source, content, postTime, 0, datetime.datetime.now())  # Date记录爬取时间
    try:
        cur.execute(
            "insert into china(Title,Url,Source,Content,PostTime,Status,Date) values('%s','%s','%s','%s','%s','%s','%s')" % (
                data))

        db_conn.commit()
    except Exception as err:
        print("sql语句执行错误", err)
        db_conn.rollback()

cur.close()
db_conn.close()
print('执行成功')
