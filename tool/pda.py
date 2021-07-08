"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     pda.py
@Author:   shenfan
@Time:     2020/9/4 10:08
"""
import json
import os
import pymysql
from decimal import Decimal
import interval
import re
import xlwt
import xlrd
import sys
from progress.bar import Bar
from jsonpath import jsonpath
from tool.compare_rule import RuleDispose
import math

fileresult = open("itemlevel.json", "w+")
filename = os.path.join(os.path.dirname(os.path.abspath(".")), "file", "pda.json")
filenamecad = os.path.join(os.path.dirname(os.path.abspath(".")), "file", "cda.json")
excelname_BJ = os.path.join(os.path.dirname(os.path.abspath(".")), "file", "分类编码规则表-北京.xls")
excelname_NJ = os.path.join(os.path.dirname(os.path.abspath(".")), "file", "分类编码规则表-南京.xls")
major_file = os.path.join(os.path.dirname(os.path.abspath(".")), "file", "major_code")
auditpage_file = os.path.join(os.path.dirname(os.path.abspath(".")), "file", "auditpage")
with open(major_file, "r") as data:
    major_code = eval(data.read())
with open(auditpage_file, "r", encoding="utf-8") as data:
    page = jsonpath(json.loads(data.read())["result"], "$..annotationInfos[*].menuShowDes")
with open(auditpage_file, "r", encoding="utf-8") as data:
    attribute = jsonpath(json.loads(data.read())["result"], "$..annotationInfos[*].professionalAttribute")
auditpage = dict(zip(page, attribute))


# 分类编码表
def read_excel(filename):
    workbook = xlrd.open_workbook(filename)
    allsheetnames = workbook.sheet_names()
    code = {}
    for sheet in allsheetnames:
        sheet_content = workbook.sheet_by_name(sheet)
        temp = []
        for row in range(1, sheet_content.nrows):
            temp.append(str(sheet_content.cell(row, 0).value) + sheet_content.cell(row, 1).value)
        code.setdefault(sheet, temp)
    return code


with open(filename, "r", encoding="utf-8") as data:
    jsondata = json.load(data)
with open(filenamecad, "r", encoding="utf-8") as data:
    jsoncaddata = json.load(data)

map_No = {}
# 定义地块编号和地块名称映射表
for item_land in jsondata["landList"]:
    map_No.setdefault(item_land["properties"]["GH-A-101"]["Value"], item_land["landName"])


# 总图审查
def Area():
    for item_land in jsondata["landList"]:
        No = item_land["properties"]["GH-A-101"]["Value"]
        Name = item_land["landName"]
        if item_land["properties"]["GH-A-104"]["Value"] == "否":
            print("*" * 100)
            print("%s地块-建设用地：" % No)
            print("\033[1;33m %s : %s\033[0m" % (
                item_land["properties"]["GH-A-102"]["Value"], item_land["properties"]["GH-A-103"]["Value"]))
        # 根据地块编号查找建筑单体
        underarea = 0
        uparea = 0
        newuparea = 0
        newunderarea = 0
        reuparea = 0
        reunderarea = 0
        chunderarea = 0
        chuparea = 0
        buildtop = 0
        for item_building in jsondata["buildingList"]:
            if Name == item_building["landName"]:
                if "properties" in item_building.keys() or "GH-A-182" in item_building["properties"].keys():
                    if len(item_building["properties"]["GH-A-182"]["Value"].strip("")) > 0:
                        buildtop = Decimal(item_building["properties"]["GH-A-182"]["Value"])
                else:
                    print("无建筑高度")
                # 新建地下建筑面积
                if item_building["properties"]["GH-A-174"]["Value"] == "新建":
                    print(item_building["buildingNo"], "新建")
                    for item_building_area in item_building["areaList"]:
                        if item_building_area["properties"]["GH-A-135"]["Value"].startswith("B"):
                            # print("\033[1;35m%s建筑\033[0m 新建地下标准楼层 \033[1;35m%s\033[0m 的构建：\033[0m"%(item_building["properties"]["GH-A-109"]["Value"],item_building_area["properties"]["GH-A-175"]["Value"]),item_building_area["uid"])
                            # print(item_building_area["properties"]["GH-A-135"]["Value"],item_building_area["properties"]["GH-A-175"]["Value"],item_building_area["properties"]["GH-A-176"]["Value"])
                            count = len(item_building_area["properties"]["GH-A-175"]["Value"].split(";"))
                            newunderarea += Decimal(item_building_area["properties"]["GH-A-176"]["Value"]) * count
                        # 新建地上建筑面积
                        elif not item_building_area["properties"]["GH-A-135"]["Value"].startswith("B"):
                            # print("\033[1;35m%s建筑\033[0m 新建地上标准楼层 \033[1;35m%s\033[0m 的构建：" %(item_building["properties"]["GH-A-109"]["Value"],item_building_area["properties"]["GH-A-175"]["Value"]),item_building_area["uid"])
                            # print(item_building_area["properties"]["GH-A-135"],
                            #       item_building_area["properties"]["GH-A-175"],
                            #       item_building_area["properties"]["GH-A-176"])
                            count = len(item_building_area["properties"]["GH-A-175"]["Value"].split(";"))
                            newuparea += Decimal(item_building_area["properties"]["GH-A-176"]["Value"]) * count
                # 保留
                if item_building["properties"]["GH-A-174"]["Value"] == "保留":
                    print(item_building["buildingNo"], "保留")
                    if "areaList" in item_building.keys():
                        print(item_building["buildingNo"], "建筑性质：保留，但有areaList")
                    if not item_building["properties"]["GH-A-402"]["Value"] == "":
                        reunderarea += Decimal(item_building["properties"]["GH-A-402"]["Value"])
                    if not item_building["properties"]["GH-A-401"]["Value"] == "":
                        reuparea += Decimal(item_building["properties"]["GH-A-401"]["Value"])
                # 拆除
                if item_building["properties"]["GH-A-174"]["Value"] == "拆除":
                    print(item_building["buildingNo"], "拆除")
                    if "areaList" in item_building.keys():
                        print(item_building["buildingNo"], "建筑性质：拆除，但有areaList")
                    if not item_building["properties"]["GH-A-402"]["Value"] == "":
                        chunderarea += Decimal(item_building["properties"]["GH-A-402"]["Value"])
                    if not item_building["properties"]["GH-A-401"]["Value"] == "":
                        chuparea += Decimal(item_building["properties"]["GH-A-401"]["Value"])
                else:
                    pass
        underarea = newunderarea + reunderarea
        uparea = newuparea + reuparea

        print("\033[1;35m地下建筑面积: \033[1m", underarea)
        print("\033[1;35m新建地下建筑面积: \033[1m", newunderarea)
        print("\033[1;35m保留地下建筑面积: \033[1m", reunderarea)
        print("\033[1;35m拆除地下建筑面积: \033[1m", chunderarea)

        print("\033[1;35m地上建筑面积: \033[1m", uparea)
        print("\033[1;35m新建地上建筑面积: \033[1m", newuparea)
        print("\033[1;35m保留地上建筑面积: \033[1m", reuparea)
        print("\033[1;35m拆除地上建筑面积: \033[1m", chuparea)

        print("\033[1;35m容积率：\033[1m", (uparea / Decimal(item_land["properties"]["GH-A-103"]["Value"])))
        print("\033[1;35m建筑高度：\033[1m", buildtop)


# 居住公共设施服务审查
def ResidentialServicesAudit():
    code = list(filter(lambda x: x.startswith(" '09"),
                       str(read_excel(excelname_BJ)["建筑类型"]).strip("[").split("]")[0].split(",")))
    for item_land in jsondata["landList"]:
        No = item_land["properties"]["GH-A-101"]["Value"]
        Name = item_land["landName"]
        print("\033[1;35m地块%s\033[0m" % No)
        if "landComponentList" in item_land.keys() and len(item_land["landComponentList"]) != 0:
            for item_land_landComponent in item_land["landComponentList"]:
                if "GH-A-171" in item_land_landComponent["properties"]:
                    for itemcode in code:
                        if item_land_landComponent["properties"]["GH-A-171"]["Value"] in itemcode and len(
                                item_land_landComponent["properties"]["GH-A-171"]["Value"]) > 0:
                            print(itemcode,
                                  "\033[1;35m地块审查项为：%s\033[0m" % item_land_landComponent["properties"]["GH-A-171"][
                                      "Value"])
        for item_building in jsondata["buildingList"]:
            if Name == item_building["landName"]:
                for itemcode in code:
                    if item_building["properties"]["GH-A-110"]["Value"] in itemcode and len(
                            item_building["properties"]["GH-A-110"]["Value"]) > 0:
                        print(itemcode, "\033[1;35m%s建筑审查项为：%s\033[0m" % (
                            item_building["properties"]["GH-A-109"]["Value"],
                            item_building["properties"]["GH-A-110"]["Value"]))


# 停车位审查
def ParkingAudit():
    for item_land in jsondata["landList"]:
        No = item_land["properties"]["GH-A-101"]["Value"]
        Name = item_land["landName"]
        land_parkingarea_motor = 0
        land_parkingarea_Nonmotor = 0
        building_parkingarea_motor = 0
        building_parkingarea_Nonmotor = 0
        outNonmotor = 0
        inNonmotor = 0
        outmotor = 0
        outmotoruid = []
        inmotor = 0
        inmotoruid = []
        outCharging = 0
        inCharging = 0
        selfparking_B = 0
        selfparking_F = 0

        print("\033[1m地块\033[1;35m%s：" % No)
        if "landComponentList" in item_land.keys() and len(item_land["landComponentList"]) != 0:
            for item_land_landComponent in item_land["landComponentList"]:
                if "GH-A-108" in item_land_landComponent["properties"].keys() and \
                        item_land_landComponent["properties"]["GH-A-108"]["Value"] == "机动车位":
                    land_parkingarea_motor += Decimal(item_land_landComponent["properties"]["GH-A-176"]["Value"])
                if "GH-A-108" in item_land_landComponent["properties"].keys() and item_land_landComponent["properties"][
                    "GH-A-108"]["Value"] == "非机动车位":
                    land_parkingarea_Nonmotor += Decimal(item_land_landComponent["properties"]["GH-A-176"]["Value"])
                    outNonmotor += land_parkingarea_Nonmotor // 2
            print("地块上的机动车位面积：%s     地块上的非机动车位面积：%s" % (land_parkingarea_motor, land_parkingarea_Nonmotor))
        print("parkingList")
        if len(item_land["parkingList"]) > 0:
            for item_parking in item_land["parkingList"]:
                if item_parking["properties"]["GH-A-138"]["Value"] in ["自走式停车位", "大巴车位", "出租车位", "无障碍车位"]:
                    outmotor += 1
                    outmotoruid.append(item_parking["uid"])
                if item_parking["properties"]["GH-A-138"]["Value"] in ["装卸车位", "机械式停车位"]:
                    outmotor += 1 * (lambda: 1 if item_parking["properties"]["GH-A-596"]["Value"] == "" else int(
                        item_parking["properties"]["GH-A-596"]["Value"]))()
                    outmotoruid.append(item_parking["uid"])
                if item_parking["properties"]["GH-A-370"]["Value"] == "是":
                    outCharging += 1
                if item_parking["properties"]["GH-A-138"]["Value"] == "自走式停车位":
                    selfparking_F += 1 * (lambda: 1 if item_parking["properties"]["GH-A-596"]["Value"] == "" else int(
                        item_parking["properties"]["GH-A-596"]["Value"]))()
            print("自走式停车位(F)：", selfparking_F)
            print("*" * 100)
        else:
            print("\033[1;35m%s地块无停车位\033[0m" % No)

        for item_building in jsondata["buildingList"]:
            if Name == item_building["landName"]:
                print("\033[1;31m%s - 建筑类型：%s 建筑类别：%s\033[0m" % (
                    item_building["buildingNo"], item_building["properties"]["GH-A-110"]["Value"],
                    item_building["properties"]["GH-A-009"]["Value"]))
                print("parkingList")
                if "parkingList" in item_building and len(item_building["parkingList"]) != 0:
                    for item_building_parking in item_building["parkingList"]:
                        if item_building_parking["properties"]["GH-A-370"]["Value"] == "是":
                            inCharging += 1
                        if item_building_parking["properties"]["GH-A-138"]["Value"] in ["自走式停车位", "大巴车位", "出租车位",
                                                                                        "无障碍车位"]:
                            inmotor += 1
                            inmotoruid.append(item_building_parking["uid"])
                        if item_building_parking["properties"]["GH-A-138"]["Value"] in ["装卸车位", "机械停车位"]:
                            inmotor += 1 * (lambda: 1 if item_parking["properties"]["GH-A-596"]["Value"] == "" else int(
                                item_parking["properties"]["GH-A-596"]["Value"]))()
                            inmotoruid.append(item_building_parking["uid"])
                        if item_building_parking["properties"]["GH-A-138"]["Value"] in ["自走式停车位"] and \
                                item_building_parking["properties"]["GH-A-135"]["Value"].startswith("F"):
                            selfparking_F += 1 * (
                                lambda: 1 if item_building_parking["properties"]["GH-A-596"]["Value"] == "" else int(
                                    item_building_parking["properties"]["GH-A-596"]["Value"]))()
                        if item_building_parking["properties"]["GH-A-138"]["Value"] in ["自走式停车位"] and \
                                item_building_parking["properties"]["GH-A-135"]["Value"].startswith("B"):
                            selfparking_B += 1 * (
                                lambda: 1 if "GH-A-596" not in item_building_parking["properties"] else int(
                                    item_building_parking["properties"]["GH-A-596"]["Value"]))()
                else:
                    print("\033[1;35m%s建筑无停车位\033[0m" % item_building["buildingNo"])
                print("自走式停车位(F)", selfparking_F)
                print("自走式停车位(B)", selfparking_B)
                print("-" * 100)
                if "areaList" in item_building and len(item_building["areaList"]) != 0:
                    for building_area in item_building["areaList"]:
                        if "GH-A-159" in building_area["properties"].keys() and building_area["properties"]["GH-A-159"][
                            "Value"] == "室内机动车停车库":
                            building_parkingarea_motor += Decimal(building_area["properties"]["GH-A-176"]["Value"])

                        if "GH-A-159" in building_area["properties"].keys() and building_area["properties"]["GH-A-159"][
                            "Value"] == "室内非机动车停车库":
                            building_parkingarea_Nonmotor += Decimal(building_area["properties"]["GH-A-176"]["Value"])
                            print("*" * 100)
        inNonmotor += building_parkingarea_Nonmotor // 2

        print("Total:")
        print("\033[1;36m地块%s-地块机动车的车位面积是：%s\033[0m" % (No, land_parkingarea_motor))
        print("\033[1;36m地块%s-建筑机动车的车位面积是：%s\033[0m" % (No, building_parkingarea_motor))
        print("\033[1;36m地块%s-机动车的车位面积是：%s\033[0m" % (No, building_parkingarea_motor + land_parkingarea_motor))

        print("\033[1;36m地块%s-地块非机动车的车位面积是：%s\033[0m" % (No, land_parkingarea_Nonmotor))
        print("\033[1;36m地块%s-地块室外非机动车的车位数量是：%s\033[0m" % (No, outNonmotor))
        print("\033[1;36m地块%s-地块室外充电桩个数是：%s\033[0m" % (No, outCharging))
        print("\033[1;36m地块%s-建筑非机动车的车位面积是：%s\033[0m" % (No, building_parkingarea_Nonmotor))
        print("\033[1;36m地块%s-建筑室内非机动车的车位数量是：%s\033[0m" % (No, inNonmotor))
        print("\033[1;36m地块%s-建筑室内充电桩数量是：%s\033[0m" % (No, inCharging))
        print("\033[1;36m地块%s-非机动车的车位面积是：%s\033[0m" % (No, building_parkingarea_Nonmotor + land_parkingarea_Nonmotor))
        print("\033[1;36m地块%s-地块室外机动车位数：%s 建筑室内机动车位数：%s 地块的机动车位数：%s\033[0m" % (
            No, outmotor, inmotor, (outmotor + inmotor)))
        print("机动车联动UID：")
        for item in outmotoruid: print(item)
        for item in inmotoruid: print(item)

        print("总自走式停车位(B)：", selfparking_B)
        print("总自走式停车位(F)：", selfparking_F)
        print("#\033[0m" * 100)


# 单体表单审查
def MonomerFormResidential():
    buildtypecate = []
    for codelist in read_excel(excelname_BJ)["建筑类型"]:
        if codelist.startswith("09"): buildtypecate.append("".join(list(filter(lambda x: not x.isdigit(), codelist))))
    for item_land in jsondata["landList"]:
        landno = item_land["properties"]["GH-A-101"]["Value"]
        landname = item_land["landName"].strip("")
        if item_land["properties"]["GH-A-102"]["Value"].strip()[0] in "R居住用地":
            print()
            print("*" * 20)
            print("\033[1;33;1m%s地块单体审查\033[1m" % landno)
            print("-" * 20, ">\033[1;33;1m居住项目——建筑单体明细表:\033[1m<", "-" * 20)
            for item_building in jsondata["buildingList"]:
                underarea = 0
                uparea = 0
                level_B = 0
                level_F = 0
                buildtop_B = 0
                buildtop_F = 0
                if item_building["properties"]["GH-A-390"]["Value"].strip() == landname and not \
                        item_building["properties"]["GH-A-174"]["Value"] == "拆除":
                    if item_building["properties"]["GH-A-110"]["Value"].strip() in ["住宅", "公寓", "别墅", "酒店式公寓", "商住楼"]:
                        print("\033[1;32m住宅：\033[1m")
                        # 新建地下建筑面积
                        if item_building["properties"]["GH-A-174"]["Value"] == "新建":
                            for item_building_area in item_building["areaList"]:
                                if item_building_area["properties"]["GH-A-135"]["Value"].startswith("B"):
                                    # print("log->",item_building_area["properties"]["GH-A-135"]["Value"],item_building_area["properties"]["GH-A-175"]["Value"],item_building_area["properties"]["GH-A-176"]["Value"])
                                    count = len(item_building_area["properties"]["GH-A-175"]["Value"].split(";"))
                                    underarea += Decimal(
                                        item_building_area["properties"]["GH-A-176"]["Value"]) * count
                                # 新建地上建筑面积
                                elif not item_building_area["properties"]["GH-A-135"]["Value"].startswith("B"):
                                    count = len(item_building_area["properties"]["GH-A-175"]["Value"].split(";"))
                                    uparea += Decimal(item_building_area["properties"]["GH-A-176"]["Value"]) * count
                        # 保留
                        if item_building["properties"]["GH-A-174"]["Value"] == "保留":
                            if "areaList" in item_building.keys(): pass
                            if not item_building["properties"]["GH-A-402"]["Value"] == "": underarea += Decimal(
                                item_building["properties"]["GH-A-402"]["Value"])
                            if not item_building["properties"]["GH-A-401"]["Value"] == "": uparea += Decimal(
                                item_building["properties"]["GH-A-401"]["Value"])
                        else:
                            pass
                        if "GH-A-392" in item_building["properties"] and item_building["properties"]["GH-A-392"][
                            "Value"]: level_F = item_building["properties"]["GH-A-392"]["Value"]
                        for item_area_uid in item_building["areaList"]:
                            if not item_area_uid["properties"]["GH-A-135"]["Value"].startswith("B"):
                                print(item_area_uid["properties"]["GH-A-135"]["Value"], item_area_uid["uid"])
                        if "GH-A-112" in item_building["properties"] and item_building["properties"]["GH-A-112"][
                            "Value"]: level_B = item_building["properties"]["GH-A-112"]["Value"]
                        if "GH-A-182" in item_building["properties"] and item_building["properties"]["GH-A-182"][
                            "Value"]: buildtop_F = item_building["properties"]["GH-A-182"]["Value"]
                        if "GH-A-121" in item_building["properties"] and item_building["properties"]["GH-A-121"][
                            "Value"]: buildtop_B = item_building["properties"]["GH-A-121"]["Value"]
                        print("楼号 | %s" % item_building["buildingNo"], end=" | ")
                        print("总建筑面积（㎡）%s" % (underarea + uparea), end=" | ")
                        print("地上建筑面积（㎡）%s" % uparea, end=" | ")
                        print("地下建筑面积（㎡）%s" % underarea, end=" | ")
                        print("层数（地上）%s" % level_F, end=" | ")
                        print("层数（地下）%s" % level_B, end=" | ")
                        print("高度（地上）%s" % buildtop_F, end=" | ")
                        print("高度（地下）%s |" % buildtop_B)
                    if item_building["properties"]["GH-A-110"]["Value"].strip() in buildtypecate:
                        print("\033[1;32m配套：\033[1m")
                        # 新建地下建筑面积
                        if item_building["properties"]["GH-A-174"]["Value"] == "新建":
                            for item_building_area in item_building["areaList"]:
                                if item_building_area["properties"]["GH-A-135"]["Value"].startswith("B"):
                                    # print("log->",item_building_area["properties"]["GH-A-135"]["Value"],item_building_area["properties"]["GH-A-175"]["Value"],item_building_area["properties"]["GH-A-176"]["Value"])
                                    count = len(item_building_area["properties"]["GH-A-175"]["Value"].split(";"))
                                    underarea += Decimal(
                                        item_building_area["properties"]["GH-A-176"]["Value"]) * count
                                # 新建地上建筑面积
                                elif not item_building_area["properties"]["GH-A-135"]["Value"].startswith("B"):
                                    # print("log->", item_building_area["properties"]["GH-A-135"]["Value"],
                                    #       item_building_area["properties"]["GH-A-175"]["Value"],
                                    #       item_building_area["properties"]["GH-A-176"]["Value"])
                                    count = len(item_building_area["properties"]["GH-A-175"]["Value"].split(";"))
                                    uparea += Decimal(item_building_area["properties"]["GH-A-176"]["Value"]) * count
                        # 保留
                        if item_building["properties"]["GH-A-174"]["Value"] == "保留":
                            if "areaList" in item_building.keys(): pass
                            if not item_building["properties"]["GH-A-402"]["Value"] == "": underarea += Decimal(
                                item_building["properties"]["GH-A-402"]["Value"])
                            if not item_building["properties"]["GH-A-401"]["Value"] == "": uparea += Decimal(
                                item_building["properties"]["GH-A-401"]["Value"])
                        else:
                            pass
                        if "GH-A-392" in item_building["properties"] and item_building["properties"]["GH-A-392"][
                            "Value"]: level_F = item_building["properties"]["GH-A-392"]["Value"]
                        if "GH-A-112" in item_building["properties"] and item_building["properties"]["GH-A-112"][
                            "Value"]: level_B = item_building["properties"]["GH-A-112"]["Value"]
                        if "GH-A-182" in item_building["properties"] and item_building["properties"]["GH-A-182"][
                            "Value"]: buildtop_F = item_building["properties"]["GH-A-182"]["Value"]
                        if "GH-A-121" in item_building["properties"] and item_building["properties"]["GH-A-121"][
                            "Value"]: buildtop_B = item_building["properties"]["GH-A-121"]["Value"]

                        print("楼号 | %s" % item_building["buildingNo"], end=" | ")
                        print("总建筑面积（㎡）%s" % (underarea + uparea), end=" | ")
                        print("地上建筑面积（㎡）%s" % uparea, end=" | ")
                        print("地下建筑面积（㎡）%s" % underarea, end=" | ")
                        print("层数（地上）%s" % level_F, end=" | ")
                        print("层数（地下）%s" % level_B, end=" | ")
                        print("高度（地上）%s" % buildtop_F, end=" | ")
                        print("高度（地下）%s |" % buildtop_B)
            parkarea = 0
            sumlevel = 0

            for item_building in jsondata["buildingList"]:
                if item_building["properties"]["GH-A-390"]["Value"].strip() == landname:
                    if "areaList" in item_building.keys():
                        for item_building_area in item_building["areaList"]:
                            if item_building_area["properties"]["GH-A-135"]["Value"].startswith("B") and \
                                    item_building_area["properties"]["GH-A-159"]["Value"] in ["室内机动车停车库", "室内非机动车停车库"]:
                                parkarea += Decimal(item_building_area["properties"]["GH-A-176"]["Value"]) * len(
                                    item_building_area["properties"]["GH-A-175"]["Value"].split(";"))
                                sumlevel += len(item_building_area["properties"]["GH-A-175"]["Value"].split(";"))
            if parkarea and sumlevel:
                print("\033[1;32m地下车库：\033[1m")
                print("总建筑面积（㎡）%s" % parkarea, end=" | ")
                print("地上建筑面积（㎡）-", end=" | ")
                print("地下建筑面积（㎡）%s" % parkarea, end=" | ")
                print("层数（地上）-", end=" | ")
                print("层数（地下）%s" % sumlevel, end=" | ")
                print("高度（地上）-", end=" | ")
                print("高度（地下）- |")


def MonomerFormNonResidential():
    buildtypecate = []
    for codelist in read_excel(excelname_BJ)["建筑类型"]:
        if codelist.startswith("09"): buildtypecate.append("".join(list(filter(lambda x: not x.isdigit(), codelist))))
    for item_land in jsondata["landList"]:
        landno = item_land["properties"]["GH-A-101"]["Value"]
        landname = item_land["landName"].strip("")
        if item_land["properties"]["GH-A-102"]["Value"].strip()[0] not in "R居住用地":
            print()
            print("*" * 20)
            print("\033[1;33;1m%s地块单体审查\033[1m" % landno)
            print("-" * 20, ">\033[1;33;1m非居住项目——建筑单体明细表:\033[1m<", "-" * 20)
            for item_building in jsondata["buildingList"]:
                underarea = 0
                underarea_uid = []
                uparea = 0
                uparea_uid = []
                level_B = 0
                level_B_uid = []
                level_F = 0
                level_F_uid = []
                buildtop_B = 0
                buildtop_B_uid = []
                buildtop_F = 0
                buildtop_F_uid = []
                if item_building["properties"]["GH-A-390"]["Value"].strip() == landname and not \
                        item_building["properties"]["GH-A-174"]["Value"] == "拆除":

                    # 新建地下建筑面积
                    if item_building["properties"]["GH-A-174"]["Value"] == "新建":
                        for item_building_area in item_building["areaList"]:
                            if item_building_area["properties"]["GH-A-135"]["Value"].startswith("B"):
                                # print("log->",item_building_area["properties"]["GH-A-135"]["Value"],item_building_area["properties"]["GH-A-175"]["Value"],item_building_area["properties"]["GH-A-176"]["Value"])

                                count = len(item_building_area["properties"]["GH-A-175"]["Value"].split(";"))
                                underarea += Decimal(
                                    item_building_area["properties"]["GH-A-176"]["Value"]) * count
                                underarea_uid.append(item_building_area["uid"])
                            # 新建地上建筑面积
                            elif not item_building_area["properties"]["GH-A-135"]["Value"].startswith("B"):
                                # print("log->", item_building_area["properties"]["GH-A-135"]["Value"],
                                #       item_building_area["properties"]["GH-A-175"]["Value"],
                                #       item_building_area["properties"]["GH-A-176"]["Value"])
                                count = len(item_building_area["properties"]["GH-A-175"]["Value"].split(";"))
                                uparea += Decimal(item_building_area["properties"]["GH-A-176"]["Value"]) * count
                                uparea_uid.append(item_building_area["uid"])
                    # 保留
                    if item_building["properties"]["GH-A-174"]["Value"] == "保留":
                        if "areaList" in item_building.keys(): pass
                        if not item_building["properties"]["GH-A-402"]["Value"] == "":
                            underarea += Decimal(item_building["properties"]["GH-A-402"]["Value"])
                            for item_uid in item_land["landComponentList"]:
                                if item_uid["name"] == "建筑地坪" and item_uid["properties"]["GH-A-109"] == item_building[
                                    "buildingNo"]:
                                    underarea_uid.append(item_uid["uid"])
                        if not item_building["properties"]["GH-A-401"]["Value"] == "":
                            uparea += Decimal(item_building["properties"]["GH-A-401"]["Value"])
                            for item_uid in item_land["landComponentList"]:
                                if item_uid["name"] == "建筑地坪" and item_uid["properties"]["GH-A-109"] == item_building[
                                    "buildingNo"]:
                                    underarea_uid.append(item_uid["uid"])
                    else:
                        pass
                    if "GH-A-392" in item_building["properties"] and item_building["properties"]["GH-A-392"][
                        "Value"]: level_F = item_building["properties"]["GH-A-392"]["Value"]
                    if "GH-A-112" in item_building["properties"] and item_building["properties"]["GH-A-112"][
                        "Value"]: level_B = item_building["properties"]["GH-A-112"]["Value"]
                    if "GH-A-182" in item_building["properties"] and item_building["properties"]["GH-A-182"][
                        "Value"]: buildtop_F = item_building["properties"]["GH-A-182"]["Value"]
                    if "GH-A-121" in item_building["properties"] and item_building["properties"]["GH-A-121"][
                        "Value"]: buildtop_B = item_building["properties"]["GH-A-121"]["Value"]
                    print("楼号 | %s" % item_building["buildingNo"], end=" | ")
                    print("总建筑面积（㎡）%s" % (underarea + uparea), end=" | ")
                    print("地上建筑面积（㎡）%s" % uparea, end=" | ")
                    print("地下建筑面积（㎡）%s" % underarea, end=" | ")
                    print("层数（地上）%s" % level_F, end=" | ")
                    print("层数（地下）%s" % level_B, end=" | ")
                    print("高度（地上）%s" % buildtop_F, end=" | ")
                    print("高度（地下）%s |" % buildtop_B)
                    # print("总面积UID", uparea_uid.append(underarea_uid))
                    # print("地上建筑面积UID", uparea_uid)
                    # print("地下建筑面积UID", underarea_uid)

            parkarea = 0
            sumlevel = 0

            for item_building in jsondata["buildingList"]:
                if item_building["properties"]["GH-A-390"]["Value"].strip() == landname:
                    if "areaList" in item_building.keys():
                        for item_building_area in item_building["areaList"]:
                            if item_building_area["properties"]["GH-A-135"]["Value"].startswith("B") and \
                                    item_building_area["properties"]["GH-A-159"]["Value"] in ["室内机动车停车库", "室内非机动车停车库"]:
                                # print("log->", item_building_area["properties"]["GH-A-135"]["Value"],
                                #       item_building_area["properties"]["GH-A-175"]["Value"],
                                #       item_building_area["properties"]["GH-A-176"]["Value"], item_building_area["uid"])
                                parkarea += Decimal(item_building_area["properties"]["GH-A-176"]["Value"]) * len(
                                    item_building_area["properties"]["GH-A-175"]["Value"].split(";"))
                                print("*" * 100)
                                print(json.dumps(item_building_area, indent=4, ensure_ascii=False), file=fileresult)
                                print("*" * 100)
                                sumlevel += len(item_building_area["properties"]["GH-A-175"]["Value"].split(";"))
            if parkarea and sumlevel:
                print("地下车库：")
                print("总建筑面积（㎡）%s" % parkarea, end=" | ")
                print("地上建筑面积（㎡）-", end=" | ")
                print("地下建筑面积（㎡）%s" % parkarea, end=" | ")
                print("层数（地上）-", end=" | ")
                print("层数（地下）%s" % sumlevel, end=" | ")
                print("高度（地上）-", end=" | ")
                print("高度（地下）- |\033[1m")


# # 特殊面积计算
# def Specialarea(address="BJ"):
#     # 读取规则引擎数据
#     try:
#         dbname = "cbim_rule"
#         sql = """SELECT param_value.param_value,rule_value.rule_value,rule_value.line_num FROM rule_lib
#         LEFT JOIN rule_value ON rule_value.rule_lib_id = rule_lib.id
#         LEFT JOIN rule_param ON rule_param.id = rule_value.head_id
#         LEFT JOIN param_value ON param_value.id = rule_param.param_value_id
#         WHERE rule_lib.lib_name LIKE "%特殊计算系数-""" + address + """%" AND (rule_value.head_type=0 or rule_value.head_type=1) AND param_value IS NOT NULL
#         ORDER BY rule_value.line_num ASC,rule_value.head_id ASC"""
#         conn = pymysql.connect(host="172.16.201.122", port=3306, user="root", passwd="dbpass", db=dbname)
#         print("-" * 20, "%s数据库" % dbname, "-" * 20)
#         cur = conn.cursor()
#         cur.execute(sql)
#         result = cur.fetchall()
#         cur.close()
#         conn.close()
#         rule = {}
#         for i in result:
#             rule.setdefault(i[2], []).append(i[0:2])
#         print("-" * 20, "%s数据库关闭" % dbname, "-" * 20)
#         totaldata = list(rule.values())
#     except:
#         print("数据库连接失败")
#         return None
#     finally:
#         print(">" * 100)
#     rule_list = []
#     for ruleitem in totaldata:
#         rule_dict = {}
#         for item in ruleitem:
#             if item[1] == "" and item[0] not in ("结构净高（m）", "结构层高（m）"):
#                 rule_dict[item[0]] = "ALL"
#                 continue
#             if item[0] in ("结构净高（m）", "结构层高（m）"):
#                 if item[1] == "": rule_dict[item[0]] = interval.Interval(-float("inf"), float("inf"))
#                 func = lambda x: re.findall(r"\d+\.?\d*", x)
#                 if len(func(item[1])) == 1:
#                     if item[1].find(",") > item[1].find(func(item[1])[0]) and \
#                             item[1].startswith("["):
#                         rule_dict[item[0]] = interval.Interval(Decimal(func(item[1])[0]), float("inf"),
#                                                                upper_closed=False)
#                     if item[1].find(",") > item[1].find(func(item[1])[0]) and \
#                             item[1].startswith("("):
#                         rule_dict[item[0]] = interval.Interval(Decimal(func(item[1])[0]), float("inf"),
#                                                                lower_closed=False, upper_closed=False)
#                     if item[1].find(",") < item[1].find(func(item[1])[0]) and \
#                             item[1].endswith("]"):
#                         rule_dict[item[0]] = interval.Interval(Decimal(func(item[1])[0]), -float("inf"),
#                                                                lower_closed=False)
#                     if item[1].find(",") < item[1].find(func(item[1])[0]) and \
#                             item[1].endswith(")"):
#                         rule_dict[item[0]] = interval.Interval(Decimal(func(item[1])[0]), -float("inf"),
#                                                                lower_closed=False, upper_closed=False)
#                 if len(func(item[1])) == 2:
#                     if item[1].startswith("[") and item[1].endswith("]"):
#                         rule_dict[item[0]] = interval.Interval(Decimal(func(item[1])[0]), Decimal(func(item[1])[1]),
#                                                                lower_closed=True, upper_closed=True)
#                     if item[1].startswith("(") and item[1].endswith("]"):
#                         rule_dict[item[0]] = interval.Interval(Decimal(func(item[1])[0]), Decimal(func(item[1])[1]),
#                                                                lower_closed=False, upper_closed=True)
#                     if item[1].startswith("[") and item[1].endswith(")"):
#                         rule_dict[item[0]] = interval.Interval(Decimal(func(item[1])[0]), Decimal(func(item[1])[1]),
#                                                                lower_closed=True, upper_closed=False)
#                     if item[1].startswith("(") and item[1].endswith(")"):
#                         rule_dict[item[0]] = interval.Interval(Decimal(func(item[1])[0]), Decimal(func(item[1])[1]),
#                                                                lower_closed=False, upper_closed=False)
#             else:
#                 rule_dict[item[0]] = item[1]
#         rule_list.append(rule_dict)
#         for i in rule_list: print(i)
#
#     tsxsname = "特殊计算系数-" + address
#     for item_land in jsondata["landList"]:
#         print("地块编号\033[1;32m%s\033[0m用地性质：\033[1;33m%s\033[0m" % (
#             item_land["properties"]["GH-A-101"]["Value"], item_land["properties"]["GH-A-102"]["Value"]))
#         for item_building in jsondata["buildingList"]:
#             if item_land["landName"] == item_building["landName"]:
#                 print("\033[1;32m地块建筑单体为：%s\033[0m" % item_building["buildingNo"])
#                 print("建筑类型：%s" % item_building["properties"]["GH-A-110"]["Value"])
#                 if "areaList" in item_building:
#                     for item_building_area in item_building["areaList"]:
#                         print(item_building_area["uid"])
#                         tssx = 1
#                         if ["GH-A-158", "GH-A-161", "GH-A-157", "GH-A-160", "GH-A-159", "GH-A-162", "GH-A-163"] in list(
#                                 item_building["properties"].keys()):
#                             GZ = {"建筑类型": item_building["properties"]["GH-A-110"]["Value"],
#                                   "空间与主体关系（阳台）": item_building_area["properties"]["GH-A-158"]["Value"],
#                                   "结构层高（m）": Decimal(item_building_area["properties"]["GH-A-161"]["Value"]),
#                                   "坡道位置": item_building_area["properties"]["GH-A-157"]["Value"],
#                                   "结构净高（m）": Decimal(item_building_area["properties"]["GH-A-160"]["Value"]),
#                                   "空间类型": item_building_area["properties"]["GH-A-159"]["Value"],
#                                   "顶盖": item_building_area["properties"]["GH-A-162"]["Value"],
#                                   "围护": item_building_area["properties"]["GH-A-163"]["Value"]}
#                             print(GZ)
#                             for checkitem in rule_list:
#                                 flag = True
#                                 for checkkey, checkvalue in GZ.items():
#                                     if checkkey not in ("结构净高（m）", "结构层高（m）"):
#                                         if checkitem[checkkey] == "ALL": continue
#                                     elif checkvalue in checkitem[checkkey]:
#                                         continue
#                                     else:
#                                         flag = False
#                                 if flag: tssx = checkitem[tsxsname]
#                             print(
#                                 "\033[1;34m特殊面积计算系数参数信息：\033[0m \033[1;32m | 构建名称：%s | 功能空间：%s | 图形面积：%s | 计算系数：%s |\033[0m" % (
#                                     item_building_area["properties"]["SC-TY-40"]["Value"],
#                                     item_building_area["properties"]["GH-A-125"]["Value"],
#                                     item_building_area["properties"]["GH-A-176"]["Value"], tssx))
#                         else:
#                             print(
#                                 "\033[1;34m特殊面积计算系数参数信息：\033[0m \033[1;32m | 构建名称：%s | 功能空间：%s | 图形面积：%s | 计算系数：%s |\033[0m" % (
#                                     item_building_area["properties"]["SC-TY-40"]["Value"],
#                                     item_building_area["properties"]["GH-A-125"]["Value"],
#                                     item_building_area["properties"]["GH-A-176"]["Value"], tssx))
#                 else:
#                     print("\033[1;32m地块建筑单体为：%s无面积区域\033[0m" % item_building["buildingNo"])


