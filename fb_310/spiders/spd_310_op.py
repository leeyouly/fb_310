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


#球队爬虫  通过解析http://info.310win.com/jsData/matchResult/2017-2018/s36.js 这个页面，
class spd_310_competition_class(Spider):
    name = "spd_310_op"
    start_urls = (
        'http://info.310win.com',
    )
    ignore_page_incremental = True

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'footBall-310-bjdc_op')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_310_BJDC_KJJG'])

        conn = cx_Oracle.connect(settings.dbusername, settings.dbpassword, settings.dbconnect)
        cursor = conn.cursor()
        findsql = "select matchId from spider.t_310_match1 t where t.leagueid in (36,11,34,31,23) " \
                  "and t.season in ('2017-2018') " \
                  "--and t.rq_all is not null " \
                  "--and t.sorce is null"
        cursor.execute(findsql)
        matchId_list = cursor.fetchall()
        cursor.close()
        conn.close()

        for matchId in matchId_list:
            url = 'http://www.310win.com/info/match/getfile.aspx?file=http://1x2.nowscore.com/'+ str(matchId[0]) +'.js'
            request = scrapy.http.Request(url,callback=self.parse_content)
            request.meta['matchId'] = str(matchId[0])
            yield request

        # url = 'http://www.310win.com/info/match/getfile.aspx?file=http://1x2.nowscore.com/987378.js'
        # request = scrapy.http.Request(url,callback=self.parse_content)
        # # request.meta['matchId'] = str(matchId[0])
        # yield request

    def parse_content(self, response):
        op_json = response.body
        matchId = response.meta['matchId']
        # game = re.findall("game=Array(.+);",op_json)[0]
        # game_tuple = eval(game)
        # for gameStr in game_tuple:
        #     if gameStr <>'':
        #         gameList = gameStr.split('|')
        #         item = Football_310_OPDictItem()
        #         item['GameCompanyId'] = gameList[0]
        #         item['Company_OPID'] = gameList[1]
        #         item['Company_engName'] = gameList[2]
        #         #Company_chnName 是从-3位置取的，不是从3的位置取的。
        #         item['Company_chnName'] = gameList[-3]
        #         item['matchId'] = matchId
        #         yield item


        gameDetail = re.findall("gameDetail=Array(.+);",op_json)
        if gameDetail <> []:
            gameDetail = gameDetail[0]
            gameDetail_tuple = eval(gameDetail)
            for gameDetailStr in gameDetail_tuple:
                listStr = gameDetailStr.split('^')
                op_id = listStr[0]
                gameDetaillistStr = listStr[1].split(';')
                for gameDetailList in gameDetaillistStr:
                    if gameDetailList <> '':
                        gameDetail = gameDetailList.split('|')
                        length = len(gameDetail)
                        item = Football_310_OPItem()
                        item['Company_OPID'] = op_id
                        item['zs'] = gameDetail[0]
                        item['h'] = gameDetail[1]
                        item['ks'] = gameDetail[2]
                        item['bhsj'] = gameDetail[3]
                        # item['zsl'] = rows[1]
                        # item['hl'] = rows[1]
                        # item['ksl'] = rows[1]
                        # item['fhl'] = rows[1]
                        if length > 4:
                            item['klzs1'] = gameDetail[4]
                            item['klzs2'] = gameDetail[5]
                            item['klzs3'] = gameDetail[6]
                        item['matchId'] = matchId
                        item['update_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())
                        yield item



