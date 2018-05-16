#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= tools
@file= url2elastic
@author= wubingyu
@create_time= 2018/5/10 下午1:10
"""
import requests
import json
import os
import re

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
	a = "[u'6325219']"
	if re.match(r"\[u'(\d+)'\]", a):
		print re.search(r"\d+", a).group()
	else:
		print 11
