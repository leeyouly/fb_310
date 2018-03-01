# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from fb_310.items import Football_310_select5from11Item
import time, datetime
last_update_date = datetime.datetime.now() - datetime.timedelta(days=5)

#从310网采集11选5的数据
class Select5from11(Spider):
    name = "spd_310_select5from11"
    start_urls = (
        'http://info.310win.com',
    )
    ignore_page_incremental = True

    def parse(self, response):
        today = datetime.datetime.now()
        delta = datetime.timedelta(days=1)
        cal_date = today
        while cal_date > last_update_date:
            str_cal_date = cal_date.strftime("%Y-%m-%d")
            url = 'http://www.310win.com/Info/Result/High.aspx?load=ajax&typeID=115&date='+str_cal_date+'&randomT-_-=0.8903625243788673'
            request = scrapy.http.Request(url, callback=self.parse_content)
            request.meta['str_cal_date'] = str_cal_date
            cal_date = cal_date - delta
            yield request

    def parse_content(self, response):
        str_cal_date = response.meta['str_cal_date']
        contentStr = response.body
        contentList = eval(contentStr)
        if contentList <> []:
            for content in contentList['Table']:
                item = Football_310_select5from11Item()
                item['IssueNum'] = content['IssueNum']
                item['Result'] = content['Result']
                item['AwardTime'] = content['AwardTime']
                item['datadate'] = str_cal_date
                yield item