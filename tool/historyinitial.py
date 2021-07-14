"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     historyinitial.py
@Author:   shenfan
@Time:     2021/7/9 11:16
"""
from tool.SQL import insert,query

db = "doctool_dev"
cmd = """SELECT sub_project.id FROM cbim_design.sub_project left JOIN cbim_design.project ON project.id = sub_project.project_id WHERE project.`owner` = '425403443028426753'"""

subpeojectid = query(db,cmd)
print(subpeojectid)

db = "delivery_dev"
cmd = """select id,model_name,is_latest_version,is_latest_version_line,version_line FROM cbim_delivery.base_model WHERE sub_project_id = {0}"""


for item in subpeojectid:
    print(cmd.format(item[0]))
    print(query(db,cmd.format(item[0])))



