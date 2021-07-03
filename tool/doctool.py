"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     doctool.py
@Author:   shenfan
@Time:     2021/4/8 19:08
"""
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import hashlib
import json
import time
import pymysql
from requests_toolbelt import MultipartEncoder

appKey = "b774cfe9fc8776b961a650df3efb2b8d"
appId = "7bf66c041b2b28c734c3e5b7534cbb9c"
conn = pymysql.connect(host="172.16.201.74", port=3306, user="root", passwd="dbpass")

# 查询当前15条协同项目
cmd = """SELECT
	project.id,
	project.work_id,
	project.`name`,
	project.task_form_name,
	project.project_manager_name,
	sub_project.id AS "sub_project_id",
	sub_project.`name` AS "sub_project_name"
FROM
	cbim_design.project
LEFT JOIN cbim_design.sub_project ON sub_project.project_id = project.id
WHERE
	project.type = 0
AND project.state = 1
AND project.name = '{0}'
"""
# 查询当前项目的设计说明文档
cmd_doc = """SELECT
	doc.version,
	major.`name`,
	template.`name`
FROM
	cbim_design.doc
LEFT JOIN cbim_design.template ON template.id = doc.template_id
LEFT JOIN cbim_design.major ON major.id = doc.major_id
WHERE
	doc.sub_project_id = {0}
	and 
	doc.latest=1"""


class Postman:
    def __init__(self):
        self.env = "https://cbim-api.cbim.org.cn"
        self.username = "pm1@cadg.cn"
        self.password = "a123456"
        self.entcode = "cadgbim"
        self.url = self.env + "/external/api/user/request_ticket"
        self.uri = "/external/api/user/request_ticket"
        self.ts = str(int(time.time() * 1000))
        self.sign = hashlib.sha1(
            (appKey + "," + self.uri + "," + self.ts).replace("-", "").encode("utf-8")).hexdigest().lower()
        self.headers = {
            "Content-Type": "application/json",
            "appid": appId,
            "sign": self.sign,
            "ts": self.ts
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
        except Exception as e:
            print(e)

    def retoken(self):
        print(self.ticket)
        return self.ticket

    def interface(self, path, method, params=None, data=None, headers=None, path_params=None, files=None):
        cookies = {
            "tool.tk": self.ticket
        }
        url = "https://cbim-api.cbim.org.cn/" + path
        if path_params:
            if isinstance(path_params, dict):
                url = url.format(**path_params)
            elif isinstance(path_params, list):
                url = url.format_map(dict(path_params))
            else:
                raise TypeError
        respose = requests.request(method=method, url=url, headers=headers, params=params, data=data,
                                   files=files, cookies=cookies, verify=False)
        print(respose.json())
        return respose


def projects():
    name = input("请输入项目名：")
    addinfo = []
    cur = conn.cursor()
    cur.execute(cmd.format(name))
    result = cur.fetchall()
    if not result:
        print("无此项目，请重新输入项目名")
        return None
    print(result)
    for item in result:
        if item[5]:
            cur.execute(cmd_doc.format(item[5]))
            temp_result = cur.fetchall()
            if temp_result:
                print("项目：", item[2])
                print("项目经理：", item[4])
                print("子项：", item[6])
                print("设计说明文档：")
                print(temp_result)
                addinfo.append((item[0], item[5], item[2]))
            else:
                addinfo.append((item[0], item[5], item[2]))
        else:
            print("项目子项数据异常")
            return None
    return addinfo


def doc():
    docinfo = projects()
    if docinfo:
        print(docinfo)
        path = "/doctool/v1/projects/{projectid}/subs/{subprojectid}/docs"
        method = "post"
        headers = {"env": "cprod", "Content-Type": "application/json;charset=UTF-8"}
        path_params = {"projectid": docinfo[0][0], "subprojectid": docinfo[0][1]}
        # 建筑  建筑-住宅模板
        data = {"entId": "", "majorId": 1, "projectId": docinfo[0][0], "projectName": docinfo[0][2], "source": 0,
                "subProjectId": docinfo[0][1], "version": "V1.0", "templateId": 483}
        resultcode = Postman().interface(path, method, path_params=path_params, headers=headers, data=json.dumps(data))
        print("已添加 建筑  建筑-住宅模板")
        # 添加 制定建筑专业的统一技术措施及BIM实施导则节点
        if resultcode.json()["code"] == 0:
            path_inode = "/doctool/v2/projects/{projectid}/majors/1"
            method_inode = "get"
            params_inode = {"majorId": 1, "projectId": docinfo[0][0], "subProjectId": docinfo[0][1]}
            result_inode = Postman().interface(path_inode, method_inode, params=params_inode, headers=headers).json()
            inodes = result_inode.json()["result"]
            if inodes:
                for inode in inodes:
                    if inode["name"] == "制定建筑专业的统一技术措施及BIM实施导则": pass
        # 结构 结构-钢筋混凝土结构
        data = {"entId": "", "majorId": 2, "projectId": docinfo[0][0], "projectName": docinfo[0][2], "source": 0,
                "subProjectId": docinfo[0][1], "version": "V1.0", "templateId": 461}
        Postman().interface(path, method, path_params=path_params, headers=headers, data=json.dumps(data))
        print("已添加 结构-钢筋混凝土结构")
        # 给排水 给排水-公建模板
        data = {"entId": "", "majorId": 3, "projectId": docinfo[0][0], "projectName": docinfo[0][2], "source": 0,
                "subProjectId": docinfo[0][1], "version": "V1.0", "templateId": 456}
        Postman().interface(path, method, path_params=path_params, headers=headers, data=json.dumps(data))
        print("已添加 给排水 给排水-公建模板")
        # 暖通 暖通-公建模板
        data = {"entId": "", "majorId": 4, "projectId": docinfo[0][0], "projectName": docinfo[0][2], "source": 0,
                "subProjectId": docinfo[0][1], "version": "V1.0", "templateId": 458}
        Postman().interface(path, method, path_params=path_params, headers=headers, data=json.dumps(data))
        print("已添加 暖通 暖通-公建模板")
        # 电气 电气-公建模板
        data = {"entId": "", "majorId": 5, "projectId": docinfo[0][0], "projectName": docinfo[0][2], "source": 0,
                "subProjectId": docinfo[0][1], "version": "V1.0", "templateId": 20005}
        Postman().interface(path, method, path_params=path_params, headers=headers, data=json.dumps(data))
        print("已添加 电气 电气-公建模板")
        # 添加 项目做法包：建筑-公租房
        path = "/material/v1/packages"
        method = "get"
        params = {"projectId": docinfo[0][0], "subProjectId": docinfo[0][1]}
        resultpackages = Postman().interface(path, method, params=params, headers=headers)
        if resultpackages.json()["code"] == 0:
            packageid = resultpackages.json()["result"][0]["id"]
        else:
            print("接口异常，请检查环境")
            return None
        path = "/material/v1/packages/%s/templates" % packageid
        method = "put"
        params = {"newTemplateId": "12040351"}
        data = {"newTemplateId": "12040351", "packageId": packageid}
        publishedpackages = Postman().interface(path, method, params=params, data=json.dumps(data), headers=headers)
        # path = "/material/v1/packages/%s"%publishedpackages.json()["result"]
        # method = "put"
        #

        # 添加 房间
        path = "/material/v1/rooms"
        method = "post"
        params = {"projectId": docinfo[0][0], "subProjectId": docinfo[0][1], "type": 1}
        data = [{"standardRoomId": 1, "source": 1}, {"standardRoomId": 2, "source": 1},
                {"standardRoomId": 3, "source": 1}, {"standardRoomId": 4, "source": 1},
                {"standardRoomId": 5, "source": 1}, {"standardRoomId": 6, "source": 1},
                {"standardRoomId": 7, "source": 1}, {"standardRoomId": 8, "source": 1},
                {"standardRoomId": 9, "source": 1}, {"standardRoomId": 10, "source": 1}]
        Postman().interface(path, method, params=params, data=json.dumps(data), headers=headers)

        # 文件拆分
        filepath = input("请输入文件：")
        path = "/utmt/cad/upload"
        method = "post"
        data = {"version": "V1.0", "latest": 1, "projectId": docinfo[0][0], "subProjectId": docinfo[0][1], "type": 2,
                "majorId": 1}
        file = {
            "file": open(filepath, "rb")
        }
        Postman().interface(path, method, data=data, files=file, headers=headers)
    else:
        return None


def test():
    headers = {"env": "cprod"}
    filepath = input("请输入文件：")
    path = "/utmt/cad/upload"
    method = "post"
    data = MultipartEncoder(
        {"version": "V1.0", "latest": "1", "projectId": "1436", "subProjectId": "2333", "type": "2", "majorId": "1",
         "file": open(filepath, "rb")})
    r = Postman().interface(path, method, data=data, headers=headers)

def testusers():
    path = "/external/api/user/queryUsers"
    method = "post"




while True:
    # doc()
    test()
