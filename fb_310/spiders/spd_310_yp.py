# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from fb_310.items import Football_310_YPItem
from fb_310.table import table_to_list
import cx_Oracle
import time
import fb_310.settings as settings


class spd_310_ypdict_class(Spider):
    name = "spd_310_yp"
    start_urls = (
        'http://info.310win.com',
    )
    ignore_page_incremental = True

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'footBall_310_yp')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_310_yp'])

        conn = cx_Oracle.connect(settings.dbusername, settings.dbpassword, settings.dbconnect)
        cursor = conn.cursor()
        findsql = "select t.matchid, t.bcgsid from spider.t_310_ypdict t, spider.t_match_simple s  where t.matchid = s.a and s.b in (4 /*,2 ,415 ,21 ,25 ,284 ,15 ,1292 ,103 ,113 ,192*/ )" \
                  "and 1=1"
        cursor.execute(findsql)
        matchId_list = cursor.fetchall()
        cursor.close()
        conn.close()

        # url = 'http://www.310win.com/handicap/1286533.html'
        # request = scrapy.http.Request(url, callback=self.parse_content)
        # request.meta['matchId'] = '1286533'
        # yield request

        for match in matchId_list:
            url = 'http://data.310win.com/changedetail/handicap.aspx?id='+str(match[0])+'&companyid='+str(match[1])+'&l=0'
            request = scrapy.http.Request(url, callback=self.parse_content)
            request.meta['matchId'] = str(match[0])
            request.meta['bcgsId'] = str(match[1])
            yield request


    def parse_content(self, response):

        matchId = response.meta['matchId']
        bcgsId = response.meta['bcgsId']

        response.body.decode('gb2312').encode('utf8')
        pageLength = len(response.body)

        if pageLength < 100 :
            item = Football_310_YPItem()
            print 'response.body=====》' + response.body.decode('gb2312').encode('utf8')
            item['sj'] = u''
            item['bf'] = u''
            item['zd'] = u''
            item['pk'] = u''
            item['kd'] = u''
            item['bhsj'] = u'未采集到数据'
            item['status'] = u''
            item['bcgsId'] = bcgsId
            item['matchId'] = matchId
            item['update_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())
            yield item
        else :
            data_table = response.xpath('//*[@id="odds2"]/table')
            data_list = table_to_list(data_table)

            for data in data_list[1:]:
                if len(data) > 5 :
                    item = Football_310_YPItem()
                    item['sj'] = data[0]
                    item['bf'] = data[1]
                    item['zd'] = data[2]
                    item['pk'] = data[3]
                    item['kd'] = data[4]
                    item['bhsj'] = data[5]
                    item['status'] = data[6]
                    item['bcgsId'] = bcgsId
                    item['matchId'] = matchId
                    item['update_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())
                else:
                    item = Football_310_YPItem()
                    item['zd'] = data[0]
                    item['pk'] = data[1]
                    item['kd'] = data[2]
                    item['bhsj'] = data[3]
                    item['status'] = data[4]
                    item['bcgsId'] = bcgsId
                    item['matchId'] = matchId
                    item['update_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())

                yield item