# 住宅空间审查
def roomlist():
    audit_room = ["卧室", "厨房", "起居室（厅）"]
    for item_land in jsondata["landList"]:
        for item_building in jsondata["buildingList"]:
            # print("\033[1;33m建筑信息：%s\033[0m" % (item_building["fileName"]))
            if item_land["landName"] == item_building["landName"]:
                if "roomList" in item_building.keys():
                    for item_building_room in item_building["roomList"]:
                        if item_building_room["properties"]["GH-A-360"]["Value"] == "卧室":
                            print("\33[1;32m卧室\033[0m", end="-")
                            print("\33[1;32m范围标高名称：%s 户型编号：%s 房间名称：%s 卧室类型：%s 使用面积：%s \033[0m" % (
                                item_building_room["properties"]["GH-A-135"]["Value"],
                                item_building_room["properties"]["GH-A-343"]["Value"],
                                item_building_room["properties"]["GH-A-360"]["Value"],
                                item_building_room["properties"]["GH-A-131"]["Value"],
                                item_building_room["properties"]["GH-A-130"]["Value"]), item_building_room["uid"])
                    for item_building_room in item_building["roomList"]:
                        if item_building_room["properties"]["GH-A-360"]["Value"] in ["起居厅", "起居室"]:
                            print("\33[1;32m起居室（厅）\033[0m", end="-")
                            print("\33[1;32m范围标高名称：%s 户型编号：%s 房间名称：%s 卧室类型：%s 使用面积：%s \033[0m" % (
                                item_building_room["properties"]["GH-A-135"]["Value"],
                                item_building_room["properties"]["GH-A-343"]["Value"],
                                item_building_room["properties"]["GH-A-360"]["Value"],
                                item_building_room["properties"]["GH-A-131"]["Value"],
                                item_building_room["properties"]["GH-A-130"]["Value"]), item_building_room["uid"])
                    for item_building_room in item_building["roomList"]:
                        if item_building_room["properties"]["GH-A-360"]["Value"] == "厨房":
                            print("\33[1;32m厨房：\033[0m", end="-")
                            print("\33[1;32m范围标高名称：%s 户型编号：%s 房间名称：%s 卧室类型：%s 使用面积：%s \033[0m" % (
                                item_building_room["properties"]["GH-A-135"]["Value"],
                                item_building_room["properties"]["GH-A-343"]["Value"],
                                item_building_room["properties"]["GH-A-360"]["Value"],
                                item_building_room["properties"]["GH-A-131"]["Value"],
                                item_building_room["properties"]["GH-A-130"]["Value"]), item_building_room["uid"])


