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

logging.basicConfig(level=logging.DEBUG)

username = "root"
password = "doucare"


def search(_ip):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname='', port=22, username=username, password=password)
	stdin, stdout, stderr = ssh.exec_command("ls")
	logging.info(stdin)
