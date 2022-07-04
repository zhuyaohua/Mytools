"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     web_time.py
@Author:   shenfan
@Time:     2022/5/11 15:56
"""
from selenium import webdriver
import os
import json

BASE_DIR = os.path.abspath("..")
DRIVE_DIR = os.path.join(BASE_DIR, "drive", "chromedriver.exe")
COOKIE_DIR = os.path.join(BASE_DIR, "drive", "cookie.json")


def set_up():
    driver = webdriver.Chrome(executable_path=DRIVE_DIR)
    driver.get("https://www.cbim.org.cn")
    r = driver.find_elements_by_xpath("//div/input")
    r[0].send_keys("18571023517")
    r[1].send_keys("s123456")
    driver.find_element_by_xpath("//div/button/span").click()
    try:
        driver.implicitly_wait(1)
        driver.find_element_by_xpath("//span[text()='继续登录']").click()
    except Exception as e:
        print(e)
        pass
    # cookies = driver.get_cookies()
    # with open(COOKIE_DIR, "w") as file:
    #     file.write(json.dumps(cookies[0]))
    return driver

# set_up()

def webindicators(url):
    driver = set_up()
    driver.execute_script("window.open('%s','_blank');"%url)
    print(driver.window_handles)
    print(driver.window_handles[-1])
    driver.get(url)
    driver.refresh()

    result = {}
    # 浏览器处理当前网页的启动时间
    result["navigationStart"] = driver.execute_script("return performance.timing.navigationStart")
    # 重定向开始-结束时间
    result["redirectStart"] = driver.execute_script("return performance.timing.redirectStart")
    result["redirectEnd"] = driver.execute_script("return performance.timing.redirectEnd")
    # 浏览器发起资源请求时间，如果有缓存，则为取缓存的开始时间
    result["fetchStart"] = driver.execute_script("return performance.timing.fetchStart")
    result["fetchEnd"] = driver.execute_script("return performance.timing.fetchEnd")
    # 查询DNS的开始-结束时间
    result["domainLookupStart"] = driver.execute_script("return performance.timing.domainLookupStart")
    result["domainLookupEnd"] = driver.execute_script("return performance.timing.domainLookupEnd")
    # 浏览器建立TCP请求的开始-完成时间
    result["connectStart"] = driver.execute_script("return performance.timing.connectStart")
    result["connenctEnd"] = driver.execute_script("return performance.timing.connenctEnd")
    # 发起请求的时间-浏览器接收完毕时间
    result["requestStart"] = driver.execute_script("return performance.timing.requestStart")
    result["responseEnd"] = driver.execute_script("return performance.timing.responseEnd")
    # 浏览器开始解析网页DOM结构的开始-加载内嵌资源完成
    result["domLoading"] = driver.execute_script("return performance.timing.domLoading")
    result["domComplete"] = driver.execute_script("return performance.timing.domComplete")

    # 网页load事件的回调函数开始执行的开始-结束时间
    result["loadEventStart"] = driver.execute_script("return performance.timing.loadEventStart")
    result["loadEventEnd"] = driver.execute_script("return performance.timing.loadEventEnd ")


    return result

if __name__ == "__main__":
    webindicators("https://test2.cbim.org.cn/home")