# 规划用地指标
def PlanningLandUse(landno):
    planninng_area = 0
    youxiaograndclass = 0
    wudinggrandclass = 0
    Therate = 0
    selfparking_F = 0
    selfparking_B = 0
    mechanicalparking_F = 0
    mechanicalparking_B = 0
    for item_land in jsondata["landList"]:
        if item_land["properties"]["GH-A-101"]["Value"] == landno:
            No = item_land["properties"]["GH-A-101"]["Value"]
            Name = item_land["landName"]
            if item_land["properties"]["GH-A-104"]["Value"] == "否":
                print("*" * 100)
                print("%s地块-建设用地：" % No)
                print("\033[1;33m %s : %s\033[0m" % (
                    item_land["properties"]["GH-A-102"]["Value"], item_land["properties"]["GH-A-103"]["Value"]))

            # 绿地率计算
            for item_land_landComponentList in item_land["landComponentList"]:
                if ("GH-A-108" in item_land_landComponentList["properties"].keys() and
                        item_land_landComponentList["properties"]["GH-A-108"]["Value"] == "绿地" and
                        item_land_landComponentList["name"] == "地形/子面域" and
                        item_land_landComponentList["properties"]["GH-A-173"]["Value"] == "有效绿地"):
                    youxiaograndclass += Decimal(item_land_landComponentList["properties"]["GH-A-176"]["Value"])
                    print("有效绿地：")
                    print("\033[1;32mGH-A-108:%s  GH-A-173:%s  GH-A-176:%s\033[0m" % (
                        item_land_landComponentList["properties"]["GH-A-108"]["Value"],
                        item_land_landComponentList["properties"]["GH-A-173"]["Value"],
                        item_land_landComponentList["properties"]["GH-A-176"]["Value"]),
                          item_land_landComponentList["uid"])
            temp = 0
            for item_building in jsondata["buildingList"]:
                if Name == item_building["landName"]:
                    if "areaList" in item_building.keys():
                        for item_building_area in item_building["areaList"]:
                            if (item_building_area["properties"]["GH-A-159"]["Value"] == "屋顶" and
                                    item_building_area["properties"]["GH-A-183"]["Value"] == "是"):
                                temp += Decimal(item_building_area["properties"]["GH-A-176"]["Value"])
                                print("屋顶绿化折算：")
                                print("\033[1;32mGH-A-159:%s  GH-A-183:%s  GH-A-176:%s\033[0m" % (
                                    item_building_area["properties"]["GH-A-159"]["Value"],
                                    item_building_area["properties"]["GH-A-183"]["Value"],
                                    item_building_area["properties"]["GH-A-176"]["Value"]), item_building_area["uid"])
                        if (temp * Decimal(0.3)) <= (
                                Decimal(item_land["properties"]["GH-A-103"]["Value"]) * Decimal(0.15)):
                            wudinggrandclass = temp * Decimal(0.3) / Decimal(
                                item_land["properties"]["GH-A-103"]["Value"])
                        else:
                            wudinggrandclass = Decimal(item_land["properties"]["GH-A-387"]["Value"]) * 0.15
                    else:
                        print("\033[1;34m %s无arealist" % (item_building["fileName"]))
            print("\033[1;33m绿地率 = %s\033[0m" % (
                    youxiaograndclass / Decimal(item_land["properties"]["GH-A-103"]["Value"]) + wudinggrandclass))

            # 停车位
            if len(item_land["parkingList"]) > 0:
                for item_parking in item_land["parkingList"]:
                    if item_parking["properties"]["GH-A-138"]["Value"] == "自走式停车位":
                        selfparking_F += 1 * (
                            lambda: 1 if item_parking["properties"]["GH-A-596"]["Value"] == "" else int(
                                item_parking["properties"]["GH-A-596"]["Value"]))()
                    if item_parking["properties"]["GH-A-138"]["Value"] == "机械式停车位":
                        mechanicalparking_F += 1 * (
                            lambda: 1 if item_parking["properties"]["GH-A-596"]["Value"] == "" else int(
                                item_parking["properties"]["GH-A-596"]["Value"]))()
            for item_building in jsondata["buildingList"]:
                if Name == item_building["landName"]:
                    if "parkingList" in item_building and len(item_building["parkingList"]) != 0:
                        for item_building_parking in item_building["parkingList"]:
                            if item_building_parking["properties"]["GH-A-138"]["Value"] in ["自走式停车位"] and \
                                    item_building_parking["properties"]["GH-A-135"]["Value"].startswith("F"):
                                selfparking_F += 1 * (
                                    lambda: 1 if item_building_parking["properties"]["GH-A-596"][
                                                     "Value"] == "" else int(
                                        item_building_parking["properties"]["GH-A-596"]["Value"]))()
                            if item_building_parking["properties"]["GH-A-138"]["Value"] in ["自走式停车位"] and \
                                    item_building_parking["properties"]["GH-A-135"]["Value"].startswith("B"):
                                selfparking_B += 1 * (
                                    lambda: 1 if item_building_parking["properties"]["GH-A-596"][
                                                     "Value"] == "" else int(
                                        item_building_parking["properties"]["GH-A-596"]["Value"]))()
                            if item_building_parking["properties"]["GH-A-138"]["Value"] in ["机械式停车位"] and \
                                    item_building_parking["properties"]["GH-A-135"]["Value"].startswith("F"):
                                mechanicalparking_F += 1 * (
                                    lambda: 1 if item_building_parking["properties"]["GH-A-596"][
                                                     "Value"] == "" else int(
                                        item_building_parking["properties"]["GH-A-596"]["Value"]))()
                            if item_building_parking["properties"]["GH-A-138"]["Value"] in ["机械式停车位"] and \
                                    item_building_parking["properties"]["GH-A-135"]["Value"].startswith("B"):
                                print(item_building_parking["uid"])
                                mechanicalparking_B += 1 * (
                                    lambda: 1 if item_building_parking["properties"]["GH-A-596"][
                                                     "Value"] == "" else int(
                                        item_building_parking["properties"]["GH-A-596"]["Value"]))()
            print("\033[1;32m地上自走式停车位 : %s\033[1m" % selfparking_F)
            print("\033[1;32m地上机械式停车位 : %s\033[1m" % mechanicalparking_F)
            print("\033[1;32m地下自走式停车位 : %s\033[1m" % selfparking_B)
            print("\033[1;32m地下机械式停车位 : %s\033[1m" % mechanicalparking_B)


