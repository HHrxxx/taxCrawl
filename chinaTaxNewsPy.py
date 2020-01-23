# 国家税务总局
# 税务新闻

import requests
from bs4 import BeautifulSoup
import pymysql

# 建立数据库连接
db_conn = pymysql.connect(host="localhost", user="root", password="root", db="taxspider", charset="utf8")
# 创建游标对象
cur = db_conn.cursor();

hdrs = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'}

for i in range(1,50):
    # url = "http://www.chinatax.gov.cn/chinatax/manuscriptList/n8107" \
    #       "24?_isAgg=0&_pageSize=20&_template=index&_channelName=%E7%A8%8E%E5%8A%A1%E6%96%B0%E9%97%BB&_keyWH=wenhao&page={}".format(i)
    url = "http://www.chinatax.gov.cn/chinatax/manuscriptList/n810724?_isAgg=0&_pageSize=20&_template=index&_channelName=税务新闻&_keyWH=wenhao&page={}".format(i)
    ur = "http://www.chinatax.gov.cn"  # 拼接
    r = requests.get(url, headers=hdrs)
    soup = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'html.parser')

    # 获取指定class下的ul
    ul_list = soup.find('ul', class_='list')
    if (ul_list is None):
        print("None")
        continue
    # 获取所有的li标签
    li_list = ul_list.find_all('li')
    print(i)
    for item in li_list:
        k = item.find_all('a')[0]  # 获取a标签
        # hre = ur+k.get('href')  # 链接
        hre = k.get('href')  # 链接
        title = k.contents[0]  # 标题
        postTime = item.find_all('span')[0].contents[0][1:-1]
        source = "国家税务总局"
        # 获取content
        r = requests.get(hre, headers=hdrs)
        soup2 = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'html.parser')
        div_list2 = soup2.find_all('div', class_='text')
        content = ""
        if (len(div_list2) == 0):
            break
        contentAll = div_list2[1]  # fontzoom
        p_list = contentAll.find_all('p')

        for i in p_list:
            content = content + i.text

        data = (title, hre, source, content, postTime, 0)
        try:
            cur.execute(
                "insert into china(Title,Url,Source,Content,PostTime,Status) values('%s','%s','%s','%s','%s','%s')" % (
                    data))

            db_conn.commit()
        except Exception as err:
            print("sql语句执行错误", err)
            db_conn.rollback()

cur.close()
db_conn.close()
print('执行成功')
