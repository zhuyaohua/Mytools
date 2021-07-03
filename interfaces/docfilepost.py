"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     docfilepost.py
@Author:   shenfan
@Time:     2020/9/8 10:03
"""

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
from common.settings import config

host = config().get("Test").get("environ").get("uri")
interfaceurl = "api/material/v1/projects/2397/subs/1031/models/rooms"
cookies = {"tool.tk":ticket().reticket()}
url = host+interfaceurl

files = {
    "file": open(r"C:\Users\SHENFAN\Desktop\中设数字\标准模板\房间表\房间用料表.txt","rb")
}

respose = requests.post(url=url,cookies=cookies,files=files,verify=False)
with open(os.path.join(os.path.dirname(os.path.abspath(".")),"file","result.json"),"w",encoding="utf-8") as data:
    data.write(json.dumps(respose.json(),indent=4,ensure_ascii=False))










