"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     postman.py
@Author:   shenfan
@Time:     2020/11/16 14:16
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
appKeycbim30= "07ec7d475a084efdb99d1e832741df74"
appidcbim30= "8af5d9e72b7b4afa8c4a008436a1cf62"

"""
cprod
"""
# appid = "8d116d26c7d8d73396e15fb4a2cba1ca"
# appkey = "048b8927d20516ed9a40d8d05dffc18d"

def signature(method,uri,timestamp,appid,randomstr,body):
    key = bytearray(appid, encoding="utf8")
    randomstr = randomstr
    if body:
        message = bytearray("%s\n%s\n%s\n%s\n%s"%(method.lower(),uri.lower(),timestamp,randomstr,body),encoding="utf-8")
    else:
        message = bytearray("%s\n%s\n%s\n%s"%(method.lower(),uri.lower(),timestamp,randomstr),encoding="utf-8")
    sign = base64.b64encode(hmac.new(key, message, digestmod="sha256").digest())
    return sign


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
        print("登录信息:")
        print("url",self.url)
        print("headers",self.headers)
        print("data",self.params)


        try:
            reponse_tickct = requests.request(method="post", url=self.url, headers=self.headers,
                                              data=json.dumps(self.params), verify=False)
            self.ticket = reponse_tickct.json().get("data").get("ticket")
            self.entid = reponse_tickct.json().get("data").get("entId")
            self.userid = reponse_tickct.json().get("data").get("userId")
            print("ticket",self.ticket)
        except:
            print("用户账号异常")
            pass

    def retoken(self):
        return self.ticket

    def interface(self, host, path, method):
        interface_ts = str(int(time.time() * 1000))
        interface_sign = hashlib.sha1((appkey + "," + path + "," + interface_ts).replace("-", "").encode("utf-8")).hexdigest().lower()

        cookies = {"delivery.tk": self.ticket,
                   "tool.tk":self.ticket
                   }
        url = host + path
        print("*" * 10, "接口测试", "*" * 10)
        print(cookies)

        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "env":"cdev",
            "ticket": self.ticket,
            "ts": interface_ts,
            "sign": interface_sign,
            "appid": appid
        }  # 将请求信息以字典、元素列表或者字节的方式提供
        print("headers: ", headers)
        path_params = {
            # "projectId":4,
            # "subProjectId":1,
            # "majorId":1
        }
        params = {
            # "projectId":947978427435061248,
            "type":1,
            "synStatus":1
        }  # 将请求信息以字典、元素列表或者字节的方式提供
        print("params: ", params)
        files = {
            # "bacthfile": open(r"C:\Users\SHENFAN\Desktop\中设数字\标准模板\房间表\房间用料表.txt","rb")
        }  # 将请求信息以文件的方式提供，必须以二进制的方式读取
        # with open(r"D:\Doctool\python\工具脚本\file\doctool.html","r",encoding="utf-8") as rawdata:
        #     data = rawdata.read()
        data = {
            # "currentNodeId":3,
            # "id": "1446684199476156160",
            # "linkId": "8120",
            # "linkType": 1,
            # "nextNodeId": 4
        }  # 将请求信息以字典、元素列表或者字节的方式提供
        if path_params:
            if isinstance(path_params, dict):
                url = url.format(**path_params)
            elif isinstance(path_params, list):
                url = url.format_map(dict(path_params))
            else:
                raise TypeError
        print(url)
        filename = path.split("/")[-1] + "-result.json"
        timestart = time.time()
        respose = requests.request(method=method, url=url, headers=headers, params=params,data=json.dumps(data),files=files, cookies=cookies, verify=False)

        timeend = time.time()
        duration = round((timeend - timestart), 3)
        print("respose: ", respose.json())
        if duration > 0.2:
            print("\033[1;45m 请求时间%s \033[0m" % duration)
        with open(os.path.join(os.path.dirname(os.path.abspath(".")), "file", filename), "w", encoding="utf-8") as data:
            data.write(json.dumps(respose.json(), indent=4, ensure_ascii=False))
        return respose

    def interface_cbim30(self, host, path, method):
        randomstr = str(uuid.uuid1())
        timestamp = str(int(time.time()*1000))
        url = host + path
        print("*" * 10, "接口测试", "*" * 10)
        # with open(r"D:\Doctool\python\工具脚本\file\doctool.html","r",encoding="utf-8") as rawdata:
        #     data = rawdata.read()
        data = {"username": "18571023517","password": "s123456","terminal": "web"}  # 将请求信息以字典、元素列表或者字节的方式提供
        Authorization = "CBIM:"+appKeycbim30+":"+randomstr+":"+str(signature(method,path,timestamp,appidcbim30,randomstr,body=json.dumps(data)),"utf-8")
        print(Authorization)
        headers = {
            "Authorization":Authorization,
            "Date":timestamp
        }  # 将请求信息以字典、元素列表或者字节的方式提供
        print(headers)
        print("headers: ", headers)
        cookies = {}
        path_params = {
        }
        params = {
        }
        print("params: ", params)
        files = {
            # "bacthfile": open(r"C:\Users\SHENFAN\Desktop\中设数字\标准模板\房间表\房间用料表.txt","rb")
        }  # 将请求信息以文件的方式提供，必须以二进制的方式读取
        if path_params:
            if isinstance(path_params, dict):
                url = url.format(**path_params)
            elif isinstance(path_params, list):
                url = url.format_map(dict(path_params))
            else:
                raise TypeError
        print(url)
        filename = path.split("/")[-1] + "-result.json"
        timestart = time.time()
        respose = requests.request(method=method, url=url, headers=headers, params=params,data=json.dumps(data),files=files, cookies=cookies, verify=False)

        timeend = time.time()
        duration = round((timeend - timestart), 3)
        print("respose: ", respose.json())
        if duration > 0.2:
            print("\033[1;45m 请求时间%s \033[0m" % duration)
        with open(os.path.join(os.path.dirname(os.path.abspath(".")), "file", filename), "w", encoding="utf-8") as data:
            data.write(json.dumps(respose.json(), indent=4, ensure_ascii=False))
        return respose

