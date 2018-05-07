#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time
import math
import socket
import hashlib
Basedir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"FTPServer")
updir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SampleFolder")

sys.path.append(Basedir)

from src.common import client_show


def upload(client, user_info):
    client_show("|--Files under the current directory....", "info")
    dic = {}
    for root, dirs, files in os.walk(updir):
        for i, j in enumerate(files):
            k = i + 1
            dic[k] = j
            client_show("%s：%s" % (k, j),"info")
    choice = input("|--Input upload file number>>>:").strip()
    if choice.isdigit() and 0 < int(choice) <= len(dic):
        command = "upload+" + user_info + "+" + dic[int(choice)]
        client.sendall(bytes(command, encoding="utf-8"))
        res = client.recv(1024)
        if str(res, encoding="utf-8") == "True":
            dir = os.path.join(updir, dic[int(choice)])
            f = open(dir, "rb")
            md5 = hashlib.md5()
            length = os.stat(dir).st_size
            client.send(str(length).encode())
            sign = client.recv(1024).decode()
            if sign == "ok":
                data = f.read()
                md5.update(data)
                client.sendall(data)
                f.close()
                client.send(md5.hexdigest().encode())
                res_sign = client.recv(1024)
                if res_sign == b'True':
                    client_show("|--The file upload success....","info")
                elif res_sign == b'False':
                    client_show("\|--The file upload failure....", "error")
                    exit()
            elif sign == "no":
                client_show("|--The disk is not space....", "error")
                exit()
    else:
        client_show("|--Input Error....", "error")


def download(client, user_info):
    dic = {}
    command = "download+" + user_info
    client.sendall(bytes(command, encoding="utf-8"))
    data = client.recv(4069)
    res = eval(str(data, encoding="utf-8"))
    if len(res) == 0:
        client_show("|--There is no file in the current directory....", "info")
    else:
        for i, j in enumerate(res):
            k = i + 1
            dic[k] = j
            client_show("%s：%s" % (k, j), "info")
        choice = input("|--Input file number>>>:").strip()
        cm = dic[int(choice)]
        client.sendall(bytes(cm, encoding="utf-8"))
        client_show("|--Ready to start downloading files....","info")
        dir = os.path.join(updir, dic[int(choice)])
        res = str(client.recv(1024).decode()).split("+")
        res_length = res[0]
        or_md5 = res[1]
        length = 0
        f = open(dir, "wb")
        m = hashlib.md5()
        while length < int(res_length):
            if int(res_length) - length > 1024:
                size = 1024
            else:
                size = int(res_length) - length
            data = client.recv(size)
            length += len(data)
            m.update(data)
            f.write(data)
            progressbar(length, int(res_length))
        else:
            new_md5 = m.hexdigest()
            f.close()
        if new_md5 == or_md5:
            client_show("|--The file download success....","info")
            return True
        else:
            client_show("|--The file download failure....","error")
            return False


def switch(client, user_info):
    command = ["ls","cd"]
    client_show("%s" % command,"info")
    c = input("Input Your Command>>>:").strip()
    if c == "ls":
        view_file(client, user_info)
    elif c == "cd":
        cm = "cd+" + user_info
        client.sendall(cm.encode("utf-8"))
        dirs = eval(client.recv(1024).decode())
        if len(dirs) != 0:
            for j in dirs:
                client_show("|--dirname:%s" % j,"info")
            choice = input("|--Input directory name>>>:").strip()
            if choice in dirs:
                client.sendall(choice.encode("utf-8"))
                sign = client.recv(1024).decode()
                if sign == "True":
                    client_show("|-- %s Directory switching success...." % choice, "info")
                else:
                    client_show("|-- %s Directory switching failure...." % choice, "error")
            else:
                client_show("|--Input Error....","info")
                client.sendall("error".encode("utf-8"))
                exit()
        else:
            client_show("|--No any diretory....", "error")
    else:
        client_show("|--Input Error....", "error")
        exit()


def view_file(client, user_info):
    command = "view+" + user_info
    client.sendall(bytes(command, encoding="utf-8"))
    dirs = client.recv(1024)
    if dirs.decode() == "False":
        dir = []
    else:
        dir = eval(str(dirs,encoding="utf-8"))
    files = client.recv(1024)
    file = eval(str(files, encoding="utf-8"))
    client.sendall("true".encode("utf-8"))
    storage = str(client.recv(1024).decode())
    if len(file) == 0 and len(dir) == 0:
        client_show("|--There is no file in the current directory....","info")
    else:
        client_show("|--The current directory contains the following file content....","info")
        client_show("|--Disk size：%skb" % storage,"info")
        for j in dirs:
            client_show("|--Directory：%s" % j,"info")
        for i in file:
            client_show("|--File：%s" % i,"info")


def operate(client, user_info):
    dic = {"1": upload, "2": download, "3": view_file, "4": switch}
    info = """------Operation instruction------
    1: Uploading files
    2: Download the file
    3: View the files under the directory
    4: Switch directory operation
    5、Sign out
    """
    while True:
        client_show("%s" % info, "info")
        choice = input("|--Input Your Choice Operate>>>:").strip()
        if choice == "1":
            upload(client,user_info)
            continue
        if choice == "2":
            download(client,user_info)
            continue
        if choice == "3":
            view_file(client,user_info)
            continue
        if choice == "4":
            switch(client,user_info)
            continue
        if choice == "5":
            break
        else:
            client_show("|--Input Error....", "error")


def com_parse(client, com):
    client.sendall(bytes(com, encoding="utf-8"))
    re = client.recv(4096)
    if str(re, encoding="utf-8") == "Success":
        return True
    else:
        return False


def login(client):
    name = input("|--Input Your Username>>>:").strip()
    pswd = input("|--Input Your Password>>>:").strip()
    user_info = name + "+" + pswd
    com = "login+" + user_info
    if com_parse(client, com):
        client_show("|--Login Success....", "info")
        operate(client, user_info)
    else:
        client_show("|--Login Error....", "error")


def register(client):
    name = input("|--Input Your Username>>>:").strip()
    pswd = input("|--Input Your Password>>>:").strip()
    com = "register+" + name + "+" + pswd
    if com_parse(client, com):
        client_show("|--Register Success....","info")
        user_info = name + "+" + pswd
        operate(client, user_info)
    else:
        client_show("|--Register Error....", "error")


def quit():
    exit()


def main_func(client, data):
    dic = {"1": login, "2": register, "3": quit}
    info = """|------User Login Interface------
    1: Land
    2: Register
    3: Sign out
    """.format(data)
    while True:
        client_show("%s" % info,"info")
        choice = input("|--Input Your Choice>>>:").strip()
        if choice == "1":
            login(client)
            continue
        if choice == "2":
            register(client)
            continue
        if choice == "3":
            quit()
            continue
        else:
            client_show("|--Input Error....","error")


def progressbar(cur, total):
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write('[%-50s] %s' % ('=' * int(math.floor(cur * 50 / total)), percent))
    sys.stdout.flush()
    time.sleep(0.01)
    if cur == total:
        sys.stdout.write('\n')


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 9999
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", PORT))
    client.send("True".encode("utf-8"))
    main_func(client, "connect")
    client.close()
