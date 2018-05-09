#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= tools
@file= demo
@author= wubingyu
@create_time= 2018/5/8 下午5:16
"""
import re


def demo():
	sql = "select a.*          FROM                                  dwh_app_join_cust_channel_week                                 a         WHERE a.APP_NAME = ?and a.CITY_NAME = ?           and a.DATA_DATE between ? and               ?                and a.CITY_NAME is not null               order by a.DATA_DATE"

	key = re.search(r'from(.*)where', sql, re.I)
	print key.group(1)


if __name__ == '__main__':
	demo()
