"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     DiskSpace.py
@Author:   shenfan
@Time:     2022/4/27 15:36
"""
import pymysql

connpool = {
    "platform_test": pymysql.connect(host="10.80.252.199", port=3366, user="root", passwd="Cbim2021-"),
    "platform_stg": pymysql.connect(host="172.16.201.252", port=3366, user="cbim", passwd="ChRd5@Hdhxt"),
    "platform_prod": pymysql.connect(host="172.16.211.251", port=3366, user="cbim", passwd="ChRd5@Hdhxt"),
    "project_test": pymysql.connect(host="10.81.3.57", port=3306, user="project_approval_manage",
                                    passwd="project_approval_manage"),
    "project_stg": pymysql.connect(host="172.16.201.252", port=3366, user="project_approval_manage",
                                   passwd="project_approval_manage"),
    "annotation": pymysql.connect(host="10.81.3.51", port=3306, user="cbim_annotation",
                                  passwd="cbim_annotation@Cbim123"),
    "project_prod": pymysql.connect(host="172.16.211.252", port=3366, user="project_approval_manage",
                                    passwd="project_approval_manage")
}


def space(account_id, *env):
    dms_sql = """
SELECT l.accountid AS accountid,l.ent_name,l.bucketid,l.tag_value,l.app_code,SUM(l.size) FROM (
SELECT n.accountid,n.ent_name,n.bucketid,n.app_code,n.pathname,n.size,n.version,m.tag_value FROM
(SELECT dms_object.id,cbim_enterprise.account_id AS accountid,cbim_enterprise.`name` AS ent_name,dms_bucket.id AS bucketid,dms_bucket.app_code,dms_object.pathname,dms_object.size,dms_object_version.version,dms_object_tag.tag_value FROM dms_dms.dms_object
LEFT JOIN dms_dms.dms_bucket ON dms_bucket.id = dms_object.bucket_id
LEFT JOIN bms_bms.cbim_enterprise ON cbim_enterprise.account_id = dms_bucket.account_id
LEFT JOIN dms_dms.dms_object_version ON dms_object_version.object_id = dms_object.id
LEFT JOIN dms_dms.dms_object_tag ON dms_object_tag.object_id = dms_object.id
WHERE dms_object_tag.tag_key = "projectId") m
RIGHT JOIN
(SELECT dms_object.id,cbim_enterprise.account_id AS accountid,cbim_enterprise.`name` AS ent_name,dms_bucket.id AS bucketid,dms_bucket.app_code,dms_object.pathname,dms_object.size,dms_object_version.version,NULL AS tag_value FROM dms_dms.dms_object
LEFT JOIN dms_dms.dms_bucket ON dms_bucket.id = dms_object.bucket_id
LEFT JOIN bms_bms.cbim_enterprise ON cbim_enterprise.account_id = dms_bucket.account_id
LEFT JOIN dms_dms.dms_object_version ON dms_object_version.object_id = dms_object.id) n
ON n.id = m.id
WHERE n.accountid = {0}) l
GROUP BY l.accountid,l.ent_name,l.bucketid,l.tag_value
"""

    pro_sql = """SELECT master_id,proj_name FROM project_approval_manage.pro_approval WHERE pro_approval.account_id = {0} and pro_approval.delete_type = 0"""
    cur = connpool[env[0]].cursor()
    cur.execute(dms_sql.format(account_id))
    file_size = cur.fetchall()
    cur = connpool[env[1]].cursor()
    cur.execute(pro_sql.format(account_id))
    pro_info = dict(cur.fetchall())
    tatol_size = 0
    for item in file_size:
        tatol_size += item[5]
        try:
            print(" 企业：\033[1;33m%s\033[0m" % item[1], "空间：\033[1;33m%s\033[0m" % item[4],
                  "项目：\033[1;33m%s\033[0m" % pro_info[int(item[3])],
                  "占用大小：\033[1;33m%.2f M(%d B)\033[0m" % (item[5] / (1024 * 1024), item[5]))
        except Exception as e:
            print(" 企业：\033[1;33m%s\033[0m" % item[1], "空间：\033[1;33m%s\033[0m" % item[4], "项目：\033[1;33m非项目空间\033[0m",
                  "占用大小：\033[1;33m%.2f M(%d B)\033[0m" % (item[5] / (1024 * 1024), item[5]))
    print(" \033[1;34m总占用大小为：%.2f M(%d B)\033[0m" % (tatol_size / (1024 * 1024), tatol_size))


space("845347552281890817", "platform_stg", "project_stg")
# space("826188538830786561", "platform_prod", "project_prod")
# space("815275008518656001", "platform_stg", "project_stg")
