# 国家税务总局
# 税收政策---最新文件

import requests
from bs4 import BeautifulSoup
import pymysql

# 建立数据库连接
db_conn = pymysql.connect(host="localhost", user="root", password="root", db="taxspider", charset="utf8")
# 创建游标对象
cur = db_conn.cursor();

hdrs = {
    'User-Agent':
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'
}
url = "http://www.chinatax.gov.cn/chinatax/whmanuscriptList/n810755?_channelName=%E6%9C%80%E6%96%B0%E6%96%87%E4%BB%B6&_isAgg=0&_pageSize=20&_template=index"
r = requests.get(url, headers=hdrs)
soup = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'html.parser')

# 获取指定class下的ul
ul_list = soup.find('ul', class_='list')
# 获取所有的a标签
href_list = ul_list.find_all('a')
# 获取所有span标签
span_list = ul_list.find_all('span')

count = 0
for item in ul_list:
    hre = href_list[count]['href']  # 链接
    source = span_list[count].contents[0]  # 来源
    title = href_list[count].contents[0]  # 标题
    count = count + 1

    #获取content，postTime
    r = requests.get(hre, headers=hdrs)
    soup2 = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'html.parser')
    div_list = soup2.find_all('div', class_='text')
    content = ""
    postTime = ""
    if(len(div_list)>=1):
        contentAll = div_list[1]  # fontzoom
        p_list = contentAll.find_all('p')
        length=len(p_list)
        cnt = 0
        for i in p_list:
            c=i.text
            if (cnt==(length-2)):
                postTime=c
            if (cnt == (length - 1)):
                break
            content = content + c
            cnt+=1

    data = (title, hre, source, content,postTime,0)
    try:
        cur.execute("insert into china(Title,Url,Source,Content,PostTime,Status) values('%s','%s','%s','%s','%s','%s')" % (data))
        # 事物提交
        db_conn.commit()
    except Exception as err:
        print("sql语句执行错误", err)
        db_conn.rollback()

cur.close()
db_conn.close()
print('执行成功')
