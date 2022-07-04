"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     update_userinfo.py
@Author:   shenfan
@Time:     2022/6/22 9:10
"""
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def updateUserInfos(host, accountid, entid, session):
    headers = {"cbim-accountid": accountid, "content-type": "application/json;charset=UTF-8",
               "cookie": "CBIM-SESSION=%s" % session}
    url = host + "/app/user/api/v1/enterprise/%s/user/list?containDeleted=false" % entid
    body = {
        "ledgerType": 1,
        "name": "",
        "withPolicies": True,
        "pageNo": 1,
        "pageSize": 9999
    }
    response = requests.request(method="POST", url=url, headers=headers, json=body, verify=False)
    print(response.json())


if __name__ == "__main__":
    updateUserInfos("https://staging.cbim.org.cn","845274790427234305","845274790427234304","s%3AKpZyCCleKrp1gclCl66Y5zp9Mmepq4qd.Bm9TRVh%2FYGKl14m21E5IJGPnHSgKCwXrLl0gdPk3izc")