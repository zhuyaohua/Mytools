"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     SQL.py
@Author:   shenfan
@Time:     2020/9/22 15:40
"""
import pymysql

connpool = {
    "delivery_pro":pymysql.connect(host="172.16.201.185", port=3306, user="root", passwd="1q2w@3e4r"),
    "delivery_dev":pymysql.connect(host="172.16.201.92", port=3306, user="root", passwd="1q2w@3e4r"),
    "rule":pymysql.connect(host="172.16.201.122", port=3306, user="root", passwd="dbpass",db="cbim_rule"),
    "doctool_dev":pymysql.connect(host="172.16.201.122", port=3306, user="root", passwd="dbpass",db="cbim_rule")
}

def query(db,cmd):
    dbcur = connpool[db]
    cur = dbcur.cursor()
    cur.execute(cmd)
    result = cur.fetchall()
    # dbcur.close()
    return result

def insert(db,cmd):
    dbcur = connpool[db]
    cur = dbcur.cursor()
    try:
        cur.execute(cmd)
        dbcur.commit()
    except:
        dbcur.rollback()

    dbcur.close()
    return result


if __name__ == "__main__":
    cmdtemp = "SELECT * FROM cbim_audit.model_info WHERE id = {0} "
    cmd_cda_temp = "SELECT * FROM cbim_audit.component_{0} WHERE model_id = {1}"
    cmd_report = "SELECT * FROM cbim_audit.audit_result WHERE model_id = {0}"
    while True:
        modelid = input("模型ID：")
        try:
            index = query("delivery_dev",cmdtemp.format(modelid))[0][3]
            result = query("delivery_dev",cmd_cda_temp.format(index,modelid))
            report = query("delivery_dev",cmd_report.format(modelid))
        except Exception as e:
            print(e)
            print("无数据")
            continue
        for i in range(len(result)):
            print()
            print("*"*20)
            print(result[i][1])
            print(result[i][2])
            for item in result[i][4].lstrip("{").rstrip("}").split("},"):
                print(item+"}")
        print(report)















