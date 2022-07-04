"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     cockpit.py
@Author:   shenfan
@Time:     2022/1/13 17:56
"""
# 首页驾驶舱数据统计

import pymysql
import re
import pandas
import prettytable
import os

connpool = {
    "platform_test": pymysql.connect(host="10.80.252.199", port=3366, user="root", passwd="Cbim2021-"),
    "platform_stg": pymysql.connect(host="172.16.201.252", port=3366, user="cbim", passwd="ChRd5@Hdhxt"),
    "platform_prod": pymysql.connect(host="172.16.211.251", port=3366, user="cbim", passwd="ChRd5@Hdhxt"),
    "project": pymysql.connect(host="10.81.3.57", port=3306, user="project_approval_manage",
                               passwd="project_approval_manage"),
    "project_stg": pymysql.connect(host="172.16.201.252", port=3366, user="project_approval_manage",
                                   passwd="project_approval_manage"),
    "annotation": pymysql.connect(host="10.81.3.51", port=3306, user="cbim_annotation",
                                  passwd="cbim_annotation@Cbim123"),
    "r2c": pymysql.connect(host="172.16.211.56", port=3306, user="root", passwd="mysql"),
    "project_prod": pymysql.connect(host="172.16.211.252", port=3366, user="project_approval_manage",
                                    passwd="project_approval_manage")
}

# 企业信息
ent_sql = """SELECT cbim_enterprise.name,cbim_enterprise.account_id FROM bms_bms.cbim_ent_user LEFT JOIN bms_bms.cbim_enterprise ON cbim_enterprise.id = cbim_ent_user.ent_id WHERE cbim_ent_user.mobile = {0}"""

# 文档
file_pro_sql = """
SELECT
m.*,tag.tag_key AS "project",tag.tag_value AS "project_value"
FROM
(SELECT
	file.id,
	file.`name` AS file_name,
	file.extention,
	file.pathname,
	tag.tag_key AS "group",
	tag.tag_value AS "group_value"
FROM
	dms_dms.dms_object file
LEFT JOIN dms_dms.dms_bucket bucket ON bucket.id = file.bucket_id
LEFT JOIN dms_dms.dms_object_tag tag ON tag.object_id = file.id
WHERE
	bucket.account_id = {}
AND bucket.app_code IN ("comm", "doc", "task")
HAVING tag_key = "group") m
LEFT JOIN dms_dms.dms_object_tag tag ON tag.object_id = m.id
WHERE tag_key = "projectId"
"""

file_sql = """
SELECT
	file.id,
	file.`name` AS file_name,
	file.extention,
	file.pathname,
	tag.tag_key AS "group",
	tag.tag_value AS "group_value"
FROM
	dms_dms.dms_object file
LEFT JOIN dms_dms.dms_bucket bucket ON bucket.id = file.bucket_id
LEFT JOIN dms_dms.dms_object_tag tag ON tag.object_id = file.id
WHERE
	bucket.account_id = {}
