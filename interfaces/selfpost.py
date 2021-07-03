"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     selfpost.py
@Author:   shenfan
@Time:     2020/12/31 10:43
"""

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
import hashlib
import json
import os
import time



class postman:
    def __init__(self,url):
        self.url = url
        self.headers = {
            "Content-Type": "application/json",
        }

    def interface(self,host,path,method):
        cookies = {}
        print("*"*10,"接口测试","*"*10)
        # print(url)
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
        }  # 将请求信息以字典、元素列表或者字节的方式提供
        print("headers: ",headers)
        path_params = {
        }
        params = {
        }  # 将请求信息以字典、元素列表或者字节的方式提供
        print("params: ",params)
        data = {
        }# 将请求信息以字典、元素列表或者字节的方式提供

        files = {
            # "file": open(r"C:\Users\SHENFAN\Desktop\中设数字\标准模板\房间表\房间用料表.txt","rb")
        }  # 将请求信息以文件的方式提供，必须以二进制的方式读取

        if path_params:
            if isinstance(path_params, dict):
                self.url = self.url.format(**path_params)
            elif isinstance(path_params, list):
                self.url = self.url.format_map(dict(path_params))
            else:
                raise TypeError

        print(self.url)

        filename = path.split("/")[-1] + "-result.json"
        timestart = time.time()
        respose = requests.request(method=method, url=self.url, headers=headers, params=params, data=json.dumps(data),
                                   files=files, cookies=cookies, verify=False)
        timeend = time.time()
        duration = round((timeend - timestart),3)
        print("respose: ",respose.json())
        if duration > 0.2:
            print("\033[1;45m 请求时间%s \033[0m"%duration)
        with open(os.path.join(os.path.dirname(os.path.abspath(".")), "file", filename), "w", encoding="utf-8") as data:
            data.write(json.dumps(respose.json(), indent=4, ensure_ascii=False))
        return respose


#test环境
p = postman("https://doms.cbim.org.cn","shenf@cadg.cn","654321","cadg")
p.interface("https://dev-design.cbim.org.cn","/external/api/taskForm/getUserPositions","post")






