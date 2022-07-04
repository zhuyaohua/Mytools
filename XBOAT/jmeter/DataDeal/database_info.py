"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     database_info.py
@Author:   shenfan
@Time:     2022/6/10 11:19
"""
import pymysql
import prettytable
import pandas

connpool = {
    "platform_prod": pymysql.connect(host="172.16.211.251", port=3366, user="cbim", passwd="ChRd5@Hdhxt"),
    "project_prod": pymysql.connect(host="172.16.211.252", port=3366, user="project_approval_manage",
                                    passwd="project_approval_manage")
}


def db_action(db_name, cmd):
    print("*"*30)
    print("Execution SQL：")
    print(cmd)
    print("*"*30)
    print("Result:")
    cur = connpool[db_name].cursor()
    cur.execute(cmd)
    feilds = [item[0] for item in cur.description]
    table = prettytable.PrettyTable()
    table.field_names = feilds
    result_raw = cur.fetchall()
    result = pandas.DataFrame(result_raw, columns=feilds)
    for item in result.values:
        table.add_row(list(item))
    print(table)
    return result_raw