# 施工图
file = open("cadresult.json", "w+")


def ReadCAD():
    type = {}
    major = []
    total = 0
    for itemCAD in jsoncaddata["objects"]:
        type[itemCAD["type"]] = type.setdefault(itemCAD["type"], 0) + 1

    print("模型构建类型:")
    for i, v in type.items():
        if i != ("GraphicLinkage" or "ManualCheckResult"):
            print("构建 {0} ---> 总共{1}个 ".format(i, v), major_code[i][0] if i in major_code else None)
        if i in major_code:
            major.append(major_code[i][0])
            total = total + (lambda: 0 if major_code[i][1] == "" else int(major_code[i][1]))()

    print("检测专业:", set(major))
    print("检测审查项：", len(type) - len(
        set(type.keys()) & {"FireBuilding", "FireBuildingUnder", "FireBuildingAbove", "FireFloorFunction"}) + 1)
    print("总构件数:%d" % (sum(type.values()) - int(type["GraphicLinkage"])))


def FindUid():
    uid = {}
    for itemCAD in jsoncaddata["objects"]:
        if itemCAD["type"] is not None:
            if itemCAD["type"] in "GraphicLinkage":
                uid[itemCAD["uid"]] = itemCAD["properties"]
    return uid


def Findmanual():
    uid_manual = {}
    for itemCAD in jsoncaddata["objects"]:
        if itemCAD["type"] is not None:
            if itemCAD["type"] in "ManualCheckResult":
                uid_manual[itemCAD["uid"]] = itemCAD["propertiesset"]
    return uid_manual


