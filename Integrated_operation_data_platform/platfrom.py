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
import re
import xlwt
import os
from selenium import webdriver
import time

logging.basicConfig(level=logging.DEBUG)

reset_url = 'http://192.168.130.87:8080/report/druid/reset-all.json'
data_url = 'http://192.168.130.87:8080/report/druid/sql.html'
login_url = 'http://192.168.130.87:8080/report/login.do'
report_url = 'http://192.168.130.87:8080/report/report.do'
login_data = {"user": "admin", "pass": "123456"}
base_url = 'http://192.168.130.87:8080/report/'

session = requests.session()


def druid_reset():
	session.post(reset_url)


def druid_data():
	driver = webdriver.Chrome()
	driver.get(data_url)
	page = driver.page_source
	# logging.debug("page:" + page)
	sqls = re.findall(r'data-dismiss="alert" title="(.*?)"', page, re.S)
	driver.quit()
	return sqls


def login():
	respond = session.post(login_url, data=login_data)


# logging.debug("body: " + respond.text)


def report():
	respond = session.post(report_url)
	# logging.debug("body:" + respond.text)
	return respond.text


def format_db(_data):
	values = re.findall(
		r'<a href="javascript:;" url="(.*?)" title="(.*?)"', _data, re.S)

	values = filter(lambda a: not str.startswith(str(a[0]), 'http'), values)
	return values


def export_excel(file_path):
	driver = webdriver.Chrome()
	driver.get(login_url + '?user=admin&pass=123456')

	platform_data = report()
	platform_data = format_db(platform_data)
	workbook = xlwt.Workbook()
	sheet = workbook.add_sheet('data_platform', cell_overwrite_ok=True)
	sheet.write(0, 0, 'title')
	for i, _data in enumerate(platform_data):
		sheet.write(i + 1, 0, _data[0])
		sheet.write(i + 1, 1, _data[1])
		druid_reset()
		time.sleep(2)
		_url = base_url + _data[0]
		print "***********" + _url
		driver.get(_url)
		druid_datas = druid_data()

		for j, sheet_sql in enumerate(druid_datas):
			print re.sub(r'&.*?;', '', sheet_sql)
			sql = re.sub(r'&.*?;', '', sheet_sql)
			print "******table:" + re.match(r'.*from(.*?)where.*', sql, re.I).group(1)
			sheet.write(i + 1, j + 2, re.match(r'.*from(.*?)where.*', sql, re.I).group(1))

	workbook.save(file_path)
	driver.close()

# def druid_operation(_url):
# 	druid_reset()
# 	druid_login(_url)
# 	druid_datas = druid_data()
# 	return druid_datas
#
#
# def druid_login(_url):
# 	_url = base_url + _url
# 	print "******** url:" + _url
# 	driver.get(_url)


# print driver.page_source


if __name__ == '__main__':
	path = os.getcwd() + '/test.xlsx'
	login()
	export_excel(path)

# druid_data()
