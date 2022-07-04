"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     create_doc_statics.py
@Author:   shenfan
@Time:     2022/5/20 9:43
"""
import pymysql
import pandas
import os

BASE_DIR = os.path.join(os.path.abspath("."), "output")

ent_info = """
SELECT DISTINCT(cbim_enterprise.account_id),cbim_enterprise.creation_time,cbim_enterprise.name FROM bms_bms.cbim_enterprise
LEFT JOIN bms_bms.cbim_ent_user ON cbim_ent_user.ent_id = cbim_enterprise.id 
WHERE cbim_enterprise.prescription_type = 1 AND cbim_enterprise.creation_time > '2022-04-25'
"""

conn = pymysql.connect(host="172.16.211.251", port=3366, user="cbim", passwd="ChRd5@Hdhxt")
cour = conn.cursor()
cour.execute(ent_info)
result = cour.fetchall()
stactis = []
for item in result:
    temp_statics = {}
    temp = {}
    temp["企业"] = item[2]
    temp["企业创建开始时间"] = item[1]
    cmd = """SELECT max(dms_bucket.creation_time) as "空间创建时间" FROM dms_dms.dms_bucket 
WHERE dms_bucket.account_id = {0} and dms_bucket.creation_time <= '{1}' and dms_bucket.app_code = 'doc'""".format(
        item[0],
        str(item[1])[0:10] + " 23:59:59")
    if cour.execute(cmd): temp["空间创建时间"] = cour.fetchall()[0][0]
    #     cmd = """
    #     SELECT max(dms_folder.creation_time) AS "文件夹创建时间" FROM dms_dms.dms_folder
    # LEFT JOIN dms_dms.dms_bucket ON dms_bucket.id = dms_folder.bucket_id
    # WHERE dms_bucket.account_id = {0} and dms_folder.creation_time <= '{1}'""".format(item[0],
    #                                                                                   str(item[1])[0:10] + " 23:59:59")
    #     cour.execute(cmd)
    #     r = cour.fetchall()
    #     temp["文件夹创建时间"] = r[0][0]
    #
    #     cmd = """
    #     SELECT max(dms_folder_tag.creation_time) AS "文件夹标签创建时间" FROM dms_dms.dms_folder
    # LEFT JOIN dms_dms.dms_bucket ON dms_bucket.id = dms_folder.bucket_id
    # RIGHT JOIN dms_dms.dms_folder_tag ON dms_folder_tag.folder_id = dms_folder.id
    # WHERE dms_bucket.account_id = {0} and dms_folder.creation_time <= '{1}'""".format(item[0],
    #                                                                                   str(item[1])[0:10] + " 23:59:59")
    #     cour.execute(cmd)
    #     r = cour.fetchall()
    #     temp["文件夹标签创建时间"] = r[0][0]
    #
    #     cmd = """
    #     SELECT max(dms_object.creation_time) AS "文件创建时间" FROM dms_dms.dms_object
    # LEFT JOIN dms_dms.dms_bucket ON dms_bucket.id = dms_object.bucket_id
    # WHERE dms_bucket.account_id = {0} and dms_object.creation_time <= '{1}'""".format(item[0],
    #                                                                                   str(item[1])[0:10] + " 23:59:59")
    #     cour.execute(cmd)
    #     r = cour.fetchall()
    #     temp["文件创建时间"] = r[0][0]
    #
    #     cmd = """
    #     SELECT max(dms_object_version.creation_time) AS "文件版本创建时间" FROM dms_dms.dms_object
    # LEFT JOIN dms_dms.dms_bucket ON dms_bucket.id = dms_object.bucket_id
    # RIGHT JOIN  dms_dms.dms_object_version ON dms_object_version.object_id = dms_object.id
    # WHERE dms_bucket.account_id = {0} and dms_object_version.creation_time <= '{1}'""".format(item[0],
    #                                                                                   str(item[1])[0:10] + " 23:59:59")
    #     cour.execute(cmd)
    #     r = cour.fetchall()
    #     temp["文件版本创建时间"] = r[0][0]

    cmd = """
    SELECT max(dms_object_tag.creation_time) AS "文件标签创建时间" FROM dms_dms.dms_object_tag
left JOIN dms_dms.dms_object ON dms_object_tag.object_id = dms_object.id
LEFT JOIN dms_dms.dms_bucket ON dms_bucket.id = dms_object.bucket_id
WHERE dms_bucket.account_id = {0} and dms_object_tag.creation_time <= '{1}'""".format(item[0],
                                                                                      str(item[1])[0:10] + " 23:59:59")
    cour.execute(cmd)
    r = cour.fetchall()
    temp["文件标签创建时间"] = r[0][0]

    if None not in temp.values():
        print(temp)
        temp_statics["企业"] = temp["企业"]
        temp_statics["项目同步时间"] = (temp["空间创建时间"] - temp["企业创建开始时间"]).total_seconds()
        temp_statics["文档同步时间"] = (temp["文件标签创建时间"] - temp["空间创建时间"]).total_seconds()
        print(temp_statics)
        print("*" * 50)
        stactis.append(temp_statics)

dataframe = pandas.DataFrame(stactis)
dataframe.to_excel(os.path.join(BASE_DIR, "文档同步完成时间.xls"), index=False)
