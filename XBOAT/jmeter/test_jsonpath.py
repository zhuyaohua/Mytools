"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     test_jsonpath.py
@Author:   shenfan
@Time:     2022/5/24 15:32
"""
import jsonpath
import json
import os
import pymysql
import pandas
import prettytable

# connpool = {
#     "platform_test": pymysql.connect(host="10.80.252.199", port=3366, user="root", passwd="Cbim2021-"),
#     "platform_stg": pymysql.connect(host="172.16.201.252", port=3366, user="cbim", passwd="ChRd5@Hdhxt"),
#     "platform_prod": pymysql.connect(host="172.16.211.251", port=3366, user="cbim", passwd="ChRd5@Hdhxt"),
#     "project": pymysql.connect(host="10.81.3.57", port=3306, user="project_approval_manage",
#                                passwd="project_approval_manage"),
#     "project_stg": pymysql.connect(host="172.16.201.252", port=3366, user="project_approval_manage",
#                                    passwd="project_approval_manage"),
#     "annotation": pymysql.connect(host="10.81.3.51", port=3306, user="cbim_annotation",
#                                   passwd="cbim_annotation@Cbim123"),
#     "r2c": pymysql.connect(host="172.16.211.56", port=3306, user="root", passwd="mysql"),
#     "project_prod": pymysql.connect(host="172.16.211.252", port=3366, user="project_approval_manage",
#                                     passwd="project_approval_manage")
# }
#
# cmd = """
# SELECT mobile FROM bms_bms.cbim_user WHERE id in ({0})
# """


# def db_action(db_name, cmd):
#     print(cmd)
#     cur = connpool[db_name].cursor()
#     cur.execute(cmd)
#     # feilds = [item[0] for item in cur.description]
#     # table = prettytable.PrettyTable()
#     # table.field_names = feilds
#     # result = pandas.DataFrame(cur.fetchall(), columns=feilds)
#     # for item in result.values:
#     #     table.add_row(list(item))
#     # print(table)
#     result_all = cur.fetchall()
#     return result_all


BASE_DIR = os.path.abspath(".")
DATA_DIR = os.path.join(BASE_DIR, "user.json")

with open(DATA_DIR, "r", encoding="utf-8") as file:
    users = json.loads(file.read())
print(users)
r = jsonpath.jsonpath(users,"$.Content..[?(@.Name=='BmsDateSource')]")
print(r)
# 
# dataFrame = pandas.DataFrame(data, index=None)
# dataFrame.to_csv(os.path.join(BASE_DIR, "manager.csv"), index=False, decimal=".")
# count_true = 0
# count = []
# for item in users:
#     if len(eval(item["projPerson"])) == 2:
#         temp = {}
#         temp["Cbim-ProjectId"] = item["masterId"]
#         temp["Cbim-CityId"] = (eval(item["projRegion"]))[len((eval(item["projRegion"]))) - 1]["id"]
#         temp["UserId"] = eval(item["projPerson"])[1]["userId"]
#         temp["mobile"] = db_action("platform_prod", cmd.format(temp["UserId"]))[0][0]
#         data.append(temp)
#
# dataFrame = pandas.DataFrame(data, index=None)
# print(dataFrame)
# dataFrame.to_csv(os.path.join(BASE_DIR, "SJR.csv"), index=False, decimal=".")
