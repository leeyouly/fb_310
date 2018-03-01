# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from fb_310.items import Football_310_OPDictItem,Football_310_OPItem
from fb_310.table import table_to_list
import cx_Oracle
import fb_310.settings as settings
import re
import urllib
import time, datetime


#亚赔字典爬虫
class spd_310_competition_class(Spider):
    name = "spd_310_op_dict"
    start_urls = (
        'http://info.310win.com',
    )
    ignore_page_incremental = True

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'T_310_OP_DICT')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_310_OP_DICT'])

        conn = cx_Oracle.connect(settings.dbusername, settings.dbpassword, settings.dbconnect)
        cursor = conn.cursor()
        findsql = "select matchId from spider.t_310_match1 t where t.leagueid in (36,11,34,31,23) and t.season in ('2017-2018') "

        # findsql = "select * from spider.t_310_match1 t where t.leagueid in (36,11,34,31,23) " \
        #           "and t.season in ('2017-2018') and t.rq_all is not null and t.sorce is null;"
        cursor.execute(findsql)
        matchId_list = cursor.fetchall()
        cursor.close()
        conn.close()

        # url = 'http://www.310win.com/info/match/getfile.aspx?file=http://1x2.nowscore.com/1395350.js'
        # url = 'http://www.310win.com/info/match/getfile.aspx?file=http://1x2.nowscore.com/1406409.js'
        # request = scrapy.http.Request(url, callback=self.parse_content)
        # request.meta['matchId'] = str(1395350)
        # yield request

        for matchId in matchId_list:
            url = 'http://www.310win.com/info/match/getfile.aspx?file=http://1x2.nowscore.com/'+ str(matchId[0]) +'.js'
            request = scrapy.http.Request(url,callback=self.parse_content)
            request.meta['matchId'] = str(matchId[0])
            yield request

    def parse_content(self, response):
        op_json = response.body
        matchId = response.meta['matchId']
        game = re.findall("game=Array(.+);",op_json)
        if game <> [] :
            game = game[0]
            game_tuple = eval(game)
            for gameStr in game_tuple:
                gameList = gameStr.split('|')
                if len(gameList) >= 5:
                    gameList = gameStr.split('|')
                    item = Football_310_OPDictItem()
                    item['GameCompanyId'] = gameList[0]
                    item['Company_OPID'] = gameList[1]
                    item['Company_engName'] = gameList[2]
                    #Company_chnName 是从-3位置取的，不是从3的位置取的。
                    item['Company_chnName'] = gameList[-3]
                    item['matchId'] = matchId
                    item['update_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())
                    yield item
                else:
                    print u'gameStr有错误，可能是离比赛还有一段时间，大部分菠菜公司未开出赔率数据--->' + response.url
        else:
            print u'未找到赔率数据--->' + response.url