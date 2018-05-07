#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= tools
@file= __init__.py
@author= wubingyu
@create_time= 2018/5/7 上午10:59
"""
import requests
import logging

logging.basicConfig(level=logging.DEBUG)

reset_url = 'http://192.168.130.87:8080/report/druid/reset-all.json'
data_url = 'http://192.168.130.87:8080/report/druid/sql.html'
login_url = 'http://192.168.130.87:8080/report/login.do'
report_url = 'http://192.168.130.87:8080/report/report.do'
login_data = {"user": "admin", "pass": "123456"}

session = requests.session()


def druid_reset():
	requests.post(reset_url)


def druid_data():
	data=requests.get(data_url).text
	logging.info(data)


def login():
	respond = session.post(login_url, data=login_data)


# logging.debug("body: " + respond.text)


def report():
	respond = session.post(report_url)
	logging.debug("body:" + respond.text)


def login_session():
	s = requests.session()
	res = s.post(login_url, data=login_data)
	s.get(report_url)
	logging.debug(s.get(report_url).text)


if __name__ == '__main__':
	# login()
	# report()
	druid_data()
