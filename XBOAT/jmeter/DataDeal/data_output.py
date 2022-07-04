"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     data_output.py
@Author:   shenfan
@Time:     2022/6/10 11:28
"""
import pandas
import os

BASEDIR = os.path.abspath(".")
OUTPUTDIR = os.path.join(os.path.dirname(os.path.dirname(BASEDIR)), "output")


def savefile(data, filename, filetype="csv"):
    dataframe = pandas.DataFrame(data, index=None)
    if filetype == "csv":
        dataframe.to_csv(os.path.join(OUTPUTDIR,filename), index=False, decimal=".")
    if filetype == "xls":
        dataframe.to_excel(os.path.join(OUTPUTDIR,filename), index=False, decimal=".")
