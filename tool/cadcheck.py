"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     cadcheck.py
@Author:   shenfan
@Time:     2021/3/8 10:16
"""

import redis

pool = redis.ConnectionPool(host="172.16.201.92",port=6379,db="0",password="1q2w@3e4r")
re = redis.StrictRedis(connection_pool=pool)
for item in re.keys():
    print(item.decode("utf-8"))


