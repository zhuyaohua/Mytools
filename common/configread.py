"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     configread.py
@Author:   shenfan
@Time:     2020/9/10 9:29
"""
import yaml
import os
from xlrd import open_workbook

class yamlReader:
    def __init__(self,yamlfile):
        if os.path.exists(yamlfile):
            self.yamlfile = yamlfile
        else:
            raise FileNotFoundError("文件不存在！")
        self.__data = None

    @property
    def data(self):
        if not self.__data:
            with open(self.yamlfile,"r",encoding="utf-8") as file:
                self.__data = list(yaml.safe_load_all(file))
        return self.__data

class SheetTypeError(Exception):
    pass

class ExcelReader:
    def __init__(self, excel, sheet=0, title_line=True):
        if os.path.exists(excel):
            self.excel = excel
        else:
            raise FileNotFoundError('文件不存在！')
        self.sheet = sheet
        self.title_line = title_line
        self._data = list()

    @property
    def data(self):
        if not self._data:
            workbook = open_workbook(self.excel)
            if type(self.sheet) not in [int, str]:
                raise SheetTypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
            elif type(self.sheet) == int:
                s = workbook.sheet_by_index(self.sheet)
            else:
                s = workbook.sheet_by_name(self.sheet)

            if self.title_line:
                title = s.row_values(0)
                for col in range(1, s.nrows):
                    self._data.append(dict(zip(title, s.row_values(col))))
            else:
                for col in range(0, s.nrows):
                    self._data.append(s.row_values(col))
        return self._data















