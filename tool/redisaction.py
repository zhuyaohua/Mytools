"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     redisaction.py
@Author:   shenfan
@Time:     2020/9/28 13:48
"""
import redis
import os
basedir = os.path.dirname(os.path.abspath("__file__"))
import json
from interfaces.postman import postman
from elasticsearch import Elasticsearch
from jsonpath import jsonpath


es = Elasticsearch([{"host":"172.16.201.71","port":9200}])



pool = {
    "drawapp":redis.ConnectionPool(host="172.16.201.57",port=6379,db="0",password="1q2w@3e4r"),
    "doctool_test":redis.ConnectionPool(host="172.16.201.71",port=6379,db="0",password="123123"),
    "delivery_pro":redis.ConnectionPool(host="172.16.201.185",port=6379,db="0",password="1q2w@3e4r"),
    "delivery_dev":redis.ConnectionPool(host="172.16.201.92",port=6379,db="0",password="1q2w@3e4r"),
    "doctool_dev":redis.ConnectionPool(host="172.16.201.122",port=6379,db="0",password="cbim2020")
}

def redisfunction(type):
    re = redis.StrictRedis(connection_pool=pool[type])
    if type == "drawapp":
        p = postman("https://cctc-oms.cbim.org.cn", "yingwang@cadg.cn", "123456", "cadg")
        p.interface("http://cbimcda.cbim.org.cn", "/api/schedule/v1/dev/clean", "get")
        #清理所有图像缓存
        for item in re.keys():
            if str(item,encoding="utf-8").startswith("v-"):
                print(item)
                print(re.hgetall(item))
                for key,value in re.hgetall(item).items():
                    print(key,str(value,encoding="utf-8"))
                re.delete(item)
    if type == "delivery_dev":
        print("---> Redis <---")
        function = int(input("执行操作：0、查询 ，1、删除:"))
        moduleid = input("模型id:")
        if function:
            for item in re.keys():
                if moduleid in str(item,encoding="utf-8"):
                    re.delete(item)
        else:
            for item in re.keys():
                if moduleid in str(item,encoding="utf-8"):
                    with open(os.path.join(basedir,"resultfile",str(item,encoding="utf-8")+".json"),"w",encoding="utf-8") as data:
                        data.write(str(re[item],encoding="utf-8"))
    if type == "doctool_dev":
        print("---> Redis <---")
        for item in re.keys():
            if "cbim_rule:standard:" in str(item,encoding="utf-8"):
                rawdata = json.loads(str(re[item],encoding="utf-8"))
                stand = jsonpath(rawdata,"$[1]..*[?(@.name)].name")
                for item in stand:
                    print(item)
                    # with open(os.path.join(basedir,"resultfile",str(item,encoding="utf-8")+".json"),"w",encoding="utf-8") as data:
                    #     data.write(str(re[item],encoding="utf-8"))

def esfunction():
    print("---> ES数据库 <---")
    function = int(input("执行操作：0、查询 ，1、删除: "))
    modelid = input("模型id:")
    if function:
        body_checkdata = {
            "query":{'term': {"modelId":modelid}},
        }
        body_matchdata = {
            "query": { "match_all": {} }
        }
        es.delete_by_query(index='no_match_data_dev',body=body_matchdata)
        es.delete_by_query(index='audit_page_dev',body=body_checkdata)
    else:
        body_checkdata = {
            "query":{'term': {"modelId":modelid}},
            "size": 10000
        }
        body_matchdata = {
                "query": { "match_all": {}},
                "size": 10000
            }
        result1 = es.search(index='no_match_data_dev',body=body_matchdata)  # index：选择数据库
        result2 = es.search(index='audit_page_dev',body=body_checkdata)  # index：选择数据库
        with open(os.path.join(basedir,"resultfile","Es_no_match_data.json"),"w") as resultdata1:
            resultdata1.write(json.dumps(result1,indent=4, ensure_ascii=False))
        with open(os.path.join(basedir,"resultfile",modelid+"Es_result_audit.json"),"w") as resultdata2:
            resultdata2.write(json.dumps(result2,indent=4, ensure_ascii=False))


if __name__ == "__main__":
    esfunction()
    # redisfunction("doctool_dev")





