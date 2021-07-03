"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     hierarchy_info.py
@Author:   shenfan
@Time:     2021/6/21 15:05
"""
from tool.SQL import query
import os
import json

major_file = os.path.join(os.path.dirname(os.path.abspath(".")), "file", "major_code")


def generator_major_code():
    cmd = """
SELECT rv.rule_value,pv.param_value,rv.line_num FROM cbim_rule.rule_value rv
LEFT JOIN cbim_rule.rule_param rp ON rp.id = rv.head_id
LEFT JOIN cbim_rule.param_value pv ON pv.id = rp.param_value_id
WHERE rv.rule_lib_id in (SELECT id FROM cbim_rule.rule_lib WHERE lib_code REGEXP "^(GH-DH|ZNSC|SZGC-DH|ZYTZ|JSGL-DH-1|JGSC-DH)" AND lib_status =0)
HAVING pv.param_value in ("审查项名称","专业属性","规范条目数","审查对象类型")
ORDER BY rv.line_num
"""
    db = "rule"
    raw_hierarchy = query(db,cmd)
    result_dict = {}
    linelist = []
    for item_line in raw_hierarchy:
        linelist.append(item_line[2])
    for line in linelist:
        tempdict = {}
        for item_data in raw_hierarchy:
            if item_data[2] == line:
                if item_data[0] == "":break
                tempdict[item_data[1]]=item_data[0]
        if {"审查对象类型","专业属性"} <= set(tempdict.keys()) and tempdict["审查对象类型"] != "":
            if "规范条目数" in tempdict.keys():
                result_dict[tempdict["审查对象类型"]] = (tempdict["专业属性"],tempdict["规范条目数"])
            else:
                result_dict[tempdict["审查对象类型"]] = (tempdict["专业属性"],"")
    return result_dict

m = generator_major_code()
with open(major_file,"w",encoding="utf-8") as data:
    data.write(json.dumps(m))








