# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from fb_310.items import Football_310_YPDictItem
from fb_310.table import table_to_list
import cx_Oracle
import fb_310.settings as settings
import re

import time, datetime


#球队爬虫  通过解析http://info.310win.com/jsData/matchResult/2017-2018/s36.js 这个页面，
class spd_310_yp_class(Spider):
    name = "spd_310_yp_dict"
    start_urls = (
        'http://info.310win.com',
    )
    ignore_page_incremental = True

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'footBall_310_ypdict')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_310_ypdict'])

        conn = cx_Oracle.connect(settings.dbusername, settings.dbpassword, settings.dbconnect)
        cursor = conn.cursor()
        findsql = "select * from spider.t_310_match1 t where t.leagueid in (36,11,34,31,23) " \
                  "and t.season in ('2017-2018') " \
                  "--and t.rq_all is not null " \
                  "--and t.sorce is null"
        cursor.execute(findsql)
        matchId_list = cursor.fetchall()
        cursor.close()
        conn.close()

        # url = 'http://www.310win.com/handicap/1396493.html'
        # request = scrapy.http.Request(url, callback=self.parse_content)
        # request.meta['matchId'] = '1286533'
        # yield request

        for matchId in matchId_list:
            url = 'http://www.310win.com/handicap/'+ str(matchId[0]) +'.html'
            request = scrapy.http.Request(url,callback=self.parse_content)
            request.meta['matchId'] = str(matchId[0])
            yield request


    def parse_content(self, response):

        data_table = response.xpath('//*[@id="odds"]/table')
        data_list = table_to_list(data_table)

        matchId = response.meta['matchId']
        gameCompanyId_list = response.xpath('//*[@id="odds"]/table/tr')
        i = 2
        for gameCompanyId in gameCompanyId_list[2:]:
            if gameCompanyId.xpath('.//td[8]/a/@href') <> []:
                href = gameCompanyId.xpath('.//td[8]/a/@href').extract()[0]
                pid = re.findall(r"companyid=(.+)", href)[0]
                data_list[i].append(pid)
            i = i + 1

        for data in data_list[2:]:
            item = Football_310_YPDictItem()
            if len(data) > 9:
                item['bcgs'] = data[0].replace(' ','').replace(u'走地',u'----走地')
                item['zd'] = data[1]
                item['pk'] = data[2]
                item['kd'] = data[3]
                item['zd2'] = data[4]
                item['pk2'] = data[5]
                item['kd2'] = data[6]
                item['bcgsId'] = data[9]
                item['matchId'] = matchId
                item['update_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())
                yield item
            else:
                print 'matchId:' + matchId + ';  data[-1] :' + data[-1]
                # print data
