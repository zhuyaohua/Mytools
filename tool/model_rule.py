"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     model_rule.py
@Author:   shenfan
@Time:     2021/5/31 19:51
"""
import pandas
from tool.compare_rule import RuleDispose
from itertools import product
import os
basedir = os.path.dirname(os.path.abspath("__file__"))

def ranslate(rulelib,checkcode):
    rawdata = RuleDispose(rulelib,checkcode).rawdata()
    tanslatedata = {}

    for item_temkey in rawdata[0]:
        if item_temkey[0] not in checkcode:
            tanslatedata.setdefault("%s【%s】"%(item_temkey[0],item_temkey[1]),[])
    for key in tanslatedata:
        for item_tem in rawdata:
            for item_temvalue in item_tem:
                if item_temvalue[0] in key:
                    if (item_temvalue[2].startswith("(") or item_temvalue[2].startswith("[")):
                        tanslatedata[key].append(item_temvalue[2])
                    else:
                        tanslatedata[key].extend(item_temvalue[2].split(","))
    values = list(tanslatedata.values())
    keys = list(tanslatedata.keys())
    input = map(lambda x: set(x) if isinstance(x, list) else set(x), values)

    combination = []
    for element in product(*input):

        combination.append(list(element))
        if len(combination) == 1048576-1:
            break

    path = os.path.join(basedir,"resultfile","%s.xlsx"%rulelib)
    temp_result = {}
    print("差积匹配完成")

    for key in keys:
        temp_result.setdefault(key,[])
        for i in range(len(combination)):
            temp_result[key].append(combination[i].pop(0))

    pandas.DataFrame(data=temp_result).to_excel(path,sheet_name=rulelib)

ranslate("抗震等级核查", "SC-S-B-012-L")



