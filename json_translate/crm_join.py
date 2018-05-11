#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= tools
@file= crm_join
@author= wubingyu
@create_time= 2018/5/11 下午2:06
"""
import re
import json
import logging

logging.basicConfig(level=logging.INFO)

join_sql = "remote-join-2.sql"

join_json = 'join.json'

items = dict()

list = []


def join_sql():
	with open("remote-join-2.sql", 'r') as f:
		items_sql = f.read().split('SELECT')[1].split('FROM')[0].strip().replace('\n', '').replace('\t', '')
		for item in items_sql.split(','):
			try:
				# print (item, items[item.split('.')[1]])
				print (items[item.split('.')[1]])
			except:
				list.append(item)
				print ("%s has no value" % item)


def addValue():
	items['status'] = '{"name": "status", "type": "long"},'
	items['addtime6'] = '{"name": "addtime6", "type": "long"},'
	items['activity'] = '{"name": "activity", "type": "long"},'
	items['consumptionlevel'] = '{"name": "consumptionlevel", "type": "long"},'
	items['buy_demand'] = '{"name": "buy_demand", "type": "long"},'


def join_json():
	with open('join.json', 'r') as f:
		for k, v in json.loads(f.read()).iteritems():
			print v
			for k, v in v.iteritems():
				print v
				for k, v in v.iteritems():
					print v
					for k, v in v.iteritems():
						print v
						for k, v in v.iteritems():
							if str(k).find('@') == -1:
								if str(v.get('type')) == 'text':
									# print ('{"name": "%s", "type": "%s", "analyzer": "ik_max_word"},' % (
									#	str(k), str(v.get('type'))))
									items[str(k)] = ('{"name": "%s", "type": "%s", "analyzer": "ik_max_word"},' % (
										str(k), str(v.get('type'))))
								else:
									#	print ('{"name": "%s", "type": "%s"},' % (str(k), str(v.get('type'))))
									items[str(k)] = ('{"name": "%s", "type": "%s"},' % (str(k), str(v.get('type'))))


if __name__ == '__main__':
	join_json()
	addValue()
	join_sql()

	print list