AND bucket.app_code IN ("comm", "doc", "task")
HAVING tag_key = "group"
"""

# 项目
pro_sql = """SELECT master_id,proj_name FROM project_approval_manage.pro_approval WHERE pro_approval.account_id = {0} and pro_approval.delete_type = 0"""

# 批注
model_sql = """SELECT id FROM cbim_annotation.drwg_model WHERE relation_id LIKE '%{}%'"""
dwg_sql = """SELECT id FROM cbim_annotation.drwg_file WHERE relation_id LIKE '%{}%'"""
anno_sql = """SELECT anno_info.id,drwg_model.relation_id AS modelid,drwg_file.relation_id AS fileid,anno_info.`status`,anno_info.assign,anno_info.assign_overdue,anno_info.destroy 
FROM cbim_annotation.anno_info
LEFT JOIN cbim_annotation.drwg_model ON drwg_model.id = anno_info.relation_id
LEFT JOIN cbim_annotation.drwg_file ON drwg_file.id = anno_info.relation_id 
WHERE anno_info.relation_id in {}"""


def file_statics(mobile):
    cur = connpool["platform_test"].cursor()
    cur.execute(ent_sql.format(mobile))
    ent_info = dict(cur.fetchall())
    file_info = {}
    for item in ent_info:
        cur.execute(file_sql.format(ent_info[item]))
        print(file_sql.format(ent_info[item]))
        file_info[item] = cur.fetchall()
    file_pro_info = {}
    for item in ent_info:
        cur.execute(file_pro_sql.format(ent_info[item]))
        file_pro_info[item] = cur.fetchall()
    cur.close()
    cur = connpool["project_stg"].cursor()
    pro_info = {}
    for item in ent_info:
        cur.execute(pro_sql.format(ent_info[item]))
        pro_info[item] = cur.fetchall()
    cur.close()
    files_statics = {}
    for item in file_info:
        model_count = 0
        dwg_count = 0
        other_count = 0
        for item_next in file_info[item]:
            if len(item_next) > 0:
                if "rvt2cim" not in item_next[3]:
                    if item_next[2] in ["cim", "rvt", "ifc", "fbx"] and item_next[5] == "model": model_count += 1
                    if item_next[2] in ["dxf", "dwg", "pdf"] and item_next[5] == "drawing":
                        dwg_count += 1
                    else:
                        other_count += 1
            else:
                files_statics[item] = {"企业级": {"模型": 0, "图纸": 0, "其他": 0}}
        files_statics[item] = {"企业级": {"模型": model_count, "图纸": dwg_count, "其他": other_count}}
    for item in pro_info:
        for item_pro in pro_info[item]:
            pmodel_count = 0
            pdwg_count = 0
            pother_count = 0
            for item_file in file_pro_info[item]:
                if len(item_file) > 0 and item_file[7] == str(item_pro[0]) and "rvt2cim" not in item_file[3]:
                    if item_file[2] in ["cim", "rvt", "ifc", "fbx"] and item_file[5] == "model": pmodel_count += 1
                    if item_file[2] in ["dxf", "dwg", "pdf"] and item_file[5] == "drawing":
                        pdwg_count += 1
                    else:
                        pother_count += 1
            files_statics[item].update({item_pro[1]: {"模型": pmodel_count, "图纸": pdwg_count, "其他": pother_count}})
    for key, value in files_statics.items():
        print("\033[1;32m %s:\033[0m" % key)
        for ikey, ivalues in value.items():
            print("\033[1;33m    %s:%s\033[0m" % (ikey, ivalues))
    cur = connpool["annotation"].cursor()
    relationid = []
    # print(file_info)
    for item in file_info:
        for item_fileid in file_info[item]:
            if item_fileid[2] in ["cim", "dxf", "dwg"]:
                cur.execute(model_sql.format(item_fileid[0]))
                relationid.append(cur.fetchall())
                cur.execute(dwg_sql.format(item_fileid[0]))
                relationid.append(cur.fetchall())
    pattern = re.compile(r'[1-9]\d*')
    result = pattern.findall(str(relationid))
    relationids = tuple(set(result))
    if relationids:
        cur.execute(anno_sql.format(relationids))
        anno_info = cur.fetchall()
        print(anno_sql.format(relationids))
    # print(anno_info)
    # temp = {}
    # for item in anno_info:
    #     print(item)
    #     if item[3]==0 and item[4]==0 and item[5]==None and item[6]==0:
    #         temp[item[2][:-2]]="未指派（id:%s）"%item[0]
    #     if item[3]==0 and item[4]==1 and item[5]==None and item[6]==0:
    #         temp[item[2][:-2]]="进行中（id:%s）"%item[0]
    #     if item[3]==0 and item[4]==1 and item[5]==1 and item[6]==0:
    #         temp[item[2][:-2]]="已逾期（id:%s）"%item[0]
    #     if item[3]==1 and item[4]==1 and item[5]==0 and item[6]==1:
    #         temp[item[2][:-2]]="已完成（id:%s）"%item[0]
    # print(temp)
    # sql_addfilename = """SELECT dms_object.`name` FROM dms_dms.dms_object WHERE dms_object.id = {0}"""
    # sql_addpro = """SELECT tag_value FROM dms_dms.dms_object_tag WHERE object_id = {0} AND tag_key = 'projectId'"""
    # sql_addproname = """SELECT proj_name FROM project_approval_manage.pro_approval WHERE master_id = {0}"""
    # cur = connpool["platform"].cursor()
    # curp = connpool["project"].cursor()
    # result_temp = []
    # for item in temp:
    #     cur.execute(sql_addfilename.format(item))
    #     r1 = cur.fetchall()[0][0]
    #     cur.execute(sql_addpro.format(item))
    #     r2 = cur.fetchall()[0][0]
    #     curp.execute(sql_addproname.format(r2))
    #     r3 = curp.fetchall()[0][0]
    #     result_temp.append((r3,(r1,temp[item],item)))
    # print(result_temp)


def db_action(db_name, cmd):
    print(cmd)
    cur = connpool[db_name].cursor()
    cur.execute(cmd)
    feilds = [item[0] for item in cur.description]
    table = prettytable.PrettyTable()
    table.field_names = feilds
    temp = cur.fetchall()
    result = pandas.DataFrame(temp, columns=feilds)
    result = result.where(result.notnull(), "-")
    file = r"D:\Doctool\python\工具脚本\XBOAT\脏数据 .xls"
    result.to_excel(file)
    for item in result.values:
        table.add_row(item)
    print(table)
    return result


# file_statics("15000000001")
cmd1 = """
SELECT dms_bucket.* FROM dms_dms.dms_bucket
WHERE id = "744864319870734336"
"""

cmd2 = """
SELECT dms_bucket.* FROM dms_dms.dms_bucket
WHERE id = "749339182727565312"
"""
cmd3 = """
SELECT * FROM dms_dms.dms_file_soft_link
WHERE src_id = "781822389259472896" ;
"""
cmd4 = """
SELECT dms_bucket.id AS bucketid,dms_bucket.app_code,dms_folder.folder_path,dms_folder_tag.tag_key,dms_folder_tag.tag_value,dms_file_soft_link.`name` AS softlinkname,dms_file_soft_link.path AS softlinkpath,dms_file_soft_link.src_path AS softlinksrcpath FROM dms_dms.dms_bucket 
LEFT JOIN dms_dms.dms_folder ON dms_folder.bucket_id = dms_bucket.id
LEFT JOIN dms_dms.dms_folder_tag ON dms_folder_tag.folder_id = dms_folder.id
LEFT JOIN dms_dms.dms_file_soft_link ON dms_file_soft_link.parent_id = dms_folder.id
WHERE dms_bucket.account_id = "744860718335135745" AND dms_bucket.app_code = "comm";
"""
cmd5 = """
SELECT dms_file_soft_link.id,dms_bucket.app_code,dms_file_soft_link.`name` FROM dms_dms.dms_file_soft_link 
LEFT JOIN dms_dms.dms_bucket ON dms_bucket.id = dms_file_soft_link.bucket_id
WHERE dms_bucket.app_code = "doc"
"""
cmd6 = """
SELECT * FROM bms_bms.cbim_enterprise WHERE name = "中设数字产品运营"
"""
cmd66 = """
SELECT
    cbim_account.id,
    ent_user.user_id,
	ent.`name` AS ent_name,
	ent_user.true_name,
	ent_group.`name`,
	ent_group.`code`
  
