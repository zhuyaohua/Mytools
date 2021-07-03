"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     SQLAction.py
@Author:   shenfan
@Time:     2020/9/8 10:48
"""
import pymysql

class dbaction:

    def __init__(self,dbname):
        self.dbname = dbname
        # self.conn = pymysql.connect(host="172.16.201.71",port=3306,user="root",passwd="dbpass",db=self.dbname)
        # self.conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="shenfan", db=self.dbname)
        # self.conn = pymysql.connect(host="172.16.201.185", port=3306, user="root", passwd="1q2w@3e4r", db=self.dbname)
        self.conn = pymysql.connect(host="172.16.201.122", port=3306, user="root", passwd="dbpass", db=self.dbname)
        print("-"*20,"%s数据库"%dbname,"-"*20)
        self.cur = self.conn.cursor()

    def connection(self):
        return self.cur

    def query(self,cmd,**kwargs):
        self.cur.execute(cmd)
        return  self.cur.fetchall()

    def close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        print("-" * 20, "%s数据库关闭"%self.dbname, "-" * 20)
db = dbaction("cbim_design")
db.connection()
for i in range(3, 50):
    cmd = "INSERT INTO sub_project (name,project_id,sub_project_number,state) VALUES ('图形实例-%s','4089','%d','1');"%(i,i)
    result = db.query(cmd)



result = db.query("select * from sub_project where project_id = '4089'")
print(result)
db.close()








