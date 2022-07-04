"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     Initialize.py
@Author:   shenfan
@Time:     2022/6/15 18:20
"""
import re
import json
import requests
import random
import string
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 获取session key
def get_cbim_session_key(host: str, username: str, passwd: str):
    url = f'{host}/cas/login?service={host}/app'
    r = requests.get(url)
    # 加密字符串
    execution = re.search('name="execution" value="(.*?)"', r.text, re.S).groups(1)[0]
    # cookie
    session_temp = r.headers['Set-Cookie']
    session_temp = re.search('SESSION=(.*?);', session_temp, re.S).groups(1)[0]
    r = requests.request(
        'post',
        url,
        headers={
            'cookie': f'SESSION={session_temp}',
        },
        data={
            'username': username,
            'password': passwd,
            'verifyCode': None,
            'execution': execution,
            '_eventId': 'submit',
            'loginMode': '2'
        },
        allow_redirects=False
    )
    # 重定向地址
    location = r.headers['Location']
    r = requests.get(location, allow_redirects=False)
    session = re.search('CBIM-SESSION=(.*?);', r.headers['Set-Cookie'], re.S).groups(1)[0]
    return session


def creat_enterprise(host: str, mobile: str, username: str, passwd: str, entname=None):
    user_url = "{0}/api/bms/v1/user".format(host)
    user_header = {
        "Authorization": "XXXX",
        "Content-Type": "application/json",
    }
    user_body = {
        "mobile": mobile,
        "username": username,
        "email": "%s@cad.com.cn" % mobile,
        "password": passwd,
        "trueName": username,
        "sex": 0,
    }
    response = requests.request(method="post", url=user_url, headers=user_header, data=json.dumps(user_body),
                                verify=False)
    print(response.json())
    userid = response.json()["data"]

    ent_url = "{0}/cas/v1/enterprise/create".format(host)
    ent_body = {
        "code": "".join(random.choice(string.ascii_letters + string.digits) for _ in range(4)),
        # "name": "初始化企业-" + "".join(random.choice(string.ascii_letters + string.digits) for _ in range(4)),
        "name": entname if entname else "初始化企业-" + "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(4)),
        "parentId": 0,
        "platform": 0,
        "prescriptionType": 1,
        "prescriptionTime": "2023-07-30 00:00:00.000 +0800",
        "userId": userid
    }
    # print(ent_body)
    response = requests.request(method="post", url=ent_url, headers=user_header, data=json.dumps(ent_body),
                                verify=False)
    # print(response.json())
    entid = str(eval(response.json()["data"]["message"])["data"])
    accountid = str(int(entid) + 1)
    header = {"entid": entid, "accountid": accountid, "Cbim-AccountId": accountid, "content-type": "application/json"}
    # print(header)
    return header


def query_project_doc(host: dict, header: dict, session: str):
    pro_url = "{project}/cbim-project-approval/proApproval/selectPage".format(**host)
    pro_header = header
    pro_header["session"] = session
    pro_body = {"pageNo": 1, "pageSize": 20, "collection": None, "proName": "", "accessType": "1"}
    pro_start_time = time.time()

    doc_url = "{doc}/app/doc/api/folder/querySpaceFolder?space=SHARE&section=PROJECT".format(**host)
    doc_header = header
    doc_header["cookie"] = "CBIM-SESSION=%s" % session
    doc_body = {"pageRequest": {"pageNo": 1, "pageSize": 10}, "sort": {"sortBy": "createTime", "sortOrder": "desc"},
                "spaceQuery": {"folder": "/team", "bucketId": ""}}
    pro_count = 0
    doc_count = 0
    while True:
        response_pro = requests.request(method="post", url=pro_url, headers=pro_header, data=json.dumps(pro_body),
                                        verify=False)

        pros_num = response_pro.json()["data"]["total"]
        pros_elapse = response_pro.elapsed.total_seconds()

        if pros_num in [1, 2, 3] and doc_count == 0:
            doc_start_time = time.time()
            doc_count = 1

        if pros_num == 3 and pro_count == 0:
            pro_end_time = time.time()
            pro_initialize_time = pro_end_time - pro_start_time
            print("\033[1;33m项目初始化完成时间：%s\033[0m" % pro_initialize_time)
            pro_count = 1

        response_doc = requests.request(method="post", url=doc_url, headers=doc_header, data=json.dumps(doc_body),
                                        verify=False)
        doc_elapse = response_doc.elapsed.total_seconds()
        doc_num = response_doc.json()["data"]["total"]

        if doc_num == 3 and pros_num == 3:
            doc_end_time = time.time()
            doc_initialize_time = doc_end_time - doc_start_time
            print("\033[1;33m文档初始化完成时间：%s\033[0m" % doc_initialize_time)
            print("\033[1;33m文档初始化校准完成时间：%s\033[0m" % (doc_end_time-pro_end_time))
            break


if __name__ == '__main__':
    mobile = "19122341276"
    username = "江国华"
    passwd = "s123456"
    entname = "中北重工"
    host = {"project": "https://staging-gw.cbim.org.cn", "doc": "https://staging.cbim.org.cn",
            "host": "https://staging.cbim.org.cn"}

    header = creat_enterprise(host["host"], mobile, username, passwd, entname=entname)
    session = get_cbim_session_key(host["host"], mobile, passwd)
    query_project_doc(host, header, session)
