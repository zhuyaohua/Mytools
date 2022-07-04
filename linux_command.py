"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     linux_command.py
@Author:   shenfan
@Time:     2022/6/17 11:12
"""
from time import *
import paramiko
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas
import jsonpath
import os


class Linux(object):
    # 通过IP, 用户名，密码，超时时间初始化一个远程Linux主机
    def __init__(self, ip, username, password, timeout=1):
        self.ip = ip
        self.username = username
        self.password = password
        self.timeout = timeout
        self.t = ''
        self.chan = ''
        # 链接失败的重试次数
        self.try_times = 1

    # 调用该方法连接远程主机
    def connect(self):
        while True:
            # 连接过程中可能会抛出异常，比如网络不通、链接超时
            try:
                self.t = paramiko.Transport(sock=(self.ip, 22))
                self.t.connect(username=self.username, password=self.password)
                self.chan = self.t.open_session()
                self.chan.settimeout(self.timeout)
                self.chan.get_pty()
                self.chan.invoke_shell()
                # 如果没有抛出异常说明连接成功，直接返回
                print('连接%s成功' % self.ip)
                # 接收到的网络数据解码为str
                print(self.chan.recv(65535).decode('gbk'))
                return
            # 这里不对可能的异常如socket.error, socket.timeout细化，直接一网打尽
            except Exception as e1:
                if self.try_times != 0:
                    print('连接%s失败，进行重试' % self.ip)
                    self.try_times -= 1
                else:
                    print('重试3次失败，结束程序')
                    exit(1)

    # 断开连接
    def close(self):
        self.chan.close()
        self.t.close()

    # 发送要执行的命令
    def send(self, cmd):
        cmd += '\r'
        result = ''
        # 发送要执行的命令
        self.chan.send(cmd)

    def recall(self, data: list):
        # 回显很长的命令可能执行较久，通过循环分批次取回回显,执行成功返回true,失败返回false
        while True:
            try:

                temp = {}
                response = requests.post(url="https://staging.cbim.org.cn/api/bms/druid/datasource.json",
                                         verify=False).json()
                tempdata = jsonpath.jsonpath(response, "$.Content..[?(@.Name=='BmsDateSource')]")

                temp["采样时间"] = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
                temp["最大连接数"] = tempdata[0]["MaxActive"]
                temp["活跃连接数"] = tempdata[0]["ActiveCount"]
                temp["空闲连接数"] = tempdata[0]["MinIdle"]
                temp["活跃连接数峰值"] = tempdata[0]["ActivePeak"]
                temp["等待线程数量"] = tempdata[0]["WaitThreadCount"]
                data.append(temp)
                sleep(10)
                ret = self.chan.recv(65535)
            except Exception as e:
                print(e)
                continue
            finally:
                if "end of run" in str(ret):
                    return data
                print(str(ret))

    def upload_file(self, localpath, remotepath):
        try:
            tran = paramiko.Transport(sock=(self.ip, self.port))
            tran.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(tran)
            result = sftp.put(localpath, remotepath)
            return True if result else False
        except Exception as ex:
            print(ex)
            tran.close()
        finally:
            tran.close()

    def download_file(self, localpath, remotepath):
        try:
            tran = paramiko.Transport(sock=(self.ip, self.port))
            tran.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(tran)
            result = sftp.get(localpath, remotepath)
            return True if result else False
        except Exception as ex:
            print(ex)
            tran.close()
        finally:
            tran.close()


def samper(steptime: int, totaltime: int):
    data = []
    t1 = time()
    while True:
        try:

            temp = {}
            response = requests.post(url="https://staging.cbim.org.cn/api/bms/druid/datasource.json",
                                     verify=False).json()
            tempdata = jsonpath.jsonpath(response, "$.Content..[?(@.Name=='BmsDateSource')]")

            temp["采样时间"] = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
            temp["最大连接数"] = tempdata[0]["MaxActive"]
            temp["活跃连接数"] = tempdata[0]["ActiveCount"]
            temp["空闲连接数"] = tempdata[0]["MinIdle"]
            temp["活跃连接数峰值"] = tempdata[0]["ActivePeak"]
            temp["等待线程数量"] = tempdata[0]["WaitThreadCount"]
            data.append(temp)
            sleep(steptime)
        except Exception as e:
            print(e)
            continue
        finally:
            t2 = time()
            if (t2 - t1) > totaltime:
                return data


if __name__ == '__main__':
    requests.post(url="https://staging.cbim.org.cn/api/bms/druid/reset-all.json", verify=False)
    basepath = os.path.abspath(".")
    filepath = os.path.join(basepath, "basedatainfo-%s.xls" % strftime("%Y-%m-%d %H%M%S", localtime(time())))
    print(basepath)
    host = Linux('172.16.211.77', 'root', 'Cbim@2021')
    host.connect()
    host.send("sh /root/jmeter/ReprotJmter/apache-jmeter-5.2.1/apache-jmeter-5.2.1/bin/Start-CT.sh BMS-CT.jmx 30 0 10 1800 120")
    data = host.recall(data=[])
    # data = samper(30, 60000)
    if data:
       dataframe = pandas.DataFrame(data, index=None)
       dataframe.to_excel(filepath, index=False)
       print(dataframe)

