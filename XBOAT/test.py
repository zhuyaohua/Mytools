"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     test.py
@Author:   shenfan
@Time:     2022/6/23 9:23
"""
import datetime
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import ItarjConsole

timestamp = [1656329425434]
out = []
for item in timestamp:
    print(datetime.datetime.fromtimestamp(item/1000).strftime("%Y-%m-%d %H:%M:%S.%f"))
    out.append(datetime.datetime.fromtimestamp(item/1000).strftime("%Y-%m-%d %H:%M:%S.%f"))