def FindReadCAD(type, condictions=set(), rulelib=None, resultcode=None):
    uid = {}
    count = 0
    #联动信息提取
    for itemCAD in jsoncaddata["objects"]:
        if itemCAD["type"] is not None:
            if itemCAD["type"] in "GraphicLinkage":
                uid[itemCAD["uid"]] = itemCAD["properties"]

    for itemCAD in jsoncaddata["objects"]:
        if itemCAD["type"] == type:
            resultvalues = []
            resultdic = {}
            for item, value in itemCAD["properties"].items():
                resultvalues.append(value["Value"])
            if condictions < set(resultvalues):
                temp = itemCAD["properties"]
                if "manualCheckResult" in itemCAD.keys():
                    temp["manualCheckResult"]=jsonpath(itemCAD["manualCheckResult"],"$.*")
                resultdic.setdefault(itemCAD["uid"],temp)

                count += len(resultdic)
                for uid, properties in resultdic.items():
                    print("\033[1;34m*\033[0m" * 100)
                    print(uid)
                    for i, v in properties.items():
                        if i != "manualCheckResult":print(i, v)
                        else:
                            print("manualCheckResult")
                            for itemmanualdata in v:
                                print("\033[1;33m-\033[0m"*100)
                                for i,v in itemmanualdata.items():
                                    print(i,v)
                            print("\033[1;33m-\033[0m"*100)

                if uid in FindUid().keys():
                    for i, v in FindUid()[uid].items():
                        print("\033[1;33m图形联动信息：\033[0m")
                        print(i, v)
                else:
                        print("\033[1;33m无图形联动信息\033[0m")

    print("总构件数：%s" % count)

