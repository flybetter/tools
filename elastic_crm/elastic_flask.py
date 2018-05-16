#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= tools
@file= elastic-final
@author= wubingyu
@create_time= 2018/5/15 下午1:40
"""
import re
import logging
from collections import OrderedDict
import json
import requests
import sys

logging.basicConfig(level=logging.DEBUG)

PAIGONG = 3
JOINED_1 = 1
JOINED_2 = 2

PAIGONG_TABLE = "elastic-paigong/paigong"
JOINED_TABLE = "elastic-joined/joined"

ELASTIC_EXPLAIN = "http://192.168.105.21:9200/_sql/_explain?sql="

ElASTIC_URL = "http://192.168.105.21:9200/%s/_search"

reload(sys)
sys.setdefaultencoding('utf-8')


class CrmScript(object):
	def __init__(self, url):
		if re.match(r'.*\?d=(\d)&ps=(\d+)&pi=(\d+)&q=(.*)', url):
			m = re.match(r'.*\?d=(\d)&ps=(\d+)&pi=(\d+)&q=(.*)', url)
			self.d = int(m.group(1))
			self.ps = int(m.group(2))
			self.pi = int(m.group(3))
			self.q = m.group(4)
			self.where = self.q2sql()
			self.sql = self.d2sql()
			self.json = self.sql2json()
			self.dsl = self.add_distinct()
			self.result = self.dsl2result()
		else:
			self.result = "the wrong lucene url:" + url
			logging.info("the wrong lucene url:" + url)

	def dsl2result(self):
		table = self.d2table()
		elastic_url = ElASTIC_URL % table
		result = requests.post(elastic_url, self.dsl).text
		return result

	def add_distinct(self):
		if self.d == JOINED_2:
			init_dsl = json.loads(self.json)
			init_dsl['collapse'] = {"field": "memid"}
			elastic_dsl = json.dumps(init_dsl)
		else:
			init_dsl = json.loads(self.json)
			init_dsl['collapse'] = {"field": "pgid"}
			elastic_dsl = json.dumps(init_dsl)
		return elastic_dsl

	def sql2json(self):
		explain_url = ELASTIC_EXPLAIN + self.sql
		return requests.get(explain_url).text

	def d2table(self):
		if self.d == PAIGONG:
			table = PAIGONG_TABLE
		else:
			table = JOINED_TABLE
		return table

	def d2sql(self):
		from_sql = "select * from " + self.d2table()
		sql = from_sql + self.where
		begin = (self.pi - 1) * self.ps
		end = self.pi * self.ps
		sql = sql + 'limit %d,%d' % (begin, end)
		return sql

	def reversed_cmp(x, y):
		if x == 'sf':
			return 1
		if y == 'sf':
			return -1
		if x > y:
			return -1
		if x < y:
			return 1
		return 0

	def q2sql(self):
		where = " where 1=1 "
		q_objects = json.loads(self.q, object_pairs_hook=OrderedDict)
		for key in sorted(q_objects.iterkeys(), self.reversed_cmp):
			logging.info("key: %s" % key)
			if key == 'ntq':
				for ntq_key in q_objects[key].iterkeys():
					where += ' and %s in ( ' % ntq_key
					ntq_values = re.findall(r'[0-9]+', q_objects[key][ntq_key])
					for ntq_value in ntq_values:
						if re.match(r'\d+', ntq_value):
							where += ntq_value + ','
					where = where[:-1]
					where += ' ) '

			if key == 'tq':
				for tq_key in q_objects[key].iterkeys():
					where += ' and %s in (' % tq_key
					tq_values = re.findall(ur"[\u4e00-\u9fa50-9A-Za-z]+",
										   str(q_objects[key][tq_key]).decode('utf-8'))
					for tq_value in tq_values:
						if re.match(r'\d+', tq_value):
							where += tq_value + ','
						else:
							where += '"%s" ,' % tq_value
					where = where[:-1]
					where += ' ) '

			if key == 'afq':
				for ntq_key in q_objects[key].iterkeys():
					where += ' and ('
					logging.debug(str(q_objects[key][ntq_key]).decode('utf-8'))
					afq_values = re.findall(ur"[\u4e00-\u9fa50-9A-Za-z]+",
											str(q_objects[key][ntq_key]).decode('utf-8'))
					for afq_value in afq_values:
						logging.debug(afq_value)
						if re.match(r'^\d+$', afq_value):
							where += ntq_key + ' = ' + afq_value + ' and '
						else:
							where += '%s = "%s" and ' % (ntq_key, afq_value)
					where = where[:-4]
					where += ' ) '

			if key == 'ofq':
				for ntq_key in q_objects[key].iterkeys():
					where += ' and ('
					logging.debug(str(q_objects[key][ntq_key]).decode('utf-8'))
					afq_values = re.findall(ur"[\u4e00-\u9fa50-9A-Za-z]+",
											str(q_objects[key][ntq_key]).decode('utf-8'))
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
					where += ' and ('
					where += "%s not in (" % ntq_key
					logging.debug(str(q_objects[key][ntq_key]).decode('utf-8'))
					afq_values = re.findall(ur"[\u4e00-\u9fa50-9A-Za-z]+",
											str(q_objects[key][ntq_key]).decode('utf-8'))
					for afq_value in afq_values:
						if re.match(r'\d+', afq_value):
							where += afq_value + ','
						else:
							where += '"%s" ,' % afq_value
					where = where[:-1]
					where += ' )) '

			if key == 'sf':
				where += ' order by'
				for sf_key, sf_value in q_objects[key].iteritems():
					if sf_value == 1:
						where += ' %s asc , ' % sf_key
					else:
						where += ' %s desc , ' % sf_key
				where = where[:-2]

			if key == 'oq':
				for oq_key in q_objects[key].iterkeys():
					where += 'and ('
					oq_values = re.findall(ur"[\u4e00-\u9fa50-9A-Za-z]+",
										   str(q_objects[key][oq_key]).decode('utf-8'))
					for oq_value in oq_values:
						if re.match(r'\d+', oq_value):
							where += oq_key + ' = ' + oq_value + ' or '
						else:
							where += '%s = "%s" or ' % (oq_key, oq_value)
					where = where[:-3]
					where += ' ) '

			if key == 'rq':
				for rq_key in q_objects[key].iterkeys():
					where += 'and ('
					rq_values = re.findall(ur"[\u4e00-\u9fa50-9A-Za-z]+",
										   str(q_objects[key][rq_key]).decode('utf-8'))
					where += rq_key + ' between "' + rq_values[0] + '" and "' + rq_values[1] + '" ) '

		logging.info(where)
		return where


if __name__ == '__main__':
	url = 'http://202.102.94.177:93/house365-crm/query?d=3&ps=20&pi=1&q={"ntq":{"pgstatus":"[1,2]"},"tq":{"channelid":1000000,"join_from":"[43,112,199,225,311,312,313,379,34,46,53,54,60,110,160,161,217,339,356,357,358,68,107,111,113,119,125,141,175,176,222,223,226,301,314,315,316,336,340,359,360,380,42,52,121,122,208,216,224,237,244,245,337,353,354,355,361,362,363,365,366,375,108,114,115,154,248,230,4,5,103,143,144,153,167,169,174,218,219,254,66,177,179,247,253,255,261,262,341,342,137,234,257,317,318,1000]","buy_bankuai":"[1,3,5,7,9,11,13,14,15,17]","seafrom":"[c2,c1234]"},"afq":{"buy_new_loupan_zh":"[\u82cf\u5b81,\u6717\u8bd7]"},"rq":{"workday":"[0,999]"},"nq":{"seafromcate":"[1211,1121,1112,1221,1212,1122,1222,1111,5]"},"sf":{"pgstatus":1,"expiretime":1,"workday":0,"pgid":1}}'
	script = CrmScript(url)
	print script.sql
	print script.json
	print script.dsl
	print script.result
