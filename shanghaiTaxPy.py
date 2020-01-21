# 上海市税务局
# 税务新闻
import requests
from bs4 import BeautifulSoup
import pymysql

# 建立数据库连接
db_conn = pymysql.connect(host="localhost", user="root", password="root", db="taxspider", charset="utf8")

# 创建游标对象
cur = db_conn.cursor();

hdrs = {
    'User-Agent':
        '(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3'
}
for i in range(1,13):
    #爬分页数据
    url = "http://shanghai.chinatax.gov.cn/xwdt/swxw/index_{}.html".format(i)
    us="http://shanghai.chinatax.gov.cn/xwdt/swxw"
    r = requests.get(url, headers=hdrs)
    soup = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'html.parser')
    # 获取指定ul 税务新闻模块
    ul_list = soup.find('ul', class_='infolist')
    # print(ul_list)
    # 获取所有的li标签
    li_list =ul_list.find_all('li')
    for item in li_list:
        k = item.find_all('a')[0]  # 获取a标签
        hre = us + k.get('href')[1:]  # 链接
        title = k.get('title')  # 标题
        postTime = item.find_all('span')[1].contents[0]  # 发布时间
        source = "上海市税务局"
        # 获取文章内容
        r = requests.get(hre, headers=hdrs)
        soup2 = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'html.parser')
        div_list2 = soup2.find_all('div', class_='TRS_Editor')
        content = ""
        if (len(div_list2) == 0):
            break
        else:
            p_list = div_list2[0].find_all('p')
        for item in p_list:
                content += item.text
        data = (title, hre, source, content, postTime, 1)
        try:
            cur.execute(
                "insert into shanghai(Title,Url,Source,Content,PostTime,Status) values('%s','%s','%s','%s','%s','%s')" % (
                    data))
            db_conn.commit()
        except Exception as err:
            print("sql语句执行错误", err)
            db_conn.rollback()

cur.close()
db_conn.close()
print('执行成功')