def is_number(s):
    if s[0]=="-" or s[0] in "0123456789":
        if s.count(".")<=1 and s.count("-")<=1:
            s=s.replace("-","").replace(".","")
            #print (s)
            for i in s:
                if i not in "0123456789":
                    return False
            else:
                return True
        else:
            return False
    else:
        return False

def check(ruledata, checkdata):
    global vaildresultkey
    vaildresult = {}
    print("规则总数%s"%len(ruledata))
    count = 0
    for ruleitems in ruledata:
        flag = True
        count =count+ 1
        for key in ruleitems:
            # 查找规则库合法参数key
            if isinstance(key, tuple):
                vaildresultkey = key

        checkkeys = list(ruleitems.keys())  # 待校验参数
        checkkeys.remove(vaildresultkey)
        for checkkey in checkkeys:
            if checkkey not in checkdata.keys():
                checkdata[checkkey] = {"Value": "未给值"}
                print("\033[1;31m缺少参数：%s\033[0m" % checkkey)

        for checkkey in checkkeys:
            if str(ruleitems[checkkey]) == "ALL":continue
            elif isinstance(checkdata[checkkey]["Value"], bool):
                if checkdata[checkkey]["Value"]  == "未给值":continue
                if checkdata[checkkey]["Value"] is False and "否" in ruleitems[checkkey]: continue
                if checkdata[checkkey]["Value"] is True and "是" in ruleitems[checkkey]:continue
                else:
                    flag = False
            elif not isinstance(checkdata[checkkey]["Value"], bool):
                if str(checkdata[checkkey]["Value"]) == "未给值":continue
                elif is_number(str(checkdata[checkkey]["Value"])):
                    if Decimal(checkdata[checkkey]["Value"]) in ruleitems[checkkey]:continue
                    else:flag = False
                if (not is_number(str(checkdata[checkkey]["Value"]))):
                    if checkdata[checkkey]["Value"] in ruleitems[checkkey]:continue
                    else:flag = False
                else:
                    flag = False
            else:flag = False
        if flag:
            print(ruleitems)
            for key in ruleitems:
                if isinstance(key, tuple): vaildresult[key]= ruleitems[key]
            break
    print("第%s次命中"%count)
    return vaildresult


