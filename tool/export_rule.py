"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     export_rule.py
@Author:   shenfan
@Time:     2021/6/23 14:10
"""
import pandas
import os
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
from tool.compare_rule import mappingrule
basedir = os.path.dirname(os.path.abspath("__file__"))
def exportdata(rulelib):
    method = "get"
    url = "https://dev-rule.cbim.org.cn/cbim-rule/v1/rule/value/lines"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
    }
    params={"ruleLibId":rulelib}
    cookies = {"tool.tk":"4c83f08401eebf077609cc829992b599"}
    response = requests.request(method=method, url=url, headers=headers, params=params,cookies=cookies, verify=False)
    linedata = response.json()["result"]
    rawdata = []
    for item in linedata.values():
        temp = []
        for itemkey in item:
            print(itemkey)
        #     temp.append(itemkey["ruleValue"])
        # print(temp)
        # rawdata.append(temp)





if __name__ == '__main__':
    exportdata("556")
