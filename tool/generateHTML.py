"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     generateHTML.py
@Author:   shenfan
@Time:     2020/9/16 14:13
"""
import json
import os

filename = os.path.join(os.path.dirname(os.path.abspath(".")),r"file\tables-result.json")
with open(filename,"r",encoding="utf-8") as data:
    jsondata = json.load(data).get("result")


HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<div>
%s
</div>
</body>
</html>
"""


values = []
for i in range(len(jsondata)):
    print(jsondata[i].get("parameter").get("name"))
    mark = r"<span>%s</span>%s"%(jsondata[i].get("parameter").get("name"),jsondata[i].get("parameter").get("valueSource"))
    values.append(mark)

html_file_path = os.path.join(os.path.dirname(os.path.abspath(".")),"file","template","doc_table.html")
with open(html_file_path,"w",encoding="utf-8") as data:
    data.write((HTML_TEMPLATE % ("".join(values))))






