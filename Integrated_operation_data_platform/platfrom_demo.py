#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= tools
@file= platfrom_demo
@author= wubingyu
@create_time= 2018/5/8 下午3:40
"""
import re


def test():
	sql = "select *  from (     select z.* , rownum row_num from (    with tab as (  select a.*          from DWH_APP_REPORT_CUST_ACCESS_H a         where a.APP_NAME = ?          and a.CITY_NAME = ?            and a.PLATFORM_CODE = ?           and a.DATA_DATE between ? and               ?                and a.CITY_NAME is not null                  )                                 select nvl(s.APP_NAME, t.APP_NAME) as APP_NAME, nvl(s.CITY_NAME, t.CITY_NAME) as CITY_NAME, nvl(s.PLATFORM_CODE,t.PLATFORxM_CODE) as PLATFORM_CODE,       nvl(s.DATA_DATE,t.DATA_DATE) as DATA_DATE,  nvl(s.DATA_HOUR,t.use_time) as DATA_HOUR,        nvl(s.USER_COUNT_NEW,0) as USER_COUNT_NEW,nvl(s.SESSION_NUM,0) as SESSION_NUM,       nvl(s.USER_COUNT_ACC,0) as USER_COUNT_ACC,nvl(s.USER_COUNT,0) as USER_COUNT,       nvl(s.PAGE_VIEW,0) as PAGE_VIEW,nvl(s.CALL_COUNT_400,0) as CALL_COUNT_400  from      (        select distinct APP_NAME,                CITY_NAME,                PLATFORM_CODE,               DATA_DATE,               b.*          from tab,              SEC_USEDATE b      ) t  left join tab s    on t.APP_NAME = s.APP_NAME    and t.CITY_NAME = s.CITY_NAME   and t.PLATFORM_CODE = s.PLATFORM_CODE   and t.use_time = s.DATA_HOUR   and t.DATA_DATE = s.DATA_DATE      left join SEC_AREA b             on t.CITY_NAME = b.area_name                order by  b.encode,t.id                    ) z) where row_num = ?   and row_num = ?"

	datas = re.findall(r'from(.*?)where', sql, re.I)

	for data in datas:
		print "**"+data


if __name__ == '__main__':
	test()
