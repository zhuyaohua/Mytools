"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     client.py
@Author:   shenfan
@Time:     2020/9/12 21:47
"""
# from wsgiref.simple_server import make_server
# import os
#
# def func1(req):
#     return [open(r"D:\Doctool\python\工具脚本\file\show_time.html","rb").read()]
# def func2(req):
#     return [b'<h1>upper</h1>']
# def func3(req):
#     return [b'<h1>404</h1>']
# def login(req):
#     return open(r"D:\Doctool\python\工具脚本\file\login.html","rb").read()
#
# def router():
#     url_patterns = [
#         ("/steel",func1),
#         ("/STEEL",func2),
#         ("/login",login),
#     ]
#     return url_patterns
#
# def application(environ,start_reponse):
#     #用来生产响应头
#     start_reponse("200 OK ",[('Content-Type','text/html')])
#     path=environ["PATH_INFO"]
#     # if path == "/steel":
#     #     return func1()
#     # elif path == "/STEEL":
#     #     return func2()
#     # else:
#     #     return func3()
#     func = None
#     for item in router():
#         if item[0] == path:
#             func = item[1]
#             break
#     return func(environ)
#
#
#
#
#
#
#
#
#
# httpd = make_server("127.0.0.1",8080,application)
# print("Serving HTTP on port 8080...")
# httpd.serve_forever()





