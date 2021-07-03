"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     compare_rule.py
@Author:   shenfan
@Time:     2021/5/25 9:53
"""
import pymysql
import interval
import re
from decimal import Decimal

pool = {
    "rule":pymysql.connect(host="172.16.201.122", port=3306, user="root", passwd="dbpass", db="cbim_rule")
}

class RuleDispose:
    def __init__(self, rulelib, resultcode):
        self.totaldata = None
        self.rulelib = rulelib
        self.resultcode = resultcode
        dbname = "cbim_rule"
        conn = pymysql.connect(host="172.16.201.122", port=3306, user="root", passwd="dbpass", db=dbname)
    # 读取规则引擎数据
        try:

            sql = """SELECT param_value.param_value as param_code,temp.param_value,case temp.rule_value WHEN "" THEN "ALL" ELSE temp.rule_value END AS rule_value,temp.line_num FROM
(SELECT param_value.param_value,rule_value.rule_value,rule_value.line_num,param_value.line_num as param_line_num FROM rule_lib
LEFT JOIN rule_value ON rule_value.rule_lib_id = rule_lib.id
LEFT JOIN rule_param ON rule_param.id = rule_value.head_id
LEFT JOIN param_value ON param_value.id = rule_param.param_value_id
WHERE rule_lib.lib_name = "%s" AND (rule_value.head_type=0 or rule_value.head_type=1) AND param_value IS NOT NULL
ORDER BY rule_value.line_num ASC,rule_value.head_id ASC) temp
LEFT JOIN param_value ON param_value.line_num = temp.param_line_num
WHERE param_value.param_head = '参数编号'"""%self.rulelib
            print("-" * 50, "%s数据库" % dbname, "-" * 50)
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            cur.close()
            conn.close()
            rule = {}
            for i in result:
                rule.setdefault(i[3],[]).append(i[0:3])
            print("执行SQL：",sql)
            print("-" * 50, "%s数据库关闭" % dbname, "-" * 50)
            self.totaldata = list(rule.values())
        except Exception as e:
            print(e)
            print("数据库连接失败")
        finally:
            print("执行数据库完成")
            print("")

    def ruledata(self):
        rule_list = []
        for ruleitem in self.totaldata:
            rule_dict = {}
            func = lambda x: re.findall(r"\d+\.?\d*", x)
            for item in ruleitem:
                # print(item)
                if item[0] == self.resultcode:rule_dict[(item[0],item[1])]=item[2]
                else:
                    if (item[2].startswith("(") or item[2].startswith("[")) and (item[2].endswith(")") or item[2].endswith("]")):
                        if len(func(item[2])) == 1:
                            if item[2].find(",") > item[2].find(func(item[2])[0]) and \
                                    item[2].startswith("["):
                                rule_dict[item[0]] = interval.Interval(Decimal(func(item[2])[0]), float("inf"), upper_closed=False)
                            if item[2].find(",") > item[2].find(func(item[2])[0]) and \
                                    item[2].startswith("("):
                                rule_dict[item[0]] = interval.Interval(Decimal(func(item[2])[0]), float("inf"), lower_closed=False,upper_closed=False)
                            if item[2].find(",") < item[2].find(func(item[2])[0]) and \
                                    item[2].endswith("]"):
                                rule_dict[item[0]] = interval.Interval(Decimal(func(item[2])[0]), -float("inf"), lower_closed=False)
                            if item[2].find(",") < item[2].find(func(item[2])[0]) and \
                                    item[2].endswith(")"):
                                rule_dict[item[0]] = interval.Interval(Decimal(func(item[2])[0]), -float("inf"), lower_closed=False,upper_closed=False)
                            if item[2].find(",")<0:
                                rule_dict[item[0]] = interval.Interval(Decimal(func(item[2])[0]), Decimal(func(item[2])[0]))
                        if len(func(item[2])) == 2:
                            if item[2].startswith("[") and item[2].endswith("]"):
                                rule_dict[item[0]] = interval.Interval(Decimal(func(item[2])[0]), Decimal(func(item[2])[1]),lower_closed=True, upper_closed=True)
                            if item[2].startswith("(") and item[2].endswith("]"):
                                rule_dict[item[0]] = interval.Interval(Decimal(func(item[2])[0]), Decimal(func(item[2])[1]),lower_closed=False, upper_closed=True)
                            if item[2].startswith("[") and item[2].endswith(")"):
                                rule_dict[item[0]] = interval.Interval(Decimal(func(item[2])[0]), Decimal(func(item[2])[1]),lower_closed=True, upper_closed=False)
                            if item[2].startswith("(") and item[2].endswith(")"):
                                rule_dict[item[0]] = interval.Interval(Decimal(func(item[2])[0]), Decimal(func(item[2])[1]),lower_closed=False, upper_closed=False)
                        if len(func(item[2])) == 0:
                            rule_dict[item[0]] = interval.Interval(-float("inf"), float("inf"), upper_closed=False,lower_closed=False)

                    else:rule_dict[item[0]]=item[2]
            rule_list.append(rule_dict)
        return rule_list

    def rawdata(self):
        return self.totaldata




def mappingrule(rulelib):
    # 读取规则引擎数据
    try:
        dbname = "cbim_rule"
        sql = """SELECT param_value.param_value as param_code,temp.param_value,temp.rule_value,temp.line_num FROM
(SELECT param_value.param_value,rule_value.rule_value,rule_value.line_num,param_value.line_num as param_line_num FROM rule_lib
LEFT JOIN rule_value ON rule_value.rule_lib_id = rule_lib.id
LEFT JOIN rule_param ON rule_param.id = rule_value.head_id
LEFT JOIN param_value ON param_value.id = rule_param.param_value_id
WHERE rule_lib.lib_name LIKE "%""" + rulelib + """%" ORDER BY rule_value.line_num ASC,rule_value.head_id ASC) temp
LEFT JOIN param_value ON param_value.line_num = temp.param_line_num
WHERE param_value.param_head = '参数编号'"""
        conn = pymysql.connect(host="172.16.201.122", port=3306, user="root", passwd="dbpass", db=dbname)
        print("-" * 20, "%s数据库" % dbname, "-" * 20)
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
        rule = {}
        for i in result:
            rule.setdefault(i[2],[]).append(i[0:2])
        print("-" * 20, "%s数据库关闭" % dbname, "-" * 20)
        totaldata = list(rule.values())
    except:
        print("数据库连接失败")
        return None
    finally:
        print(">" * 100)
    return rule


if __name__ == "__main__":
    print(RuleDispose("特殊计算系数-CD", "GH-A-577").ruledata())