if __name__ == "__main__":
    # count = 0
    # for i in range(2):
    #     print("")
    #     print("#"*80,"第%i次调用："%i,"#"*80)
    #     p = postman("https://cctc-oms.cbim.org.cn","shenf@cadg.cn","123456","cadg")
    #     if p.interface("https://cctc-doctool.cbim.org.cn","/api/utmt/v1/drawLists/version","get").json()["result"]:
    #         count += 1
    #         print("&"*100,"失败")
    # print("失败%i次"%count)

    # cdm环境
    # p = postman("http://account.cbim.cctc.com","shenhongxiang","Star2021","cadg")
    # p.interface("http://doctool.cbim.cctc.com","/api/doctool/v1/projects","get")

    # p1 = postman("https://c-extapi.cbim.org.cn","Delivery-dev-01@cadg.cn","d123456","delivery")
    # p1.interface("https://deliverytest.cbim.org.cn:8888","/api/cbim-delivery/pda/v2/base/projects","get")
    # p1.interface("https://dev-cbim-design.cbim.org.cn","/external/api/taskForm/getTaskForms","post")
    # p1.interface_cbim30("https://test-cas.cbim.org.cn:8443","/v1/external/user/ticket","post")

    # CCTC环境
    p = postman("https://cctc-oms.cbim.org.cn", "2013061@cadg.cn", "d123456", "cadg")
    p.interface("https://cctc-dms.cbim.org.cn", "/external/api/user/myInfo", "post")

    #cprod环境交付平台
    # p = postman("https://cdm.cbim.org.cn", "shenf@cadg.cn", "s123456", "dev")
    # p.interface("https://cdm.cbim.org.cn", "/external/api/user/myInfo", "post")




