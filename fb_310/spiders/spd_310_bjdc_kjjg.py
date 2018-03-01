# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from fb_310.items import Football_310_BJDCItem
from fb_310.table import table_to_list
import cx_Oracle
import fb_310.settings as settings
import re
import urllib
import time, datetime


#球队爬虫  通过解析http://info.310win.com/jsData/matchResult/2017-2018/s36.js 这个页面，
class spd_310_competition_class(Spider):
    name = "spd_310_bjdc_kjjg"
    start_urls = (
        'http://info.310win.com',
    )
    ignore_page_incremental = True

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'footBall-310-bjdc')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_310_BJDC_KJJG'])

        conn = cx_Oracle.connect(settings.dbusername, settings.dbpassword, settings.dbconnect)
        cursor = conn.cursor()
        #2700到2800 还未跑 2700之前的有部分数据已经有了，建议先检查仔划定跑数区间
        findsql = "select A from T_DANCHANG_DATE t where t.id > 1350"
        #qhrb/qhds_pzyk.csv 应该是rownum < 1000的数据
        cursor.execute(findsql)
        matchId_list = cursor.fetchall()
        cursor.close()
        conn.close()

        for matchId in matchId_list:
            url = 'http://www.310win.com/beijingdanchang/kaijiang_dc_'+ str(matchId[0]) +'_all.html'
            request = scrapy.http.Request(url,callback=self.get_url_list)
            request.meta['sp_count'] = str(matchId[0])
            yield request


    def get_url_list(self, response):
        data_table = response.xpath('//*[@id="lottery_container"]/table')
        data_list = table_to_list(data_table)
        sp_count = response.meta['sp_count']
        matchId_list = response.xpath('//div[@id="lottery_container"]/table/tr')
        i = 1
        for matchId in matchId_list[1:]:
            href = matchId.xpath('.//td[13]/a/@href').extract()[0]
            pid = re.findall(r"/handicap/(.+?)\.html", href)[0]
            data_list[i].append(pid)
            i = i+1
        # insert into etl_log.Etl_Log_Stg (data_row,is_successful,target_table,datetime_stamp,log_desc,source_name,start_dt,end_dt) values (1,'Y','T_310_BJDC_KJJG',TO_DATE('2017-09-05 23:14:01','yyyy/mm/dd hh24:mi:ss'),'','footBall-310-season',TO_DATE('2017-09-05 23:12:38','yyyy/mm/dd hh24:mi:ss'),TO_DATE('2017-09-05 23:14:01','yyyy/mm/dd hh24:mi:ss'))
        for rows in data_list[1:]:
            item = Football_310_BJDCItem()
            item['cc'] = rows[0]
            item['ss'] = rows[1]
            item['matchTime'] = rows[2]
            item['zdrq'] = rows[3]
            item['bf1'] = rows[4]
            item['kd'] = rows[5]
            item['rqspf'] = rows[6]
            item['jqs'] = rows[7]
            item['sxds'] = rows[8]
            item['bf2'] = rows[9]
            item['bqcsf'] = rows[10]
            item['hgpk'] = rows[11]
            item['sj'] = rows[12]
            item['sp_count'] = sp_count
            item['matchId'] = rows[13]
            yield item


