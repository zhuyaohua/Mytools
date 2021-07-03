# -*- coding: utf-8 -*-
from xlutils.copy import copy
from xlrd import open_workbook

excel=r'D:\Doctool\python\工具脚本\file\room.xls'
column=0
row=0
cnt=0

#------------逐个读取文本（有多个文本）存在excel中--------------
for cnt in range(1,21):
    
#------------读取要存放的数据-----------------
    f = open(r"C:\Users\SHENFAN\Desktop\中设数字\标准模板\房间表"+str(cnt)+".txt")
    line = f.readline()
    while line:
        title=line
        rb=open_workbook(excel,formatting_info=True)
        wb = copy(rb)
        sheet=wb.get_sheet(0)
        sheet.write(row,0,title.decode('utf8'))
        wb.save(excel)
        row=row+1   
        line = f.readline()
    f.close()






