"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     home_statics.py
@Author:   shenfan
@Time:     2022/3/22 11:44
"""
import requests
import pymysql
import pandas

connpool = {
    "platform_test": pymysql.connect(host="10.80.252.199",port=3366,user="root",passwd="Cbim2021-"),
    "platform_stg": pymysql.connect(host="172.16.201.252",port=3366,user="cbim",passwd="ChRd5@Hdhxt"),
    "project": pymysql.connect(host="10.81.3.57",port=3306,user="project_approval_manage",passwd="project_approval_manage"),
    "annotation": pymysql.connect(host="10.81.3.51",port=3306,user="cbim_annotation",passwd="cbim_annotation@Cbim123")
}

#企业信息
ent_sql = """SELECT `name`,account_id FROM bms_bms.cbim_enterprise WHERE cbim_enterprise.`name` = '{0}'"""

#文档
file_pro_sql = """SELECT DISTINCT file.id,file.`name` AS file_name,file.extention,file.pathname,tag.tag_key AS tag_key,tag.tag_value FROM dms_dms.dms_object file LEFT JOIN dms_dms.dms_bucket bucket ON bucket.id = file.bucket_id LEFT JOIN dms_dms.dms_object_tag tag ON tag.object_id = file.id WHERE bucket.account_id = {0} AND tag.tag_key = 'projectId' AND bucket.app_code in ('comm','doc','task')"""

file_sql = """SELECT DISTINCT file.id,file.`name` AS file_name,file.extention,file.pathname,NULL AS tag_key,null AS tag_value FROM dms_dms.dms_object file LEFT JOIN dms_dms.dms_bucket bucket ON bucket.id = file.bucket_id WHERE bucket.account_id = {} AND bucket.app_code in ("comm","doc","task")"""


#项目
pro_sql = """SELECT proj_name,master_id FROM project_approval_manage.pro_approval WHERE pro_approval.account_id = {0} and pro_approval.delete_type = 0"""

#批注
model_sql = """SELECT id FROM cbim_annotation.drwg_model WHERE relation_id LIKE '%{}%'"""
dwg_sql = """SELECT id FROM cbim_annotation.drwg_file WHERE relation_id LIKE '%{}%'"""
anno_sql = """SELECT anno_info.id,drwg_model.relation_id AS modelid,drwg_file.relation_id AS fileid,anno_info.`status`,anno_info.assign,anno_info.assign_overdue,anno_info.destroy 
FROM cbim_annotation.anno_info
LEFT JOIN cbim_annotation.drwg_model ON drwg_model.id = anno_info.relation_id
LEFT JOIN cbim_annotation.drwg_file ON drwg_file.id = anno_info.relation_id 
WHERE anno_info.relation_id in {}"""


def file_statics(entname):
    cur = connpool["platform_test"].cursor()
    cur.execute(ent_sql.format(entname))
    entprise = dict(cur.fetchall())
    print(entprise)
    # 查询企业下文档
    cur = connpool["project"].cursor()
    cur.execute(pro_sql.format(entprise[entname]))
    print(dict(cur.fetchall()))


file_statics("蔚蓝能源科技")
