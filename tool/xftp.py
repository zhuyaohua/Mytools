"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     xftp.py
@Author:   shenfan
@Time:     2021/3/4 15:02
"""
import paramiko


def remote_scp(host_ip, remote_path, local_path, username, password):
    t = paramiko.Transport((host_ip, 22))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    src = remote_path
    des = local_path
    sftp.get(src, des)
    t.close()


if __name__ == '__main__':
    host_ip = "172.16.201.92"
    remote_path = "/extradir/files"
    local_path = r"C:\Users\SHENFAN\Desktop\中设数字\xftp"
    username = "root"
    password = "CBIM2020"
    remote_scp(host_ip, remote_path, local_path, username, password)




