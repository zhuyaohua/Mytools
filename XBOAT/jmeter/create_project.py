"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     create_project.py
@Author:   shenfan
@Time:     2022/4/29 15:07
"""
import requests
import json
import urllib3
import time
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

xboat_url_form = "https://staging-gw.cbim.org.cn/cbim-project-approval/proApproval/getFormModel"
xboat_region = "https://staging-gw.cbim.org.cn/cbim-project-approval/form/presetOption"
xboat_url = "https://staging-gw.cbim.org.cn/cbim-project-approval/proApproval/save"
xboat_head = {"accountid": "832258896088403969",
              "session": "s%3AwDZGVmrIG6IW49kZrsMOFcjWLAdkko4M.p1f%2B2YutypO46Ygv4mZ3pf2GySqDiJkiL%2BYe7Aj4zC8",
              "entid": "832258896088403968", "content-type": "application/json"}
formdata = requests.get(url=xboat_url_form, headers=xboat_head).json()
regeiondata = requests.post(url=xboat_region, headers=xboat_head, data=json.dumps({"id": "constructionArea"}),
                            verify=False).json()

currentVersionId = formdata["data"]["currentVersionId"]
formdata_input = formdata["data"]["formDefine"]
user = [("郭郭郭","830012616087855104"),("沈番","749640057096544256"),("何晶晶","745276028416221184"),("李昊","744915459759611904"),("李黄煌","744863550427422720")]



for item_province in regeiondata["data"]["list"]:
    if item_province in ["广西省","吉林省","辽宁省","湖北省","陕西省","山东省"]:
        break
    temp_label = []
    temp_value = []
    for item_city in item_province["children"]:
        step = random.randint(0, 99)
        print(step)
        if step % 3 == 0:

            m = random.randint(0,4)
            try:
                for item_county in item_city["children"]:
                    n = random.randint(0,4)
                    formdata_input["FormValues"]["id_1638515436382"]["label"] = [item_province["label"], item_city["label"], item_county["label"]]
                    formdata_input["FormValues"]["id_1638515436382"]["value"] = [item_province["value"], item_city["value"], item_county["value"]]
                    formdata_input["FormValues"]["id_1638515436376"]["label"] = ["中设数字项目-%s" % item_county["label"]]
                    formdata_input["FormValues"]["id_1638515436376"]["value"] = ["中设数字项目-%s" % item_county["label"]]

                    formdata_input["FormValues"]["id_1638515436377"]["label"] = ["SZ%s" % int(float(time.time())*100000)]
                    formdata_input["FormValues"]["id_1638515436377"]["value"] = ["SZ%s" % int(float(time.time())*100000)]

                    formdata_input["FormValues"]["id_1638515694120"]["label"] = [user[n][0]]
                    formdata_input["FormValues"]["id_1638515694120"]["value"] = [user[n][1]]
                    data = {
                        "approvalFatherId": "",
                        "currentVersionId": currentVersionId,
                        "formData": formdata_input,
                        "id": "",
                        "projApprovalType": "generalProject",
                        "submmitTag": 2
                    }
                    response = requests.post(url=xboat_url, headers=xboat_head, data=json.dumps(data), verify=False)
                    print(response.json())
                    time.sleep(10)
            except KeyError:
                formdata_input["FormValues"]["id_1638515436382"]["label"] = [item_province["label"], item_city["label"]]
                formdata_input["FormValues"]["id_1638515436382"]["value"] = [item_province["value"], item_city["value"]]
                formdata_input["FormValues"]["id_1638515436376"]["label"] = ["中设数字项目-%s" % item_city["label"]]
                formdata_input["FormValues"]["id_1638515436376"]["value"] = ["中设数字项目-%s" % item_city["label"]]

                formdata_input["FormValues"]["id_1638515436377"]["label"] = ["SZ%s" % int(float(time.time())*100000)]
                formdata_input["FormValues"]["id_1638515436377"]["value"] = ["SZ%s" % int(float(time.time())*100000)]

                formdata_input["FormValues"]["id_1638515694120"]["label"] = user[m][0]
                formdata_input["FormValues"]["id_1638515694120"]["value"] = user[m][1]
                data = {
                    "approvalFatherId": "",
                    "currentVersionId": currentVersionId,
                    "formData": formdata_input,
                    "id": "",
                    "projApprovalType": "generalProject",
                    "submmitTag": 2
                }
                response = requests.post(url=xboat_url, headers=xboat_head, data=json.dumps(data), verify=False)
                print(response.json())
                time.sleep(10)
        else:
            break




