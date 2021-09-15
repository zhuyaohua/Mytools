"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     hmactest.py
@Author:   shenfan
@Time:     2021/9/14 18:12
"""
import hmac
import base64
import json
method = "post"
uri = "/v1/external/user/ticket"
timestamp = "1631613318445"
randoms = "de124f66-1541-11ec-8a26-38baf88ac8da"
body = {"username": "18571023517","password": "s123456","terminal": "web"}
key = bytearray("07ec7d475a084efdb99d1e832741df74",encoding="utf-8")
m =bytearray("%s\n%s\n%s\n%s\n%s"%(method.lower(),uri.lower(),timestamp,randoms,json.dumps(body)),encoding="utf-8")

h = hmac.new(key, m, digestmod="sha256").digest()
print(str(base64.b64encode(h),encoding="utf-8"))










