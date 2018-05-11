#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= tools
@file= luence_crm
@author= wubingyu
@create_time= 2018/5/10 上午9:45
"""
import requests
import logging
import json

logging.basicConfig(level=logging.INFO)


def lucene_url(lucene_url):
	response = requests.get(lucene_url)
	logging.info(response.text)
	json_0 = json.loads(json.loads(response.text)['value'])['docs']
	logging.debug("json_0: %s" % json_0)
	for a in json.loads(json_0):
		logging.info(
			"lucene: " + str(a['join_id']) + ' ' + str(a['memid']) + ' ' + str(a['expiretime']) + "***" + json.dumps(a,
																													 ensure_ascii=False))


if __name__ == '__main__':
	host = 'http://202.102.94.177:93/house365-crm/query?d=3&ps=20&pi=1&q='
	url = host + '{"tq":{"channelid":1000000},"sf":{"expiretime":0}}'
	lucene_url(url)
