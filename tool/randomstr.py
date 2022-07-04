"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     randomstr.py
@Author:   shenfan
@Time:     2022/1/26 19:06
"""
import random


def Unicode(n):
    string = []
    for i in range(0,n):
        val1 = random.randint(65, 90)
        val2 = random.randint(97, 122)
        val = random.choice([val1, val2])
        string.append(chr(val))
    result = "".join(string)
    print("长度为：%s"%len(result))
    print(result)

def GBK2312(n):
    string = []
    for i in range(0,n):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xf9)
        val = f'{head:x}{body:x}'
        string.append(bytes.fromhex(val).decode('gb2312'))
    result = "".join(string)
    print("长度为：%s"%len(result))
    print(result)


Unicode(128)
# GBK2312(40)

