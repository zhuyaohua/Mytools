"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     doctoolapitest.py
@Author:   shenfan
@Time:     2020/9/7 17:08
"""

from interfaces.tk import ticket
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import os
import json

host = "https://test-doctool.cbim.org.cn/"
interfaceurl = "/v1/projects/2397/subs/1031/docs/1208/navi?projectId=2397&subProjectId=1031&docId=1208&templateId=20532&parentId=0"
cookies = {"tool.tk":ticket().reticket()}
print(cookies)

url = host+interfaceurl
# param = {"type":1}

# respose = requests.get(url=url,params=param,cookies=cookies,verify=False)
respose = requests.get(url=url,cookies=cookies,verify=False)
with open(os.path.join(os.path.dirname(os.path.abspath(".")),"file","result_doc1028.json"),"w",encoding="utf-8") as data:
    data.write(json.dumps(respose.json(),indent=4,ensure_ascii=False))







