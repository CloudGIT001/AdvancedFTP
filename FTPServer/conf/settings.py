#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
user_home = "%s/FTPServer/home" % basedir
user_info = "%s/FTPServer/db" % basedir
log_dir = "%s/FTPServer/logs" % basedir

HOST = "0.0.0.0"
PORT = 9999
