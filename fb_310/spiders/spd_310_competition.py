# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from fb_310.items import Football_310_CompetitionItem
import re


#赛事爬虫 
class spd_310_competition_class(Spider):
    name = "spd_310_competition"
    # allowed_domains = ["http://simu.7hcn.com/"]
    start_urls = (
        'http://info.310win.com',
    )
    ignore_page_incremental = True


    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'footBall-310-competition')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_310_COMPETITION'])
        url = 'http://info.310win.com/jsData/leftData/leftData.js'
        print '----------------------------------------------------------'
        request = scrapy.http.Request(url,callback=self.pase_content)
        yield request


    def pase_content(self, response):
        rdatas = response.body
        arrArea0 = re.search("\[\[.*\]",rdatas).group()
        arrArea1_1 = re.search("arrArea\[1\] = \[\[.*\]",rdatas).group()
        arrArea1 = re.search("\[\[.*\]",arrArea1_1).group()
        arrArea2_1 = re.search("arrArea\[2\] = \[\[.*\]",rdatas).group()
        arrArea2 = re.search("\[\[.*\]",arrArea2_1).group()
        arrArea3_1 = re.search("arrArea\[3\] = \[\[.*\]",rdatas).group()
        arrArea3 = re.search("\[\[.*\]",arrArea3_1).group()
        arrArea4_1 = re.search("arrArea\[4\] = \[\[.*\]",rdatas).group()
        arrArea4 = re.search("\[\[.*\]",arrArea4_1).group()
        arrArea5_1 = re.search("arrArea\[5\] = \[\[.*\]",rdatas).group()
        arrArea5 = re.search("\[\[.*\]",arrArea5_1).group()
        datasArea0 = eval(arrArea0)
        datasArea1 = eval(arrArea1)
        datasArea2 = eval(arrArea2)
        datasArea3 = eval(arrArea3)
        datasArea4 = eval(arrArea4)
        datasArea5 = eval(arrArea5)
        for dataArea in (datasArea0,datasArea1,datasArea2,datasArea3,datasArea4,datasArea5):
        #for dataArea in (datasArea1):
            for rows1 in range(len(dataArea)):
                for rows2 in range(len(dataArea[rows1][4])):
                    item = Football_310_CompetitionItem()
                    item['competitiongroups'] = dataArea[rows1][0]
                    item['competitiongroupc'] = dataArea[rows1][1]
                    item['competitiongroupe'] = dataArea[rows1][2]
                    item['continentsid'] = dataArea[rows1][3]
                    item['leagueId'] = dataArea[rows1][4][rows2][0]
                    item['leaguegroups'] = dataArea[rows1][4][rows2][1]
                    item['leaguegroupc'] = dataArea[rows1][4][rows2][2]
                    item['leaguegroupe'] = dataArea[rows1][4][rows2][3]
                    item['leaguegroupid'] = dataArea[rows1][4][rows2][4]
                    yield item

                for rows2 in range(len(dataArea[rows1][5])):
                    item = Football_310_CompetitionItem()
                    item['competitiongroups'] = dataArea[rows1][0]
                    item['competitiongroupc'] = dataArea[rows1][1]
                    item['competitiongroupe'] = dataArea[rows1][2]
                    item['continentsid'] = dataArea[rows1][3]
                    item['leagueId'] = dataArea[rows1][5][rows2][0]
                    item['leaguegroups'] = dataArea[rows1][5][rows2][1]
                    item['leaguegroupc'] = dataArea[rows1][5][rows2][2]
                    item['leaguegroupe'] = dataArea[rows1][5][rows2][3]
                    item['leaguegroupid'] = dataArea[rows1][5][rows2][4]
                    yield item




