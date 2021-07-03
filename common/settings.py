"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     settings.py
@Author:   shenfan
@Time:     2020/9/14 20:24
"""
import os
from common.configread import yamlReader

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#配置文件路径
CONFIG_FILE = os.path.join(BASE_DIR,"config","config.yaml")

class config:
    def __init__(self,config=CONFIG_FILE):
        self.config = yamlReader(config).data

    def get(self,element,index=0):
        return self.config[index].get(element)







