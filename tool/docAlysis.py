"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     docAlysis.py
@Author:   shenfan
@Time:     2020/9/21 11:07
"""

import json
import os

BASEDIR = os.path.join(os.path.dirname(os.path.dirname(__file__)),"file","result.json")
print(BASEDIR)
with open(BASEDIR,"r",encoding="utf-8") as data:
    jsondata = json.load(data)

dic = []
for i in range(len(jsondata)):
    temp = {}
    name = jsondata[i].get("name")
    code = jsondata[i].get("prefix")+jsondata[i].get("code")
    projectManager = jsondata[i].get("users").get("projectManager")
    APPROVER = jsondata[i].get("users").get("APPROVER")
    VERIFIER = jsondata[i].get("users").get("VERIFIER")
    DESCIPLINE_CHIEF = jsondata[i].get("users").get("DESCIPLINE_CHIEF")
    DRAFING_DESIGNER = jsondata[i].get("users").get("DRAFING_DESIGNER")
    CHECKER = jsondata[i].get("users").get("CHECKER")

    temp.setdefault("name",name)
    temp.setdefault("code",code)
    temp.setdefault("项目经理",projectManager)
    temp.setdefault("审定",APPROVER)
    temp.setdefault("工种负责人", DESCIPLINE_CHIEF)
    temp.setdefault("设计制图人", DRAFING_DESIGNER)
    temp.setdefault("校对", CHECKER)
    temp.setdefault("审核", VERIFIER)
    dic.append(temp)

print(dic)


