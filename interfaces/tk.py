"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     tk.py
@Author:   shenfan
@Time:     2020/9/7 11:29
"""
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import hashlib
import time
from common.settings import config

class ticket:
    def __init__(self,env,username,entcode):
        self.username = username
        self.entcode = entcode
        self.__uri = config().get(env).get("ticket").get("uri")
        self.__appkey = config().get(env).get("ticket").get("appkey")
        self.__appid = config().get(env).get("ticket").get("appid")
        self.__ts = str(int(time.time()*1000))
        sha1 = hashlib.sha1((self.__appkey + "," + self.__uri + "," + self.__ts).replace("-","").encode("utf-8"))
        self.__sign = sha1.hexdigest().lower()
        self.__headers = {
            "Content-Type": "application/json",
            "appid": self.__appid,
            "sign": self.__sign,
            "ts": self.__ts,
        }
        self.__data =eval(config().get(env).get("ticket").get("ticketdata"))
        self.__url = config().get(env).get("environ").get("cas")
        self.__loginurl = config().get(env).get("environ").get("uri")+"/api/user/public/v1/user/applyToken?email={0}&entCode={1}&tgt=".format(self.username,self.entcode)

    def reticket(self):
        self.loginurl = self.__loginurl+requests.post(url=self.__url,headers=self.__headers,json=self.__data,verify=False).json().get("data").get("ticket")
        return requests.get(self.loginurl,verify=False).json().get("result")

    def reheaders(self):
        cookie = self.reticket()
        return self.__headers.update({"Cookie":cookie})


print(ticket("Test","shenf@cadg.cn","cadg").reticket())



















