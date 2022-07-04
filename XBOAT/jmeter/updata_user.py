"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     updata_user.py
@Author:   shenfan
@Time:     2022/5/18 9:15
"""
import requests
import json
import urllib3
import jsonpath
import re
import os
import random

BASE_DIR = os.path.abspath("..")
DATA_DIR = os.path.join(BASE_DIR, "user.json")
DATA_DIR_DEP = os.path.join(BASE_DIR, "dep_tree.json")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open(DATA_DIR, "r", encoding="utf-8") as file:
    users = jsonpath.jsonpath(json.loads(file.read()), "$.data.users.*.name")

with open(DATA_DIR_DEP, "r", encoding="utf-8") as file:
    depinfo = re.findall(r"(?<='depId': ')\d+(?=', )", str(json.loads(file.read())))
print(random.choice(users), random.choice(depinfo))


def query_all_user(entid, accountid, seesion):
    url = "https://www.cbim.org.cn/app/user/api/v1/enterprise/%s/user/list?containDeleted=false" % entid
    headers = {
        "content-type": "application/json;charset=utf-8",
        "cbim-accountid": accountid,
        "cookie": "CBIM-SESSION=%s" % seesion
    }
    data = {
        "ledgerType": 1,
        "name": "",
        "withPolicies": True,
        "pageNo": 1,
        "pageSize": 2000
    }
    reponse = requests.request("POST", url=url, headers=headers, data=json.dumps(data), verify=False).json()
    print(reponse)
    return reponse


def updata_dep(entid, accountid, seesion):
    headers = {
        "content-type": "application/json;charset=utf-8",
        "cbim-accountid": accountid,
        "cookie": "CBIM-SESSION=%s" % seesion
    }
    userinfo = jsonpath.jsonpath(query_all_user(entid, accountid, seesion), "$.data.list.*")
    for item in userinfo:
        if item["trueName"].isalpha():
            url = "https://www.cbim.org.cn/app/user/api/v1/enterprise/%s/user/%s" % (entid, item["id"])

            data = {
                "before": {
                    "trueName": item["trueName"],
                    "sex": 0,
                    "mobile": item["mobile"],
                    "number": "",
                    "departments": [{
                        "id": item["department"][0]["id"]
                    }]
                },
                "after": {
                    "trueName": random.choice(users) + "(测试)",
                    "sex": 0,
                    "mobile": item["mobile"],
                    "number": "",
                    "departments": [{
                        "id": random.choice(depinfo),
                        "jobIds": []
                    }],
                    "isOutAssist": False
                }
            }
            reponse = requests.request("PUT", url=url, headers=headers, data=json.dumps(data), verify=False).json()
            print(reponse)
    return len(userinfo)


def updata_user(entid, accountid, seesion):
    headers = {
        "content-type": "application/json;charset=utf-8",
        "Authorization": "CBIM-SESSION=%s" % seesion
    }
    userinfo = jsonpath.jsonpath(query_all_user(entid, accountid, seesion), "$.data.list.*")
    mobile = 15000000000
    for item in userinfo:
        if item["mobile"] not in ["18571023517", "13171102617", "19022341200", "15327181300", "13100697039",
                                  "15133133325", "18889622765", "18571852821"]:
            print(item["mobile"])
            url = "https://test2.cbim.org.cn/api/bms/v1/user/%s" % (item["id"])
            data = {
                "avatarUrl": "",
                "email": "",
                "isOutAssist": False,
                "mobile": str(mobile),
                "modifiedById": 0,
                "number": "",
                "sex": 0,
                "trueName": "",
                "username": ""
            }
            reponse = requests.request("PUT", url=url, headers=headers, data=json.dumps(data), verify=False).json()
            mobile = + 1


# updata_dep("832258896088403968", "832258896088403969","s%3AqaDSShtJ162SecUZ0cewntonut2dWPde.RkPFS%2Brx24jmWo9wSXGjOGdCWlQCG%2FRopn6iD1VcVwM")

if __name__ == "__main__":
    updata_user("832258896088403968", "832258896088403969",
                "s%3Aw-lx_OYkQKcp8Rv4Fo0pqXwy7rSOglFG.MiJbxk87WmoWj9yEPQcjfrkO5Oubod9UNCfgvMa8%2Fkc")
    # query_all_user("832258896088403968", "832258896088403969","s%3AtqZrOIcV9lfqX00KkRtBQa-PznDz21m1.o3oAJxnai3pltX23Dx6QAriynrTmAQF2GTkeU5zcmfo")