FROM
	bms_bms.cbim_account
LEFT JOIN bms_bms.cbim_enterprise ent ON ent.account_id = cbim_account.id
LEFT JOIN bms_bms.cbim_ent_user ent_user ON ent_user.ent_id = ent.id
LEFT JOIN bms_bms.cbim_ent_user_group user_group ON user_group.ent_id = ent.id AND user_group.user_id = ent_user.user_id
LEFT JOIN bms_bms.cbim_ent_group ent_group ON ent_group.ent_id = ent.id AND ent_group.id = user_group.group_id
WHERE
	cbim_account.id = "832258896088403969"
"""

cmd7 = """
SELECT dms_bucket.id AS bucketid,dms_bucket.app_code,dms_folder.folder_path,dms_folder.parent_id,dms_folder_tag.tag_key,dms_folder_tag.tag_value as folder_tag,dms_object.name as file_name,dms_object_tag.tag_value as file_tag FROM dms_dms.dms_bucket 
LEFT JOIN dms_dms.dms_folder ON dms_folder.bucket_id = dms_bucket.id
LEFT JOIN dms_dms.dms_folder_tag ON dms_folder_tag.folder_id = dms_folder.id
LEFT JOIN dms_dms.dms_object ON dms_object.folder_id = dms_folder.id
LEFT JOIN dms_dms.dms_object_tag ON dms_object_tag.object_id = dms_object.id
WHERE dms_bucket.account_id = "744860718335135745" AND dms_bucket.app_code = "task" and dms_object_tag.tag_key = "projectId"
"""

cmd8 = """
SELECT * FROM (SELECT dms_bucket.id,dms_bucket.app_code,dms_bucket.account_id,dms_object.id AS objectid,dms_object.`name`,dms_object_tag.tag_value AS object_tag ,dms_folder.id AS filderid,dms_folder.folder_path,dms_folder_tag.tag_value AS folder_tag FROM dms_dms.dms_object 
LEFT JOIN dms_dms.dms_object_tag ON dms_object_tag.object_id = dms_object.id
LEFT JOIN dms_dms.dms_folder ON dms_folder.id = dms_object.folder_id
LEFT JOIN dms_dms.dms_folder_tag ON dms_folder_tag.folder_id = dms_object.folder_id
LEFT JOIN dms_dms.dms_bucket ON dms_bucket.id = dms_object.bucket_id
WHERE dms_object_tag.tag_key = "projectId" AND dms_folder_tag.tag_key = "projectId") temp
WHERE temp.folder_tag = "" or temp.folder_tag = "" or temp.folder_tag <> temp.object_tag

