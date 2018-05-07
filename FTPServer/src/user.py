#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import pickle
import random
import hashlib


Base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(Base_dir)
from conf import settings
from src.common import server_show
from src.common import progressbar


class User(object):
    def __init__(self, username, psd):
        self.name = username
        self.password = psd
        self.home_path = settings.user_home + "/" + self.name

    def login(self):
        user_dic = User.info_read(self.name)
        print(user_dic,)
        if user_dic.get(self.name) == self.password:
            server_show("login success....", "info")
            user_dic["dir"] = self.home_path
            User.info_write(self.name, user_dic)
            return True
        else:
            server_show("login error....", "error")
            return False

    def register(self):
        dic = {}
        dic[self.name] = self.password
        dic["storage"] = random.randint(10240, 20480)
        dic["dir"] = self.home_path
        if User.info_write(self.name, dic):
            server_show("register success....", "info")
            os.mkdir(self.home_path)
            os.mkdir("%s/others" % self.home_path)
            with open("%s\ofile" % self.home_path, "w") as f:
                f.write("ofile")
            return True
        else:
            server_show("register fail....", "error")
            return False

    def view_file(self):
        if not os.path.exists(self.home_path):
            os.mkdir(self.home_path)
            os.mkdir("%s/others" % self.home_path)
            with open("%s\ofile" % self.home_path, "w") as f:
                f.write("ofile")
        user_dic = User.info_read(self.name)
        if user_dic["dir"] == os.path.join(os.path.join(Base_dir, "home"), self.name):
            dir = os.path.join(os.path.join(Base_dir, "home"), self.name)
        else:
            dir = user_dic["dir"]
        for root, dirs, files in os.walk(dir):
            return dirs, files

    def cd_command(self, con):
        for root, dirs, files in os.walk(self.home_path):
            return dirs

    def cd_dir(self, con, dir, name):
        next_dir = self.home_path + "/" + dir
        user_dic = User.info_read(name)
        user_dic["dir"] = next_dir
        User.info_write(name, user_dic)
        return True

    def mkdir(self, con, res_dir):
        user_dic = User.info_read(self.name)
        if user_dic["dir"] == os.path.join(os.path.join(Base_dir, "home"), self.name):
            dir = os.path.join(os.path.join(Base_dir, "home"), self.name)
        else:
            dir = user_dic["dir"]
        next_dir = dir + "/" + res_dir
        if os.path.exists(next_dir):
            server_show("The directory has already existed.....", "error")
        else:
            os.mkdir(next_dir)
            server_show("Directory create success....", "info")
            return True

    @staticmethod
    def download_file(filename, name, con):
        user_dic = User.info_read(name)
        if user_dic["dir"] == os.path.join(os.path.join(Base_dir, "home"), name):
            user_dir = os.path.join(os.path.join(Base_dir, "home"), name)
        else:
            user_dir = user_dic["dir"]
        dir = os.path.join(user_dir, filename)
        f = open(dir, "rb")
        m = hashlib.md5()
        data = f.read()
        m.update(data)
        a = str(len(data)) + "+" + m.hexdigest()
        con.sendall(bytes(a, encoding="utf-8"))
        con.sendall(data)
        f.close()
        return True

    @staticmethod
    def receive(filename, name, res, con):
        user_dic = User.info_read(name)
        if user_dic["dir"] == os.path.join(os.path.join(Base_dir, "home"), name):
            dir = os.path.join(os.path.join(os.path.join(Base_dir, "home"), name), filename)
        else:
            dir_name = user_dic["dir"]
            dir = os.path.join(dir_name, filename)
        if res / 1024 < user_dic["storage"]:
            con.sendall("ok".encode("utf-8"))
            length = 0
            f = open(dir, "wb")
            md5 = hashlib.md5()
            while length < res:
                if res - length > 1024:
                    size = 1024
                else:
                    size = res - length
                data = con.recv(size)
                length += len(data)
                md5.update(data)
                f.write(data)
                progressbar(length, res)
            else:
                new_md5 = md5.hexdigest()
                f.close()
            or_md5 = con.recv(1024)
            if new_md5 == or_md5.decode():
                server_show("The file download success....", "info")
                return True
            else:
                server_show("Inconsistency of documents", "error")
                return False
        elif res / 1024 > user_dic["storage"]:
            con.sendall("no".encode("utf-8"))
            server_show("Lack of disk space", "error")
            return False

    @staticmethod
    def info_read(name):
        user_dir = os.path.join(settings.user_info, name)
        if os.path.exists(user_dir):
            with open(user_dir, "rb") as f:
                dic = pickle.load(f)
                return dic
        else:
            print("The user data is empty....")

    @staticmethod
    def info_write(name, dic):
        user_dir = os.path.join(settings.user_info, name)
        with open(user_dir, "wb") as f:
            pickle.dump(dic, f)
            return True