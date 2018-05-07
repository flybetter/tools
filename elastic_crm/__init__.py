#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= tools
@file= __init__.py
@author= wubingyu
@create_time= 2018/4/24 下午3:08
"""
import requests
import json
import logging
import re

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG)

lucene_project = "http://202.102.94.177:93/house365-crm/query?"

elastic_project = "http://192.168.105.21:9200/_sql"


# ?sql=


def lucene_url(url):
	result = requests.get(url).text
	logging.debug("result: %s" % result)

	json_0 = json.loads(json.loads(result)['value'])['docs']
	logging.debug("json_0: %s" % json_0)
	for a in json.loads(json_0):
		logging.info(json.dumps(a, ensure_ascii=False))


def elastic_url(url):
	result = requests(url).text
	logging.debug("result: %s" % result)
	# TODO(some logic business)
	pass


def url2sql(url):
	if re.match(r'(.*)\?d=(\d)&ps=(\d{1,2})&pi=(\d)&q=(.*)', url):
		m = re.match(r'(.*)\?d=(\d)&ps=(\d{1,2})&pi=(\d)&q=(.*)', url)
		logging.info('d:%s' % m.group(2))
		d = m.group(2)
		logging.info('ps:%s' % m.group(3))
		ps = m.group(3)
		logging.info('pi:%s' % m.group(4))
		pi = m.group(4)
		logging.info('q:%s' % m.group(5))
		q = m.group(5)
		q2sql(q)

	else:
		logging.info(" the wronge lucene url")


def q2sql(q):
	where = "select * from remote-meminfo-wu where 1=1 "
	q_objects = json.loads(q)
	for key in q_objects.iterkeys():
		logging.info("key: %s" % key)
		if key == 'ntq':
			for ntq_key in q_objects[key].iterkeys():
				where += '\n  and ( '
				logging.debug((q_objects[key])[ntq_key])
				ntq_values = re.findall(r'[0-9A-Za-z]+', (q_objects[key])[ntq_key])
				for afq_value in ntq_values:
					where += ntq_key + ' = ' + afq_value + ' or '
				where = where[:-3]
				where += ' ) '

		if key == 'tq':
			for ntq_key in q_objects[key].iterkeys():
				where += '\n and ('
				logging.debug((q_objects[key])[ntq_key])
				ntq_values = re.findall(r'[0-9A-Za-z]+', str((q_objects[key])[ntq_key]))
				for ntq_value in ntq_values:
					if re.match(r'\d+', ntq_value):
						where += ntq_key + ' = ' + ntq_value + ' or '
					else:
						where += ntq_key + ' = "' + ntq_value + '" or '
				where = where[:-3]
				where += ' ) '

		if key == 'afq':
			for ntq_key in q_objects[key].iterkeys():
				where += '\n and ('
				logging.debug(str(q_objects[key][ntq_key]).decode('utf-8'))
				afq_values = re.findall(ur"[\u4e00-\u9fa50-9A-Za-z]+", str(q_objects[key][ntq_key]).decode('utf-8'))
				for afq_value in afq_values:
					logging.debug(afq_value)
					if re.match(r'\d+', afq_value):
						where += ntq_key + ' = ' + afq_value + ' and '
					else:
						where += '%s = "%s" and ' % (ntq_key, afq_value)
				where = where[:-4]
				where += ' ) '

		if key == 'ofq':
			for ntq_key in q_objects[key].iterkeys():
				where += '\n and ('
				logging.debug(str(q_objects[key][ntq_key]).decode('utf-8'))
				afq_values = re.findall(ur"[\u4e00-\u9fa50-9A-Za-z]+", str(q_objects[key][ntq_key]).decode('utf-8'))
				for afq_value in afq_values:
					logging.debug(afq_value)
					if re.match(r'\d+', afq_value):
						where += ntq_key + ' = ' + afq_value + ' or '
					else:
						where += '%s = "%s" or ' % (ntq_key, afq_value)
				where = where[:-3]
				where += ' ) '

		if key == 'nq':
			for ntq_key in q_objects[key].iterkeys():
				where += '\n and ('
				where += "%s not in (" % ntq_key
				logging.debug(str(q_objects[key][ntq_key]).decode('utf-8'))
				afq_values = re.findall(ur"[\u4e00-\u9fa50-9A-Za-z]+", str(q_objects[key][ntq_key]).decode('utf-8'))
				for afq_value in afq_values:
					if re.match(r'\d+', afq_value):
						where += afq_value + ','
					else:
						where += '"%s" ,' % afq_value
				where = where[:-1]
				where += ' )) '

		if key == 'sf':
			where += '\n order by'
			for sf_key, sf_value in q_objects[key].iteritems():
				if sf_value == '0':
					where += ' %s desc, ' % sf_key
				else:
					where += ' %s asc, ' % sf_key
			where = where[:-2]

		if key == ' or':
			for ntq_key in q_objects[key].iterkeys():
				where += 'and ('
				logging.debug(str(q_objects[key][ntq_key]).decode('utf-8'))
				afq_values = re.findall(ur"[\u4e00-\u9fa50-9A-Za-z]+", str(q_objects[key][ntq_key]).decode('utf-8'))
				for afq_value in afq_values:
					logging.debug(afq_value)
					if re.match(r'\d+', afq_value):
						where += ntq_key + ' = ' + afq_value + ' or '
					else:
						where += '%s = "%s" or ' % (ntq_key, afq_value)
				where = where[:-3]
				where += ' ) '

	logging.info(where)


def sql2url(sql):
	pass


if __name__ == '__main__':
	url = 'http://202.102.94.177:93/house365-crm/query?d=3&ps=20&pi=1&q={"ntq":{"pgstatus":"[1,2]"},"tq":{"channelid":1000000,"join_from":"[43,112,199,225,311,312,313,379,34,46,53,54,60,110,160,161,217,339,356,357,358,68,107,111,113,119,125,141,175,176,222,223,226,301,314,315,316,336,340,359,360,380,42,52,121,122,208,216,224,237,244,245,337,353,354,355,361,362,363,365,366,375,108,114,115,154,248,230,4,5,103,143,144,153,167,169,174,218,219,254,66,177,179,247,253,255,261,262,341,342,137,234,257,317,318,1000]","buy_bankuai":"[1,3,5,7,9,11,13,14,15,17]","seafrom":"[c2,c1234]"},"afq":{"buy_new_loupan_zh":"[\u82cf\u5b81,\u6717\u8bd7]"},"rq":{"workday":"[0,999]"},"nq":{"seafromcate":"[1211,1121,1112,1221,1212,1122,1222,1111,5]"},"sf":{"pgstatus":1,"expiretime":1,"workday":0,"pgid":1}}'
	url2sql(url)
	lucene_url(url)

