"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     R2C_Statics.py
@Author:   shenfan
@Time:     2022/5/7 10:37
"""
from sshtunnel import SSHTunnelForwarder
import pymysql
import pandas
import os
from bokeh.plotting import figure
from bokeh.io import show, save

BASE_DIR = os.path.join(os.path.abspath("."), "output")


def get_ssh_tunnel(ssh_uesrname, ssh_password, ssh_host, ssh_remote_host):
    server = SSHTunnelForwarder(
        ssh_address_or_host=(ssh_host, 22),
        ssh_username=ssh_uesrname,
        ssh_password=ssh_password,
        remote_bind_address=(ssh_remote_host, 3306),
        local_bind_address=('0.0.0.0', 3306)
    )
    server.start()

    return server


def get_db_cour(mysql, ssh_server=None):
    if ssh_server:
        dpip = ssh_server.local_bind_host
        dbport = ssh_server.local_bind_port
        db = pymysql.connect(
            host=dpip,
            port=dbport,
            user=mysql["user"],
            passwd=mysql["passwd"]
        )
    else:
        db = pymysql.connect(
            host=mysql["host"],
            port=mysql["port"],
            user=mysql["user"],
            passwd=mysql["passwd"]
        )

    return db.cursor()


# dms上传&解压时间
cmd_dms_sql = """
SELECT n.*,dms_object.creation_time AS upload_complete_time FROM dms_dms.dms_object
RIGHT JOIN
(SELECT m.id,m.`name`,m.size,MAX(dms_object.creation_time) AS unzip_complete_time FROM dms_dms.dms_object
RIGHT JOIN (SELECT dms_object.id,dms_object.`name`,dms_object.size,dms_unzip.unzip_folder_id FROM dms_dms.dms_object 
LEFT JOIN dms_dms.dms_object_version ON dms_object_version.object_id = dms_object.id
LEFT JOIN dms_dms.dms_unzip ON dms_unzip.zip_file_id = dms_object.id
WHERE dms_object.extention in ("cim","njm") AND dms_object_version.version = 1 AND dms_unzip.unzip_folder_id IS NOT NULL) m
ON m.unzip_folder_id = dms_object.folder_id
GROUP BY m.id) n
ON n.id = dms_object.id
"""

# 图形转化开始-完成时间
cmd_r2c_sql = """
SELECT rvt2cim_task.relation_id,rvt2cim_task.dms_id,rvt2cim_task.create_date AS start_translate_time,rvt2cim_task.update_date AS complete_translate_time,rvt2cim_task.`status` FROM rendering.rvt2cim_task 
"""

# dms rvt上传&转化&解压时间
cmd_dms_r2c_sql = """
SELECT MAX(dms_object.creation_time) AS unzip_complete_time FROM dms_dms.dms_object
RIGHT JOIN (SELECT dms_object.id,dms_object.`name`,dms_unzip.unzip_folder_id FROM dms_dms.dms_object 
LEFT JOIN dms_dms.dms_object_version ON dms_object_version.object_id = dms_object.id
LEFT JOIN dms_dms.dms_unzip ON dms_unzip.zip_file_id = dms_object.id
WHERE dms_object.id ={0} AND dms_object_version.version = 1 AND dms_unzip.unzip_folder_id IS NOT NULL) m
ON m.unzip_folder_id = dms_object.folder_id
GROUP BY m.id
"""
# dms rvt模型信息
cmd_dms_rvt_sql = """
SELECT dms_object.`name`,dms_object.size,dms_object.creation_time AS upload_complete_time FROM dms_dms.dms_object
where  dms_object.id = {0}
"""

# dms数据库连接
mysql_dms = {"host": "172.16.211.251", "port": 3366, "user": "cbim", "passwd": "ChRd5@Hdhxt"}
mysql_r2c = {"host": "172.16.211.56", "port": 3306, "user": "root", "passwd": "mysql"}

# dms CIM、NJM、RVT、IFX、FBX
cmd_dms_model_sql = """
SELECT COUNT(size),size FROM dms_dms.dms_object WHERE extention in ("cim","njm","rvt","ifx","fbx") GROUP BY size
"""


def model_translate():
    cour_dms = get_db_cour(mysql_dms)
    cour_dms.execute(cmd_dms_sql)
    result = cour_dms.fetchall()
    static_info = []
    for item in result:
        temp = {}
        temp["模型"] = item[1]
        temp["大小（M）"] = round(item[2] / (1024 * 1024), 2)
        try:
            temp["解压时间(s)"] = (item[3] - item[4]).total_seconds()
        except TypeError:
            break
        static_info.append(temp)
    dataframe = pandas.DataFrame(static_info)
    file_output = os.path.join(BASE_DIR, "CIM&NJM解压时间统计.xls")
    dataframe.to_excel(file_output, index=False)


def r2c_translate():
    cour_dms = get_db_cour(mysql_r2c)
    cour_dms.execute(cmd_r2c_sql)
    result = cour_dms.fetchall()
    cour_dms = get_db_cour(mysql_dms)
    result_r2c_statics = []
    for item in result:
        cour_dms.execute(cmd_dms_r2c_sql.format(item[1]))
        result_unzip = cour_dms.fetchall()
        cour_dms.execute(cmd_dms_rvt_sql.format(item[0][:-2]))
        result_rvt = cour_dms.fetchall()
        if result_unzip and result_rvt:
            temp = {}
            temp["模型"] = result_rvt[0][0]
            temp["大小（M）"] = round(result_rvt[0][1] / (1024 * 1024), 2)
            temp["转换状态"] = item[4]
            try:
                temp["转化&解压时间(s)"] = (result_unzip[0][0] - result_rvt[0][2]).total_seconds()
                result_r2c_statics.append(temp)
            except TypeError:
                break
    dataframe = pandas.DataFrame(result_r2c_statics)
    file_output = os.path.join(BASE_DIR, "RVT转化&解压时间统计.xls")
    dataframe.to_excel(file_output, index=False)


def model_statics():
    cour_model = get_db_cour(mysql_dms)
    cour_model.execute(cmd_dms_model_sql)
    result = dict(cour_model.fetchall())
    statics = []
    x = []
    y = []
    p = figure(plot_width=1800, plot_height=900, title="模型大小分布图")
    p.xaxis.axis_label = '模型大小'
    p.yaxis.axis_label = '频次'
    for key, value in result.items():
        temp = {}
        x.append(round(value / (1024 * 1024), 2))
        y.append(key)
        temp["模型大小/M"] = round(value / (1024 * 1024), 4)
        temp["频次"] = key
        statics.append(temp)
    p.vbar(x=x, width=1, bottom=0, top=y, line_width=1, line_alpha=0.8)
    show(p)
    dataframe = pandas.DataFrame(statics)
    file_output = os.path.join(BASE_DIR, "模型统计.xls")
    dataframe.to_excel(file_output, index=False)




# model_translate()
r2c_translate()
# model_statics()
