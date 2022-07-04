"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     create_dep.py
@Author:   shenfan
@Time:     2022/5/17 9:14
"""
import os
import json
import jsonpath
import requests
import time
import random

BASE_DIR = os.path.abspath("..")
DATA_DIR = os.path.join(BASE_DIR, "jmeter", "dep.json")

with open(DATA_DIR, "r", encoding="utf-8") as file:
    dep = json.loads(file.read())

entId = "837992076821008384"
accountId = "837992076821008385"
session = "CBIM-SESSION=s%3AMO9vysPylw5EN0fdekxCHjzxlslmtLM6.X2a0rHjUIBzBCWMDostok5xHZEnMGGj7WIID9XceJUA"


def create_dep(name, parentId, entId=entId, accountId=accountId, session=session):
    X_url = "https://test2.cbim.org.cn/app/user/api/v1/enterprise/%s/department" % entId
    X_headers = {"cbim-accountid": accountId, "cookie": session}
    X_data = {"name": name, "parentId": parentId}
    reponse = requests.request(method="POST", url=X_url, headers=X_headers, data=X_data, verify=False)
    time.sleep(3)
    if reponse.json()["data"] is None:
        return "832566047872782336"
    else:
        print(reponse.json())
        return reponse.json()["data"]


dep_temp = {}


def dic_find(rootNode, iterNode=None):
    for item in dep:
        iterNode = create_dep(item["name"], rootNode)
        if not dep["children"]:
            dep_temp[iterNode] = {}


print(dep)
