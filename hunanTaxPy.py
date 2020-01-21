# 湖南省税务局
# 税务新闻
import requests
from bs4 import BeautifulSoup
import pymysql

# 建立数据库连接
db_conn = pymysql.connect(host="localhost", user="root", password="root", db="taxspider", charset="utf8")
# 创建游标对象
cur = db_conn.cursor();

hdrs = {'User-Agent':'(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1'}

for i in range(1,10):
    url = "http://hunan.chinatax.gov.cn/lists/20190402001936/{}".format(i)
    ur="http://hunan.chinatax.gov.cn"#用于拼接文章详情的链接
    r = requests.get(url, headers=hdrs)
    soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), 'html.parser')

    # 获取指定div
    ul_list = soup.find('div', class_='newsList')
    # 获取所有的li标签
    li_list = ul_list.find_all('li')
    for item in li_list:
        if (len(item.find_all('a')) == 0): continue
        k = item.find_all('a')[0]  # 获取a标签
        hre = ur + k.get('href')  # 链接
        title = k.get('title')  # 标题
        postTime = item.find_all('span')[2].contents[0]  # 发布时间
        source = "湖南省税务局"
        # 获取文章内容
        r = requests.get(hre, headers=hdrs)
        soup2 = BeautifulSoup(r.content.decode('utf-8', 'ignore'), 'html.parser')
        div_list2 = soup2.find_all('div', class_='dynamic-detail__content')
        content = ""
        if (len(div_list2) == 0):
            break
        else:
            span_list = div_list2[0].find_all('p')
            for item in span_list:
                content += item.text

        data = (title, hre, source, content, postTime, 1)
        try:
            cur.execute(
                "insert into hunan(Title,Url,Source,Content,PostTime,Status) values('%s','%s','%s','%s','%s','%s')" % (
                    data))
            db_conn.commit()
        except Exception as err:
            print("sql语句执行错误", err)
            db_conn.rollback()

cur.close()
db_conn.close()
print('执行成功')