# 成都经济技术指标表
def Specialarea(rulelib, resultcode):
    checkdata = RuleDispose(rulelib, resultcode).ruledata()
    landlist = jsonpath(jsondata, "$.landList[*]")
    buildinglist = jsonpath(jsondata, "$.buildingList[*]")
    areacheck = []
    coefficient = {}
    for item in buildinglist:
        temp = {}
        temp["GH-A-110"] = item["properties"]["GH-A-110"]
        item_arealist = jsonpath(item, "$.areaList[*]")
        for item_area in item_arealist:
            item_area["properties"].update(temp)
            areacheck.append(item_area)
    for item in areacheck:
        print("\033[1;36m%s\033[0m"%item["uid"])
        result = check(checkdata, item["properties"])
        if len(result) == 0:result[(rulelib, )] = "1"
        print("\033[1;33m%s\033[0m"%item["properties"]["SC-TY-40"]["Value"],end="|")
        print("\033[1;33m%s\033[0m"%result)
        coefficient[item["properties"]["SC-TY-40"]["Value"]]=list(result.values())[0]
    return coefficient


def indicatorCDM():
    coefficient = Specialarea("特殊计算系数-CD", "GH-A-577")
    landlist = jsonpath(jsondata, "$.landList[*]")
    print(landlist)
    buildinglist = jsonpath(jsondata, "$.buildingList[*]")
    print(buildinglist)
    landarea = jsonpath(jsondata,"$.landList[*].properties")
    print(landarea)
    #根据用地性质维度
    land = []
    for item_land in landlist:
        temp = {}
        fitness = 0
        utilities = 0
        basal = 0
        youxiaograndclass = 0
        outmotor_count = 0
        land_parkingarea_motor = 0
        land_parkingarea_nomotor = 0

        temp.update({"GH-A-101":item_land["properties"]["GH-A-101"]["Value"],"GH-A-102":item_land["properties"]["GH-A-102"]["Value"],"GH-A-103":item_land["properties"]["GH-A-103"]["Value"],"GH-A-387":item_land["properties"]["GH-A-387"]["Value"]})
        for item_landComponentList in item_land["landComponentList"]:
            if item_landComponentList["name"] == "地形/子面域":
                if item_landComponentList["properties"]["GH-A-108"]["Value"] == "机动车位":
                    land_parkingarea_motor += Decimal(item_landComponentList["properties"]["GH-A-176"]["Value"])
                if item_landComponentList["properties"]["GH-A-108"]["Value"] == "非机动车位":
                    land_parkingarea_nomotor += Decimal(item_landComponentList["properties"]["GH-A-176"]["Value"])
                if item_landComponentList["properties"]["GH-A-108"]["Value"] == "全民健身场所":
                    fitness += Decimal(item_landComponentList["properties"]["GH-A-176"]["Value"])
                if item_landComponentList["properties"]["GH-A-108"]["Value"] == "市政公用设施点位":
                    utilities += Decimal(item_landComponentList["properties"]["GH-A-176"]["Value"])
                basal += Decimal(item_landComponentList["properties"]["GH-A-176"]["Value"])
            if "GH-A-108" in item_landComponentList["properties"].keys() and item_landComponentList["properties"]["GH-A-108"]["Value"] == "绿地" and item_landComponentList["name"] == "地形/子面域" and item_landComponentList["properties"]["GH-A-173"]["Value"] == "有效绿地":
                youxiaograndclass += Decimal(item_landComponentList["properties"]["GH-A-176"]["Value"])

        for item_parking in item_land["parkingList"]:
            if len(item_land["parkingList"]) > 0:
                if item_parking["properties"]["GH-A-138"]["Value"] == "机械式停车位":
                        outmotor_count += 1 * (lambda: 1 if item_parking["properties"]["GH-A-596"]["Value"] == "" else int(item_parking["properties"]["GH-A-596"]["Value"]))()
        temp["地块机动车位面积"] = land_parkingarea_motor
        temp["地块非机动车位面积"] = land_parkingarea_nomotor
        temp["全民健身场所"] = fitness
        temp["市政公用设施点位"] = utilities
        temp["建筑密度"] = basal/Decimal(temp["GH-A-103"])
        temp["有效绿地面积"] = youxiaograndclass
        temp["室外机械式停车位数"] = outmotor_count


        land.append(temp)
    print("\033[1;33m%s\033[0m"%land)
    building = []
    #建筑面积
    for item_building in buildinglist:
        temp = {}
        residential_area_upper = 0
        residential_area_downner = 0
        wudinggrandclass = 0
        inmotor_count = 0
        building_parkingarea_motor = 0
        building_parkingarea_nomotor = 0
        for item_building_area in item_building["areaList"]:
            count = len(item_building_area["properties"]["GH-A-175"]["Value"].split(";"))
            if item_building_area["properties"]["GH-A-135"]["Value"].startswith("B"):
                residential_area_downner += Decimal(item_building_area["properties"]["GH-A-176"]["Value"])*Decimal(coefficient[item_building_area["properties"]["SC-TY-40"]["Value"]])*count

            elif not item_building_area["properties"]["GH-A-135"]["Value"].startswith("B"):
                residential_area_upper += Decimal(item_building_area["properties"]["GH-A-176"]["Value"])*Decimal(coefficient[item_building_area["properties"]["SC-TY-40"]["Value"]])*count

            if item_building_area["properties"]["GH-A-159"]["Value"] == "屋顶" and item_building_area["properties"]["GH-A-183"]["Value"] == "是":
                wudinggrandclass += Decimal(item_building_area["properties"]["GH-A-176"]["Value"])*Decimal(coefficient[item_building_area["properties"]["SC-TY-40"]["Value"]])

            if "GH-A-159" in item_building_area["properties"].keys() and item_building_area["properties"]["GH-A-159"]["Value"] == "室内机动车停车库":
                building_parkingarea_motor += Decimal(item_building_area["properties"]["GH-A-176"]["Value"])*Decimal(coefficient[item_building_area["properties"]["SC-TY-40"]["Value"]])
            if "GH-A-159" in item_building_area["properties"].keys() and item_building_area["properties"]["GH-A-159"]["Value"] == "室内非机动车停车库":
                building_parkingarea_nomotor += Decimal(item_building_area["properties"]["GH-A-176"]["Value"])*Decimal(coefficient[item_building_area["properties"]["SC-TY-40"]["Value"]])

        for item_building_parking in item_building["parkingList"]:
            if item_building_parking["properties"]["GH-A-138"]["Value"] == "机械停车位":
                inmotor_count += 1 * (lambda: 1 if item_parking["properties"]["GH-A-596"]["Value"] == "" else int(
                    item_parking["properties"]["GH-A-596"]["Value"]))()

        temp["buildingNo"] = item_building["buildingNo"]
        temp["landName"] = item_building["landName"]
        temp["GH-A-110"] = item_building["properties"]["GH-A-110"]["Value"]
        temp["地上建筑面积"] = residential_area_upper
        temp["地下建筑面积"] = residential_area_downner
        temp["建筑-室内机动车停车库面积"] = building_parkingarea_motor
        temp["建筑-室内非机动车停车库面积"] = building_parkingarea_nomotor
        temp["临时屋顶绿化面积"] = wudinggrandclass
        temp["室内机械式停车位数"] = inmotor_count


        building.append(temp)
    print("\033[1;33m%s\033[0m"%building)

    for item in land:
        key = item["GH-A-101"]
        temp = []
        total_motor_parkarea = item["地块机动车位面积"]
        total_nomotor_parkarea = item["地块非机动车位面积"]
        total_construction_area_upper = 0
        total_construction_area_downner = 0
        total_wudinggrandclass = 0
        total_motor_count = item["室外机械式停车位数"]
        for item_step in building:
            if item_step["landName"] == key:
                total_motor_parkarea += item_step["建筑-室内机动车停车库面积"]
                item_step.pop("建筑-室内机动车停车库面积")
                total_nomotor_parkarea += item_step["建筑-室内非机动车停车库面积"]
                item_step.pop("建筑-室内非机动车停车库面积")
                total_construction_area_upper += item_step["地上建筑面积"]
                total_construction_area_downner += item_step["地下建筑面积"]
                item_step["屋顶绿化面积"] = item_step["临时屋顶绿化面积"]*Decimal(0.3) if item_step["临时屋顶绿化面积"]*Decimal(0.3) < Decimal(item["GH-A-103"])*Decimal(0.15) else item["GH-A-387"]*Decimal(0.15)
                item_step.pop("临时屋顶绿化面积")
                total_wudinggrandclass += item_step["屋顶绿化面积"]
                total_motor_count += item_step["室内机械式停车位数"]
                item_step.pop("室内机械式停车位数")



                temp.append(item_step)

        item["总地上建筑面积"] = total_construction_area_upper
        item["总地下建筑面积"] = total_construction_area_downner
        item["容积率"] = total_construction_area_upper/Decimal(item["GH-A-103"])
        item["绿地率"] = (total_wudinggrandclass+item["有效绿地面积"])/Decimal(item["GH-A-103"])
        item.pop("有效绿地面积")
        item["机动车位面积"] = total_motor_parkarea
        item.pop("地块机动车位面积")
        item["机械停车位占总机动车停车位的比例"]= total_motor_count/math.floor(total_motor_parkarea/2)
        item["室外地面机动车停车位占总机动车停车位的比例 "] = item["室外机械式停车位数"]/math.floor(total_motor_parkarea/2)
        item["非机动车位面积"] = total_nomotor_parkarea
        item.pop("地块非机动车位面积")
        item.pop("室外机械式停车位数")
        item[key] = temp

    print("\033[1;36m%s\033[0m"%land)
    for land_item in land:
        for i,v in land_item.items():
            print("\033[1;34m{0} 《===》{1}\033[0m".format(i,v))






if __name__ == "__main__":
    pass
    # indicatorCDM()


    # pass
    # Area()
    # ResidentialServicesAudit()
    # ParkingAudit()
    # MonomerFormResidential()
    # MonomerFormNonResidential()
    # Specialarea(address="GB")
    # roomlist()
    # read_excel(excelname_BJ)
    # PlanningLandUse("5")
    # ReadCAD("FireBuildingUnder")
    # ReadCAD("FireFloorFunction")
    # ReadCAD("FunctionRoom_Base")
    # ReadCAD("FireBuildingUnder")
    # ReadCAD("FireFloorFunction")
    # ReadCAD()
    FindReadCAD("FunctionRoom_EvacuationDistance",{"网络机房"})
    # # FindReadCAD("FunctionRoom_EvacuationWidth")
    # FindReadCAD("FunctionRoom_Base",rulelib="XF-A-ZD-合法疏散门个数", resultcode="FH-A-081")
    # print(FindUid())
