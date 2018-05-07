#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= helloworld
@file= __init__.py
@author= wubingyu
@create_time= 2018/4/13 上午10:38
"""
import os
import json

items = dict()


def openMapping():
	with open('/Users/wubingyu/Desktop/mapping.txt', "r") as f:
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


def addPaigongSomeValue():
	items['STATUS'] = '{"name": "importfrom", "type": "long"},'
	items['addtime6'] = '{"name": "addtime6", "type": "long"},'
	items['developers'] = '{"name": "developers", "type": "long"},'
	items['addtime6'] = '{"name": "addtime6", "type": "long"},'
	items['developers'] = '{"name": "developers", "type": "text", "analyzer": "ik_max_word"},'
	items['recommendlpids'] = '{"name": "recommendlpids", "type": "text", "analyzer": "ik_max_word"},'


def addMeminfoSomeValue():
	items['focuspower'] = '{"name": "focuspower", "type": "text", "analyzer": "ik_max_word"},'
	items['buyintention'] = '{"name": "buyintention", "type": "long"},'
	items['addtime5'] = '{"name": "addtime5", "type": "long"},'
	items['addtime6'] = '{"name": "addtime6", "type": "long"},'
	items['developers'] = '{"name": "developers", "type": "text", "analyzer": "ik_max_word"},'
	items['recommendlpids'] = '{"name": "recommendlpids", "type": "text", "analyzer": "ik_max_word"},'


def openSql():
	with open('/Users/wubingyu/Desktop/stand_tmp/stand_sql.sql', 'r') as f:
		items_sql = f.read().split('SELECT')[1].split('FROM')[0].strip().replace('\n', '').replace('\t', '')
		for item in items_sql.split(','):

			try:
				# print (item, items[item.split('.')[1]])
				print (items[item.split('.')[1]])
			except:
				print ("%s has no value" % item)


if __name__ == '__main__':
	openMapping()
	addMeminfoSomeValue()
	openSql()
