"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     txt_to_excel.py
@Author:   shenfan
@Time:     2020/9/8 14:18
"""
import numpy as np
import xlrd
import xlwt
import os

path = r"C:\Users\SHENFAN\Desktop\中设数字\标准模板\房间表\房间用料表.txt"
f = open(path,'r',encoding='utf-16 le')
wb = xlwt.Workbook(encoding = 'utf-16 le')
ws1 = wb.add_sheet('first')
row = 0
col = 0
k = 0
for lines in f:
    a = lines.split("\t")
    k+=1
    for i in range(len(a)):
        ws1.write(row, col ,a[i])
        col += 1
    row += 1
    col = 0
wb.save(r"D:\Doctool\python\工具脚本\file\room.xls")




