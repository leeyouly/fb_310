# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from fb_310.items import Football_310_LeagueItem, Football_310_TeamItem, Football_310_MatchItem
import re
import time
import sys
import cx_Oracle
import fb_310.settings as settings
reload(sys)
sys.setdefaultencoding('utf-8')
timestamp = time.time()
timestruct = time.localtime(timestamp)
print time.strftime('%Y-%m-%d %H:%M:%S', timestruct)

#赛事爬虫 
class spd_310_competition_class(Spider):
    name = "spd_310_match1"
    # allowed_domains = ["http://simu.7hcn.com/"]
    start_urls = (
        'http://info.310win.com',
    )
    ignore_page_incremental = True


    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'footBall-310-match')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_310_match'])


        conn = cx_Oracle.connect(settings.dbusername, settings.dbpassword, settings.dbconnect)
        cursor = conn.cursor()
        findsql = "select t.gameid,t.gamegroupid from spider.t_310_competition t where t.gamegroupid in (0) and t.gameid = 37  "
        # findsql = "select 217,0 from dual "
        cursor.execute(findsql)
        leagueId_list = cursor.fetchall()
        cursor.close()
        conn.close()

        for leagueId in leagueId_list:
            url = 'http://info.310win.com/jsData/LeagueSeason/sea' + str(leagueId[0]) + '.js'
            request = scrapy.http.Request(url,callback=self.parse_season)
            request.meta['leagueId'] = leagueId[0]
            request.meta['gamegroupId'] = leagueId[1]
            yield request

    #先拿到有多少个赛季
    def parse_season(self,response):
        seasonStr = re.findall('var arrSeason = (.+);',response.body)
        leagueId = response.meta['leagueId']
        gamegroupId = response.meta['gamegroupId']
        if seasonStr <> [] and gamegroupId == 1:
            seasonList = eval(seasonStr[0])
            for season in seasonList:
                url = 'http://info.310win.com/jsData/matchResult/'+season+'/s'+str(leagueId)+'.js?version=2018012715'
                request = scrapy.http.Request(url,callback=self.parse_League)
                request.meta['season'] = season
                request.meta['leagueId'] = leagueId
                yield request

        elif seasonStr <> [] and gamegroupId == 0:
            seasonList = eval(seasonStr[0])
            for season in seasonList:
                url = 'http://info.310win.com/cn/SubLeague/'+str(leagueId)+'.html'
                # url = 'http://info.310win.com/jsData/matchResult/'+season+'/s'+str(leagueId)+'.js?version=2018012715'
                request = scrapy.http.Request(url,callback=self.parse_SubLeague)
                request.meta['seasonList'] = seasonList
                request.meta['leagueId'] = leagueId
                yield request
        else:
            print 'parse_season faild --> ' + response.url
            print 'season faild content --> ' + response.body


    #解析groupId=0的比赛，类似英冠, 此方法不解析数据，只为拿到正真的url
    def parse_SubLeague(self, response):
        leagueId = response.meta['leagueId']
        seasonList = response.meta['seasonList']
        for season in seasonList:
            url = response.xpath('/html/head/script[6]/@src').extract()[0]
            urlpart = re.findall('/s'+str(leagueId)+'(.+)',url)[0]
            urlreal = 'http://info.310win.com/jsData/matchResult/' + season + '/s' + str(leagueId) + urlpart
            # urlreal = 'http://info.310win.com/jsData/matchResult/2017/s217_1685.js?version=2018012814'

            request = scrapy.http.Request(urlreal, callback=self.parse_conteSubLeagueDetail)
            request.meta['season'] = season
            request.meta['leagueId'] = leagueId
            yield request

    #解析英冠类比赛
    def parse_conteSubLeagueDetail(self,response):
        leagueId = response.meta['leagueId']
        season = response.meta['season']
        rdatas = response.body
        leagueStr = re.findall('var arrLeague = (.+);', rdatas)
        # 如果第一个联赛信息都未解析到，下面的肯定都解析不到
        if leagueStr <> []:
            leagueList = eval(leagueStr[0])
            item = Football_310_LeagueItem()
            item['leagueid'] = leagueList[0]
            item['leaguenames'] = leagueList[1]
            item['leaguenamec'] = leagueList[2]
            item['leaguenameeng'] = leagueList[3]
            item['season'] = leagueList[4]
            # item['sumround'] = leagueList[7]
            # item['currentround'] = leagueList[8]
            item['leagua'] = leagueList[7]
            item['leaguaeng'] = leagueList[9]
            item['leaguedesc'] = leagueList[10]
            item['update_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())
            item['source'] = response.url
            yield item

            # 球队信息(采集一次应该就可以了)
            teamStr = re.findall('var arrTeam = (.+);', rdatas)
            if teamStr <> []:
                teamList = eval(teamStr[0])
                for team in teamList:
                    item = Football_310_TeamItem()
                    item['leagueid'] = leagueId
                    item['teamid'] = team[0]
                    item['teamnames'] = team[1]
                    item['teamnamec'] = team[2]
                    item['teamnameeng'] = team[3]
                    # item['unknowid'] = team[-1]
                    item['update_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())
                    item['source'] = response.url
                    yield item
            else:
                print 'parse team faild -- > ' + response.url

            # 拿到该联赛有多少轮次
            roundSum = len(re.findall('jh(.+);', rdatas))
            # ☆☆☆☆☆解析比赛信息☆☆☆☆
            for round in range(roundSum):
                matchStr = re.findall('jh\["R_' + str(round + 1) + '"\] = (.+);', rdatas)
                if matchStr <> []:
                    matchList = eval(matchStr[0].replace(',,,', ',"","",').replace(',,', ',"",'))
                    for match in matchList:
                        if isinstance(match[4],list):
                            for matchDetail in match[4:]:
                                item = Football_310_MatchItem()
                                item['matchid'] = str(matchDetail[0])
                                item['leagueid'] = str(matchDetail[1])
                                item['unknownid'] = str(matchDetail[2])
                                item['season'] = season
                                item['roundtime'] = 'R_' + str(round + 1)
                                item['matchtime'] = matchDetail[3]
                                item['hometeamid'] = str(matchDetail[4])
                                item['guestteamid'] = str(matchDetail[5])
                                item['sorce'] = matchDetail[6]
                                item['sorce_half'] = matchDetail[7]
                                item['hometeamlab'] = str(matchDetail[8])
                                item['guestteamlab'] = str(matchDetail[9])
                                item['rq_all'] = str(matchDetail[10])
                                item['rq_half'] = str(matchDetail[11])
                                item['dx_all'] = str(matchDetail[12])
                                item['dx_half'] = str(matchDetail[13])
                                item['update_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())
                                yield item
                        else:
                            item = Football_310_MatchItem()
                            item['matchid'] = str(match[0])
                            item['leagueid'] = str(match[1])
                            item['unknownid'] = str(match[2])
                            item['season'] = season
                            item['roundtime'] = 'R_' + str(round + 1)
                            item['matchtime'] = match[3]
                            item['hometeamid'] = str(match[4])
                            item['guestteamid'] = str(match[5])
                            item['sorce'] = match[6]
                            item['sorce_half'] = match[7]
                            item['hometeamlab'] = str(match[8])
                            item['guestteamlab'] = str(match[9])
                            item['rq_all'] = str(match[10])
                            item['rq_half'] = str(match[11])
                            item['dx_all'] = str(match[12])
                            item['dx_half'] = str(match[13])
                            item['update_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())
                            yield item
        else:
            print u'英冠类未采集到数据--->' + response.url

        #英冠比赛有附加赛和附加赛决赛
        subLeagueStr= re.findall('var arrSubLeague = (.+);', rdatas)
        if subLeagueStr <> []:
            subLeagueList = eval(subLeagueStr[0])
            for subLeague in subLeagueList[1:]:
                url = 'http://info.310win.com/jsData/matchResult/' + season + '/s' + str(leagueId) +'_'+ str(subLeague[0]) + '.js?version=2018012814'
                request = scrapy.http.Request(url, callback=self.parse_conteSubLeagueDetail2)
                request.meta['season'] = season
                request.meta['leagueId'] = leagueId
                yield request
        else:
            print u'未找到英冠类附加赛的list--->' + response.url

    #解析附加赛和附加决赛
    def parse_conteSubLeagueDetail2(self, response):
        leagueId = response.meta['leagueId']
        season = response.meta['season']
        rdatas = response.body
        leagueStr = re.findall('var arrLeague = (.+);', rdatas)
        # 如果第一个联赛信息都未解析到，下面的肯定都解析不到
        if leagueStr <> []:
            # 拿到该联赛有多少轮次
            roundSum = len(re.findall('jh(.+);', rdatas))
            # ☆☆☆☆☆解析比赛信息☆☆☆☆
            for round in range(roundSum):
                matchStr = re.findall('jh\["R_' + str(round + 1) + '"\] = (.+);', rdatas)
                if matchStr <> []:
                    matchList = eval(matchStr[0].replace(',,,', ',"","",').replace(',,', ',"",'))
                    row = 0
                    for match in matchList:
                        if isinstance(match[4],list):
                            for matchDetail in match[4:]:
                                item = Football_310_MatchItem()
                                item['matchid'] = str(matchDetail[0])
                                item['leagueid'] = str(matchDetail[1])
                                item['unknownid'] = str(matchDetail[2])
                                item['season'] = season
                                item['roundtime'] = 'R_' + str(round + 1)
                                item['matchtime'] = matchDetail[3]
                                item['hometeamid'] = str(matchDetail[4])
                                item['guestteamid'] = str(matchDetail[5])
                                item['sorce'] = matchDetail[6]
                                item['sorce_half'] = matchDetail[7]
                                item['hometeamlab'] = str(matchDetail[8])
                                item['guestteamlab'] = str(matchDetail[9])
                                item['rq_all'] = str(matchDetail[10])
                                item['rq_half'] = str(matchDetail[11])
                                item['dx_all'] = str(matchDetail[12])
                                item['dx_half'] = str(matchDetail[13])
                                item['update_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())
                                yield item
                        else:
                            item = Football_310_MatchItem()
                            item['matchid'] = str(match[0])
                            item['leagueid'] = str(match[1])
                            item['unknownid'] = str(match[2])
                            item['season'] = season
                            item['roundtime'] = 'R_' + str(round + 1)
                            item['matchtime'] = match[3]
                            item['hometeamid'] = str(match[4])
                            item['guestteamid'] = str(match[5])
                            item['sorce'] = match[6]
                            item['sorce_half'] = match[7]
                            item['hometeamlab'] = str(match[8])
                            item['guestteamlab'] = str(match[9])
                            item['rq_all'] = str(match[10])
                            item['rq_half'] = str(match[11])
                            item['dx_all'] = str(match[12])
                            item['dx_half'] = str(match[13])
                            item['update_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())
                            yield item
                        row = row + 1
                else:
                    print u'解析英冠类附加赛异常-->' + response.url


    #解析groupId为1的比赛 类似英超
    def parse_League(self, response):
        #解析联赛信息
        leagueId = response.meta['leagueId']
        season = response.meta['season']
        rdatas = response.body
        leagueStr = re.findall('var arrLeague = (.+);',rdatas)
        #如果第一个联赛信息都未解析到，下面的肯定都解析不到
        if leagueStr <> []:
            leagueList = eval(leagueStr[0])
            item = Football_310_LeagueItem()
            item['leagueid'] = leagueList[0]
            item['leaguenames'] = leagueList[1]
            item['leaguenamec'] = leagueList[2]
            item['leaguenameeng'] = leagueList[3]
            item['season'] = leagueList[4]
            item['sumround'] = leagueList[7]
            item['currentround'] = leagueList[8]
            item['leagua'] = leagueList[9]
            item['leaguaeng'] = leagueList[11]
            item['leaguedesc'] = leagueList[12]
            item['update_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())
            item['source'] = response.url
            yield item

            # 球队信息(采集一次应该就可以了)
            teamStr = re.findall('var arrTeam = (.+);',rdatas)
            if teamStr <> []:
                teamList = eval(teamStr[0])
                for team in teamList:
                    item = Football_310_TeamItem()
                    item['leagueid'] = leagueId
                    item['teamid'] = team[0]
                    item['teamnames'] = team[1]
                    item['teamnamec'] = team[2]
                    item['teamnameeng'] = team[3]
                    # item['unknowid'] = team[-1]
                    item['update_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())
                    item['source'] = response.url
                    yield item
            else:
                print 'parse team faild -- > ' + response.url

            # 拿到该联赛有多少轮次
            roundSum = len(re.findall('jh(.+);', rdatas))
            # ☆☆☆☆☆解析比赛信息☆☆☆☆
            for round in range(roundSum):
                matchStr = re.findall('jh\["R_'+str(round+1)+'"\] = (.+);', rdatas)
                if matchStr <> []:
                    matchList = eval(matchStr[0].replace(',,,',',"","",').replace(',,',',"",'))
                    for match in matchList:
                        item = Football_310_MatchItem()
                        item['matchid'] = str(match[0])
                        item['leagueid'] = str(match[1])
                        item['unknownid'] = str(match[2])
                        item['season'] = season
                        item['roundtime'] = 'R_'+str(round+1)
                        item['matchtime'] = match[3]
                        item['hometeamid'] = str(match[4])
                        item['guestteamid'] = str(match[5])
                        item['sorce'] = match[6]
                        item['sorce_half'] = match[7]
                        item['hometeamlab'] = str(match[8])
                        item['guestteamlab'] = str(match[9])
                        item['rq_all'] = str(match[10])
                        item['rq_half'] = str(match[11])
                        item['dx_all'] = str(match[12])
                        item['dx_half'] = str(match[13])
                        item['update_dt'] = time.strftime("%Y-%m-%d %X", time.localtime())
                        yield item
                else:
                    print 'parse match faild--> ' + response.url

        else:
            print 'parse_content -- > ' + response.url
