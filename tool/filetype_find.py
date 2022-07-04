"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     filetype_find.py
@Author:   shenfan
@Time:     2021/2/1 17:11
"""
import magic
import os
print(magic.from_buffer(open(r"D:\Doctool\HTML\20220322笔记",'rb').read(2048)))