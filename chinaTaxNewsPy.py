# 国家税务总局
# 税务新闻

import requests
from bs4 import BeautifulSoup
import pymysql

# 建立数据库连接
db_conn = pymysql.connect(host="localhost", user="root", password="root", db="taxspider", charset="utf8")
# 创建游标对象
cur = db_conn.cursor();

hdrs = {'User-Agent': '(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3'}

for i in range(1, 10):
    url = "http://www.chinatax.gov.cn/chinatax/manuscriptList/n810724?_isAgg=0&_pageSize=20&_template=index&_channelNam" \
          "e=%E7%A8%8E%E5%8A%A1%E6%96%B0%E9%97%BB&_keyWH=wenhao&page={}".format(i)
    r = requests.get(url, headers=hdrs)
    soup = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'html.parser')

    # 获取指定class下的ul
    ul_list = soup.find('ul', class_='list')
    # 获取所有的li标签
    li_list = ul_list.find_all('li')

    for item in li_list:
        k = item.find_all('a')[0]  # 获取a标签
        hre = k.get('href')  # 链接
        title = k.contents[0]  # 标题
        postTime = item.find_all('span')[0].contents[0]
        source="国家税务总局"
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
            content = content+i.text

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
