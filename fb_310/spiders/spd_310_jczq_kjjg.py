# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from fb_310.items import Football_310_JCZQItem
from fb_310.table import table_to_list
import fb_310.settings as settings
import re
import time, datetime

today = datetime.datetime.now()
day_datadate = today.strftime('%Y%m%d')
day_datadate = datetime.datetime.strptime(day_datadate, '%Y%m%d')
year_datadate = today.strftime('%Y')
last_year = int(year_datadate) - 1
last_update_date = datetime.datetime.now() - datetime.timedelta(days=3000)

#球队爬虫  通过解析http://info.310win.com/jsData/matchResult/2017-2018/s36.js 这个页面，
class spd_310_competition_class(Spider):
    name = "spd_310_jczq_kjjg"
    start_urls = (
        'http://info.310win.com',
    )
    ignore_page_incremental = True

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'footBall-310-jczq')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_310_JCZQ_KJJG'])

        today = datetime.datetime.now()
        delta = datetime.timedelta(days=10)
        cal_date = today
        while cal_date >= last_update_date:
            cal_date = cal_date - delta
            str_cal_date = cal_date.strftime("%Y-%m-%d")

            login_post_data = {
                '__VIEWSTATE':'/wEPDwULLTIwNDI5MjczNjJkZCFwyb+R5Fqd/KqDYLS9AElqTtMx',
                '__EVENTVALIDATION':'/wEWBAKb8InjBgLg2ZN+AsKGtEYCjOeKxgblHhaMDdukbhjxKZfuNbq9e2LEJA==',
                'txtStartDate':str_cal_date,
                'txtEndDate':'2017-09-11',
                'Button1':'',
            }
            # url_link = 'http://spds.qhrb.com.cn/SP11/Chart1.aspx?pid=31873&bid=3819058&type=1&mt=1'
            url_link = "http://www.310win.com/jingcaizuqiu/kaijiang_jc_all.html"
            request = scrapy.http.FormRequest(url_link, callback=self.get_url_list, formdata=login_post_data, )
            request.meta['datadate'] = str_cal_date
            yield request

    def get_url_list(self, response):
        data_table = response.xpath('//*[@id="lottery_container"]/table')
        data_list = table_to_list(data_table)
        datadate = response.meta['datadate']
        matchId_list = response.xpath('//div[@id="lottery_container"]/table/tr')
        i = 1
        for matchId in matchId_list[1:]:
            href = matchId.xpath('.//td[13]/a/@href').extract()[0]
            pid = re.findall(r"/handicap/(.+?)\.html", href)[0]
            data_list[i].append(pid)
            i = i + 1
        # insert into etl_log.Etl_Log_Stg (data_row,is_successful,target_table,datetime_stamp,log_desc,source_name,start_dt,end_dt) values (1,'Y','T_310_BJDC_KJJG',TO_DATE('2017-09-05 23:14:01','yyyy/mm/dd hh24:mi:ss'),'','footBall-310-season',TO_DATE('2017-09-05 23:12:38','yyyy/mm/dd hh24:mi:ss'),TO_DATE('2017-09-05 23:14:01','yyyy/mm/dd hh24:mi:ss'))
        for rows in data_list[1:]:
            item = Football_310_JCZQItem()
            item['cc'] = rows[0]
            item['ss'] = rows[1]
            item['zdrq'] = rows[2]
            item['bf1'] = rows[3]
            item['kd'] = rows[4]
            item['bc'] = rows[5]
            item['rqspf'] = rows[6]
            item['spf'] = rows[7]
            item['bf2'] = rows[8]
            item['jqzs'] = rows[9]
            item['bqc'] = rows[10]
            item['hgpk'] = rows[11]
            item['sj'] = rows[12]
            item['matchId'] = rows[-1]
            item['timeInterval'] = datadate
            yield item