"""

cmd9 = """
SELECT dms_object.`name`,dms_object.pathname,dms_object_version.version,dms_unzip.state FROM dms_dms.dms_object
LEFT JOIN dms_dms.dms_object_version ON dms_object_version.object_id = dms_object.id
LEFT JOIN dms_dms.dms_unzip ON dms_unzip.zip_file_id = dms_object.id AND dms_unzip.zip_file_version = dms_object_version.version
where dms_object.id = "817785320975241216"
"""

cmd10 = """SELECT dms_object.pathname,dms_object.`name` FROM dms_dms.dms_object WHERE dms_object.pathname LIKE '%817785320975241216%' """

cmd11 = """SELECT count(id)  FROM dms_dms.dms_object WHERE dms_object.pathname LIKE '%817785320975241216%' """

cmd12 = """
SELECT cbim_user.id AS userid,cbim_user.true_name,cbim_user.mobile,cbim_ent_user.is_admin,cbim_enterprise.id AS entid,cbim_enterprise.`name` FROM bms_bms.cbim_user
LEFT JOIN bms_bms.cbim_ent_user ON cbim_ent_user.user_id = cbim_user.id
LEFT JOIN bms_bms.cbim_enterprise ON cbim_enterprise.id = cbim_ent_user.ent_id
WHERE cbim_user.mobile LIKE "%14000%"
ORDER BY cbim_user.id
"""

cmd13 = """
select * from dms_dms.dms_object where id = "825672030589423617";
"""
cmd14 = """
SELECT m.*,dms_object.pathname AS unzip_pathname,dms_object.`name` AS unzip_name FROM 
(SELECT dms_object.id,dms_object.`name`,dms_object.pathname,dms_object_version.version,dms_unzip.state,dms_unzip.unzip_folder_id FROM dms_dms.dms_object
LEFT JOIN dms_dms.dms_object_version ON dms_object_version.object_id = dms_object.id
LEFT JOIN dms_dms.dms_unzip ON dms_unzip.zip_file_id = dms_object.id AND dms_unzip.zip_file_version = dms_object_version.version
where dms_object.id = "825672030471983104") m 
LEFT JOIN dms_dms.dms_object ON dms_object.folder_id = m.unzip_folder_id;
"""

cmd16 = """
SELECT m.*,dms_object.pathname AS unzip_pathname,dms_object.`name` AS unzip_name FROM 
(SELECT dms_object.id,dms_object.`name`,dms_object.pathname,dms_object_version.version,dms_unzip.state,dms_unzip.unzip_folder_id FROM dms_dms.dms_object
LEFT JOIN dms_dms.dms_object_version ON dms_object_version.object_id = dms_object.id
LEFT JOIN dms_dms.dms_unzip ON dms_unzip.zip_file_id = dms_object.id AND dms_unzip.zip_file_version = dms_object_version.version
where dms_object.id = "828676860396310528") m 
LEFT JOIN dms_dms.dms_object ON dms_object.folder_id = m.unzip_folder_id;
"""

cmd17 = """
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
WHERE n.accountid = 825316304704638977) l
GROUP BY l.accountid,l.ent_name,l.bucketid,l.tag_value
"""
# print("dms_bucket")
# db_action("platform_stg",cmd1)
# print("dms_file_soft_link")
# db_action("platform_stg",cmd4)
# print("dms_bucket")
# db_action("platform_stg",cmd2)
# print("dms_file_soft_link")
# db_action("platform_stg",cmd16)
# db_action("platform_stg", cmd9)
# db_action("platform_stg", cmd14)
# db_action("platform_prod", cmd13)
cmd18 = """
SELECT * FROM bms_bms.cbim_ent_department WHERE ent_id = "815275008518656000"
"""
cmd19 = """
select * from dms_dms.dms_unzip where dms_unzip.zip_file_id = "828676860396310528"
"""
cmd20 = """
SELECT dms_object.id,cbim_enterprise.account_id AS accountid,cbim_enterprise.`name` AS ent_name,dms_bucket.id AS bucketid,dms_bucket.app_code,dms_object.pathname,dms_object.size,dms_object_version.version,dms_object_tag.tag_value FROM dms_dms.dms_object_tag
LEFT JOIN dms_dms.dms_object ON dms_object_tag.object_id = dms_object.id
LEFT JOIN dms_dms.dms_bucket ON dms_bucket.id = dms_object.bucket_id
LEFT JOIN bms_bms.cbim_enterprise ON cbim_enterprise.account_id = dms_bucket.account_id
LEFT JOIN dms_dms.dms_object_version ON dms_object_version.object_id = dms_object.id
WHERE dms_object.id = "828676860396310528"
"""
cmd21 = """
SELECT rvt2cim_task.relation_id,rvt2cim_task.dms_id,rvt2cim_task.create_date,rvt2cim_task.status AS start_translate_time,rvt2cim_task.update_date AS complete_translate_time FROM rendering.rvt2cim_task where relation_id like "%833397889484066816%"
"""

cmd22 = """
SELECT dms_bucket.account_id,dms_folder.folder_path,dms_folder_tag.tag_value FROM dms_dms.dms_folder 
LEFT JOIN dms_dms.dms_bucket ON dms_bucket.id = dms_folder.bucket_id
LEFT JOIN dms_dms.dms_folder_tag ON dms_folder_tag.folder_id = dms_folder.id
WHERE dms_folder_tag.tag_key = "projectId"  AND dms_folder.parent_id in (SELECT dms_folder.id FROM dms_dms.dms_folder 
LEFT JOIN dms_dms.dms_bucket ON dms_bucket.id = dms_folder.bucket_id
WHERE dms_bucket.id = "804440423253807104" AND dms_bucket.app_code = "doc" AND dms_folder.parent_id = "0")
"""

cmd23 = """
SELECT pro_approval.proj_name,pro_approval.master_id FROM 
(SELECT MAX(pro_version.version),pro_version.form_id FROM project_approval_manage.pro_version 
WHERE pro_version.account_id = "797820274153230337" and pro_version.delete_type = 0 GROUP BY pro_version.parent_id) tem
LEFT JOIN project_approval_manage.pro_approval ON pro_approval.id = tem.form_id
"""
cmd24 = """
select dms_bucket.app_code,dms_object.id,dms_object.name,dms_file_soft_link.path from dms_dms.dms_object 
left join dms_dms.dms_file_soft_link on dms_file_soft_link.src_id = dms_object.id 
left join dms_dms.dms_bucket on dms_bucket.id = dms_file_soft_link.bucket_id
where dms_object.folder_id = 3083653
"""
cmd25 = """
select * from dms_dms.dms_file_soft_link where id = 813470313620918272
"""

cmd26 = """
SELECT dms_object.id,dms_object.pathname,dms_object.`name`,dms_object.size,dms_object_version.version FROM dms_dms.dms_object
LEFT JOIN dms_dms.dms_object_version ON dms_object_version.object_id = dms_object.id
WHERE dms_object.id = "839953151422500864"
"""

cmd27 = """
SELECT * FROM bms_bms.cbim_user WHERE account_id = "832258896088403969"
"""

cmd28 = """
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
WHERE n.accountid = "843147832784457729") l
GROUP BY l.tag_value,l.bucketid,l.accountid,l.ent_name
"""

cmd30 = """SELECT user_id,true_name,mobile FROM bms_bms.cbim_ent_user WHERE ent_id = '845274790427234304'"""

cmd31 = """SELECT * FROM bms_bms.cbim_user WHERE id = '744920821418106880'"""
# db_action("r2c", cmd21)
# db_action("platform_stg", cmd6)
# db_action("platform_stg", cmd18)
# db_action("platform_prod", cmd19)
# db_action("platform_prod", cmd24)
# db_action("platform_prod", cmd25)
db_action("platform_stg", cmd31)
