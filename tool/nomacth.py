"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     nomacth.py
@Author:   shenfan
@Time:     2021/6/29 18:15
"""
import pandas
import json
import os
import jsonpath
from tool.SQL import query
basedir = os.path.dirname(os.path.abspath("__file__"))

with open(os.path.join(basedir,"resultfile","Es_no_match_data.json"),"r") as resultdata:
    rawdata = json.load(resultdata)

no_match = jsonpath.jsonpath(rawdata,"$.._source")
no_match_key = jsonpath.jsonpath(rawdata,"$.._source.ruleLibCode")


def output(rule_lib_code):

    header = """SELECT param_value.param_value as param_code,temp.param_value FROM
    (SELECT param_value.param_value,rule_value.rule_value,rule_value.line_num,param_value.line_num as param_line_num FROM rule_lib
    LEFT JOIN rule_value ON rule_value.rule_lib_id = rule_lib.id
    LEFT JOIN rule_param ON rule_param.id = rule_value.head_id
    LEFT JOIN param_value ON param_value.id = rule_param.param_value_id
    WHERE rule_lib.lib_code = "%s" AND (rule_value.head_type=0 or rule_value.head_type=1) AND param_value IS NOT NULL
    ORDER BY rule_value.line_num ASC,rule_value.head_id ASC) temp
    LEFT JOIN param_value ON param_value.line_num = temp.param_line_num
    WHERE param_value.param_head = '参数编号'
    GROUP BY param_value.param_value;"""%rule_lib_code

    libname = """
    SELECT lib_name FROM rule_lib WHERE lib_code = "%s"
    """%rule_lib_code

    headers = query("rule",header)
    sheet= query("rule",libname)[0][0]
    frame_data = {}
    for item in headers:
        frame_data.setdefault("【{0}】{1}".format(item[0],item[1]),[])

    df = pandas.DataFrame()
    for item in no_match:
        if item["ruleLibCode"] == rule_lib_code:
            temp_item = eval(item["data"])
            temp_dict = {}
            for key,value in temp_item.items():
                aimkey = list(filter(lambda text: key in text, list(frame_data.keys())))
                temp_dict[aimkey[0]]=value
            df_temp = pandas.DataFrame(data = temp_dict,index=[0])
            print(df_temp)
            df = df.append(df_temp,ignore_index=True)
            print(df)

    df.to_excel(os.path.join(basedir,"resultfile","output","Output-%s.xlsx"%rule_lib_code),sheet_name=sheet)



if __name__ == "__main__":
    for key in set(no_match_key):
        output(key)
    # output("A-1-12")




