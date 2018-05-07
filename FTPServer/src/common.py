#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import math
import time
import logging
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from conf import settings


def server_logging(content,levelname):
    _filename = os.path.join(settings.log_dir,"server_sys.log")
    log = logging.getLogger(_filename)
    logging.basicConfig(filename=_filename,level=logging.INFO,format='%(asctime)s-%(levelname)s-%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    if levelname == "debug":
        logging.debug(content)
    if levelname == 'info':
        logging.info(content)
    if levelname == 'warning':
        logging.warning(content)
    if levelname == 'error':
        logging.error(content)
    if levelname == 'critical':
        logging.critical(content)


def client_logging(content,levelname):
    _filename = os.path.join(settings.log_dir,"client_sys.log")
    log = logging.getLogger(_filename)
    logging.basicConfig(filename=_filename,level=logging.INFO,format='%(asctime)s-%(levelname)s-%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    if levelname == "debug":
        logging.debug(content)
    if levelname == 'info':
        logging.info(content)
    if levelname == 'warning':
        logging.warning(content)
    if levelname == 'error':
        logging.error(content)
    if levelname == 'critical':
        logging.critical(content)


def server_show(msg,msg_type):
    if msg_type == "info":
        show_msg = "\033[1;35m%s\033[0m"%msg
    elif msg_type == "error":
        show_msg = "\033[1;31m%s\033[0m"%msg
    elif msg_type == "msg":
        show_msg = "\033[1;37m%s\033[0m"%msg
    else:
        show_msg = "\033[1;32m%s\033[0m"%msg
    print(show_msg)
    server_logging(msg,msg_type)


def client_show(msg,msg_type):
    if msg_type == "info":
        show_msg = "\033[1;35m%s\033[0m"%msg
    elif msg_type == "error":
        show_msg = "\033[1;31m%s\033[0m"%msg
    elif msg_type == "msg":
        show_msg = "\033[1;37m%s\033[0m"%msg
    else:
        show_msg = "\033[1;32m%s\033[0m"%msg
    print(show_msg)
    client_logging(msg,msg_type)


def progressbar(cur, total):
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write('[%-50s] %s' % ('=' * int(math.floor(cur * 50 / total)), percent))
    sys.stdout.flush()
    time.sleep(0.01)
    if cur == total:
        sys.stdout.write('\n')


