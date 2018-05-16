#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= tools
@file= Fomatted-log
@author= wubingyu
@create_time= 2018/5/15 下午3:36
"""
import json
import logging
from elastic_flask import CrmScript
import re
from elastic_crm import *

logging.basicConfig(level=logging.INFO)


def get_url():
	with open("crm.log", "r") as f:
		lines = f.readlines()
		i = 0
		for a, line in enumerate(lines):
			if re.match(r'.*query:{.*', line):
				i = i + 1
				logging.warn("line num:" + str(a) + "  " + line)
				q = re.match(r'.*query:(.*)', line)
				d = check_d(q.group(1))
				url = "http://202.102.94.177:93/house365-crm/query?d=%s&ps=20&pi=1&q=%s" % (d, q.group(1))
				logging.info(url)
				crmScript = CrmScript(url)
				print "nums" + str(i)
				print crmScript.result


if __name__ == '__main__':
	get_url()
