"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     test.py
@Author:   shenfan
@Time:     2020/9/22 17:47
"""
import sys
import difflib
import os
import functools

file_new=os.path.join(os.path.dirname(os.path.abspath(".")),"data","cdanew.json")
file_old =os.path.join(os.path.dirname(os.path.abspath(".")),"data","CDAold.json")
@functools.lru_cache(maxsize=12)
def readfile(file):
    try:
        fd=open(file,"r",encoding="utf-8")
        text=fd.read().splitlines()  #读取之后进行行分割
        return text
    except Exception as e:
        print("read file error")
        print(e)
        sys.exit()


@functools.lru_cache(maxsize=12)
def Compare(file_1,file_2):
    if file_1 =="" or file_2 == "":
        print("file 1 or file 2 not empty")
        sys.exit()

    text1=readfile(file_1)
    text2=readfile(file_2)
    #创建一个diff对象
    diff=difflib.HtmlDiff()
    #得出比较结果
    result=diff.make_file(text1, text2)

    try:
        fd_diff=open("diff.html","w")
        fd_diff.write(result)

    except Exception as e:
        print("write html file error")
        print(e)
        sys.exit()

def rate(fileold,filenew):
    lineinfo = {}
    lineinfo["fileold"]=len(open(fileold,"r",encoding="utf-8").readlines())
    lineinfo["filenew"]=len(open(filenew,"r",encoding="utf-8").readlines())
    print("旧文件行数：%s -----> 新文件行数：%s"% (lineinfo["fileold"],lineinfo["filenew"]))
    lineinfo["fileold_size"] = os.path.getsize(fileold)/float(1024*1024)
    lineinfo["filenew_size"] = os.path.getsize(filenew)/float(1024*1024)
    print("旧文件大小：%s MB -----> 新文件大小：%s MB"% (round(lineinfo["fileold_size"],2), round(lineinfo["filenew_size"],2)))
    lineinfo["rate"]=(lineinfo["fileold_size"]-lineinfo["filenew_size"])/lineinfo["fileold_size"]
    print("优化率",round(lineinfo["rate"],4))
    return lineinfo



if __name__ == '__main__':
    rate(file_old,file_new)
    Compare(file_new,file_old)


