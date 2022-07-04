"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     area.py
@Author:   shenfan
@Time:     2022/4/29 11:04
"""
import requests
from bs4 import BeautifulSoup
import json
import time
import urllib3
import jsonpath
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
从国家统计局爬取省市区数据
"""
#创建对应项目
xboat_url_form = "https://prod-gw.cbim.org.cn/cbim-project-approval/proApproval/getFormModel"
xboat_region = "https://prod-gw.cbim.org.cn/cbim-project-approval/form/presetOption"
xboat_url = "https://prod-gw.cbim.org.cn/cbim-project-approval/proApproval/save"
xboat_head = {"accountid": "804371238595203073", "session": "s%3A07Dc-ntrWq7X20wjmsi6_AC06AdgMWm8.%2BUeK4CGJ4Jav0pBC1xQQFgPsxEEdQGHf44Tn%2BmXVphg", "entid": "804371238595203072", "content-type": "application/json"}
formdata = requests.get(url=xboat_url_form, headers=xboat_head).json()
regeiondata = requests.post(url=xboat_region,headers=xboat_head,data=json.dumps({"id": "constructionArea"}),verify=False).json()
regeiondata_province = jsonpath.jsonpath(regeiondata, "$.data.list.*.label")
regeiondata_city = jsonpath.jsonpath(regeiondata, "$.data.list.*.children.*.label")
regeiondata_county = jsonpath.jsonpath(regeiondata, "$.data.list.*.children.*.children.*.label")


def get_response(url, attr):
    try:
        response = requests.get(url)
        response.encoding = 'gb2312'  # 编码转换
        soup = BeautifulSoup(response.text, features="html.parser")
        table = soup.find_all('tbody')[1].tbody.tbody.table
        if attr:
            trs = table.find_all('tr', attrs={'class': attr})
        else:
            trs = table.find_all('tr')
        return trs

    except:
        print(url)

t = random.randint(0,2)
print(t)
def area_info(year=2019):
    count = 0
    base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/%s/' % year
    trs = get_response(base_url, 'provincetr')
    for tr in trs:  # 循环每一行
        for td in tr:  # 循环每个省
            if td.a is None:
                continue
            href_url = td.a.get('href')
            province_name = td.a.get_text()
            province_code = str(href_url.split(".")[0]) + "0000000000"
            province_url = base_url + href_url

            trs = get_response(province_url, None)
            for tr in trs[1:]:  # 循环每个市
                city_code = tr.find_all('td')[0].string
                city_name = tr.find_all('td')[1].string
                city_url = base_url + tr.find_all('td')[1].a.get('href')
                trs = get_response(city_url, None)
                for tr in trs[1:]:  # 循环每个区县
                    county_code = tr.find_all('td')[0].string
                    county_name = tr.find_all('td')[1].string

                    if province_name not in ["北京市", "上海市", "重庆市", "天津市", "香港市", "澳门市"]:
                        if not (province_name[:-1] in regeiondata_province and city_name in regeiondata_city and county_name in regeiondata_county):
                            print("八仙系统行政地区缺失：\033[1;32m %s-%s-%s \033[0m"%(province_name[:-1], city_name, county_name))
                            count += 1
                    else:
                        if not (county_name in regeiondata_city):
                            print("八仙系统行政地区缺失：\033[1;32m %s-%s \033[0m"%(province_name[:-1], county_name))
                            count += 1
                time.sleep(2)
            time.sleep(2)
    print("缺失地区：%d" % count)



area_info()

print(formdata["formDefine"])




