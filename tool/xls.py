"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     xls.py
@Author:   shenfan
@Time:     2020/11/1 15:21
"""
import xlwt
import pandas
from interfaces.SQLAction import dbaction

sheetname = []
cellname = []
workbook = xlwt.Workbook(encoding="utf-8")
db = dbaction("cbim_rule")

#添加sheet名
cmd_param_name = 'SELECT name FROM param_lib WHERE `code` = "GH-A";'
for items in db.query(cmd_param_name):
    for item in items:
        sheetname.append(item)
print(sheetname)

#样式
pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = 48
headstyle = xlwt.XFStyle()
headstyle.pattern = pattern
font = xlwt.Font()
font.name = u'微软雅黑'
font.bold = True
headstyle.font = font

alignment  = xlwt.Alignment()
alignment.horz = 1
# alignment.wrap=1
cellstyle = xlwt.XFStyle()
cellstyle.alignment = alignment
headstyle.alignment = alignment




#添加表头
cmd_param_head = """
SELECT name FROM param_head WHERE param_lib_id in(SELECT id FROM param_lib WHERE `code` = "GH-A");
"""
param_head = []
for item in db.query(cmd_param_head):
    param_head.append(item[0])
print(param_head)
sheet = workbook.add_sheet(sheetname[0],cell_overwrite_ok=True)
sheet.col(1).width=256*30
sheet.col(4).width=256*60
sheet.col(5).width=256*60
sheet.col(6).width=256*80
sheet.col(7).width=256*30
sheet.col(9).width=256*30
sheet.col(11).width=256*80
sheet.col(12).width=256*80

for i in range(len(param_head)):
    sheet.write(0,i,param_head[i],headstyle)


#填充数据
cmd_param = """
SELECT param_head,param_value,line_num FROM param_value WHERE param_lib = "100184"
"""
param_value = []
param_value_line = set([])
for items in db.query(cmd_param):
    param_value_line.add(items[2])
    param_value.append(items)
print(param_value_line)
print(param_value)
print(sheet.name)
count = 1
for line in param_value_line:
    print(line)
    for items in param_value:
        if items[2] == line:
            if items[0] in param_head:
                print(count)
                print(param_head.index(items[0]))
                print(items[1])
                sheet.write(count,param_head.index(items[0]),items[1],cellstyle)
    count+=1

workbook.save("规则引擎.xls")






























