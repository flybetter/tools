SELECT a.join_id, a.loupanids, a.memfirstimport
	, a.memid, a.activity_id, a.channel_name, a.channel_type, a.active_type
	, a.active_name, a.join_name, a.join_channelid, a.join_fromcate, a.join_from
	, a.join_attend, a.join_buy, a.join_visit_state, a.join_visit_vret, a.join_visit_user
	, a.join_visit_time, a.join_visit_remark, a.join_isweb, a.join_bi_campaign, a.join_bi_tag
	, a.mlastmarktime, a.join_dateline, a.join_alllasttime, a.join_remark, a.join_memphone
	, a.join_lasttime, a.join_lastfrom, a.data_source, a.deviceinfo, b.activity_name
	, b.activity_type, c.memname, c.channelid, c.phonetype, c.memphone
	, c.memtel, c.membirthdate, c.memdistrict, c.memdistrict_zh, c.memuser
	, c.memfromcate, c.memfrom, c.memfirstfrom, c.remark_mes, c.importfrom
	, c.status, c.jointime, c.edittime, c.addtime1, c.addtime2
	, c.addtime3, c.addtime4, c.addtime, c.focuspower, c.buyintention
	, c.addtime5, c.addtime6, d.revisitnum, d.lastpgstatus, d.lastovertime
	, d.lastoverresult, d.lastmarktime, d.memhobby, d.iscardmonths, d.developers
	, d.recommendlpids, d.preference, d.exporttime
	, d.importtime, e.buy_pay_time, e.buy_demand, e.buy_area, e.buy_bankuai
	, e.buy_property, e.buy_purchase, e.buy_floor, e.buy_floor2, e.buy_new_why
	, e.buy_new_hux, e.buy_new_type, e.buy_new_total, e.buy_new_total_other, e.buy_new_meters
	, e.buy_new_meters_other, e.buy_new_unitprice, e.buy_new_unitprice_other, e.buy_new_loupan, e.buy_new_loupan_zh
	, h.repair_money, h.repair_type, h.repair_meters, h.repair_process, h.repair_demand
	, h.repair_need, i.life_active_type, i.life_domestic_type, i.life_marry_budget, i.life_fresh_need
	, i.life_car_time, i.life_pet_need, i.life_flea_need, i.life_actives_type, i.life_leisure_type
	, p.remark, p.pgid
FROM crm_join_info a
	LEFT JOIN crm_pg_join l ON a.join_id = l.joinid
	LEFT JOIN crm_paigong p ON l.pgid = p.pgid
	LEFT JOIN crm_activity b ON a.activity_id = b.activity_id
	LEFT JOIN crm_mem_info c ON a.memid = c.memid
	LEFT JOIN crm_mem_other d ON c.memid = d.memid
	LEFT JOIN crm_mem_buyinfo e ON c.memid = e.memid
	LEFT JOIN crm_mem_repairinfo h ON c.memid = h.memid
	LEFT JOIN crm_mem_lifeinfo i ON c.memid = i.memid
WHERE a.TIMESTAMP >:sql_last_value 



