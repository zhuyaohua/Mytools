"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     report.py
@Author:   shenfan
@Time:     2022/6/14 9:23
"""
import pandas
import os

OUTPUTDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath("."))), "output", "all-100-1-juhe.jtl")
with open(OUTPUTDIR, "r", encoding="utf-8") as strem:
    data = strem.readlines()

