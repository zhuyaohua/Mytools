"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     interfaceSet.py
@Author:   shenfan
@Time:     2020/9/16 11:37
"""


from common.settings import config
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import json
import os



method = "post"
host = config().get("Test").get("environ").get("uri")
# # cookies = {"delivery.tk":"5f5647ae822ff41eea9faa3057d23559","tool.tk":"a5a6ed5d29847c4361e29111d3fbddef"}
cookies = {
    "delivery.tk":"ee747503047d8232a60dadcce186e952",
    "tool.tk":"TGT-101-ptM29QG-3w3onYyiK7cZBKTQA2qSDOB-0tDWLoxIVIbvVjiX44MFjO-iu6xds-8m93U-apps"
}
# cookies = {"tool.tk":ticket("Test","shenf@cadg.cn","pttest").reticket()}
interfaceurl = "/api/cbim-delivery/pda/v1/rule/engine/design/formRuleCal"
# url = host+interfaceurl
url = "https://delivery.cbim.org.cn/api/cbim-delivery/pda/v1/rule/engine/design/formRuleCal"
headers = {
    "Content-Type": "application/json;charset=UTF-8"
} #将请求信息以字典、元素列表或者字节的方式提供
path_params = {

}
params = {
    "type":1
} #将请求信息以字典、元素列表或者字节的方式提供
# data  = {
# } #将请求信息以字典、元素列表或者字节的方式提供
with open(r"D:\Doctool\python\工具脚本\file\pda.json","r",encoding="utf-8") as rawdata:
    data = json.load(rawdata)

files = {
# "file": open(r"C:\Users\SHENFAN\Desktop\中设数字\标准模板\房间表\房间用料表.txt","rb")
} #将请求信息以文件的方式提供，必须以二进制的方式读取

print(type(params))

if path_params:
    if isinstance(path_params,dict):
        url=url.format(**path_params)
    elif isinstance(path_params,list):
        url=url.format_map(dict(path_params))
    else:
        raise TypeError

filename = interfaceurl.split("/")[-1]+"-result.json"
print(url)
def interface():
    respose = requests.request(method=method,url=url,headers=headers,params=params,data=json.dumps(data),files=files,cookies=cookies,verify=False)
    print(str(respose.text))
    print(respose.content)
    with open(os.path.join(os.path.dirname(os.path.abspath(".")),"file",filename),"w",encoding="utf-8") as resultdata:
        resultdata.write(json.dumps(respose.json(),indent=4,ensure_ascii=False))

for i in range(1):
    print(i)
    interface()
