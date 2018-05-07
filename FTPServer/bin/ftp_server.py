#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import socketserver

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print(BASE_DIR)
from conf import settings
from src.common import server_show
from src.user import User


class FTPserver(socketserver.BaseRequestHandler):
    def handle(self):
        if self.request.recv(1024) == b'True':
            server_show("Receives the {0} connection request, is communicating....".format(self.client_address), "info")
            # try:
            while True:
                self.cmd = self.request.recv(4069)
                if not self.cmd:
                    break
                elif self.cmd == b'':
                    break
                else:
                    data = str(self.cmd.decode(encoding="utf-8"))
                    res = data.split("+")
                    if hasattr(self, res[0]):
                        func = getattr(self, res[0])
                        func(res)
                    else:
                        server_show("wrong action", "error")

    def login(self, res):
        server_show("Receiving client login request is landing....", "msg")
        name = res[1]
        psd = res[2]
        user = User(name, psd)
        sign = user.login()
        if sign:
            self.request.sendall(bytes("Success", encoding="utf-8"))
        else:
            self.request.sendall(bytes("Failure", encoding="utf-8"))

    def register(self, res):
        server_show("Receiving client registration request is being registered....", "msg")
        name = res[1]
        psd = res[2]
        user = User(name, psd)
        if user.register():
            self.request.sendall(bytes("Success", encoding="utf-8"))
        else:
            self.request.sendall(bytes("Failure", encoding="utf-8"))

    def view(self, res):
        server_show("Receives the client's request to view the current directory file...", "msg")
        name = res[1]
        psd = res[2]
        user = User(name, psd)
        dirs, files = user.view_file()
        dir = str(dirs)
        file = str(files)
        if len(dirs) == 0:
            self.request.sendall("False".encode("utf-8"))
        else:
            self.request.sendall(bytes(dir, encoding="utf-8"))
        self.request.sendall(bytes(file, encoding="utf-8"))
        self.request.recv(1024)
        dic = User.info_read(name)
        storage = str(dic["storage"])
        self.request.sendall(bytes(storage, encoding="utf-8"))
        server_show("Current directory file view success...", "info")

    def upload(self, res):
        server_show("Receive the request from the client to upload the file....", "msg")
        name = res[1]
        filename = res[3]
        self.request.sendall(bytes("True", encoding="utf-8"))
        res = int(self.request.recv(1024).decode())
        if User.receive(filename, name, res, self.request):
            self.request.sendall(bytes("True", encoding="utf-8"))
        else:
            self.request.sendall(bytes("False", encoding="utf-8"))

    def download(self, res):
        server_show("Receive the request from the client to download the file....", "msg")
        name = res[1]
        psd = res[2]
        user = User(name, psd)
        dirs, files = user.view_file()
        file = str(files)
        self.request.sendall(bytes(file, encoding="utf-8"))
        res = self.request.recv(1024).decode()
        if User.download_file(res, name, self.request):
            server_show("The file download success....", "info")
        else:
            server_show("The file download failure....", "error")

    def cd(self, res):
        server_show("Receive the request from the client 'cd' command", "msg")
        name = res[1]
        psd = res[2]
        user = User(name, psd)
        res = user.cd_command(self.request)
        dirs = str(res)
        self.request.sendall(str(dirs).encode("utf-8"))
        dir1 = self.request.recv(1024).decode()
        if dir1 == "error":
            server_show("client input error", "error")
            self.request.close()
        else:
            sign = user.cd_dir(self.request, dir1, name)
            self.request.sendall(str(sign).encode("utf-8"))


if __name__ == '__main__':
    server_show("wait for the client connection....", "info")
    server = socketserver.ThreadingTCPServer(("localhost", settings.PORT), FTPserver)
    server.serve_forever()
