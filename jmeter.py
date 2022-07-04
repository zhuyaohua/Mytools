"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     jmeter.py
@Author:   shenfan
@Time:     2021/12/16 10:21
"""
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import time
import hashlib
import json
import os
import time
import hmac
import base64
import uuid


appid = "43be49a510d8221efbb2d63d579aab15"
appkey = "515a2e95179d603d7d82a68102c58ff2"

class postman:
    def __init__(self, env, username, password, entcode):
        self.env = env
        self.username = username
        self.password = password
        self.entcode = entcode
        self.url = self.env + "/external/api/user/request_ticket"
        self.uri = "/external/api/user/request_ticket"
        self.ts = str(int(time.time() * 1000))
        self.sign = hashlib.sha1(
            (appkey + "," + self.uri + "," + self.ts).replace("-", "").encode("utf-8")).hexdigest().lower()
        self.headers = {
            "Content-Type": "application/json",
            "appid": appid,
            "sign": self.sign,
            "ts": self.ts,
        }
        self.params = {
            "userName": self.username,
            "password": self.password,
            "code": self.entcode
        }

        try:
            reponse_tickct = requests.request(method="post", url=self.url, headers=self.headers,
                                              data=json.dumps(self.params), verify=False)
            self.ticket = reponse_tickct.json().get("data").get("ticket")
            self.entid = reponse_tickct.json().get("data").get("entId")
            self.userid = reponse_tickct.json().get("data").get("userId")
            print(self.ticket)
        except:
            print("用户账号异常")
            pass

    def retoken(self):
        return self.ticket

if __name__ == "__main__":
    p = postman("http://account.cbim.cctc.com","shenhongxiang","Star2021","cadg")








