"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     UI.py
@Author:   shenfan
@Time:     2022/5/26 16:15
"""

import os
import pywinauto
from pywinauto.keyboard import send_keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time
import pandas
import random


BASE_DIR = os.path.abspath("..")
DRIVER = os.path.join(os.path.dirname(BASE_DIR), "drive", "chromedriver.exe")
CSV = os.path.join(os.path.dirname(BASE_DIR), "data", "user_ent_managers（企业管理员）.csv")
DATA = os.path.join(os.path.dirname(BASE_DIR), "data", "压测模型.cim")
SCREEN_PATH = os.path.join(os.path.dirname(BASE_DIR), "data", "screen")

dataframe = pandas.read_csv(CSV)
params = dataframe.values.tolist()
username = random.choice(params)[0]
passwd = random.choice(params)[1]
print(username, passwd)


def get_screent_img(driver, value):
    '''将页面截图下来'''
    image_path = SCREEN_PATH
    screen_name = image_path + value + '.png'
    print(screen_name)
    try:
        driver.get_screenshot_as_file(screen_name)
    except NameError as ne:
        print(ne)
        get_screent_img(driver, value)


def file_uploads(filepath):
    """
    web上传文件
    :param filepath:
    """
    app = pywinauto.Application()
    app = app.connect(title_re="打开", class_name="#32770")
    app["打开"]["Edit1"].set_edit_text(filepath)
    app["打开"]["Button1"].click()


def browseroptions(browser):
    if browser == "Chrome":
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        chrome_options.add_argument('--start-maximized')  # 指定浏览器分辨率
        chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        # chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        # chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('lang=zh_CN.UTF-8')
        return chrome_options


def graphics_case(url):
    chrome_options = browseroptions("Chrome")
    driver = webdriver.Chrome(executable_path=DRIVER, options=chrome_options)
    driver.get(url)
    driver.maximize_window()

    driver.find_element_by_xpath('//input[@placeholder="手机号"]').send_keys(username)
    driver.find_element_by_xpath('//input[@placeholder="密码"]').send_keys(passwd)
    driver.find_element_by_xpath("//div/button/span").click()

    # result = WebDriverWait(driver, 30, 1).until(expected_conditions.element_to_be_clickable((By.XPATH, "//div/input")))
    # if result: result.click()
    WebDriverWait(driver, 30, 1).until(expected_conditions.visibility_of_all_elements_located(
        (By.XPATH, '//aside[contains(@class,"cbim")]/div[@class="ant-layout-sider-children"]')))
    element = driver.find_element_by_xpath('//aside[contains(@class,"cbim")]/div[@class="ant-layout-sider-children"]')
    ActionChains(driver).move_to_element(element).perform()
    driver.find_element_by_xpath('//ul/div[@eventkey="doc"]').click()
    WebDriverWait(driver, 30, 1).until(
        expected_conditions.visibility_of_all_elements_located((By.XPATH, '//li[@title="下一页"]')))
    WebDriverWait(driver, 30, 1).until(
        expected_conditions.visibility_of_all_elements_located((By.XPATH, '//span[text()="非项目文档"]')))
    driver.find_element_by_xpath('//span[text()="非项目文档"]').click()
    WebDriverWait(driver, 30, 1).until(
        expected_conditions.visibility_of_all_elements_located((By.XPATH, '//span[text()="中设数字模型性能测试项目"]')))
    driver.find_element_by_xpath('//span[text()="中设数字模型性能测试项目"]').click()
    WebDriverWait(driver, 30, 1).until(
        expected_conditions.visibility_of_all_elements_located((By.XPATH, '//span[text()="模型预览"]')))
    driver.find_element_by_xpath('//span[text()="模型预览"]').click()
    WebDriverWait(driver, 30, 1).until(
        expected_conditions.visibility_of_all_elements_located((By.XPATH, '//span[text()="新建文件夹"]')))
    driver.find_element_by_xpath('//span[text()="新建文件夹"]').click()
    folder = "模型-" + str(username)
    driver.find_element_by_xpath('//span/input[@class="ant-input" and @maxlength]').send_keys(folder)
    driver.find_element_by_xpath('//span[text()="确 定"]').click()
    WebDriverWait(driver, 30, 1).until(
        expected_conditions.visibility_of_all_elements_located((By.XPATH, '//span[text()="%s"]' % folder)))
    driver.find_element_by_xpath('//span[text()="%s"]' % folder).click()
    driver.find_element_by_xpath('//span[text()="上传文件"]').click()
    time.sleep(2)
    file_uploads(DATA)
    upstart_time = time.time()
    WebDriverWait(driver, 3000, 1).until(
        expected_conditions.visibility_of_all_elements_located((By.XPATH, '//span[contains(text(),"cim")]')))
    upend_time = time.time()
    print("上传时间：%s" % (upend_time - upstart_time))
    driver.find_element_by_xpath('//span[contains(text(),"cim")]/..').click()
    model_start = time.time()
    count = 0
    while count<10:
        get_screent_img(driver, "模型%s"%count)
        time.sleep(5)
        count = count +1


    # model_redering_end = time.time()
    #
    # print("模型渲染时间：%s" % (model_redering_end - model_start))


if __name__ == "__main__":
    # synch(clearmodels,31)
    graphics_case("https://www.cbim.org.cn/doc")
    # clearmodels("x")
    # while True:
    #     graphics_case(1)
