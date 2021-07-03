"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     cbz.py.py
@Author:   shenfan
@Time:     2020/12/11 17:30
"""

import json
import os
import numpy
import matplotlib.pyplot
import mpl_toolkits.mplot3d
from decimal import Decimal

filename = os.path.join(os.path.dirname(os.path.abspath(".")),"file","cbz.json")
with open(filename,"r",encoding="utf-8") as data:
    jsondata = json.load(data)

def OuterContoursPoints(*landno):
    building_no = [item for item in jsondata["OuterContoursPoints"]]
    # if len(landno) == 0 :
    #     for itemno in building_no:
    #         for floor_key,floor_value in jsondata["OuterContoursPoints"][itemno].items():
    #             point = []
    #             print("建筑 %s 的楼层 %s 的坐标信息："%(itemno,floor_key))
    #             for item_point in floor_value:
    #                 print(item_point)
    #                 point.append(item_point)
    #             #绘制3D视图
    #             ax = matplotlib.pyplot.subplot(projection='3d')
    #             ax.set_title("%s-%s：" % (itemno, floor_key))
    #             x = [p["X"] for p in point]
    #             y = [p["Y"] for p in point]
    #             z = [p["Z"] for p in point]
    #             ax.scatter(x, y, z, c='r')
    #
    #             ax.set_xlabel('X')
    #             ax.set_ylabel('Y')
    #             ax.set_zlabel('Z')
    #
    #             matplotlib.pyplot.show()
    # else:
    #     for floor_key, floor_value in jsondata["OuterContoursPoints"][landno[0]].items():
    #         point = []
    #         print("建筑 %s 的楼层 %s 的坐标信息：" % (landno[0], floor_key))
    #         for item_point in floor_value:
    #             print(item_point)
    #             point.append(item_point)
    #         # 绘制3D视图
    #         ax = matplotlib.pyplot.subplot(projection='3d')
    #         ax.set_title("%s-%s：" % (landno[0], floor_key))
    #         x = [p["X"] for p in point]
    #         y = [p["Y"] for p in point]
    #         z = [p["Z"] for p in point]
    #         ax.scatter(x, y, z, c='r')
    #         ax.set_xlabel('X')
    #         ax.set_ylabel('Y')
    #         ax.set_zlabel('Z')
    #         # matplotlib.pyplot.show()
    #         ax = matplotlib.pyplot.subplot()
    #         ax.scatter(x, y,c='r')
    #         print("投影图像：")
    #         ax.set_xlabel('X')
    #         ax.set_ylabel('Y')
    #         matplotlib.pyplot.show()
    # 绘制地块上建筑的所有x0y平面上的投影坐标
    xoypoint = {}
    for itemno in building_no:
        temp = []
        for pointkey,ponit in jsondata["OuterContoursPoints"][itemno].items():
            if pointkey.rfind("F") >= 0:
                for itempoint in ponit:
                    itempoint.pop("Z")
                    temp.append(itempoint)
        xoypoint[itemno]=temp

    fig = matplotlib.pyplot.figure(figsize=(8, 4),dpi=256)
    matplotlib.pyplot.xticks(numpy.arange(-4,4,1))
    matplotlib.pyplot.yticks(numpy.arange(-4,4,1))
    for key,value in xoypoint.items():
        x = [p["X"] for p in value]
        y = [p["Y"] for p in value]
        print(x,y)
        # ax = matplotlib.pyplot.subplot()
        # ax.set_title("%s" % key)
        # ax.scatter(x, y,c='r')
        # ax.set_xlabel('X')
        # ax.set_ylabel('Y')
        # matplotlib.pyplot.show()
        ax = fig.add_subplot()
        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')
        matplotlib.pyplot.plot(x,y)
        matplotlib.pyplot.scatter(x,y)
    matplotlib.pyplot.show()

def OuterContourHeight(*landno):
    building_no = [item for item in jsondata["OuterContoursPoints"]]
    xoypoint = {}
    for itemno in building_no:
        temptop = set()
        templev = set()
        for pointkey, ponit in jsondata["OuterContoursPoints"][itemno].items():
            if True:
                for itempoint in ponit:
                    templev.add("%s %s"%(pointkey,itempoint["Z"]))
                    temptop.add(float(itempoint["Z"]))
        print("\033[1;32;0m%s:\033[0m"%itemno)
        print("\033[1;33;0m各楼层%s:\033[0m"%templev)
        print("\033[1;34;0m%s:\033[0m"%temptop)


if __name__ == "__main__":
    OuterContoursPoints()
    # OuterContourHeight()



