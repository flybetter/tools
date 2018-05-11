#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= tools
@file= crm_paigong
@author= wubingyu
@create_time= 2018/5/11 下午2:07
"""
import re
import json
import logging

logging.basicConfig(level=logging.INFO)

paigong_sql = "remote-paigong-3.sql"

paigong_json = 'paigong.json'

items = dict()

list = []


def paigong_sql():
	with open("remote-paigong-3.sql", 'r') as f:
		items_sql = f.read().split('SELECT')[1].split('FROM')[0].strip().replace('\n', '').replace('\t', '')
		for item in items_sql.split(','):
			try:
				# print (item, items[item.split('.')[1]])
				print (items[item.split('.')[1]])
			except:
				list.append(item)
				print ("%s has no value" % item)


def addValue():
	items['addtime6'] = '{"name": "addtime6", "type": "long"},'
	items['pgstatus'] = '{"name": "pgstatus", "type": "long"},'



def join_json():
	with open('paigong.json', 'r') as f:
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
	paigong_sql()

	print list
