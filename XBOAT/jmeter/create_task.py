"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     create_task.py
@Author:   shenfan
@Time:     2022/5/30 18:13
"""
import pandas
import os

BASE_DIR = os.path.abspath("..")
CSV = os.path.join(os.path.dirname(BASE_DIR), "data", "user_ent_managers（企业管理员）.csv")
dataframe = pandas.read_csv(CSV)
params = dataframe.values.tolist()
print(params)



