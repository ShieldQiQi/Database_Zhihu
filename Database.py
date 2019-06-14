# Create in 2019-05-28
# Project: Store data from Zhihu in Mysql Database
# Author: SHIELD_QIQI
from pymysql import *

# 创建一个MYSQL类，用以连接数据库
class MysqlQI:
    def __init__(self):
        super().__init__()
    # connect my sql Database
    conn = connect(host='localhost', port=3306, user='SHIELD_QIQI', passwd='92c5', db='urldata', charset='utf8')
    # 设置自动提交
    conn.autocommit(1)
    cur = conn.cursor()
