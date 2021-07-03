"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     update_rule.py
@Author:   shenfan
@Time:     2021/6/8 13:43
"""
from tool.SQL import query
import os

major_file = os.path.join(os.path.dirname(os.path.abspath(".")), "file", "major_code")

cmd = """
SELECT cbim_rule.param_value.param_value,cbim_rule.rule_value.rule_value,cbim_rule.rule_value.line_num FROM cbim_rule.rule_value 
LEFT JOIN cbim_rule.rule_param ON cbim_rule.rule_param.id = cbim_rule.rule_value.head_id
LEFT JOIN cbim_rule.param_value ON cbim_rule.param_value.id = cbim_rule.rule_param.param_value_id
WHERE cbim_rule.rule_value.rule_lib_id in (SELECT id FROM cbim_rule.rule_lib WHERE lib_code in ("GH-DH","ZNSC","SZGC-DH","ZYTZ","JSGL-DH-1","JGSC-DH") AND lib_status =0) ORDER BY line_num
"""

rawsult = query("rule",cmd)
type_code = {}




