#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= tools
@file= __init__.py
@author= wubingyu
@create_time= 2018/5/8 上午9:21
"""
import paramiko
import logging
import os

logging.basicConfig(level=logging.DEBUG)

username = "root"
password = "doucare"


def test_env():
	print os.environ


if __name__ == '__main__':
	test_env()
