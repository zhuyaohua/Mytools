"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     project_info.py
@Author:   shenfan
@Time:     2022/6/10 12:15
"""
import requests
import json
from XBOAT.jmeter.DataDeal.database_info import db_action
from XBOAT.jmeter.DataDeal.data_output import savefile
import urllib3
import jsonpath

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

xboat_url = "https://staging-gw.cbim.org.cn/cbim-project-approval/proApproval/selectPage"
xboat_head = {
    "accountid": "845274790427234305",
    "session": "s%3AaUVZHoF4e2bFOcosE7-0ANArqjgnq7Kt.J7MpysapOOeajOlTxCAXLPAalgMgJcN4gXjtoI%2FZcd4",
    "entid": "845274790427234304",
    "content-type": "application/json"
}
data = {
    "pageNo": 1,
    "pageSize": 9999,
    "collection": None,
    "proName": "",
    "accessType": "1"
}
cmd = """
SELECT mobile FROM bms_bms.cbim_user WHERE id in ({0})
"""
response = requests.post(url=xboat_url, headers=xboat_head, data=json.dumps(data), verify=False).json()
count_true = 0
datas = []
for item in response["data"]["records"]:
    temp = {}
    temp["Cbim-ProjectId"] = item["masterId"]
    temp["Cbim-CityId"] = (eval(item["projRegion"]))[len((eval(item["projRegion"]))) - 1]["id"]
    temp["projectid"] = item["id"]
    response_user = requests.post(url="https://staging-gw.cbim.org.cn/cbim-project-approval/entRole/queryProjectUser",
                                  headers=xboat_head,
                                  data=json.dumps({"proApprovalId": item["id"]}),
                                  verify=False).json()
    data = jsonpath.jsonpath(response_user,"$.data..userList.*")
    print(data)
    for item_user in data:
        temp[item_user["name"].split("-")[0]+"userid"] = item_user["id"]
        temp[item_user["name"].split("-")[0]+"name"] = item_user["name"]
        temp[item_user["name"].split("-")[0]+"mobile"] = item_user["mobile"]
    temp["passwd"] = "cbim123456"

    datas.append(temp)

print(datas)
savefile(datas, "manager_deals.csv")
